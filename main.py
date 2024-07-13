from terminaltables import AsciiTable

import os
from dotenv import load_dotenv

import superjob
import headhunter


LANGUAGES = [
    'JavaScript',
    'TypeScript',
    'Swift',
    'Go',
    'C++',
    'C#',
    'PHP',
    'Ruby',
    'Python',
    'Java'
]

PERIOD_DAYS_OF_VACANCIES_HH = 30


def convert_stat_from_dict_to_list(lang: str, statistic: dict):
    row = []
    row.append(lang)
    for v in statistic[lang]:
        row.append(str(statistic[lang][v]))
    return row


def print_table(statistic, title):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    for lang in statistic:
        row = convert_stat_from_dict_to_list(lang, statistic)
        table_data.append(row)
    table = AsciiTable(table_data, title)
    print(table.table)


if __name__ == '__main__':
    load_dotenv()
    superjob_api_key = os.getenv('SUPERJOB_API_KEY')
    statistic_sj = superjob.get_summury_about_jobs(
        'Москва',
        LANGUAGES,
        superjob_api_key
    )
    statistic_hh = headhunter.get_summury_about_jobs(
        'Россия',
        'Москва',
        LANGUAGES,
        PERIOD_DAYS_OF_VACANCIES_HH
    )
    print_table(statistic_sj, 'SuperJob Moscow')
    print_table(statistic_hh, 'HeadHunter Moscow')
