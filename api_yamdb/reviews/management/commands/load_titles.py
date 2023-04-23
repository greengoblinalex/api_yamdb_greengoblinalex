import csv
from django.core.management import BaseCommand

from reviews.models import Title, Genre, Category, TitleGenre

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""
FILES = [
         'category.csv', 'genre.csv', 'titles.csv', 'genre_title.csv',

         # 'comments.csv', 'review.csv', 'users.csv'
         # раскомментировать как появятся другие модели
         ]
MODELS = [Category, Genre, Title, TitleGenre, ]
          # добавить новые модели как появятся


def import_csv(file, model):
    with open(file, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print(file)
        for row in reader:
            obj = model()
            # for field in model._meta.fields:
            #     if field.name in row:
            #         setattr(obj, field.name, row[field.name])
            print(row)

            # obj.save()


# def import_related_csv(file, model):
#     with open(file, encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         print(file)
#         for row in reader:
#             obj = model()
#             for field in model._meta.fields:
#                 if field.name in row:
#                     setattr(obj, field.name, row[field.name])
#             print(row)
#             obj.save()


def exist_models(model):
    ...


class Command(BaseCommand):
    help = "Loads data from somefiles.csv"

    def handle(self, *args, **options):
        if (
            Title.objects.exists() or
            Genre.objects.exists() or
            Category.objects.exists() or
            TitleGenre.objects.exists()
        ):
            print('data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading data")
        for file, model in zip(FILES, MODELS):
            import_csv(f'static/data/{file}', model)


