from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
from pprint import pprint

class Parser:
    headers = Headers(browser='firefox', os='win').generate()

    def __init__(self, HOST):
        self.HOST = HOST
    
    def _get_list_of_vacancy(self):
        html = requests.get(url=self.HOST,headers=self.headers)
        html.encoding='utf8'
        html = html.text
        soup = BeautifulSoup(html, features='lxml')
        all_vacancies = soup.find(id='a11y-main-content')
        list_vacancies = all_vacancies.find_all(class_="serp-item")
        return list_vacancies
    
    def _get_salary(self, vacancy):
        if vacancy.find(class_='vacancy-serp-item__layout').find('span', class_ = 'bloko-header-section-3') == None:
            return 'Не указана'
        return vacancy.find(class_='vacancy-serp-item__layout').find('span', class_ = 'bloko-header-section-3').text.replace('\u202f', ' ')

    def _get_city(self, vacancy):
        try:
            result = vacancy.find(class_='vacancy-serp-item__layout').find(class_ = 'vacancy-serp-item__info').find_all(class_ = 'bloko-text')[1].text
            return result[:result.index(',')]
            
        except:
            return vacancy.find(class_='vacancy-serp-item__layout').find(class_ = 'vacancy-serp-item__info').find_all(class_ = 'bloko-text')[1].text
    
    def get_vanacies_USD(self):
        data_list = []
        for vacancy in self._get_list_of_vacancy():
            if 'Django' in vacancy.find(class_ = 'vacancy-serp-item__layout').find(class_ = 'g-user-content').text or 'Flask' in vacancy.find(class_ = 'vacancy-serp-item__layout').find(class_ = 'g-user-content').text:
                if 'USD' in self._get_salary(vacancy=vacancy):
                    data_list.append({
                        'link': vacancy.find(class_='vacancy-serp-item__layout').find('h3', class_ = 'bloko-header-section-3').find('a', class_ = 'serp-item__title')['href'],
                        'Salary': self._get_salary(vacancy=vacancy),
                        'Company name': vacancy.find(class_='vacancy-serp-item__layout').find(class_ = 'vacancy-serp-item__info').find('a', 'bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' '),
                            'City': self._get_city(vacancy=vacancy)
                    })
        return data_list

    def selecting_data(self):
        data_list = []
        for vacancy in self._get_list_of_vacancy():
            if 'Django' in vacancy.find(class_ = 'vacancy-serp-item__layout').find(class_ = 'g-user-content').text or 'Flask' in vacancy.find(class_ = 'vacancy-serp-item__layout').find(class_ = 'g-user-content').text:
                data_list.append({
                    'link': vacancy.find(class_='vacancy-serp-item__layout').find('h3', class_ = 'bloko-header-section-3').find('a', class_ = 'serp-item__title')['href'],
                    'Salary': self._get_salary(vacancy=vacancy),
                    'Company name': vacancy.find(class_='vacancy-serp-item__layout').find(class_ = 'vacancy-serp-item__info').find('a', 'bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' '),
                    'City': self._get_city(vacancy=vacancy)
                })
        return data_list