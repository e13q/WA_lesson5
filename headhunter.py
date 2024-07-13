import time

import requests

from utility import get_response_from_api
from utility import get_all_pages_vacancies_av_salary
from utility import get_vacancy_av_salary

TEXT_API_ERROR = 'Ошибка получения данных с API hh.ru'

URL_API_GET_AREAS = 'https://api.hh.ru/areas'

URL_API_GET_VACANCIES = 'https://api.hh.ru/vacancies'

COUNT_MAX_VACANCIES_FOR_REQUEST = 100

PAGE_START_NUMBER = 0

SECONDS_WAITING_TIME = 10


def get_area_id(country_name: str, city_name: str) -> int:
    response = get_response_from_api(
        URL_API_GET_AREAS
    )
    response = response.json()
    for country in response:
        if country_name == country.get('name'):
            for city in country.get('areas'):
                if city_name == city.get('name'):
                    return city.get('id')


def processing_vacancies(response, params):
    vacancies = response.get('items')
    vacancies_count = response.get('found')
    pages_count = response.get('pages')
    page_current = params.get('page')
    page_current += 1
    print(f'{params.get("text")}, страница {page_current} / {pages_count}')
    processing_items = 0
    sum_of_salaries = 0
    for vacancy in vacancies:
        salary = vacancy.get('salary')
        if salary:
            salary_currency = salary.get('currency')
            salary_from = salary.get('from')
            salary_to = salary.get('to')
            if ('RUR' in salary_currency) and (salary_from or salary_to):
                vacancy_av_salary = get_vacancy_av_salary(
                    salary_from,
                    salary_to
                )
                if vacancy_av_salary:
                    processing_items += 1
                    sum_of_salaries += vacancy_av_salary
    return (
        vacancies_count,
        sum_of_salaries,
        processing_items,
        page_current,
        pages_count
    )


def get_vacancies_av_salary_page(params, page_current, *args):
    params.update({'page': page_current})
    response = get_response_from_api(
            url=URL_API_GET_VACANCIES,
            params=params
        )
    response = response.json()
    return processing_vacancies(response, params)


def get_summury_about_jobs(
        area_id: int,
        jobs: list,
        period: int = None
):
    params = {
        'area':  area_id,
        'period': period,
        'per_page': COUNT_MAX_VACANCIES_FOR_REQUEST,
        'page': PAGE_START_NUMBER
    }
    average_salary_info = {}
    for job in jobs:
        params.update({'text': job})
        try:
            all_pages_vacancies_av_salary = get_all_pages_vacancies_av_salary(
                    params,
                    get_vacancies_av_salary_page
                )
        except (requests.exceptions.RequestException):
            print(TEXT_API_ERROR)
            exit()
        average_salary_info.update({job: all_pages_vacancies_av_salary})
        print(f'Ожидаем {SECONDS_WAITING_TIME} секунд, чтобы не получить бан')
        time.sleep(SECONDS_WAITING_TIME)
    return average_salary_info
