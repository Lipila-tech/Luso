from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UploadFileForm, EditMediaFileForm
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile
from .utils import get_user_files
from django.db.models import Q


def media_edit(request, filename):
    media_file = get_object_or_404(UploadedFile, filename=filename)

    if request.method == 'POST':
        form = EditMediaFileForm(
            request.POST, request.FILES, instance=media_file, user=request.user.creatorprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")
            return redirect(reverse('file_manager:media_play', kwargs={'filename': filename}))
    else:
        form = EditMediaFileForm(instance=media_file, user=request.user.creatorprofile)

    fs = FileSystemStorage()
    file_url = fs.url(filename)
    content_type = media_file.content_type
    context = {
        'filename': filename,
        'file_url': file_url,
        'm_type': content_type,
        'form': form
    }

    return render(request, 'file_manager/media_edit.html', context)


def media_delete(request, filename):
    pass


def media_play(request, filename):
    fs = FileSystemStorage()
    file_url = fs.url(filename)
    media_file = get_object_or_404(UploadedFile, filename=filename)

    content_type = media_file.content_type
    reference = media_file.long_reference
    title = media_file.short_reference
    upload_date = media_file.upload_date
    owner = media_file.owner

    context = {'file_url': file_url,
               'owner': owner,
               'filename': filename,
               'short_reference': title,
               'm_type': content_type,
               'long_reference': reference,
               'upload_date': upload_date}
    return render(request, 'file_manager/media_play.html', context)


def media_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            media_file = UploadedFile.objects.create(
                owner=request.user,
                filename=filename,
                content_type=file.content_type,
            )
            # Get the full path using fs.path(filename)
            file_path = fs.path(filename)
            media_file.file = file_path  # Save the full path to the file field
            media_file.save()
            messages.success(request, "File uploaded")
            return redirect(reverse("file_manager:media_edit", kwargs={'filename': filename}))
    else:
        form = UploadFileForm()
        return render(request, 'file_manager/media_upload.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def get_media(request, m_type):
    """
    Gets all media files on the system

    Args:
        request: The incoming HTTP request
        m_type(str): The type of media to retrieve. Options are (Video, Audio)

    Returns:
        Renders HTML template showing all video/audio files.
    """
    context = {'m_type': m_type}
    media = []

    try:
        if m_type == 'Video':
            media = get_list_or_404(UploadedFile, content_type='video/mp4')
        elif m_type == 'Audio':
            media = get_list_or_404(UploadedFile, content_type='audio/mpeg')
    except Http404:
        return render(request, 'file_manager/media_all.html', context)

    context['media'] = media
    return render(request, 'file_manager/media_all.html', context)


@login_required
@user_passes_test(lambda u: u.is_creator)
def get_user_media(request, m_type):
    context = {'m_type': m_type}
    if m_type == 'Video':
        files = get_user_files(request.user, 'video/mp4')
        context['media'] = files
    elif m_type == 'Audio':
        files = get_user_files(request.user, 'audio/mpeg')
        context['media'] = files
  
    return render(request, 'file_manager/media_all.html', context)
