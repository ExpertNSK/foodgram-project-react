import csv

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient, Tag


TABLES_DICT = {
    Ingredient: 'ingredients.csv'
}


class Command(BaseCommand):
    help = 'Load data from csv file'

    def handle(self, *args, **kwargs):
        for model, base in TABLES_DICT.items():
            with open(
                f'{settings.BASE_DIR}/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    name, measurement_unit = row
                    model.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit,
                    )

        self.stdout.write(self.style.SUCCESS('Successfully load data'))
