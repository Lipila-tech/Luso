from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def video_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()  # Get default storage system
            filename = fs.save(file.name, file)  # Save file to MEDIA_ROOT
            uploaded_file_url = fs.url(filename)  # Get the URL of the uploaded file
            return render(request, "file_manager/video_upload.html", {'filename': filename, 'uploaded_file_url': uploaded_file_url})
    else:
        form = UploadFileForm()
    return render(request, 'file_manager/video_upload.html', {'form': form})