from django import template
from django.db import models
from django.test import TestCase
from django.utils.encoding import smart_text


class TestModel(models.Model):
    name = models.CharField(max_length=255)


class TestModel2(models.Model):
    name = models.CharField(max_length=255)


class TestModel3(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'avoid_clash_with_real_app'


class TestRenderAs(TestCase):

    def test_simple_render_as_invocation(self):
        t = template.Template("{% load render_as %}{% render_as obj 'simple' %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Test model whatever", t.render(c))

    def test_type_as_variable(self):
        t = template.Template("{% load render_as %}{% render_as obj type %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o, 'type': 'simple'})
        self.assertEqual("Test model whatever", t.render(c))

    def test_simple_render_as_invocation_default_template(self):
        t = template.Template("{% load render_as %}{% render_as obj 'simple' %}")
        o = TestModel2.objects.create(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Just a simple TestModel2 object", t.render(c))

    def test_nested_render_as_invocation(self):
        t = template.Template("{% load render_as %}{% render_as obj 'nested' %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o, 'extra': 'something'})
        self.assertEqual(u"whatever, something", t.render(c))


class TestRenderAsErrors(TestCase):

    def test_too_few_args_0(self):
        with self.assertRaises(template.TemplateSyntaxError) as raised:
            template.Template("{% load render_as %}{% render_as %}")
        self.assertEqual(
            u"'render_as' tag requires two arguments",
            smart_text(raised.exception),
        )

    def test_too_few_args_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as raised:
            template.Template("{% load render_as %}{% render_as thing %}")
        self.assertEqual(
            u"'render_as' tag requires two arguments",
            smart_text(raised.exception),
        )

    def test_too_many_args_3(self):
        with self.assertRaises(template.TemplateSyntaxError) as raised:
            template.Template("{% load render_as %}{% render_as thing other_thing yet_another_thing %}")
        self.assertEqual(
            u"'render_as' tag requires two arguments",
            smart_text(raised.exception),
        )

    def test_unresolvable_variable(self):
        t = template.Template("{% load render_as %}{% render_as thing 'simple' %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        with self.assertRaises(template.TemplateSyntaxError) as raised:
            t.render(c)
        self.assertEqual(
            u"no such variable 'thing' in render_as call",
            smart_text(raised.exception),
        )

    def test_unresolvable_type_variable(self):
        t = template.Template("{% load render_as %}{% render_as obj simple %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        with self.assertRaises(template.TemplateSyntaxError) as raised:
            t.render(c)
        self.assertEqual(
            u"no such variable 'simple' in render_as call",
            smart_text(raised.exception),
        )

    def test_not_an_object(self):
        t = template.Template("{% load render_as %}{% render_as obj 'simple' %}")
        c = template.Context({'obj': u"huzzah"})
        self.assertEqual(u"Just a simple huzzah", t.render(c))

    def test_no_such_template(self):
        t = template.Template("{% load render_as %}{% render_as obj 'missing' %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        with self.assertRaises(template.TemplateDoesNotExist):
            t.render(c)

    def test_template_syntax_error(self):
        t = template.Template("{% load render_as %}{% render_as obj 'syntax_error' %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        with self.assertRaises(template.TemplateSyntaxError) as raised:
            t.render(c)
        self.assertTrue(
            u"Invalid block tag on line" in smart_text(raised.exception),
        )

    def test_context_popped_after_error(self):
        t = template.Template("{% load render_as %}{% render_as obj 'syntax_error' %}")
        o = TestModel.objects.create(name='whatever')
        c = template.Context({'obj': o})
        with self.assertRaises(template.TemplateSyntaxError):
            t.render(c)
        self.assertEqual(
            [
                {'False': False, 'None': None, 'True': True},
                {'obj': o},
            ],
            c.dicts,
        )


class TestRenderAsNonModelObject(TestCase):

    def test_correct_template(self):
        class MyClass(object):
            pass

        t = template.Template("{% load render_as %}{% render_as obj 'correct' %}")
        c = template.Context({'obj': MyClass()})
        self.assertEqual(u"Test non-model object.\n", t.render(c))


class TestRenderAsWithTestModel3(TestCase):

    def test_simple_render_as_invocation_default_template_different_appname(self):
        t = template.Template("{% load render_as %}{% render_as obj 'simple2' %}")
        o = TestModel3(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Just a simple 2 TestModel3 object", t.render(c))

    def test_simple_render_as_invocation_different_appname(self):
        t = template.Template("{% load render_as %}{% render_as obj 'simple' %}")
        o = TestModel3(name='whatever')
        c = template.Context({'obj': o})
        self.assertEqual("Test model 3 whatever\n", t.render(c))
