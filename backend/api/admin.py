from django.contrib import admin
from .models import (
    Student, Payment, School,
    LoanPayment, LoanRequest, Parent
)

# custom
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'grade_level',
                    'enrollment_number', 'parent_id', 'school', 'tuition')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number', 'payment_amount',
                    'payment_method', 'transaction_id', 'payment_date')


class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address',
                    'mobile_number', 'employer', 'address')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'city', 'province', 'administrator')


class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'payment_amount',
                    'payment_method', 'transaction_id', 'payment_date')


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'loan_amount', 'students', 'created_at')

class SchoolAdminView(admin.AdminSite):
    site_header = "Lipila School Administration"
    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [path("my_view/", self.admin_site.admin_view(self.my_view))]
    #     return my_urls + urls

    # def my_view(self, request):
    #     # ...
    #     context = dict(
    #         # Include common variables for rendering the admin template.
    #         self.admin_site.each_context(request),
    #         # Anything else you want in the context...
    #         # key=value,
    #     )
    #     return TemplateResponse(request, "custom_admin_view.html", context)

school_admin = SchoolAdminView(name="School Admin")


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(LoanPayment, LoanPaymentAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)

admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = ''
