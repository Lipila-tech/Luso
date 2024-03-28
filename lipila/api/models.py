from django.db import models
from django.contrib.auth.models import User


# Global variables
CITY_CHOICES = (
    ('kitwe', 'Kitwe'),
    ('lusaka', 'Lusaka'),
    ('ndola', 'Ndola'),
)

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)


INVOICE_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('paid', 'paid'),
    ('rejected', 'rejected'),
)

USER_CATEGORY_CHOICES = (
    ('clothing', 'Clothing Shop'),
    ('creator', 'Content Creator'),
    ('grocery', 'Grocery Store'),
    ('school', 'Tuition Center'),
    ('other', 'Other'),
)


class MyUser(User):
    phone_number = models.CharField(
        max_length=20, blank=False, null=False, unique=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=10, default="Zambia")
    address = models.CharField(
        max_length=255, default="", blank=False, null=False)
    company = models.CharField(
        max_length=255, default="", blank=False, null=False)
    city = models.CharField(
        max_length=9, choices=CITY_CHOICES, default='KItwe')
    profile_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    user_category = models.CharField(
        max_length=30, choices=USER_CATEGORY_CHOICES, default='other')

    REQUIRED_FIELDS = ['email', 'phone_number']

    @staticmethod
    def get_user_by_id(ids):
        return MyUser.objects.filter(id__in=str(ids))

    def __str__(self):
        return self.username


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    product_owner = models.ForeignKey(User, related_name='product',
                                      on_delete=models.CASCADE)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{} -> {}".format(self.product_name, self.product_owner)


class LipilaDisbursement(models.Model):
    payer = models.ForeignKey(User,
                              related_name='disbursed',
                              on_delete=models.CASCADE,
                              )
    payee = models.ForeignKey(MyUser,
                              related_name='paid',
                              on_delete=models.CASCADE,
                              )
    payee_account = models.CharField(max_length=30)
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=55)
    transaction_id = models.CharField(max_length=20)
    payment_date = models.DateField()
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def get_account_number(self):
        """ returns the username of the student"""
        return self.payee.phone_number

    def __str__(self):
        return "{} {} {} {} {} {} {} {}".format(self.payee,
                                                self.payment_amount,
                                                self.payment_method,
                                                self.transaction_id,
                                                self.payment_date,
                                                self.payee_account,
                                                self.description,
                                                self.status,
                                                )


class LipilaCollection(models.Model):
    """
    COllect payment from a non registered user to a registered user
    """
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    payer_account = models.CharField(max_length=10, null=False, blank=False)
    payee = models.ForeignKey(User, related_name='user_payment',
                              on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-timestamp']

    def get_reference_id(self):
        return self.reference_id


class LipilaUserCollection(models.Model):
    """
    COllect payment from a registered user to a registered user.
    """
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    payer = models.ForeignKey(MyUser, related_name='receipts',
                              on_delete=models.CASCADE)
    payee = models.ForeignKey(User, related_name='payment',
                              on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-timestamp']

    def get_reference_id(self):
        return self.reference_id

class BNPL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(
        MyUser, related_name='credit', on_delete=models.CASCADE)
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
    debtor = models.ForeignKey(MyUser, related_name='loan',
                               on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')


class Invoice(models.Model):
    """
    Model representing an invoice for non lipila registered customers.
    """
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='invoice')
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


class InvoiceLipilaUser(models.Model):
    """
    Model representing an invoice for Lipila registereds customers.
    """
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bill_from')
    receiver =  models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bill_to')
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
