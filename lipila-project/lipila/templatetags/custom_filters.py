from django import template
from django.contrib.auth.models import User
from accounts.models import CreatorProfile

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


@register.filter
def get_users(value):
    users = User.objects.count()
    return users

@register.filter
def get_hours(value):
    return 125

@register.filter
def get_transactions(value):
    return 231

@register.filter
def get_patron(value):
    patron = CreatorProfile.objects.count()
    return patron

@register.simple_tag
def get_messages():
    messages = []
    msg1 = {
        'sender': 'Peter Chola',
        'message': 'I need some anti rabies',
        'time': '4 hrs ago'
    }
    msg2 = {
        'sender': 'Obby S',
        'message': 'I need some anti rabies',
        'time': '3 hrs ago'
    }
    messages.append(msg1)
    messages.append(msg2)
    return messages

@register.filter
def message_counter(value, id):
    if isinstance(id, int):
        return id
    else:
        return 0
    
@register.simple_tag
def get_notifications():
    notifications = []
    msg1 = {
        'title': 'Upgrade',
        'body': 'Upgrade your account',
        'time': '4 hrs ago'
    }
    msg2 = {
        'title': 'Request',
        'body': 'I need some anti rabies',
        'time': '3 hrs ago'
    }
    msg3 = {
        'title': 'Payment Received',
        'body': 'I need some anti rabies',
        'time': '3 hrs ago'
    }
    notifications.append(msg1)
    notifications.append(msg2)
    notifications.append(msg3)
    return notifications


@register.filter
def notification_counter(value, id):
    if isinstance(id, int):
        return id
    else:
        return 0
