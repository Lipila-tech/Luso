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
        subscription = TierSubscriptions.objects.get(
            patron=user, tier__pk=tier_id)
        return True
    except TierSubscriptions.DoesNotExist:
        return False
