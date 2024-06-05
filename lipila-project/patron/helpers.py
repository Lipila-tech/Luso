"""
patron app Helper Functions
"""
from accounts.models import CreatorProfile, PatronProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from typing import Union, List
from patron.models import Tier, TierSubscriptions


def get_creator_subscribers(creator: CreatorProfile)->List:
    """
    Retrieves all patrons subscribed to a creator.

    Args:
        creator: A User object representing the creator.

    Returns:
        A queryset of User objects representing the creator's patrons.
    """

    subscriptions = TierSubscriptions.objects.filter(
        tier__creator=creator, tier__visible_to_fans=True
    ).prefetch_related('patron')  # Prefetch patrons for efficiency

    # Extract the patron Users from the subscriptions
    patrons = [subscription.patron for subscription in subscriptions]
    return patrons


def is_patron_subscribed(patron, tier_id):
    """
    Checks if a patron is subscribed to a given tier.

    Args:
        patron: A User object representing the patron.
        tier_id: The ID of the Tier to check for subscription.

    Returns:
        True if the patron is subscribed to the tier, False otherwise.
    """

    try:
        subscription = TierSubscriptions.objects.get(
            patron=patron, tier__pk=tier_id)
        return True
    except TierSubscriptions.DoesNotExist:
        return False
