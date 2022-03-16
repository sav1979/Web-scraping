# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:52:51 2022

@author: sklad_2
"""

import requests
from bs4 import BeautifulSoup as bs


KEYWORDS = {'инстаграмм', 'РФ', 'web', 'windows'}
BASE_URL = 'https://habr.com/ru/all/'


def get_url_text(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        return False
    
# проверяем ответ от сервера.
def main(url=BASE_URL):
    text = get_url_text(url)
    soup = bs(text, features='html.parser')
    articles = soup.find_all('article')
    article_list = []
    for article in articles:
        article_time = article.find('span', class_='tm-article-snippet__datetime-published').text
        article_title = article.find('a', class_='tm-article-snippet__title-link')
        article_title_link = article_title['href']
        hubs = [h.text.strip() for h in article.find_all('a', class_='tm-article-snippet__title-link')]
        st_list = hubs[0].lower().split()
        
# регистр приводим к строке
        for st in st_list:
            if st in KEYWORDS:
                text = ''.join(hubs)
                article_list.append(f"{article_time} - {text} - https://habr.com{article_title_link}")
    return article_list


if __name__ == '__main__':
    output_list = []
    pages = int(input('Введите количество страниц: '))
    for page in range(pages):
        print(f'Обрабатываем страницу {page + 1} из {pages}')
        if page == 0:
            output_list += main()
        else:
            output_list += main(url=f'{BASE_URL}page{page+1}/')
    print(*output_list, sep='\n')