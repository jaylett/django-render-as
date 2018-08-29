# Django "render_as" template tag

`{% render_as obj "type" %}` is a simple template tag that renders a
suitable template based on the object passed to it and a type. For
Django model objects, the template will be one of:

 * `<app>/<model>_<type>.html`
 * `render_as/default_<type>.html`

For non-model objects, the template will be one of:

 * `<module>/<class>_<type>.html`
 * `render_as/default_<type>.html`

where `<module>` is the last component of the module path and
`<class>` will be the lower-cased classname (so for an object whose
class is `my_library.sub_library.MyClass` the first template checked
will be `sub_library/myclass.html`).

With the template backend option `debug` enabled, a
`TemplateSyntaxError` exception is raised for errors; otherwise just
renders blank.

Note that this is currently untested with template engines other than
DTL, although it should in theory work.

[James Aylett][Home]
[Home]: http://tartarus.org/james/
