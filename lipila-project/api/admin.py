from django.contrib import admin
from .models import (BusinessUser, LipilaDisbursement, LipilaCollection)
from business.models import Product, BNPL, Student
from lipila.models import (
    ContactInfo, CustomerMessage,
    HeroInfo, UserTestimonial, AboutInfo)
from patron.models import Tier, Contribution, PatronUser, CreatorUser
from accounts.models import Profile


class BusinessUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'account_number', 'bio', 'business_category',
                    'address', 'company', 'city', 'country', 'first_name', 'profile_image')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'other_name',
                    'school', 'address', 'grade')


class CreatorUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'account_number')


class PatronAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number')


class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class ContributionAdmin(admin.ModelAdmin):
    list_display = ('creator', 'patron', 'tier', 'amount', 'timestamp')


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


# Register your models here.
admin.site.register(PatronUser, PatronAdmin)
admin.site.register(CreatorUser, CreatorUserAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(Profile)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(BusinessUser, BusinessUserAdmin)
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

admin.site.site_header = 'Lipila Adminstration'
admin.site.site_url = '/'
admin.site.site_title = 'lipila'

# superuser: pita, password: test@123
