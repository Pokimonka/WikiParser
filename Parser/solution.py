from bs4 import BeautifulSoup
import requests
import csv

default_url = "https://ru.wikipedia.org/"
letter_count = {}
letter = ''


def parse(url_for_parse):
    page = requests.get(url_for_parse)
    soup = BeautifulSoup(page.text, features='lxml')
    animals_list = soup.find('div', id='mw-pages')
    category = animals_list.select_one('div.mw-category.mw-category-columns')
    category_group = category.select('div.mw-category-group')
    let = ''
    for cat in category_group:
        let = cat.h3.text  # буква
        animals = cat.ul.contents[0::2]  # список животных

        if not letter_count.get(let):
            letter_count[let] = len(animals)
        else:
            letter_count[let] += len(animals)

    next_btn = animals_list.find_all('a', title="Категория:Животные по алфавиту")
    return [let, next_btn[1].attrs['href']]


if __name__ == '__main__':
    url = default_url + "/wiki/Категория:Животные_по_алфавиту"

    while letter != 'A':
        parse_result = parse(url)
        letter = parse_result[0]
        n_btn = parse_result[1]

        url = default_url + n_btn

    letter_count.pop("A")

    with open("beasts.csv", "w") as file:
        for l_c in letter_count:
            writer = csv.writer(file)
            writer.writerow((l_c, letter_count[l_c]))
