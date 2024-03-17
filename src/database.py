import psycopg2


class DBVacancies:
    def __init__(self, database_name, user_name, host, dict_vacancies):
        self.database_name = database_name
        self.user_name = user_name
        self.host = host
        self.dict_vacancies = dict_vacancies

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
            print(f'{e}:Отсутствует подключение')

    def create_tables(self):
        """Создание таблиц"""
        conn_params = psycopg2.connect(
            database=self.database_name,
            user=self.user_name,
            host=self.host
        )
        try:
            with psycopg2.connect(**conn_params) as conn:
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
        except psycopg2.ProgrammingError as e:
            print(f'{e}:Не удалось создать таблицы')

    def insert_data(self):
        """Заполнение таблиц."""
        conn_params = psycopg2.connect(
            database=self.database_name,
            user=self.user_name,
            host=self.host
        )
        try:
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cur:
                    for vacancy in self.dict_vacancies:
                        # Вставляем данные о компании, если ее еще нет в таблице
                        cur.execute("INSERT INTO employers (employer_id, employer_name) "
                                    "VALUES (%s, %s) ON CONFLICT (employer_id) DO NOTHING",
                                    (vacancy["employer_id"], vacancy["employer_name"]))

                        # Вставляем данные о вакансии
                        cur.execute("INSERT INTO vacancies (vacancy_name, salary, employer_id) VALUES (%s, %s, %s)",
                                    (vacancy["vacancy_name"], vacancy["salary"], vacancy["employer_id"]))
                conn.commit()
        except psycopg2.ProgrammingError as e:
            print(f'{e}:Не удалось добавить данные')
