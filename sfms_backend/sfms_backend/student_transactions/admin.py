from django.contrib import admin
from .models import Student, Payment, Term, Program


class StudentAdmin(admin.ModelAdmin):
    list_display = ("firstname", 'lastname', 'tuition', 'program', 'student_no')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'pay_date', 'amount', 'term', 'status')

class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'tuition')


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Program, ProgramAdmin)