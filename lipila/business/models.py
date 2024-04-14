from django.db import models
from django.contrib.auth.models import User

# Options
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)

BUSINESS_CATEGORY_CHOICES = (
    ('school', 'School'),
    ('grocery', 'Grocery'),
    ('independent_online_retailers', 'Independent Online Retailers'),
    ('other', 'Other'),
)

CITY_CHOICES = (
    ('kitwe', 'Kitwe'),
    ('lusaka', 'Lusaka'),
    ('ndola', 'Ndola'),
)

INVOICE_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('paid', 'paid'),
    ('rejected', 'rejected'),
)

class BusinessUser(User):
    phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=10, default="Zambia")
    address = models.CharField(
        max_length=255, default="", blank=True, null=True)
    company = models.CharField(
        max_length=255, default="", blank=True, null=True)
    city = models.CharField(
        max_length=9, choices=CITY_CHOICES, default='Kitwe')
    profile_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    business_category = models.CharField(
        max_length=30, choices=BUSINESS_CATEGORY_CHOICES, default='other')
    facebook_url = models.CharField(max_length=250, null=True, blank=True, default='')
    linkedin_url = models.CharField(max_length=250, null=True, blank=True, default='')
    twitter_url = models.CharField(max_length=250, null=True, blank=True, default='')
    instagram_url = models.CharField(max_length=250, null=True, blank=True, default='')

    REQUIRED_FIELDS = ['email']

    @staticmethod
    def get_user_by_id(ids):
        return BusinessUser.objects.filter(id__in=str(ids))

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(User, related_name='product',
                                      on_delete=models.CASCADE)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return "{} -> {}".format(self.name, self.owner, self.quantity)


class BNPL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(
        BusinessUser, related_name='credit', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='bnpl', on_delete=models.CASCADE)
    initial_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(
        User, related_name='approvals', on_delete=models.CASCADE, null=True, blank=True)

    def _str__(self):
        return f"{self.requsted_by.username}, requested: {self.amount}"


class LoanCollection(models.Model):
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    payer_account = models.CharField(max_length=10, null=False, blank=False)
    debtor = models.ForeignKey(BusinessUser, related_name='loan',
                               on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')


class Invoice(models.Model):
    """
    Model representing an invoice for non lipila registered customers.
    """
    creator = models.ForeignKey(BusinessUser, on_delete=models.CASCADE, related_name='invoice')
    customer_name = models.CharField(max_length=255)
    customer_phone_number = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    reference_number = models.CharField(max_length=50, blank=True)
    due_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=INVOICE_STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice for {self.customer_name} - {self.total_amount}"


class InvoiceBusinessUser(models.Model):
    """
    Model representing an invoice for Lipila registereds customers.
    """
    creator = models.ForeignKey(BusinessUser, on_delete=models.CASCADE, related_name='bill_from')
    receiver =  models.ForeignKey(BusinessUser, on_delete=models.CASCADE, related_name='bill_to')
    reference_number = models.CharField(max_length=50, blank=True)
    due_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=INVOICE_STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice for {self.customer_name} - {self.total_amount}"