from django.contrib import admin
from api.models import (
    LoanPayment, LoanRequest,
)

# custom
from django.contrib import admin


class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'payment_amount',
                    'payment_method', 'transaction_id', 'payment_date')


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('parent_id', 'loan_amount', 'students', 'created_at')

class SchoolAdminView(admin.AdminSite):
    site_header = "Lipila Loan Administration"
    
#register school site models
loans_site = SchoolAdminView(name="LoansAdmin")
loans_site.register(LoanPayment, LoanPaymentAdmin)
loans_site.register(LoanRequest, LoanRequestAdmin)
