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


@register.filter(name='comma_format')
def comma_format(value):
  """
  Formats a number with comma separators for thousands.
  """
  try:
    # Handle potential non-numeric input (e.g., empty string)
    if not value:
      return value
    return "{:,}".format(int(value))  # Convert to int for safety and format with comma separators
  except (ValueError, TypeError):
    return value  # Return the original value if conversion fails

