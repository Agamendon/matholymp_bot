import requests
import telebot
from bs4 import BeautifulSoup
import time
import datetime
from flask import Flask, request
import os
import threading


TOKEN = '1649976187:AAFz6_PCCD3cDKSmbUDY6BZ6PtsA_1Cl1_s'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


def get_page(url, sess: requests.Session):
    site_request = sess.get('https://matholymp.com.ua/')
    return site_request.text


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


def run():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56"
    }

    session = requests.Session()
    session.headers.update(headers)

    prev_headers = []
    try:
        page_text = get_page('https://matholymp.com.ua/', session)
        prev_headers = get_headers(page_text)
    except Exception as e:
        print(e)

    # send me message to ensure that bot is working
    bot.send_message('551027089', 'Started work on UTC {}'.format(datetime.datetime.now()))
    print('Started work on UTC {}'.format(datetime.datetime.now()))

    while True:
        try:
            page_text = get_page('https://matholymp.com.ua/', session)
            curr_headers = get_headers(page_text)
            if are_headers_same(prev_headers, curr_headers):
                print(f'Check on {datetime.datetime.now()}, headers are same')
            else:
                print('false')
                bot.send_message('@matholymp_notifications', get_link(str(curr_headers[0])))
                prev_headers = curr_headers

        except Exception as e:
            pass

        time.sleep(10)


@server.route("/" + TOKEN, methods=['POST'])
def webhook_():
    return '!', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dry-harbor-03840.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == '__main__':
    threading.Thread(target=run).start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
