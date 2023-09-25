from src.class_save_csv import Saver

class Mylist:

    """Работает со списком вакансии"""
    def __init__(self):
        self.vacancy_list = []
        self.csv_saver = Saver()

    def __len__(self):
        return len(self.vacancy_list)

    def clear_list(self):
        """Удаляет вакансии из списка"""

        self.vacancy_list.clear()

    def add_vacancy(self, vacancy: object):
        """Добавляет вакансию в список"""

        self.vacancy_list.append(vacancy)

    def get_vacancy(self, index: int):
        """Получает вакансию с индексом"""

        return self.vacancy_list[index-1]

    def delete_vacancy(self, vacancy: object):
        """Удаляет одну вакансию из списка"""

        if vacancy in self.vacancy_list:
            self.vacancy_list.remove(vacancy)
        else:
            pass

    def sorting_vacancies_data(self):
        """Сортирует вакансии по дате"""

        self.vacancy_list.sort(reverse=True, key=lambda vacancy: vacancy.data_published)

    def sorting_vacancies_salary(self):
        """Сортирует вакансии по средней зарплате"""

        self.vacancy_list.sort(reverse=True, key=lambda vacancy: vacancy.salary_average)

    def filter_list_word(self, word: str):
        """Фильтрует вакансии по слову"""

        for vacancy in self.vacancy_list:
            if word in vacancy.requirement or word in vacancy.name:
                pass
            else:
                self.vacancy_list.remove(vacancy)
        return self

    def save_csv(self):
        """Сохраняет вакансии в CSV-файле"""

        path = self.csv_saver.save_vacancies_csv(self.vacancy_list)
        return path

    def __str__(self):
        return '\n'.join([f'Vacancy N {index + 1}\n{vacancy.__str__()}' for index, vacancy in enumerate(self.vacancy_list)])