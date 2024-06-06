from django.contrib import admin
from .models import (LipilaDisbursement, LipilaCollection)
from business.models import Product, BNPL, Student
from lipila.models import (
    ContactInfo, CustomerMessage,
    HeroInfo, UserTestimonial, AboutInfo)
from patron.models import Tier, Payments
from accounts.models import PatronProfile, CreatorProfile


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'other_name',
                    'school', 'address', 'grade')


class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'price', 'description', 'visible_to_fans', 'updated_at')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'timestamp')


class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('payer', 'payee', 'payee_account', 'payment_amount', 'payment_method',
                    'description', 'transaction_id', 'payment_date')


class LipilaCOllectionAdmin(admin.ModelAdmin):
    list_display = ('payer', 'payee', 'amount',
                    'description', 'reference_id', 'timestamp', 'status')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'price',
                    'date_created', 'description', 'quantity')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.none()


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('street', 'location', 'phone1', 'phone2',
                    'email1', 'email2', 'hours', 'days', 'timestamp')


class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',
                    'subject', 'message', 'timestamp')


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ('slogan', 'message', 'hero_image', 'timestamp')


class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'timestamp')


class UserTestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')


class BNPLAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'requested_by',
        'product',
        'amount',
        'status',
        'approved_by'
    )


class PatronProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_image', 'account_number', 'city',]


class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'patron_title', 'profile_image', 'account_number', 'bio',
                    'city', 'creator_category', 'facebook_url', 'twitter_url',
                    'instagram_url', 'linkedin_url',
                    ]


admin.site.register(Tier, TierAdmin)
admin.site.register(Payments, PaymentAdmin)
admin.site.register(LipilaDisbursement, DisbursementAdmin)
admin.site.register(LipilaCollection, LipilaCOllectionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BNPL, BNPLAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(CustomerMessage, CustomerMessageAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AboutInfo, AboutInfoAdmin)
admin.site.register(UserTestimonial, UserTestimonialAdmin)
admin.site.register(CreatorProfile, CreatorProfileAdmin)
admin.site.register(PatronProfile, PatronProfileAdmin)

admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = '/'
admin.site.site_title = 'lipila'

# superuser: pita, password: test@123
