import sqlite3
import requests
from bs4 import BeautifulSoup
import shutil
from getpass import getpass
from uuid import uuid3, NAMESPACE_DNS
from datetime import date
import os.path
from slugify import slugify

LOGIN_URL = 'https://manybooks.net/mnybks-login-form'
URL = 'https://manybooks.net'


def scrape_book(email=None, pass_=None, db_name=None):
    email = input('Email: ') if not email else email
    pass_ = getpass() if not pass_ else pass_
    payload = {
        "email": "razmik_zaxaryan@mail.ru" if not email else email,
        "pass": pass_,
        "ga_event": "lrf:z8FPuBMXNKfo6hm",
        "form_build_id": "form-E5JtoETu4rABv9eo6GoJK3axCDYA5RWoT-R62kIux2A",
        "form_id": "mb_user_login_form",
        "_triggering_element_name": "op",
        "_triggering_element_value": "Continue",
    }
    if not os.path.isdir('media'):
        os.mkdir('media')
    with requests.session() as s:
        s.post(LOGIN_URL, data=payload)
        response_html = s.get(URL).text
        soup = BeautifulSoup(response_html, 'html.parser')
        for item in soup.findChildren("div", {"class": "genres-list form-group"})[0].ul:
            response_html = s.get(f'{URL}{item.a["href"]}').text
            soup = BeautifulSoup(response_html, 'html.parser')
            print('href: ', f'{URL}{item.a["href"]}')
            for content in soup.find_all("div", {"class": "content"}):
                response_html = s.get(f'{URL}{content.a["href"]}').text
                print('--href: ', f'{URL}{content.a["href"]}')
                soup = BeautifulSoup(response_html, 'html.parser')
                published = soup.find('div', {
                    "class": "field field--name-field-published-year field--type-integer field--label-hidden "
                             "field--item"})
                pages = soup.find('div', {
                    "class": "field field--name-field-pages field--type-integer field--label-hidden field--item"})
                title = soup.find('div', {'itemprop': "name"}).text
                book_excerpt = soup.find('div', {
                    "class": "field field--name-field-excerpt field--type-text-long field--label-hidden field--item"})
                author = soup.find('a', {'itemprop': "author"})
                data_author = None
                if author:
                    author_href = author['href']
                    author_name = author.text
                    response_html = s.get(f'{URL}{author_href}').text
                    print('---href: ', f'{URL}{author_href}')
                    soup_ = BeautifulSoup(response_html, 'html.parser')
                    try:
                        avatar_src = soup_.find_all('img', {"class": "img-responsive"})[1]['src']
                        avatar_path = None
                        if not os.path.exists(f'media/avatar/{author_name}.jpg'):
                            if not os.path.isdir('media/avatar'):
                                os.mkdir('media/avatar')
                            if 'no-avatar' not in avatar_src:
                                response = s.get(f'{URL}{avatar_src}', stream=True)
                                with open(f'media/avatar/{author_name}.jpg', 'wb') as out_file:
                                    shutil.copyfileobj(response.raw, out_file)
                                avatar_path = f'avatar/{author_name}.jpg'
                        else:
                            avatar_path = f'avatar/{author_name}.jpg'
                    except IndexError:
                        pass
                    information = soup_.find('div', {
                        "class": "field field--name-field-information field--type-string-long field--label-hidden "
                                 "field--item"})
                    data_author = {
                        'full_name': author_name,
                        'image': avatar_path,
                        'info': str(information) if information else None
                    }
                ISBN = uuid3(NAMESPACE_DNS, f'{title}{author}{published}')
                if not os.path.exists(f'media/photo/{ISBN}.jpg'):
                    if not os.path.isdir('media/photo'):
                        os.mkdir('media/photo')
                    if not os.path.isdir('media/PDF'):
                        os.mkdir('media/PDF')
                    img_src = soup.find('img', {"itemprop": "image"})["src"]
                    response = s.get(f'{URL}{img_src}', stream=True)
                    with open(f'media/photo/{ISBN}.jpg', 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    pdf_href = soup.find('a', {"name": "download"})
                    with open(f'media/PDF/{ISBN}.pdf', 'wb') as out_file:
                        out_file.write(s.get(f'{URL}{pdf_href["href"]}').content)
                data_dict = {
                    'ISBN': ISBN.__str__(),
                    'title': title,
                    'author': data_author,
                    'published': date(int(published.text), 1, 1) if published and int(published.text) > 0 else None,
                    'pages': pages.text if pages else None,
                    'image': f'photo/{ISBN}.jpg',
                    'pdf_path': f'PDF/{ISBN}.pdf',
                    'book_excerpt': str(book_excerpt) if book_excerpt else None,
                    'genre': item.text
                }
                add_to_db(data_dict, db_name)


def add_to_db(data: dict, db=None):
    try:
        sqlite_connection = sqlite3.connect(db)
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM bookApp_book WHERE ISBN LIKE ?", (data['ISBN'],))
        author = data.pop('author')
        genre = data.pop('genre')
        if not cursor.fetchall():
            sqlite_insert_book = "INSERT INTO bookApp_book" \
                                 "(ISBN, title, published, pages, image, pdf, book_excerpt, slug)" \
                                 " VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sqlite_insert_book, (*data.values(), slugify(data['title'].lower())))
            if author:
                cursor.execute("SELECT * FROM bookApp_author WHERE full_name LIKE ?", (author['full_name'],))
                author_id = cursor.fetchall()
                if not author_id:
                    sqlite_insert_author = "INSERT INTO bookApp_author " \
                                           "(full_name, avatar, info, slug) VALUES (?, ?, ?, ?)"
                    cursor.execute(sqlite_insert_author, (*author.values(), slugify(author['full_name'].lower())))
                    author_id = [(cursor.lastrowid,)]
                cursor.execute("INSERT INTO bookApp_book_authors (book_id, author_id) VALUES (?, ?)",
                               (data['ISBN'], author_id[0][0]))
        cursor.execute("SELECT * FROM bookApp_genre WHERE title LIKE ?", (genre,))
        genre_id = cursor.fetchall()
        if not genre_id:
            sqlite_insert_genre = "INSERT INTO bookApp_genre " \
                                  "(slug, title) VALUES (?, ?)"
            cursor.execute(sqlite_insert_genre, (slugify(genre.lower()), genre))
            genre_id = [(cursor.lastrowid,)]
        cursor.execute("INSERT INTO bookApp_book_genres (book_id, genre_id) VALUES (?, ?)", (data['ISBN'], genre_id[0][0]))
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


if __name__ == '__main__':
    print('URl: ', URL)
    scrape_book(db_name='db.sqlite3')
