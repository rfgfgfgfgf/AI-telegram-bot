import telebot
from config import TOKEN
from logic import Text2ImageAPI
from config import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Шлепа бот. Мой создатель - rfgfgfgfgf. Мои команды: /help, /start, /coin, /weather /help, /start, /command_text")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Привет, проверь мои команды: /help, /start, /command_text')
    
@bot.message_handler(func=lambda message:True)
def command_text(message):
    promt = message.text


    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(promt, model_id)
    images = api.check_generation(uuid)[0]

    file_path = 'decoded_image.jpg'
    api.save_image(images,file_path)


    with open(file_path,'rb') as photo:
        bot.send_photo(message.chat.id, photo)

# Запускаем бота
bot.polling()
