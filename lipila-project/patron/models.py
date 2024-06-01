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

ONETIME_AMOUNT = 100
FAN_AMOUNT = 25
SUPERFAN_AMOUNT = 50


class Tier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name='tiers')
    updated_at = models.DateTimeField(auto_now=True)
    visible_to_fans = models.BooleanField(default=True)

    @classmethod
    def create_default_tiers(cls, creator):
        # Create default tiers if they don't exist
        defaults = [
            {"name": "Onetime", "price": ONETIME_AMOUNT,
                "description": "Make a one-time contribution to support the creator's work.", 'creator': creator, 'visible_to_fans':True},
            {"name": "Fan", "price": FAN_AMOUNT,
                "description": "Support the creator and get access to exclusive content.", 'creator': creator, 'visible_to_fans':True},
            {"name": "Superfan", "price": SUPERFAN_AMOUNT,
                "description": "Enjoy additional perks and behind-the-scenes content.", 'creator': creator, 'visible_to_fans':True}
        ]
        for tier_data in defaults:
            Tier.objects.get_or_create(
                name=tier_data["name"], defaults=tier_data)

    def __str__(self):
        return f"{self.name} -> {self.price}"


class TierSubscriptions(models.Model):
    patron = models.ForeignKey(PatronProfile, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)


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
