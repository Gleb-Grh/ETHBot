import requests
from datetime import datetime
from telebot import types, telebot
from t_data import token # полученный в botfather token

    
def telegramBot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, 
                         "Привет! Это бот для запроса курса ethereum введи /button, чтобы получить информацию о цене покупки или продажи")    
    
    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Покупка")
        item2 = types.KeyboardButton("Продажа")
        markup.add(item1,item2)
        bot.send_message(message.chat.id,'Нажмите на нужную кнопку',reply_markup=markup)
        
    @bot.message_handler(content_types=["text"])
    def message_replay(message):
        try:
            req = requests.get('https://yobit.net/api/3/ticker/eth_rur')
            responce = req.json()
            if message.text == "Покупка":
                buy_price = responce['eth_rur']['buy']
                bot.send_message(message.chat.id,
                                    f'{datetime.now().strftime("%d-%m-%Y %H:%M")}' 
                                    f'\nBuy ETH price: {buy_price}')
            elif message.text == "Продажа":
                sell_price = responce['eth_rur']['sell']
                bot.send_message(message.chat.id,
                                    f'{datetime.now().strftime("%d-%m-%Y %H:%M")}' 
                                    f'\nSell ETH price: {sell_price}')
            else:
                bot.send_message(message.chat.id, "Пожалуйста проверьте команду")
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, "Что то пошло не так")    

    bot.polling()


if __name__ == '__main__':

    telegramBot(token)