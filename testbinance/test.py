import requests
import telebot
from api import token

def get_data():
    req=requests.get("https://yobit.net/api/3/ticker/ltc_btc")
    response=req.json()
    sell_price=response["ltc_btc"]["sell"]
    print(f"{sell_price}")

def telegram_bot(token):
    bot=telebot.TeleBot(token)  

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id,"Тест")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower()=="price":
            try:
                req=requests.get("https://yobit.net/api/3/ticker/ltc_btc")
                response=req.json()
                sell_price=response["ltc_btc"]["sell"]
                bot.send_message(message.chat.id,f"{sell_price}")
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id,"Какая то ошибка!")  

    bot.polling()    

if __name__=="__main__":
    telegram_bot(token)
    #get_data()
