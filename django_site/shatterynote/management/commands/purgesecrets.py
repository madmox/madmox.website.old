from django.core.management.base import BaseCommand
from shatterynote.models import Secret


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        Secret.objects.purge()
