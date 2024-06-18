import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "db","db.sqlite3")
USER_TABLE_CSV = os.path.join(BASE_DIR, "db", "users.csv")
FILM_TABLE_CSV = os.path.join(BASE_DIR, "db", "films.csv")

USER_TABLE_NAME = "user"
FILM_TABLE_NAME = "film"

