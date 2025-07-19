from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Blocks an IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_addresses', nargs='+', type=str,
                          help='IP address(es) to block')

    def handle(self, *args, **options):
        for ip in options['ip_addresses']:
            try:
                # Validate IP address format
                validate_ipv46_address(ip)
                
                # Create blocked IP entry if it doesn't exist
                blocked_ip, created = BlockedIP.objects.get_or_create(ip_address=ip)
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully blocked IP "{ip}"')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'IP "{ip}" was already blocked')
                    )
                    
            except ValidationError:
                raise CommandError(f'Invalid IP address format: "{ip}"')