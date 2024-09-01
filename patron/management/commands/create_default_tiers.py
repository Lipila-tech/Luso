
from django.core.management.base import BaseCommand
from patron.models import Tier

class Command(BaseCommand):
    help = 'Creates default tiers'

    def handle(self, *args, **options):
        Tier.create_default_tiers()
        self.stdout.write(self.style.SUCCESS('Default tiers created successfully'))
