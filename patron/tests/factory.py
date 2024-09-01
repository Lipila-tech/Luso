import factory
from django.contrib.auth import get_user_model
from accounts.models import CreatorProfile

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class CreatorProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreatorProfile

    user = factory.SubFactory(UserFactory)
    patron_title = 'testpatron'
    about = 'test'
    creator_category = 'musician'
