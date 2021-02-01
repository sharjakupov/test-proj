import csv
import requests
from bs4 import BeautifulSoup as bs

url = 'https://valuta.kg/'

def get_html(html): 
    r = requests.get(html)
    return r.text 

def get_page_data(html):
    soup = bs(html,'html.parser')
    table_data = soup.find('div',id='rate-list',class_="rate-list active").find_all('tr')
    bankitem = []
    data1 = []
    for bankinfo in table_data:
        try:
            bankN = bankinfo.find('h4').text
            bankitem.append(bankN)
            rate = str(bankinfo.find_all('td',class_='td-rate')).split('"')
            USDBuy = rate[7].strip()
            USDSell = rate[19].strip()
            EURBuy = rate[31].strip()
            EURSell = rate[43].strip()
            RUBBuy = rate[55].strip()
            RUBSell = rate[67].strip()
            KZTBuy = rate[79].strip()
            KZTSell = rate[91].strip()

            data = {'bankN':bankitem[-1],
                    'USDBuy': USDBuy, 'USDSell': USDSell,
                    'EURBuy': EURBuy, 'EURSell': EURSell,
                    'RUBBuy': RUBBuy, 'RUBSell': RUBSell,
                    'KZTBuy': KZTBuy, 'KZTSell': KZTSell}
            data1.append(data)

        except (AttributeError, IndexError):
            continue 
        print(data)  
        
    with open('banks.csv','a') as file:
        writer = csv.DictWriter(file,fieldnames = data.keys())
        writer.writeheader()
        writer.writerows(data1)
                
def main():
    get_page_data(get_html(url))
        
if __name__=='__main__':
    main()


import csv
import telebot
from telebot import types
from decouple import config
from bs4 import BeautifulSoup as bs
import requests
# from obmennik import main


TOKEN = '1532383036:AAEIP68N-PmiXsHYd0yvHqi_yKVCtza4a9A'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def start(message): 
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Choose currency', reply_markup=inline_keyboard)

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('USD', callback_data = 'Type')
btn2 = types.InlineKeyboardButton('EUR', callback_data = 'Type')
btn3 = types.InlineKeyboardButton('RUB', callback_data = 'Type')
btn4 = types.InlineKeyboardButton('KZT', callback_data = 'Type')
inline_keyboard.add(btn1,btn2,btn3,btn4)



list_ = []

def parse():
    with open('banks.csv','r') as file: 
        reader = csv.reader(file)
        for line in file.readlines():
            line = line.split(",")
            line = line[0]+line[2]
            print(f'{line}')
            list_.append(line)

parse()


@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if  c.data == 'Type':
        chat_id = c.message.chat.id
        inline_keyboard2 = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton('SELL',callback_data = 'SELL')
        b2 = types.InlineKeyboardButton('BUY',callback_data ='BUY')
        inline_keyboard2.add(b1,b2)
        msg = bot.send_message(chat_id, 'Choose category', reply_markup=inline_keyboard2)
        
    if c.data == 'SELL':
        chat_id = c.message.chat.id
        for i in list_:
            bot.send_message(chat_id, text=f"{i}")