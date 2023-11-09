from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from .models import School, Student

# Define permissions
school_view_permission = Permission.objects.create(
    name='Can view schools',
    content_type=ContentType.objects.get_for_model(School),
)

student_view_permission = Permission.objects.create(
    name='Can view students',
    content_type=ContentType.objects.get_for_model(Student),
)

# Assign permissions to groups
schools_group = Group.objects.get(name='schools')
schools_group.permissions.add(school_view_permission)
schools_group.permissions.add(student_view_permission)
