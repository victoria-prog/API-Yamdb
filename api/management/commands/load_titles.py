from csv import DictReader
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

# Import the model
from api.models import MyUser, Title, Category


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if Title.objects.exists():
            print('title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        # Show this before loading the data into the database
        print("Loading title data")
        # Code to load the data into database
        for row in DictReader(open('./static/data/titles.csv')):
            category = get_object_or_404(Category, id=row['category'])
            author = get_object_or_404(MyUser, id=row['author'])
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category=category,
                author=author
            )
            title.save()
