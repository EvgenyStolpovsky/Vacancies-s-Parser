from abc import ABC, abstractmethod
from connector_class import Connector
import requests


my_api_key: str = {'X-Api-App-Id': 'v3.r.119226455.7687e82d99284b1eaf5d22069f2b0f04254822c8.0dbf35dc534d7fae2b471f5cbdfc01641957355e'}


class Engine(ABC):
    '''Абстрактный класс для парсинга вакансий'''
    @abstractmethod
    def get_request(self, keyword):
        '''Парсинг сайта по ключевому слову'''
        pass

    @staticmethod
    def get_connector(file_name):
        '''Возвращает экземпляр класса Connector для использования записанной в файл json информацией о вакансиях'''
        connector = Connector(file_name)
        return connector

    def rec_vacancies(self, file_name, vacancies):
        '''Записывает собранные с сайтов вакансии в файл json'''
        connector = self.get_connector(file_name)
        connector.insert(vacancies)


class HH(Engine):
    '''Класс для парсинга вакансий с портала HeadHunter'''

    @staticmethod
    def _get_salary(salary_info: dict):
        '''Обработка поля salary(зарплата): выводит зарплату 'от', если же она не указана,
                то выводить зарплату 'до'. Или выводит 0, если поле отсутствует'''
        if salary_info:
            if salary_info.get('to'):
                return salary_info['to']
            if salary_info.get('from'):
                return salary_info['from']
        return 0

    @staticmethod
    def _get_remote_work(remote_work_info: dict):
        '''Обработка поля remote_work(удаленная работа)'''
        if remote_work_info:
            if remote_work_info['id'] == 'fullDay':
                return 'В офисе'
            if remote_work_info['id'] == 'remote':
                return 'Удаленно'
        return 'Другое'

    def get_request(self, keyword):
        '''Парсинг 500 вакансий и создание из них объекта типа list'''
        vacancies = []
        for page in range(5):
            response = requests.get(f'https://api.hh.ru/vacancies?text={keyword}', params={'per_page': 100, 'page': page}).json()
            for vacancy in response['items']:
                vacancies.append({
                    'name': vacancy['name'],
                    'company_name': vacancy['employer']['name'],
                    'url': vacancy['alternate_url'],
                    'description': vacancy['snippet']['requirement'],
                    'remote_work': self._get_remote_work(vacancy.get('schedule', {})),
                    'salary': self._get_salary(vacancy.get('salary', {})),
                })
        return vacancies


class SuperJob(Engine):
    '''Класс для парсинга вакансий с портала SuperJob'''

    @staticmethod
    def _get_salary(salary_info: dict):
        '''Обработка поля salary(зарплата): выводит зарплату 'от', если же она не указана,
        то выводить зарплату 'до'. или выводит 0, если поле отсутствует'''
        if salary_info.get('payment_to'):
            return salary_info['payment_to']
        if salary_info.get('payment_from'):
            return salary_info['payment_from']
        return 0

    @staticmethod
    def _get_remote_work(remote_work_info: dict):
        '''Обработка поля remote_work(удаленная работа)'''
        if remote_work_info:
            if remote_work_info['id'] == 1:
                return 'В офисе'
            if remote_work_info['id'] == 2:
                return 'Удаленно'
        return 'Другое'

    def get_request(self, keyword):
        '''Парсинг 500 вакансий и создание из них объекта типа list'''
        vacancies = []
        for page in range(5):
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=my_api_key,
                                    params={'keywords': keyword, 'count': 100,
                                            'page': page}).json()
            for vacancy in response['objects']:
                vacancies.append({
                    'name': vacancy['profession'],
                    'company_name': vacancy['firm_name'],
                    'url': vacancy['link'],
                    'description': vacancy['candidat'],
                    'remote_work': self._get_remote_work(vacancy.get('place_of_work', {})),
                    'salary': self._get_salary(vacancy),
                })
        return vacancies