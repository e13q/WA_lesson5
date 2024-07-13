import requests

from utility import get_response_from_api
from utility import get_vacancy_av_salary
from utility import get_all_pages_vacancies_av_salary

TEXT_API_ERROR = 'Ошибка получения данных с API superjob.ru'

TEXT_IT_CATALOG_NAME = 'IT, Интернет, связь, телеком'

URL_API_GET_CATALOGUES = 'https://api.superjob.ru/2.0/catalogues/'

URL_API_GET_VACANCIES = 'https://api.superjob.ru/2.0/vacancies/'

COUNT_MAX_VACANCIES_FOR_REQUEST = 100

PAGE_START_NUMBER = 0


def get_it_job_key(auth_header):
    request = get_response_from_api(
        url=URL_API_GET_CATALOGUES,
        headers=auth_header
    )
    jobs_catalog = request.json()
    for job in jobs_catalog:
        if job.get('title_rus') == TEXT_IT_CATALOG_NAME:
            return job.get('key')


def get_pages_count(vacancies_count):
    pages_count = 1
    if vacancies_count > COUNT_MAX_VACANCIES_FOR_REQUEST:
        pages_count = vacancies_count / COUNT_MAX_VACANCIES_FOR_REQUEST
        if (pages_count) % 1 > 0:
            pages_count += int(pages_count) + 1
        else:
            pages_count += int(pages_count)
    return pages_count


def processing_vacancies(response, params):
    vacancies = response.get('objects')
    vacancies_count = len(vacancies)
    pages_count = get_pages_count(vacancies_count)
    page_current = params.get('current_page')
    page_current += 1
    print(f'{params.get("keyword")}, страница {page_current} / {pages_count}')
    processing_items = 0
    sum_of_salaries = 0
    for vacancy in vacancies:
        salary_currency = vacancy.get('currency')
        salary_from = vacancy.get('payment_from')
        salary_to = vacancy.get('payment_to')
        if 'rub' in salary_currency and (salary_from or salary_to):
            vacancy_av_salary = get_vacancy_av_salary(salary_from, salary_to)
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


def get_vacancies_av_salary_page(params, page_current, auth_header):
    params.update({'current_page': page_current})
    response = get_response_from_api(
            url=URL_API_GET_VACANCIES,
            params=params,
            headers=auth_header
        )
    response = response.json()
    return processing_vacancies(response, params)


def get_summury_about_jobs(
        city_name: str,
        it_job_key: int,
        jobs: list,
        auth_header: dict
):
    params = {
            'town': city_name,
            'catalogues': it_job_key,
            'count': COUNT_MAX_VACANCIES_FOR_REQUEST,
            'page': PAGE_START_NUMBER
        }
    average_jobs_salary = {}
    for job in jobs:
        params.update({'keyword': job})
        try:
            all_pages_vacancies_av_salary = get_all_pages_vacancies_av_salary(
                    params,
                    get_vacancies_av_salary_page,
                    auth_header
                )
        except (requests.exceptions.RequestException):
            print(TEXT_API_ERROR)
            exit()
        average_jobs_salary.update({job: all_pages_vacancies_av_salary})
    return average_jobs_salary
