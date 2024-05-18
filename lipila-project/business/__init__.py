from django.apps import AppConfig
from django import template

class WebAppConfig(AppConfig):
  name = 'business'

  def ready(self):
    from .templatetags import messages
    template.add_to_search(messages)  # Add the tag library to search paths
