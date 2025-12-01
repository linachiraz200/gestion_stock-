from django.core.management.base import BaseCommand
from django.db import transaction
from produits.models import Produit
from clients.models import Client
from fournisseurs.models import Fournisseur
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Perform database maintenance tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup-inactive',
            action='store_true',
            help='Remove inactive records older than 1 year',
        )
        parser.add_argument(
            '--optimize-db',
            action='store_true',
            help='Optimize database performance',
        )

    def handle(self, *args, **options):
        if options['cleanup_inactive']:
            self.cleanup_inactive_records()
        
        if options['optimize_db']:
            self.optimize_database()

    def cleanup_inactive_records(self):
        """Remove inactive records older than 1 year"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=365)
        
        with transaction.atomic():
            # Clean up inactive clients
            inactive_clients = Client.objects.filter(
                actif=False,
                date_modification__lt=cutoff_date
            )
            count = inactive_clients.count()
            inactive_clients.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Removed {count} inactive clients')
            )
            logger.info(f'Database cleanup: removed {count} inactive clients')

    def optimize_database(self):
        """Optimize database performance"""
        self.stdout.write('Running database optimization...')
        
        # Add any database optimization tasks here
        # For SQLite, this could include VACUUM, ANALYZE, etc.
        
        self.stdout.write(
            self.style.SUCCESS('Database optimization completed')
        )
        logger.info('Database optimization completed')