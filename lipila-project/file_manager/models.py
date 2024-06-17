from django.db import models
from django.core.files.storage import FileSystemStorage

# Use a custom storage class if needed (optional)
# class MyCustomStorage(FileSystemStorage):
#     pass

fs = FileSystemStorage()  # Default storage

class UploadedFile(models.Model):
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=255)
    file = models.FileField(upload_to=fs.path, storage=fs)  # Using default storage

    def __str__(self):
        return self.filename
