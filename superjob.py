from utility import get_response_from_api
from utility import get_vacancy_av_salary
from utility import get_all_pages_vacancies_av_salary

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


def process_vacancies(vacancies):
    processed_vacancies = 0
    sum_of_salaries = 0
    for vacancy in vacancies:
        salary_currency = vacancy.get('currency')
        salary_from = vacancy.get('payment_from')
        salary_to = vacancy.get('payment_to')
        if 'rub' in salary_currency and (salary_from or salary_to):
            vacancy_av_salary = get_vacancy_av_salary(salary_from, salary_to)
            if vacancy_av_salary:
                processed_vacancies += 1
                sum_of_salaries += vacancy_av_salary
    return (
        sum_of_salaries,
        processed_vacancies
    )


def get_vacancies_page(params, page_current, auth_header):
    params['current_page'] = page_current
    response = get_response_from_api(
            url=URL_API_GET_VACANCIES,
            params=params,
            headers=auth_header
        )
    response = response.json()
    vacancies = response.get('objects')
    total_vacancies = response.get('total')
    page_current = params.get('current_page')
    page_current += 1
    pages_count = page_current
    if response['more']:
        pages_count = page_current + 1
    return vacancies, total_vacancies, page_current, pages_count


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
        params['keyword'] = job
        all_pages_vacancies_av_salary = get_all_pages_vacancies_av_salary(
                params,
                get_vacancies_page,
                process_vacancies,
                auth_header
            )
        average_jobs_salary[job] = all_pages_vacancies_av_salary
    return average_jobs_salary
