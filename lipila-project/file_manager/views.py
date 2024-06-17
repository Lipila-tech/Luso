from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile


def play_video_file(request, filename):
    fs = FileSystemStorage()
    file_url = fs.url(filename)
    return render(request, 'file_manager/play_video.html', {'file_url':file_url, 'filename': filename})

def play_audio_file(request, filename):
    fs = FileSystemStorage()
    file_url = fs.url(filename)
    return render(request, 'file_manager/play_audio.html', {'file_url':file_url, 'filename': filename})


def list_video_uploads(request):
    all_uploads = UploadedFile.objects.filter(content_type='video/mp4')  # Assuming UploadedFile model exists
    context = {'uploads': all_uploads}
    return render(request, 'file_manager/list_video_uploads.html', context)

def list_audio_uploads(request):
    all_uploads = UploadedFile.objects.filter(content_type='audio/mpeg')  # Assuming UploadedFile model exists
    context = {'uploads': all_uploads}
    return render(request, 'file_manager/list_audio_uploads.html', context)


def you_tube_player(request):
    return render(request, 'file_manager/you_tube_player.html')

def video_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file = UploadedFile.objects.create(
                filename=filename,
                content_type=file.content_type,  # Get content type from uploaded file
            )
            # Get the full path using fs.path(filename)
            file_path = fs.path(filename)
            uploaded_file.file = file_path  # Save the full path to the file field
            uploaded_file.save()  # Save the model instance
            uploaded_file_url = fs.url(filename)
            return render(request, "file_manager/video_upload.html", {'filename': filename, 'uploaded_file_url': uploaded_file_url})
    else:
        form = UploadFileForm()
        return render(request, 'file_manager/video_upload.html', {'form': form})

def audio_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file = UploadedFile.objects.create(
                filename=filename,
                content_type=file.content_type,  # Get content type from uploaded file
            )
            # Get the full path using fs.path(filename)
            file_path = fs.path(filename)
            uploaded_file.file = file_path  # Save the full path to the file field
            uploaded_file.save()  # Save the model instance
            uploaded_file_url = fs.url(filename)
            return render(request, "file_manager/audio_upload.html", {'filename': filename, 'uploaded_file_url': uploaded_file_url})
    else:
        form = UploadFileForm()
    return render(request, 'file_manager/audio_upload.html', {'form': form})