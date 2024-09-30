from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from patron.models import Tier

fs = FileSystemStorage()  # Default storage

class UploadedFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="multimedia")
    filename = models.CharField(max_length=255)
    short_reference = models.CharField(max_length=255, blank=True)
    long_reference = models.TextField(max_length=500, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    tiers = models.ManyToManyField(Tier, related_name='multimedia', blank=True)
    file = models.FileField(
        upload_to=fs.path,
        storage=fs,
         validators=[FileExtensionValidator(
             allowed_extensions=['mp3', 'wav', 'mp4', 'avi', 'mov', 'pdf', 'png', 'jpg', 'jpeg'])])

    def __str__(self):
        return self.filename
