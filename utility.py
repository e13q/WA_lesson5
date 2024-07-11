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


def get_summary_job_average_salary(
        vacancies_count,
        sum_of_salaries,
        processing_items
):
    if not processing_items:
        average_salary = None
    else:
        average_salary = int(sum_of_salaries / processing_items)
    return {
        'vacancies_found': vacancies_count,
        "vacancies_processed": processing_items,
        "average_salary": average_salary
    }


def get_all_pages_vacancies_av_salary(
        params,
        fuction_processing,
        auth_header=None
):
    sum_of_salaries = 0
    processing_items = 0
    vacancies_count = 0
    page_current = 0
    pages_count = 1
    while page_current < pages_count:
        (
            vacancies_count,
            sum_of_salaries_page,
            processing_items_page,
            page_current,
            pages_count
        ) = fuction_processing(params, page_current, auth_header)
        sum_of_salaries += sum_of_salaries_page
        processing_items += processing_items_page
    summary_job_average_salary = get_summary_job_average_salary(
        vacancies_count,
        sum_of_salaries,
        processing_items
    )
    return summary_job_average_salary
