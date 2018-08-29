import os.path

from django import template
from django.template.loader import select_template


register = template.Library()


@register.tag
def render_as(parser, token):
    """
    Template tag which renders a suitable template for the object. Call as:

    {% render_as obj type %}

    The template is found by looking in order for:

     * <app>/<model>_<type>.html
     * render_as/default_<type>.html

    and rendering with the context at the time of the call, updated to
    include `object` as the first parameter to the {% render_as ... %} call.
    """

    try:
        tag_name, object_ref, type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(u"'%s' tag requires two arguments" % token.contents.split()[0])
    return RenderAsNode(object_ref, type)


class RenderAsNode(template.Node):
    def __init__(self, object_ref, type_ref):
        self.object_var = template.Variable(object_ref)
        self.type = template.Variable(type_ref)

    def render(self, context):
        result = u""
        try:
            obj = self.object_var.resolve(context)
        except template.VariableDoesNotExist:
            if context.template.engine.debug:
                raise template.TemplateSyntaxError(
                    u"no such variable '%s' in render_as call" % self.object_var
                )
            else:
                return u""
        try:
            type = self.type.resolve(context)
        except template.VariableDoesNotExist:
            if context.template.engine.debug:
                raise template.TemplateSyntaxError(
                    u"no such variable '%s' in render_as call" % self.type
                )
            else:
                return u""

        try:
            # default to <app>/<model>...
            app_name = obj._meta.app_label
            model_name = obj._meta.model_name
        except AttributeError:
            # fall back to most specific module and lowercased
            # class name
            try:
                app_name = type(obj).__module__.split(".")[-1]
            except TypeError:
                # SafeText has snuck its way in
                app_name = obj.__class__.__module__.split(".")[-1]
            model_name = obj.__class__.__name__.lower()

        if isinstance(context, template.Context):
            ctx = context.flatten()
        else:
            ctx = dict(context)
        ctx['object'] = obj
        try:
            main_template = os.path.join(app_name, "render_as", "%s_%s.html" % (model_name, type))
            backup_template = os.path.join('render_as', "default_%s.html" % (type,))
            t = select_template([main_template, backup_template])
            result = t.render(ctx)
        except Exception:
            if context.template.engine.debug:
                raise
        return result
