from csv import DictReader
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

# Import the model
from api.models import MyUser, Review, Title


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from review.csv"

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if Review.objects.exists():
            print('review data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        # Show this before loading the data into the database
        print("Loading review data")
        # Code to load the data into database
        for row in DictReader(open('./static/data/review.csv')):
            title = get_object_or_404(Title, id=row['title_id'])
            author = get_object_or_404(MyUser, id=row['author'])
            review = Review(
                id=row['id'], title=title,
                text=row['text'], author=author,
                score=row['score'], pub_date=row['pub_date']
            )
            review.save()
