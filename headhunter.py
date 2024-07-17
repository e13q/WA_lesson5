import time

from utility import get_response_from_api
from utility import get_all_pages_vacancies_av_salary
from utility import get_vacancy_av_salary

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


def process_vacancies(vacancies):
    processed_vacancies = 0
    sum_of_salaries = 0
    for vacancy in vacancies:
        salary = vacancy.get('salary')
        if not salary:
            continue
        salary_currency = salary.get('currency')
        salary_from = salary.get('from')
        salary_to = salary.get('to')
        if not (('RUR' in salary_currency) and (salary_from or salary_to)):
            continue
        vacancy_av_salary = get_vacancy_av_salary(
            salary_from,
            salary_to
        )
        if vacancy_av_salary:
            processed_vacancies += 1
            sum_of_salaries += vacancy_av_salary
    return (
        sum_of_salaries,
        processed_vacancies
    )


def get_vacancies_page(params, page_current, auth_header=None):
    params['page'] = page_current
    response = get_response_from_api(
            url=URL_API_GET_VACANCIES,
            params=params
        )
    response = response.json()
    vacancies = response.get('items')
    total_vacancies = response.get('found')
    pages_count = response.get('pages')
    return vacancies, total_vacancies, pages_count


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
    average_jobs_salary = {}
    for job in jobs:
        params['text'] = job
        all_pages_vacancies_av_salary = get_all_pages_vacancies_av_salary(
                params,
                get_vacancies_page,
                process_vacancies
            )
        average_jobs_salary[job] = all_pages_vacancies_av_salary
        print(f'Ожидаем {SECONDS_WAITING_TIME} секунд, чтобы не получить бан')
        time.sleep(SECONDS_WAITING_TIME)
    return average_jobs_salary
