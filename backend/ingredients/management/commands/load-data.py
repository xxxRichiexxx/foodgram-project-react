import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            action='store',
            help='название файла',
        )

    def handle(self, *args, **options):
        file_name = options.get('file')
        if file_name:
            path = os.path.join(
                os.path.dirname(settings.BASE_DIR), "data/"
            ) + file_name
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
