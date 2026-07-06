from django.core.management import call_command
from django.core.management.base import BaseCommand

from myApp.models import BlogPost, SectionImage


class Command(BaseCommand):
    help = ('Load the site_content fixture, but only when the database is empty. '
            'Safe to run on every deploy: it never overwrites existing content.')

    def handle(self, *args, **options):
        if SectionImage.objects.exists() or BlogPost.objects.exists():
            self.stdout.write('Database already has content - nothing to do.')
            return
        self.stdout.write('Empty database detected - loading site_content fixture...')
        call_command('loaddata', 'site_content')
        self.stdout.write(self.style.SUCCESS('Site content loaded.'))
