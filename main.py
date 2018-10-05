# -*- coding: utf8 -*-
import telebot
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

import webbrowser
cidn = 366459870
url = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi?n=700"
bot = telebot.TeleBot("")

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
}
date = datetime.strftime(datetime.now(), "%d.%m.%Y")
group = "ПФ-41".encode('cp1251')



def html(group, date, sdate):
    PARAMS = {'group': group,
              'sdate': sdate,
              'edate': date
              }
    r = requests.post(url, PARAMS)
    with open("res.html", "wb") as f:
        f.write(r.content)
    pass

def day(soup):
    a = []
    for hh in soup.find_all('h4')[3:]:
        print()
        a.append("Розклад Групи ПФН-41 на " + hh.text.strip()+"\n")
    for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if cols[2].text.strip() == '':
                continue
            predmet = cols[2].text.strip()
            chas = cols[1].text.strip()
            chas1 = '(' + chas[0:-5] + ' - ' + chas[5:] + ')'
            para = cols[0].text.strip()
            a.append(str(para) + ' Пара ' + str(chas1))
            a.append(str(predmet)+ "\n")
    b = '\n'.join(a)
    return b




# handle the "/start" command
@bot.message_handler(commands=['today'])
def command_start(message):
    sdate = date
    cid = message.from_user.id
    html(group, sdate, sdate)
    soup = BeautifulSoup(open('res.html'), "html.parser")
    bot.send_message(cid, day(soup))

@bot.message_handler(commands=['tomorrow'])
def command_start(message):
    sdate = date
    html(group, sdate, sdate)
    soup = BeautifulSoup(open('res.html'), "html.parser")
    bot.send_message(cid, day(soup))

@bot.message_handler(commands=['day'])
def command_start(message):

    print (str(date+timedelta(days=1)))

if __name__ == '__main__':
    bot.polling(none_stop = True)