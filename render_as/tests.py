from django.test import TestCase
from django.db import models
from django import template


class TestModel(models.Model):
    name = models.CharField(max_length=255)


class TestModel2(models.Model):
    name = models.CharField(max_length=255)


class TestModel3(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        # If we clash with a real app, and we're using South for that app, then
        # the db table for this model won't be created
        app_label = 'avoid_clash_with_real_app'


class TestRenderAs(TestCase):
    
    def test_simple_render_as_invocation(self):
        t = template.Template("{% load render_as %}{% render_as obj simple %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Test model whatever", t.render(c))

    def test_simple_render_as_invocation_default_template(self):
        t = template.Template("{% load render_as %}{% render_as obj simple %}")
        o = TestModel2.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Just a simple TestModel2 object", t.render(c))

    def test_nested_render_as_invocation(self):
        t = template.Template("{% load render_as %}{% render_as obj nested %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o, 'extra': 'something'})
        self.assertEqual(u"whatever, something", t.render(c))


class TestRenderAsErrors(TestCase):
    
    def test_too_few_args_0(self):
        try:
            t = template.Template("{% load render_as %}{% render_as %}")
        except template.TemplateSyntaxError, e:
            self.assertEqual(u"'render_as' tag requires two arguments", unicode(e))
        else:
            self.fail("Did not raise TemplateSyntaxError")
        
    def test_too_few_args_1(self):
        try:
            t = template.Template("{% load render_as %}{% render_as thing %}")
        except template.TemplateSyntaxError, e:
            self.assertEqual(u"'render_as' tag requires two arguments", unicode(e))
        else:
            self.fail("Did not raise TemplateSyntaxError")
        
    def test_too_many_args_3(self):
        try:
            t = template.Template("{% load render_as %}{% render_as thing other_thing yet_another_thing %}")
        except template.TemplateSyntaxError, e:
            self.assertEqual(u"'render_as' tag requires two arguments", unicode(e))
        else:
            self.fail("Did not raise TemplateSyntaxError")
        
    def test_unresolvable_variable(self):
        t = template.Template("{% load render_as %}{% render_as thing simple %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual(u"[[ no such variable 'thing' in render_as call ]]", t.render(c))
        
    def test_not_an_object(self):
        t = template.Template("{% load render_as %}{% render_as obj simple %}")
        c = template.Context({'obj': u"huzzah" })
        self.assertEqual(u"Just a simple huzzah", t.render(c))
        
    def test_no_such_template(self):
        t = template.Template("{% load render_as %}{% render_as obj missing %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual(u"[[ no such template in render_as call (render_as/testmodel_missing.html, render_as/default_missing.html) ]]", t.render(c))
    
    def test_template_syntax_error(self):
        t = template.Template("{% load render_as %}{% render_as obj syntax_error %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual(u"[[ template syntax error in render_as call (render_as/testmodel_syntax_error.html, render_as/default_syntax_error.html) ]]", t.render(c))

    def test_context_popped_after_error(self):
        t = template.Template("{% load render_as %}{% render_as obj syntax_error %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        t.render(c)
        self.assertEqual([{'obj': o}], c.dicts)


class TestRenderAsNonModelObject(TestCase):

    def test_correct_template(self):
        class MyClass(object):
            pass

        t = template.Template("{% load render_as %}{% render_as obj correct %}")
        c = template.Context({'obj': MyClass()})
        self.assertEqual(u"Test non-model object.\n", t.render(c))


from django.core.management.color import no_style
from django.db import connections, transaction, DEFAULT_DB_ALIAS


class TestRenderAsWithTestModel3(TestCase):
    """
    Somewhat messy, since setting the app_label in TestModel3 (which
    is more robust than messing with _meta.app_label) means the db
    table won't be created automatically. So we do the following,
    extracted from the syncdb command (and bearing in mind that
    TestModel3 is really simple so doesn't need references, indices,
    or custom SQL).
    """
    
    def setUp(self):
        db = DEFAULT_DB_ALIAS
        connection = connections[db]
        tables = connection.introspection.table_names()
        if connection.introspection.table_name_converter(TestModel3._meta.db_table) in tables:
            return
        sql, references = connection.creation.sql_create_model(TestModel3, no_style(), [])
        cursor = connection.cursor()
        for statement in sql:
            cursor.execute(statement)
        tables.append(connection.introspection.table_name_converter(TestModel3._meta.db_table))
        transaction.commit_unless_managed(using=db)

    def test_simple_render_as_invocation_default_template_different_appname(self):
        t = template.Template("{% load render_as %}{% render_as obj simple2 %}")
        o = TestModel3.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Just a simple 2 TestModel3 object", t.render(c))
    
    def test_simple_render_as_invocation_different_appname(self):
        t = template.Template("{% load render_as %}{% render_as obj simple %}")
        o = TestModel3.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Test model 3 whatever\n", t.render(c))
