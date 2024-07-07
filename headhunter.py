import requests

import time


def get_area_id(country_name: str, city_name: str) -> int:
    f = requests.get('https://api.hh.ru/areas')
    for country in f.json():
        if country_name == country['name']:
            for city in country['areas']:
                if city_name == city['name']:
                    return city['id']


def get_vacancies_salary_sum_and_additions(
        id: int,
        period: int = None,
        text_search: str = '',
        current_page: int = 0
) -> tuple:
    params_ = {
        'area':  id,
        'period': period,
        'text': text_search,
        'per_page': 100,
        'page': current_page
    }
    try:
        response = requests.get('https://api.hh.ru/vacancies', params=params_)
        response.raise_for_status()
    except ():
        print('Ошибка получения данных с API hh.ru')
        print(response.text)
        exit()
    response = response.json()
    pages_count = response['pages']
    vacancies_count = response['found']
    vacancies = response['items']
    sum_of_salaries = 0
    processing_items = 0
    print(f'{text_search}, страница {current_page+1} из {pages_count}')
    for vacancy in vacancies:
        salary = vacancy['salary']
        if not salary or salary['currency'] != 'RUR':
            continue
        if salary['from'] and salary['to']:
            sum_of_salaries += int(salary['from'] + salary['to']) / 2
            processing_items += 1
        if salary['from'] and not salary['to']:
            sum_of_salaries += int(salary['from']) * 1.2
            processing_items += 1
        if not salary['from'] and salary['to']:
            sum_of_salaries += int(salary['to']) * 0.8
            processing_items += 1
    return sum_of_salaries, processing_items, pages_count, vacancies_count


def get_av_salary(id: int, period: int = None, text_search: str = ''):
    current_page = 0
    (
        sum_of_salaries,
        processing_items,
        pages_count,
        vacancies_count
    ) = get_vacancies_salary_sum_and_additions(
            id=id,
            period=period,
            text_search=text_search
        )
    if pages_count > current_page + 1:
        for current_page in range(1, pages_count):
            (
                new_sum,
                new_items,
                _,
                _
            ) = get_vacancies_salary_sum_and_additions(
                    id=id,
                    period=period,
                    text_search=text_search,
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
        country_name: str,
        city_name: str,
        jobs: dict,
        period: int = None
):
    area_id = get_area_id(country_name, city_name)
    out = {}
    for job in jobs:
        out[job] = get_av_salary(id=area_id, period=period, text_search=job)
        print('Ожидаем 10 секунд, чтобы не получить бан')
        time.sleep(10)
    return out
