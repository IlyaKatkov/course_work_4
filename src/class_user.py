from src.class_api import HeadHunterAPI, SuperJobAPI
from src.class_mylist import Mylist
from src.vacancy import Vacancy
import copy

class Userinput:
    """Класс, предназначенный для взаимодейстия с пользователем"""
    new_param = {
            'website': [],
            'city': [],
            'words': [],
            'date': 7
        }

    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.sj_api = SuperJobAPI()
        self.all_list = Mylist()
        self.param = copy.deepcopy(self.new_param)

    def __call__(self):
        while True:

            print('1 - Начать работу')
            print('exit - для выхода')

            command = input()

            if command.lower() == 'exit':
                print('Возвращайтесь позже!')
                quit()
            elif command == "1":
                self.choosing_parameters()
            else:
                print('Неизвестная команда')

    def choosing_parameters(self):
        """Открывает второе меню"""

        self.param = self.new_param
        while True:
            self.delete_duplicates()
            print('Вам небходимо выбрать сайт, город, дату и ключевое слово для поиска')
            print(f'Мы ищем вакансии в последние {self.param["date"]} дней')
            if self.param['website'] != []:
                print(f"Вы выбрали следующий сайт - {', '.join(self.param['website'])}")
            if self.param['city'] != []:
                print(f"Вы выбрали следующий город - {', '.join(self.param['city'])}")
            if self.param['words'] != []:
                print(f"Вы выбрали следующие слова - {', '.join(self.param['words'])}")
            print('1 - выбрать сайт')
            print('2 - добавить слова для поиска')
            print('3 - выбрать город')
            print('4 - выбрать дату поиска')
            if self.param['website'] != [] and self.param['city'] != [] and self.param['words'] != []:
                print('5 - research vacancies')
            print('5 - поиск вакансий')
            print('exit - выход')
            command = input()

            if command == 'exit':
                self.__call__()
            elif command == '1':
                self.choosing_website()
            elif command == '2':
                self.choosing_words()
            elif command == '3':
                self.choosing_city()
            elif command == '4':
                self.choosing_date()
            elif command == '5':
                self.research_vacancies()
            else:
                print('Неизвестная команда')

    def choosing_website(self):

        """Меню для выбора сайтов"""
        while True:
            print('Мы можем посмотреть вакансии от HeadHunter и SuperJob. Какой сайт вы хотели бы выбрать?')
            print('1 - HeadHunter')
            print('2 - SuperJob')
            print('3 - HeadHunter и SuperJob')
            print('exit - выход')
            command = input()

            if command == 'exit':
                break
            elif command == '1':
                self.param['website'].append('HeadHunter')
                break
            elif command == '2':
                self.param['website'].append('SuperJob')
                break
            elif command == '3':
                self.param['website'].append('HeadHunter')
                self.param['website'].append('SuperJob')
                break
            else:
                print('Неизвестная команда')

    def choosing_words(self):

        """Меню для добаления и удаления слова из поиска"""
        while True:
            self.delete_duplicates()
            if self.param['words'] != []:
                print(f"Вы выбрали следующее слово - {', '.join(self.param['words'])}")
            print('Добавьте слово для поиска или нажмите "delete" для удаления всех слов или нажмите "exit" для выхода')
            command = input().lower()
            if command == 'exit':
                break
            elif command == 'delete':
                self.param['words'].clear()
                break
            else:
                self.param['words'].append(command)
                break

    def choosing_city(self):
        """Добавляет город для поиска"""
        print('Добавьте город для поиска или нажмите "exit" для выхода')
        while True:
            command = input().lower()
            if command == 'exit':
                break
            if self.check_city(command):
                self.param['city'].append(command)
                break
            else:
                print('Попробуйте снова, неизвестная команда')

    def check_city(self, user_input: str):
        """Проверяет город, который ввёл пользователь"""
        if self.hh_api.saver_areas.open_and_find_info(user_input) or self.sj_api.saver_areas.open_and_find_info(
                user_input):
            return True
        else:
            return False

    def choosing_date(self):
        """Выбирает количество дней для поиска"""
        while True:
            print('Выберите дни для поиска')
            print('1 - 1 день')
            print('2 - 7 дней')
            print('3 - 14 дней')
            print('4 - 30 дней')
            print('exit - выход')
            command = input()
            if command == 'exit':
                break
            elif command == '1':
                self.param['date'] = 1
                break
            elif command == '2':
                self.param['date'] = 7
                break
            elif command == '3':
                self.param['date'] = 14
                break
            elif command == '4':
                self.param['date'] = 30
                break
            else:
                print('Неизвестная команда')

    def research_vacancies(self):

        """Получение вакансий от HeadHunter и SuperJob"""

        if 'HeadHunter' in self.param['website']:
            if self.param['city'] != []:
                for item in range(len(self.param['city'])):
                    self.hh_api.add_area(self.param['city'][item])
            if self.param['words'] != []:
                self.hh_api.add_words(self.param['words'])
            self.hh_api.change_date(self.param['date'])

            vacancies_hh = self.hh_api.get_vacancies()

            if vacancies_hh != []:
                for item in vacancies_hh:
                   vacancy = Vacancy.create_vacancy_from_hh(item)
                   self.all_list.add_vacancy(vacancy)

        if 'SuperJob' in self.param['website']:
            if self.param['city'] != []:
                for item in range(len(self.param['city'])):
                    self.sj_api.add_area(self.param['city'][item])
            if self.param['words'] != []:
                self.sj_api.add_words(self.param['words'])
            self.sj_api.change_date(self.param['date'])

            vacancies_sj = self.sj_api.get_vacancies()

            if vacancies_sj != []:
                for item in vacancies_sj:
                   vacancy = Vacancy.create_vacancy_from_sj(item)
                   self.all_list.add_vacancy(vacancy)

        self.param = copy.deepcopy(self.new_param)

        self.sorting_vacancies()

    def sorting_vacancies(self):

        """Сортирует вакансии"""
        while True:
            print(f'Мы нашли {len(self.all_list)} вакансий. Мы можем их отсортировать. Что необходимо делать?')
            print('1 - Отсортировать вакансии про дате')
            print('2 - Отсортировать вакансии по зарплате')
            print('3 - Отфильтровать по слову')
            print('exit - выход')

            command = input()

            if command == 'exit':
                break
            elif command == '1':
                self.all_list.sorting_vacancies_data()
                self.all_list_vacancies()
            elif command == '2':
                self.all_list.sorting_vacancies_salary()
                self.all_list_vacancies()
            elif command == '3':
                print('Какое слово вы хотите использовать для фильтрации?')
                word_filter = input().lower()
                self.all_list.filter_list_word(word_filter)
                self.all_list_vacancies()
            else:
                print('Неизвестная команда')

    def all_list_vacancies(self):
        """Показывает все вакансии"""

        print(self.all_list)

    def delete_duplicates(self):

        """Удаляет дубликаты"""

        self.param = {
            'website': list(set(self.param['website'])),
            'city': list(set(self.param['city'])),
            'words': list(set(self.param['words'])),
            'date': self.param['date']
        }



