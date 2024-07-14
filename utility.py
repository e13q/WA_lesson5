import requests


def get_vacancy_av_salary(salary_from, salary_to):
    if salary_from and salary_to:
        av_salary = int(salary_from+salary_to/2)
    elif salary_from:
        av_salary = int(salary_from * 1.2)
    elif salary_to:
        av_salary = int(salary_to * 0.8)
    return av_salary


def get_response_from_api(
        url,
        params=None,
        headers=None,
        data=None
):
    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        data=data
    )
    response.raise_for_status()
    return response


def get_all_pages_vacancies_av_salary(
        params,
        get_vacancies_for_page,
        process_vacancies,
        auth_header=None
):
    sum_of_salaries = 0
    processed_vacancies = 0
    page_current = 0
    pages_count = 1
    total_vacancies = 0
    while page_current < pages_count:
        (
            vacancies_from_page,
            total_vacancies,
            page_current,
            pages_count
        ) = get_vacancies_for_page(
            params, page_current, auth_header
        )
        sum_of_salaries_page, processed_vacancies_page = process_vacancies(
            vacancies_from_page
        )
        sum_of_salaries += sum_of_salaries_page
        processed_vacancies += processed_vacancies_page
    if not processed_vacancies:
        average_salary = None
    else:
        average_salary = int(sum_of_salaries / processed_vacancies)
    return {
        'vacancies_found': total_vacancies,
        "vacancies_processed": processed_vacancies,
        "average_salary": average_salary
    }
