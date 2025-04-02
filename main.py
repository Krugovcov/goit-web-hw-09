import requests
import json
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"


def get_quotes_and_authors():
    quotes = []
    authors = {}
    page = 1

    while True:
        url = f"{BASE_URL}/page/{page}/"
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_elements = soup.select("div.quote")

        for quote_element in quote_elements:
            text = quote_element.find("span", class_="text").text
            author_name = quote_element.find("small", class_="author").text
            tags = [tag.text for tag in quote_element.find_all("a", class_="tag")]

            quotes.append({
                "text": text,
                "author": author_name,
                "tags": tags
            })

            if author_name not in authors:
                author_page = quote_element.find("a")["href"]
                author_data = get_author_info(BASE_URL + author_page)
                authors[author_name] = author_data

        next_page = soup.select_one("li.next a")
        if not next_page:
            break

        page += 1

    return quotes, list(authors.values())


def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.find("h3", class_="author-title").text.strip()
    birth_date = soup.find("span", class_="author-born-date").text.strip()
    birth_place = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    return {
        "name": name,
        "birth_date": birth_date,
        "birth_place": birth_place,
        "description": description
    }


def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    quotes, authors = get_quotes_and_authors()
    save_to_json("quotes.json", quotes)
    save_to_json("authors.json", authors)
    print("Дані збережено у файли quotes.json та authors.json")
