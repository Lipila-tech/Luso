from django.db import models
from accounts.models import CreatorProfile, PatronProfile
# Options
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)

CREATOR_CATEGORY_CHOICES = (
    ('artist', 'Artist'),
    ('musician', 'Musician'),
    ('videocreator', 'Video Creator'),
    ('podcaster', 'Podcaster'),
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

ONETIME_AMOUNT = 50
FAN_AMOUNT = 10
SUPERFAN_AMOUNT = 30


class Tier(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def create_default_tiers(cls):
        # Create default tiers if they don't exist
        defaults = [
            {"name": "Onetime", "price": ONETIME_AMOUNT},
            {"name": "Fan", "price": FAN_AMOUNT},
            {"name": "Superfan", "price": SUPERFAN_AMOUNT}
        ]
        for tier_data in defaults:
            Tier.objects.get_or_create(
                name=tier_data["name"], defaults=tier_data)

    def __str__(self):
        return f"{self.name} -> {self.price}"


class Contribution(models.Model):
    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name='contributions_received')
    patron = models.ForeignKey(
        PatronProfile, on_delete=models.CASCADE, related_name='contributions_made')
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contribution of {self.amount} by {self.patron} to {self.creator} on {self.contribution_date}"
