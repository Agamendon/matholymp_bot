import requests
import telebot
from bs4 import BeautifulSoup
import time


def get_page(url, sess: requests.Session):
    request = sess.get('https://matholymp.com.ua/')
    return request.text


def get_headers(text):
    soap = BeautifulSoup(text, features='html.parser')
    a_list = soap.find_all('h3', {'class': 'entry-title'})
    return a_list


def are_headers_same(prev_arr, curr_arr):
    if prev_arr == curr_arr:
        return 1
    else:
        return 0


def get_link(text):
    soup = BeautifulSoup(text, features="html.parser")

    for a in soup.find_all('a', href=True):
        print(a['href'])
        return a['href']


if __name__ == "__main__":
    bot = telebot.TeleBot('1649976187:AAFz6_PCCD3cDKSmbUDY6BZ6PtsA_1Cl1_s')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56"}
    session = requests.Session()
    session.headers.update(headers)

    page_text = get_page('https://matholymp.com.ua/', session)
    prev_headers = get_headers(page_text)

    bot.send_message('@matholymp_notifications', 'Сервіс почав роботу')

    while True:
        try:
            page_text = get_page('https://matholymp.com.ua/', session)
            curr_headers = get_headers(page_text)
            if are_headers_same(prev_headers, curr_headers):
                print('true')
            else:
                print('false')
                bot.send_message('@matholymp_notifications', get_link(str(curr_headers[0])))
                prev_headers = curr_headers

        except Exception as e:
            pass

        time.sleep(10)
