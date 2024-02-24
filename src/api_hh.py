from abc import ABC, abstractmethod


import requests


class BasicAPI(ABC):
    """Абстрактный класс для получения API с сайтов."""

    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        """Метод получения вакансий."""
        pass


class HeadHunterAPI(BasicAPI):
    """Класс для получения вакансий компании company_id"""

    def __init__(self, company_id: int):
        self.company_id = company_id
        self.params = {
            "employer_id": self.company_id,  # id компаний.
            "per_page": 100,  # количество вакансий.
            "page": None,  # номер страницы.
        }
        self.headers = {"HH-User-Agent": "GetVacancies (my@email.com)"}

    def get_vacancies(self) -> list[dict]:
        """
        Метод получения вакансий с платформы hh.ru.
        :return: Список с вакансиями
        """
        url = f"https://api.hh.ru/vacancies"
        list_vacancies = list()
        try:
            response = requests.get(url=url, headers=self.headers, params=self.params).json()["items"]
            for vacancy in response:
                employer_id = vacancy['employer']['id']
                employer_name = vacancy['employer']['name']
                vacancy_name = vacancy['name']
                salary_from = vacancy['salary']['from'] if vacancy['salary'] is not None else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary'] is not None else 0
                if salary_from is not None and salary_to is not None:
                    salary = (salary_from + salary_to) / 2
                elif salary_from is not None:
                    salary = salary_from
                elif salary_to is not None:
                    salary = salary_to
                else:
                    salary = None
                list_vacancies.append({
                    "employer_id": employer_id,
                    "employer_name": employer_name,
                    "vacancy_name": vacancy_name,
                    "salary": salary
                })
            return list_vacancies
        except Exception as err:
            print(f"{err}: Сервис hh.ru не доступен")
