import csv
import datetime

class Saver:
    """Сохраненяет информацию о вакансиях в CSV-файле"""
    def __init__(self):
        pass

    def save_vacancies_csv(self, vacancies):
        path = self.get_path_csv()
        with open(path, 'w', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                ['id', 'name', 'data_published', 'salary_from', 'salary_to', 'currency', 'area', 'url', 'employer', 'employer_url', 'requirement', 'experience', 'employment'])
            for vacancy in vacancies:
                writer.writerow([vacancy.id, vacancy.name, vacancy.data_published, vacancy.salary_from, vacancy.salary_to, vacancy.currency,
                                 vacancy.area, vacancy.url, vacancy.employer, vacancy.employer_url, vacancy.requirement, vacancy.experience, vacancy.employment])
        return path

    def get_path_csv(self):
        """Получает путь к новому файлу"""

        data_now = datetime.datetime.now()
        result = 'data/research/' + str(data_now)[:19] + ' vacancies.csv'
        return result


