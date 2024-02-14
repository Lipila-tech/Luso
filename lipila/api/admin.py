from django.contrib import admin
from .models import (MyUser,
                     Product, LipilaPayment, BusinessPayment,
                     LipilaDisbursement
                     )


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'bio',
                    'address', 'company', 'city', 'country', 'first_name', 'profile_image')


class LipilaPaymentAdmin(admin.ModelAdmin):
    list_display = ('receiver_account', 'payer_account', 'amount', 'timestamp',
                    'reference_id', 'description', 'payer_email',
                    'payer_name', 'status')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return LipilaPayment.objects.all()
        else:
            return LipilaPayment.objects.none()


class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('payer', 'payee', 'payee_account', 'payment_amount', 'payment_method',
                    'description', 'transaction_id', 'payment_date')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_owner', 'price',
                    'date_created', 'status')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.none()


class BusinessPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_owner', 'payer_account', 'amount', 'timestamp',
                    'reference_id', 'description', 'payer_email',
                    'payer_name', 'status')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return BusinessPayment.objects.all()
        else:
            return BusinessPayment.objects.none()


# Register your models here.
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(LipilaPayment, LipilaPaymentAdmin)
admin.site.register(LipilaDisbursement, DisbursementAdmin)
admin.site.register(BusinessPayment, BusinessPaymentAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = '/api/v1/index'

# superuser: pita, password: test@123
