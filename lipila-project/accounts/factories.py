import factory
from factory.django import DjangoModelFactory
from .models import CustomUser, CreatorProfile, PayoutAccount
from .globals import zambia_provinces, CREATOR_CATEGORY_CHOICES, WALLET_TYPES


# Factory for CustomUser
class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('email')
    username = factory.Faker('user_name')
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
