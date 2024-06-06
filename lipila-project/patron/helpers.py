"""
patron app Helper Functions
"""
from accounts.models import CreatorProfile, PatronProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from typing import Union, List
from patron.models import Tier, TierSubscriptions
from django.urls import reverse


def get_tier(id):
    tier = Tier.objects.get(pk=id)
    return tier


def get_creator_subscribers(creator: CreatorProfile) -> List:
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


def get_creator_url(view_name, creator, domain=None):
    """
    This function generates an absolute URL for a Django view given the view name and arguments.

    Args:
        view_name (str): The name of the Django view as defined in your urlpatterns.
        creator (str): a creators patron name.
        domain (str, optional): The specific domain to use for the absolute URL.
            Defaults to None, which uses the current request's domain if available 
            or settings.ALLOWED_HOSTS otherwise.

    Returns:
        str: The absolute URL for the specified view and arguments.
    """
    relative_url = reverse(view_name)
    if domain:
        # Use the provided domain
        absolute_url = f"{domain}{relative_url}{creator}"
    else:
        # Try to get domain from request (if context) or settings
        try:
            from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(None)
            absolute_url = f"{current_site.domain}{relative_url}{creator}"
        except:
            # Fallback to ALLOWED_HOSTS if request not available
            from django.conf import settings
            # Assuming single allowed host for simplicity
            allowed_hosts = settings.ALLOWED_HOSTS[0]
            absolute_url = f"{allowed_hosts}{relative_url}{creator}"
    return absolute_url
