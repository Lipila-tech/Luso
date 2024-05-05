"""
patron app Helper Functions
"""
from patron.models import CreatorUser, PatronUser
from django.contrib.auth.models import User
from typing import Union, List


class NoPatronsFoundError(Exception):
    pass

class NoCreatorsFoundError(Exception):
    pass

def get_patrons() -> List[PatronUser]:
    """
    Get all users who are patrons
    Returns:
        A list of all patron objects.
    Raises:
        NoPatronsFoundError: If no patron objects are found.
    """
    patron_objects = PatronUser.objects.all()
    if not patron_objects:
        raise NoPatronsFoundError("No patron objects found.")
    return patron_objects

def get_creators() -> List[CreatorUser]:
    """
    Get all users who are creators
    Returns:
        A list of all creator objects.
    Raises:
        NoCreatorsFoundError: If no creator objects are found.
    """
    creator_objects = CreatorUser.objects.all()
    if not creator_objects:
        raise NoCreatorsFoundError("No creator objects found.")
    return creator_objects

def get_patron_or_creator(user:str)-> Union[PatronUser, CreatorUser]:
    pass