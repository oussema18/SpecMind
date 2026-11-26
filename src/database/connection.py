import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)


def connect_to_database():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


if __name__ == "__main__":
    with connect_to_database() as connection:
        print(connection.execute(
            "SELECT current_database(), current_user, current_schema()"
        ).fetchone())
