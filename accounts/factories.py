import factory
from factory.django import DjangoModelFactory
from .models import CustomUser, CreatorProfile, PayoutAccount
from patron.models import Tier
from .globals import zambia_provinces, CREATOR_CATEGORY_CHOICES, WALLET_TYPES, DEFAULT_PRICES


# Factory for CustomUser
class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = "test@123"
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_creator = factory.Faker('boolean')
    is_superuser = False
    has_group = factory.Faker('boolean')

# Factory for CreatorProfile
class CreatorProfileFactory(DjangoModelFactory):
    class Meta:
        model = CreatorProfile

    user = factory.SubFactory(CustomUserFactory)
    patron_title = factory.Faker('slug')
    is_verified = factory.Faker('boolean')
    about = factory.Faker('text', max_nb_chars=150)
    location = factory.Faker('random_element', elements=[choice[0] for choice in zambia_provinces])
    adults_group = factory.Faker('boolean')
    country = 'Zambia'
    address = factory.Faker('address')
    creator_category = factory.Faker('random_element', elements=[choice[0] for choice in CREATOR_CATEGORY_CHOICES])
    facebook_url = factory.Faker('url')
    twitter_url = factory.Faker('url')
    instagram_url = factory.Faker('url')
    linkedin_url = factory.Faker('url')

# Factory for PayoutAccount
class PayoutAccountFactory(DjangoModelFactory):
    class Meta:
        model = PayoutAccount

    user_id = factory.SubFactory(CreatorProfileFactory)
    wallet_type = factory.Faker('random_element', elements=[choice[0] for choice in WALLET_TYPES])
    wallet_provider = factory.Faker('company')
    account_name = factory.Faker('name')
    account_number = factory.Faker('numerify', text='#############')
    account_currency = 'ZMW'


# Factory for Tier
class TierFactory(DjangoModelFactory):
    class Meta:
        model = Tier

    name = factory.Faker('sentence', nb_words=4)
    reference = factory.Faker('paragraph', nb_sentences=3)
    price = factory.Faker('random_element', elements=[choice[0] for choice in DEFAULT_PRICES])
    creator = None
    visible_to_fans = factory.Faker('boolean')
    is_editable = factory.Faker('boolean')


# Create a single user with related profile and payout account
# user = CustomUserFactory()
# profile = CreatorProfileFactory(user=user)
# payout_account = PayoutAccountFactory(user_id=profile)
# tier = TierFactory(creator=profile)

# Or create multiple instances
# users = CustomUserFactory.create_batch(3)
# profiles = CreatorProfileFactory.create_batch(3, user=factory.Iterator(users))
# payout_accounts = PayoutAccountFactory.create_batch(3, user_id=factory.Iterator(profiles))
# tiers = TierFactory.create_batch(3, creator=factory.Iterator(profiles))

