import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


USER = "user"
PASSWORD = "password"
PORT = 3306
HOST = "localhost"
DATABASE = "my_database"
QUERY = "SELECT * FROM titanic;"

MAX_RETRIES = 10
RETRY_DELAY_SECONDS = 10


def create_connection():
    # створюємо рядок підключення до mysql через sqlalchemy
    connection_url = (
        f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    )

    return create_engine(connection_url)


def read_titanic():
    # створюємо підключення до бази даних
    connection = create_connection()

    # повторюємо спроби, якщо mysql ще не готовий
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # виконуємо select і повертаємо результат як dataframe
            return pd.read_sql(QUERY, con=connection)

        except OperationalError:
            # якщо спроби закінчилися, показуємо помилку
            if attempt == MAX_RETRIES:
                raise

            # повідомляємо про повторну спробу
            print(
                f"MySQL is not ready yet. Retrying in {RETRY_DELAY_SECONDS} seconds "
                f"({attempt}/{MAX_RETRIES})..."
            )

            # чекаємо перед наступною спробою
            time.sleep(RETRY_DELAY_SECONDS)


def main():
    # зчитуємо таблицю titanic у dataframe
    df = read_titanic()

    print(df)

    print("\nDataFrame shape:")
    print(df.shape)


if __name__ == "__main__":
    main()