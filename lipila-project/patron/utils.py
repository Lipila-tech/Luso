"""
patron app Util Functions
"""
from accounts.models import CreatorProfile
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from typing import Union, List
from patron.models import Tier, TierSubscriptions, SubscriptionPayments, Contributions, WithdrawalRequest
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth import get_user_model
import random, re , string


def remove_white_spaces(patron_title: str)-> str:
    """
    Replaces all whitespace with an empty string

    Args:
        patron_title(str): The string to replace whitespaces if any.

    Return:
        String with no white spaces.
    """
    
    # Regular expression pattern to match any whitespace
    pattern = r'\s+'

    # Replace all whitespace with an empty string
    output_string = re.sub(pattern, '', patron_title)
    return output_string


def generate_reference_id():
  """Generates a random 10-character reference ID with digits and letters."""

  characters = string.ascii_letters + string.digits
  return ''.join(random.choice(characters) for _ in range(10))


def calculate_total_withdrawals(creator):
    """
    This function calculates the total amount of withdrawals done by a creator.

    Args:
        creator: A CreatorProfile model instance representing the creator.

    Returns:
        A decimal value representing the total amount of withdrawals.
    """
    # Filter withdrawals for subscriptions belonging to the given creator's tiers
    withdrawals = WithdrawalRequest.objects.filter(
        creator=creator, status='success'
    ).aggregate(total_amount=Sum('amount'))

    if withdrawals['total_amount'] is not None:
        return float(withdrawals['total_amount'])
    else:
        return 0.0


def calculate_total_payments(creator):
    """
    This function calculates the total amount of payments received by a creator.

    Args:
        creator: A CreatorProfile model instance representing the creator.

    Returns:
        A decimal value representing the total amount of payments.
    """
    # Filter payments for subscriptions belonging to the given creator's tiers
    payments = SubscriptionPayments.objects.filter(
        payee__tier__creator=creator, status='success'
    ).aggregate(total_amount=Sum('amount'))

    if payments['total_amount'] is not None:
        return float(payments['total_amount'])
    else:
        return 0.0


def calculate_total_contributions(creator):
    """
    This functions calculates the total amoutn of contributions received by a creator.

    Args:
        Creator: A CretaorProfile model instance representing the creator.

    Returns:
        A decimal value representing the total amount of contributions.
    """
    # Filter contributions for subscriptions belonging to the given creator's tiers
    contributions = Contributions.objects.filter(
        payee=creator, status='success'
    ).aggregate(total_amount=Sum('amount'))

    if contributions['total_amount'] is not None:
        return float(contributions['total_amount'])
    else:
        return 0.0


def calculate_creators_balance(creator):
    """
    This function calculates the avaialble balance.
    Args:
        creator: A CreatorProfile model instance representing the creator.

    Returns:
        A decimal value representing the total amount of withdrawals.
    """
    total_payments = calculate_total_payments(creator)
    total_contributions = calculate_total_contributions(
        get_user_model().objects.get(username=creator))
    withdrawals = calculate_total_withdrawals(creator)
    balance = (total_payments + total_contributions) - withdrawals
    return balance


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


def get_creator_url(view_name, patron_title, domain=None):
    """
    This function generates an absolute URL for a Django view given the view name and arguments.

    Args:
        view_name (str): The name of the Django view as defined in your urlpatterns.
        title (str): a creators patron name.
        domain (str, optional): The specific domain to use for the absolute URL.
            Defaults to None, which uses the current request's domain if available 
            or settings.ALLOWED_HOSTS otherwise.

    Returns:
        str: The absolute URL for the specified view and arguments.
    """
    relative_url = reverse(view_name)
    title = remove_white_spaces(patron_title)
    if domain:
        # Use the provided domain
        absolute_url = f"{domain}{relative_url}{title}"
    else:
        # Try to get domain from request (if context) or settings
        try:
            from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(None)
            absolute_url = f"{current_site.domain}{relative_url}{title}"
        except:
            # Fallback to ALLOWED_HOSTS if request not available
            from django.conf import settings
            # Assuming single allowed host for simplicity
            allowed_hosts = settings.ALLOWED_HOSTS[0]
            absolute_url = f"{allowed_hosts}{relative_url}{title}"
    return absolute_url
