from django import template


register = template.Library()

@register.filter(name="add_class")
def add_class(value, arg):
    return value.as_widget(attrs={"class":arg})

@register.filter(name='currency')
def currency(number):
    return "ZK "+ str(number)

@register.filter
def add_css_class(field, css_class):
    """
    Add a CSS class to the form field.
    """
    return field.as_widget(attrs={'class': css_class})