from django.contrib import admin
from .models import (
    Student, Payment, School,
    LoanPayment, LoanRequest, Parent
)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'grade_level',
                    'enrollment_number', 'parent_id', 'school', 'tuition')
    search_fields = ('enrollment_number', 'first_name', 'last_name', 'grade_level')
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Student.objects.all()
        elif request.user.is_staff:
            school = School.objects.filter(administrator=request.user)
            school_ids = [school.id for school in school]
            return Student.objects.filter(school=int(school_ids[0]))
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
    

class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'payment_amount',
                    'payment_method', 'transaction_id', 'payment_date')


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'loan_amount', 'students', 'created_at')

    

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(LoanPayment, LoanPaymentAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)

admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = ''