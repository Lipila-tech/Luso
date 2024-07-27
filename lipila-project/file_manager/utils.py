from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_list_or_404
from .models import UploadedFile


def get_user_files(user, content_type)->list:
    """
    Retrives all files belonging to a user.

    Args:
        user(CustomUserObjetc): The  creator of the file
        content_type(str): The type of files to retrive (video/mp4 or audio/mpeg)

    Returns:
        List object.
    """
    files = get_list_or_404(
                UploadedFile, owner=user, content_type=content_type)
    return files