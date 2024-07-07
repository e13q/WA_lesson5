import requests

import os
from dotenv import load_dotenv


AUTH_HEADER = {
    'X-Api-App-Id': os.getenv('SUPERJOB_API_KEY')
}


def get_it_job_key():
    req = requests.get(
        'https://api.superjob.ru/2.0/catalogues/',
        headers=AUTH_HEADER
    )
    req.raise_for_status()
    for job in req.json():
        if job['title_rus'] == 'IT, Интернет, связь, телеком':
            return job['key']


def get_vacancies_salary_sum_and_additions(
        city_name: str,
        job_key: int,
        keyword: str = '',
        current_page: int = 0
) -> tuple:
    params_ = {
        'town': city_name,
        'catalogues': job_key,
        'keyword': keyword,
        'count': 100,
        'page': current_page
    }
    try:
        response = requests.get(
            'https://api.superjob.ru/2.0/vacancies/',
            headers=AUTH_HEADER,
            params=params_
        )
        response.raise_for_status()
    except ():
        print('Ошибка получения данных с API superjob.ru')
        print(response.text)
        exit()
    response = response.json()
    vacancies_count = len(response['objects'])
    vacancies = response['objects']
    sum_of_salaries = 0
    processing_items = 0
    print(f'{keyword}, страница {current_page+1}')
    for vacancy in vacancies:
        if vacancy['currency'] != 'rub':
            continue
        if vacancy['payment_from'] != 0 and vacancy['payment_to'] != 0:
            sum_of_salaries += int(
                vacancy['payment_from']+vacancy['payment_to']/2)
            processing_items += 1
        if vacancy['payment_from'] == 0 and vacancy['payment_to'] != 0:
            sum_of_salaries += int(vacancy['payment_from'] * 1.2)
            processing_items += 1
        if vacancy['payment_from'] != 0 and vacancy['payment_to'] == 0:
            sum_of_salaries += int(vacancy['payment_to'] * 0.8)
            processing_items += 1
    return sum_of_salaries, processing_items, vacancies_count


def get_av_salary(city_name: str, job_key: int, keyword: str = ''):
    current_page = 0
    (
        sum_of_salaries,
        processing_items,
        vacancies_count
    ) = get_vacancies_salary_sum_and_additions(
            city_name=city_name,
            job_key=job_key,
            keyword=keyword,
        )
    pages_count = 0
    if vacancies_count > 100:
        pages_count = int(vacancies_count / 100)
        if (vacancies_count/100) % 1 > 0:
            pages_count += 1
    if pages_count > current_page + 1:
        for current_page in range(1, pages_count):
            (
                new_sum,
                new_items,
                _,
                _
            ) = get_vacancies_salary_sum_and_additions(
                    city_name=city_name,
                    job_key=job_key,
                    keyword=keyword,
                    current_page=current_page
                )
            sum_of_salaries += new_sum
            processing_items += new_items
    if processing_items == 0:
        average_salary = None
    else:
        average_salary = int(sum_of_salaries / processing_items)
    return {
        'vacancies_found': vacancies_count,
        "vacancies_processed": processing_items,
        "average_salary": average_salary
    }


def get_summury_about_jobs(
        city_name: str,
        jobs: dict
):
    load_dotenv()
    it_job_key = get_it_job_key(),
    out = {}
    for job in jobs:
        out[job] = get_av_salary(city_name, it_job_key, job)
    return out
