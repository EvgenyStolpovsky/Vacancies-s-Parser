import json
from engine_classes import SuperJob, HeadHunter
from classes import Vacancy

#Запрос у пользователя ключевого слова
word_for_search = input('Введите вакансию для поиска: ').strip()

#парсинг 500 вакансий по заданному слову с сайта HeadHunter и сохранение в json файл
h = HeadHunter()
response = h.get_request(word_for_search)
into_file_hh = h.save_vacancies('list.json', response)

#парсинг 500 вакансий по заданному слову с сайта SuperJob и добавление в list.json
s = SuperJob()
response = s.get_request(word_for_search)
into_file_sj = s.save_vacancies('vacancies_list.json', response)

#вывод меню
print('По вашему запросу собрано 500 вакансий с сайта SuperJob и 500 вакансий с сайта HeadHunter.\nВыберите '
      "дальнейшее действие:\nВывести список всех вакансий: нажмите s\nВывести 10 самых высокооплачиваемых вакансий: "
      "нажмите t\nВывести вакансии с возможностью удаленной работы: нажмите n\nЕсли вы хотите завершить программу: "
      "нажмите z")