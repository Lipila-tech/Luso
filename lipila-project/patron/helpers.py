"""
patron app Helper Functions
"""
from accounts.models import CreatorProfile, PatronProfile
from django.contrib.auth.models import User
from typing import Union, List


class NoPatronsFoundError(Exception):
    pass

class NoCreatorsFoundError(Exception):
    pass

def get_patrons() -> List[PatronProfile]:
    """
    Get all users who are patrons
    Returns:
        A list of all patron objects.
    Raises:
        NoPatronsFoundError: If no patron objects are found.
    """
    patron_objects = PatronProfile.objects.all()
    if not patron_objects:
        raise NoPatronsFoundError("No patron objects found.")
    return patron_objects

def get_creators() -> List[CreatorProfile]:
    """
    Get all users who are creators
    Returns:
        A list of all creator objects.
    Raises:
        NoCreatorsFoundError: If no creator objects are found.
    """
    creator_objects = CreatorProfile.objects.all()
    if not creator_objects:
        raise NoCreatorsFoundError("No creator objects found.")
    return creator_objects

def get_patron_or_creator(user)-> Union[PatronProfile, CreatorProfile]:
    if not isinstance(user, User):
            raise User.DoesNotExist('Not a user instance')
    try:
        user = PatronProfile.objects.get(pk=user)
        return user
    except PatronProfile.DoesNotExist:
        pass
    try:
        user = CreatorProfile.objects.get(pk=user)
        return user
    except CreatorProfile.DoesNotExist:
        pass
    try:
        user = User.objects.get(id=user.id)
        return user
    except User.DoesNotExist:
        return None