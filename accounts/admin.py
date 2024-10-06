from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from api.models import (
    LipilaDisbursement, MomoColTransaction, MomoColTransaction)
from lipila.models import (
    ContactInfo, CustomerMessage,
    HeroInfo, UserTestimonial, AboutInfo)
from patron.models import (Tier,
                           ProcessedWithdrawals, WithdrawalRequest, Payment)
from accounts.models import CreatorProfile, CustomUser, UserSocialAuth


class AirtelTransactionModel(admin.ModelAdmin):
    list_display = ['reference', 'transaction_id', 'msisdn',
                    'amount', 'status', 'created_at', 'updated_at']
    search_fields = ['reference', 'transaction_id', 'msisdn']


class UserSocialAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'created_at', 'updated_at')
    search_fields = ('user__username', 'provider')


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser', 'is_creator', 'has_group')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_creator', 'has_group')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)


class ProcessedWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('withdrawal_request', 'approved_by',
                    'rejected_by', 'request_date', 'processed_date', 'status')


class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('creator', 'amount', 'account_number',
                    'request_date', 'status', 'processed_date', 'reason')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payee', 'payer', 'amount', 'status',
                    'reference', 'msisdn',
                    'wallet_type', 'timestamp', 'transaction_id')


class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'price', 'reference',
                    'visible_to_fans', 'updated_at', 'is_editable')
    search_fields = ['name']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payee', 'amount', 'authenticated_payer', 'anonymous_payer', 'status', 'reference', 'msisdn',
                    'timestamp', 'transaction_id', 'wallet_type')


class DisbursementAdmin(admin.ModelAdmin):
    list_display = ['send_money_to', 'processed_date', 'updated_at', 'amount',
                    'transaction_id', 'wallet_type', 'reference']


class LipilaCollectionAdmin(admin.ModelAdmin):
    list_display = ['msisdn', 'processed_date', 'updated_at', 'amount',
                    'transaction_id', 'wallet_type', 'reference']


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('street', 'location', 'phone1', 'phone2',
                    'email1', 'email2', 'hours', 'days', 'timestamp')


class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_seen', 'handler',
                    'subject', 'message', 'timestamp')


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ('slogan', 'message', 'hero_image', 'timestamp')


class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'timestamp')


class UserTestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')


class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'patron_title', 'profile_image', 'about',
                    'location', 'creator_category', 'facebook_url', 'twitter_url',
                    'instagram_url', 'linkedin_url',
                    ]


# Register
admin.site.register(MomoColTransaction, AirtelTransactionModel)
admin.site.register(UserSocialAuth, UserSocialAuthAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ProcessedWithdrawals, ProcessedWithdrawalAdmin)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
admin.site.register(LipilaDisbursement, DisbursementAdmin)
admin.site.register(MomoColTransaction, LipilaCollectionAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(CustomerMessage, CustomerMessageAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AboutInfo, AboutInfoAdmin)
admin.site.register(UserTestimonial, UserTestimonialAdmin)
admin.site.register(CreatorProfile, CreatorProfileAdmin)


# Unregister
admin.site.unregister(Group)


url = reverse('staff_dashboard')
# Configure site
admin.site.site_header = 'Luso Adminstration'
admin.site.site_url = url
admin.site.site_title = 'lipila'

# superuser: pita, password: test@123
