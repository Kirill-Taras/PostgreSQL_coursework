from config import employers
from src.DBManager import DBManager
from src.api_hh import HeadHunterAPI
from src.database import DBVacancies


def interface():
    print("Доброго времени суток!")
    print("Выберите один из вариантов:")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список всех вакансий с зарплатой выше средней")
    print("5. Получить список всех вакансий по ключевому слову")
    print("6. Завершить программу")


if __name__ == "__main__":
    main()
