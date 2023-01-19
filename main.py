import telebot
from telebot import types
import requests
import json
# Создаем экземпляр бота
bot = telebot.TeleBot('5975589505:AAGPJnFr7xLjOdnta3b1gEEy_UCO5s9QE6I')
# Функция, обрабатывающая команду /start
vetvinfo = {"num" : 0,"content" : ""}

@bot.message_handler(content_types=["text"])
def start(m):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Искать игру")
        btn2 = types.KeyboardButton("Назад")
        markup.add(btn1,btn2)
        bot.send_message(m.chat.id,
                         text='Это бот который собирает информацию о играх и выдает ее вам внужном виде!\nВы можете ознакомиться с функционалом на панели кнопок',
                         reply_markup=markup)
        bot.register_next_step_handler(m, handle_text)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])

def handle_text(message):
    msg = message.text.lower()
    print(msg)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Искать игру")
    btn2 = types.KeyboardButton("Назад")
    markup.add(btn2)
    if msg == "искать игру":
        # url = "https://www.cheapshark.com/api/1.0/games?title=Garrysmod&limit=60&exact=0"
        # payload={}
        # headers = {}
        # response = requests.request("GET", url, headers=headers, data=payload)
        bot.send_message(message.chat.id, text="Окей введи название игры:",reply_markup=markup)
        bot.register_next_step_handler(message, namevetv1)
    else:
       bot.send_message(message.chat.id, "Выберите кноку!")
@bot.message_handler(content_types=["text"])
def namevetv1(message):
    gamename = message.text.lower()
    if gamename != "назад":
        gamename =gamename.replace(" ", "")
        url = f"https://www.cheapshark.com/api/1.0/games?title={gamename}&limit=10&exact=0"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = response.json()
        print(resp)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Искать игру")
        btn2 = types.KeyboardButton("Назад")
        markup.add(btn2)
        if len(resp) != 0:
            for i in resp:
                bot.send_photo(message.chat.id, i["thumb"])
                gamesstring = "1.Название: {}\n2.SteamID: {}\n3.Минимальная цена: {}$\n".format(i["external"],i["steamAppID"],i["cheapest"])
                bot.send_message(message.chat.id, text=gamesstring,reply_markup=markup)
        else:
            bot.send_message(message.chat.id,"Игр с таким именем не нашлось!")
        bot.register_next_step_handler(message, namevetv1)
    else:
        bot.send_message(message.chat.id,"Подтвердите выход из Поиска игр. Для этого нажмите \"Назад\" еще раз!")
        bot.register_next_step_handler(message, start)


# Запускаем бота
bot.polling(none_stop=True, interval=0)

# import requests
#
# url = "https://www.cheapshark.com/api/1.0/games?title=Garrysmod&limit=60&exact=0"
#
# payload={}
# headers = {}
#
# response = requests.request("GET", url, headers=headers, data=payload)
# fl = open("file.json", "w")
# fl.write(response.text)
# fl.close()
# print(response.text)