from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from .forms import UploadFileForm, EditMediaFileForm
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile


def edit_media_file(request, filename):
    media_file = get_object_or_404(UploadedFile, filename=filename)

    if request.method == 'POST':
        form = EditMediaFileForm(
            request.POST, request.FILES, instance=media_file)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")
            return redirect(reverse('file_manager:media_play', kwargs={'filename': filename}))
    else:
        form = EditMediaFileForm(instance=media_file)

    fs = FileSystemStorage()
    file_url = fs.url(filename)
    content_type = media_file.content_type
    context = {
        'filename': filename,
        'file_url': file_url,
        'f_type': content_type,
        'form': form
    }

    return render(request, 'file_manager/media_edit.html', context)


def delete_media_file(request, filename):
    pass


def play_media_file(request, filename):
    fs = FileSystemStorage()
    file_url = fs.url(filename)
    media_file = get_object_or_404(UploadedFile, filename=filename)

    content_type = media_file.content_type
    description = media_file.long_description
    title = media_file.short_description
    upload_date = media_file.upload_date

    context = {'file_url': file_url,
               'filename': filename,
               'short_description': title,
               'f_type': content_type,
               'long_description': description,
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


def get_media(request, m_type):
    context = {'m_type': m_type}
    if m_type == 'Video':
        context['uploads'] = get_list_or_404(
            UploadedFile, content_type='video/mp4')
    elif m_type == 'Audio':
        context['uploads'] = get_list_or_404(
            UploadedFile, content_type='audio/mpeg')
    return render(request, 'file_manager/media_all.html', context)
