import sys

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    help = 'Waits for the database to become available'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        count = 0
        db_conn = None
        while not db_conn and count < 30:
            try:
                # Try to get database connection
                db_conn = connections['default']
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database available!'))
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
                count += 1
                db_conn = None

        if count == 30:
            self.stdout.write(self.style.ERROR('Database not available after 30 attempts, exiting...'))
            sys.exit('Database not available, exiting...')