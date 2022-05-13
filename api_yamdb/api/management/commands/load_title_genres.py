from csv import DictReader
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

# Import the model
from api.models import GenreTitle, Title, Genre


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
        if GenreTitle.objects.exists():
            print('title_genre data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        # Show this before loading the data into the database
        print("Loading title_genre data")
        # Code to load the data into database
        for row in DictReader(open('./static/data/genre_title.csv')):
            title = get_object_or_404(Title, id=row['title_id'])
            genre = get_object_or_404(Genre, id=row['genre_id'])
            genre_title = GenreTitle(
                id=row['id'], title=title,
                genre=genre
            )
            genre_title.save()
