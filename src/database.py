import psycopg2


class DBVacancies:
    def __init__(self, database_name, user_name, host):
        self.database_name = database_name
        self.user_name = user_name
        self.host = host

    def create_database(self):
        """Создание базы данных."""
        conn_params = psycopg2.connect(
            user=self.user_name,
            host=self.host
        )
        try:
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'DROP DATABASE IF EXISTS {self.database_name}')
                    cur.execute(f'CREATE DATABASE {self.database_name}')
        except psycopg2.ProgrammingError as e:
            print('Отсутствует подключение')

    def create_tables(self):
        """Создание таблиц в созданной базе данных."""
        conn = psycopg2.connect(
            database=self.database_name,
            user=self.user_name,
            host=self.host
        )
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                    employer_id SERIAL PRIMARY KEY,
                    employer_name VARCHAR(255) UNIQUE
                 )
                    """)
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        vacancy_name TEXT NOT NULL,
                        salary INT,
                        employer_id INT REFERENCES employers(employer_id)
                    )
                    """)
        conn.commit()
        conn.close()


def insert_data(self):
        """Заполнение таблиц данными."""

