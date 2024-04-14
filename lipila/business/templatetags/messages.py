from django import template
from django.contrib.auth.models import User

register = template.Library()

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
def get_creators(value):
    return 301