import psycopg2


class DBManager:

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def db_connect(self, query):
        """Метод для запроса к базе данных"""
        with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                answer = cur.fetchall()
        return answer

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        return self.db_connect(
                    'SELECT employer_name, COUNT(vacancy_id) FROM'
                    'vacancies JOIN employers ON vacancies.employer_id = employers.employer_id GROUP BY employer_name'
        )

    def get_all_vacancies(self):
        """Получает список всех вакансий"""
        return self.db_connect(
            'SELECT vacancies.vacancy_name, vacancies.salary, employers.employer_name FROM '
            'vacancies JOIN employers ON vacancies.employer_id = employers.employer_id'
        )

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        return self.db_connect(
            'SELECT avg(salary) FROM vacancies'
        )

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        return self.db_connect(
            'SELECT vacancy_name FROM '
            'vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)'
        )

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        return self.db_connect(f"SELECT vacancy_name FROM vacancies WHERE LOWER(vacancy_name) "
                               f"LIKE LOWER(%s), '%{keyword}%'")

