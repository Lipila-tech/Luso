"""
patron app Helper Functions
"""
from accounts.models import CreatorProfile, PatronProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from typing import Union, List
from patron.models import Tier, TierSubscriptions


def get_patrons(user)-> List:
    """
    Gets all users who are a creators patrons.
        Args:
            user: The creator user..
        Returns: A list of patrons.
    """
    creator_object = get_object_or_404(CreatorProfile, user=user)
    tiers = Tier.objects.filter(creator=creator_object)
    patrons = []
    data = {}
    for tier in tiers:
        subs = TierSubscriptions.objects.filter(tier=tier)
        for sub in subs:
            data['patron'] = sub.patron
            data['tier'] = sub.tier
            patrons.append(data)
    return patrons
        
    
