from django import template
from patron.models import TierSubscriptions
from django.shortcuts import redirect
from django.contrib import messages
register = template.Library()

@register.filter(name='is_patron_subscribed')
def is_patron_subscribed(user, tier_id):
  """
  A template filter to check if a patron is subscribed to a tier.

  Args:
      user: A User object representing the patron.
      tier_id: The ID of the Tier to check for subscription.

  Returns:
      True if the patron is subscribed to the tier, False otherwise.
  """

  try:
    subscription = TierSubscriptions.objects.get(patron=user, tier__pk=tier_id)
    return True
  except TierSubscriptions.DoesNotExist:
    return False

@register.filter(name='unsubscribe_patron')
def unsubscribe_patron(request, tier_id):
  """
  A template tag to unsubscribe a user from a tier.

  Args:
      request: The incoming HTTP request object.
      tier_id: The ID of the Tier to unsubscribe from.

  Returns:
      A redirect response to the current page after unsubscribing (or None if not subscribed).
  """
  print('button clicked')

  if request.user.is_authenticated:
    try:
      subscription = TierSubscriptions.objects.get(patron=request.user, tier__pk=tier_id)
      subscription.delete()
      messages.success(request, f"Successfully unsubscribed from {subscription.tier.name}")
      return redirect(request.path)  # Redirect to current page
    except TierSubscriptions.DoesNotExist:
      pass  # User not subscribed, do nothing

  return None  # User not authenticated or error