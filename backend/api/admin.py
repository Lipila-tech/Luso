from django.contrib import admin
from .models import (
    Student, Payment, School, Parent
)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'grade_level',
                    'enrollment_number', 'parent_id', 'tuition')
    search_fields = ('enrollment_number', 'first_name', 'last_name', 'grade_level')
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Student.objects.all()
        elif request.user.is_staff:
            school = School.objects.filter(administrator=request.user) # get schools by admin
            school_ids = [school.id for school in school] # get school ids
            parent_id = Parent.objects.filter(school=int(school_ids[0])) # find the school the parent belongs to
            return Student.objects.filter(parent_id=int(parent_id))
        else:
            return Student.objects.none()


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number', 'payment_amount',
                    'payment_method', 'transaction_id', 'payment_date')
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Payment.objects.all()
        elif request.user.is_staff:
            school = School.objects.filter(administrator=request.user)
            school_ids = [school.id for school in school]
            return Payment.objects.filter(school=int(school_ids[0]))
        else:
            return Payment.objects.none()


class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address',
                    'mobile_number', 'employer', 'address', 'school')
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Parent.objects.all()
        elif request.user.is_staff:
            school = School.objects.filter(administrator=request.user)
            school_ids = [school.id for school in school]
            return Parent.objects.filter(school=int(school_ids[0]))
        else:
            return Parent.objects.none()


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'city', 'province', 'administrator')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return School.objects.all()
        elif request.user.is_staff:
            return School.objects.filter(administrator=request.user)
        else:
            return School.objects.none()
        

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Parent, ParentAdmin)

admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = ''

# superuser: pita, password: test@123