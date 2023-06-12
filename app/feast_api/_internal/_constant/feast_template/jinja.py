from jinja2 import Template

def render_j2_template(template_name: str, **kwargs):
    template = Template(template_name)
    rendered_template = template.render(**kwargs).lstrip()
    return rendered_template
