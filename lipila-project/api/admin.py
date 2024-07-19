from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from .models import (LipilaDisbursement, LipilaCollection)
from lipila.models import (
    ContactInfo, CustomerMessage,
    HeroInfo, UserTestimonial, AboutInfo)
from patron.models import (Tier, SubscriptionPayments,
                           ProcessedWithdrawals, WithdrawalRequest, Contributions)
from accounts.models import PatronProfile, CreatorProfile, CustomUser


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)



class ProcessedWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('withdrawal_request', 'approved_by',
                    'rejected_by', 'request_date', 'processed_date', 'status')


class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('creator', 'amount', 'account_number',
                    'request_date', 'status', 'processed_date', 'reason')


class ContributionsAdmin(admin.ModelAdmin):
    list_display = ('payee', 'payer', 'amount', 'status',
                    'description', 'payer_account_number',
                    'wallet_type', 'timestamp', 'reference_id')


class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'price', 'description',
                    'visible_to_fans', 'updated_at')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payee', 'amount', 'status', 'description', 'payer_account_number',
                    'timestamp', 'reference_id', 'wallet_type')


class DisbursementAdmin(admin.ModelAdmin):
    list_display = ['send_money_to', 'processed_date', 'updated_at', 'amount',
                    'reference_id', 'wallet_type', 'description']


class LipilaCollectionAdmin(admin.ModelAdmin):
    list_display = ['payer_account_number', 'processed_date', 'updated_at', 'amount',
                    'reference_id', 'wallet_type', 'description']


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


class PatronProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_image', 'account_number', 'city',]


class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'patron_title', 'profile_image', 'account_number', 'about',
                    'city', 'creator_category', 'facebook_url', 'twitter_url',
                    'instagram_url', 'linkedin_url',
                    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(SubscriptionPayments, PaymentAdmin)
admin.site.register(Contributions, ContributionsAdmin)
admin.site.register(ProcessedWithdrawals, ProcessedWithdrawalAdmin)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
admin.site.register(LipilaDisbursement, DisbursementAdmin)
admin.site.register(LipilaCollection, LipilaCollectionAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(CustomerMessage, CustomerMessageAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AboutInfo, AboutInfoAdmin)
admin.site.register(UserTestimonial, UserTestimonialAdmin)
admin.site.register(CreatorProfile, CreatorProfileAdmin)
admin.site.register(PatronProfile, PatronProfileAdmin)
admin.site.unregister(Group)
admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = '/'
admin.site.site_title = 'lipila'

# superuser: pita, password: test@123
