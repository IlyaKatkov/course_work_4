from abc import ABC, abstractmethod
import requests
import json
import datetime
import time
from src.class_save_json import Json_saver
import copy

class API(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_date(self, days=14):
        pass

    @abstractmethod
    def add_words(self, words):
        pass

    @abstractmethod
    def add_area(self, city):
        pass

    @abstractmethod
    def load_all_areas(self):
        pass

class HeadHunterAPI(API):

    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'
    HH_AREAS_JSON = 'data/areas/headhunter_areas.json'
    params_start = {
        'text': 'python',
        'per_page': 100,
        'area': 25,
        'date': 7
    }

    def __init__(self):
        self.param = copy.deepcopy(self.params_start)
        self.change_date()
        self.saver_areas = Json_saver(self.HH_AREAS_JSON)
        if self.saver_areas.check_file():
            pass
        else:
            self.load_all_areas()

    def get_vacancies(self):
        """Получение информации о вакансиях"""

        response = requests.get(self.HH_API_URL, self.param)
        response_data = json.loads(response.text)
        self.param = copy.deepcopy(self.params_start)
        if 'items' in response_data:
            return response_data['items']
        else:
            return []

    def change_date(self, days: int =7):
        """Количество дней для поиска"""

        self.param['period'] = days

    def add_words(self, words):
        """Добавляет слово для поиска"""

        self.param['text'] = words

    def add_area(self, city):
        """Добавляет город для поиска"""

        self.param['area'] = self.saver_areas.open_and_find_info(city)

    def load_all_areas(self):
        """Загрузка всех областей и сохранение json-файла"""

        response = requests.get(HeadHunterAPI.HH_API_URL_AREAS)
        data = response.content.decode()
        response.close()
        dict_areas = json.loads(data)
        areas = {}
        for k in dict_areas:
            for i in range(len(k['areas'])):
                if len(k['areas'][i]['areas']) != 0:
                    for j in range(len(k['areas'][i]['areas'])):
                        areas[k['areas'][i]['areas'][j]['name'].lower()] = k['areas'][i]['areas'][j]['id']
                else:
                    areas[k['areas'][i]['name'].lower()] = k['areas'][i]['id']
        self.saver_areas.save_file(areas)

class SuperJobAPI(API):
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_AREAS_JSON = 'data/areas/superjob_areas.json'
    params_start = {
        'keyword': 'python',
        'count': 100,
        'page': None,
        'town': 25,
        'date_published_from': 7
    }

    def __init__(self):
        self.params = self.params_start
        self.change_date()
        self.saver_areas = Json_saver(self.SJ_AREAS_JSON)
        if self.saver_areas.check_file():
            pass
        else:
            self.load_all_areas()

    def change_date(self, days: int =7):
        search_from = datetime.datetime.now() - datetime.timedelta(days=days)
        unix_time = int(time.mktime(search_from.timetuple()))
        self.params['date_published_from'] = unix_time

    def add_words(self, words):
        self.params['keyword'] = words

    def add_area(self, city):
        self.params['town'] = self.saver_areas.open_and_find_info(city)

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': "v3.r.137840149.e9b04347666a944d7abedbe7686617a1c153e648.356d5ccfc8c2e71c2bad2dc15b420e2ec1bc89b7"
    }
        response = requests.get(self.SJ_API_URL, headers=headers, params=self.params)
        response_data = json.loads(response.text)
        self.params = copy.deepcopy(self.params_start)
        if 'objects' in response_data:
            return response_data['objects']
        else:
            return []
    def load_all_areas(self):
        headers = {
            'X-Api-App-Id': "v3.r.137840149.e9b04347666a944d7abedbe7686617a1c153e648.356d5ccfc8c2e71c2bad2dc15b420e2ec1bc89b7"
        }
        result = {}
        response = requests.get(self.SJ_API_URL_AREAS, headers=headers, params={'id_country': 1, 'all': 1})
        response_data = json.loads(response.text)
        for area in response_data['objects']:
            result[area["title"].lower()] = area["id"]

        self.saver_areas.save_file(result)