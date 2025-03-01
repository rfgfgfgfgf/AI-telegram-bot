import telebot
from config import TOKEN
from logic import Text2ImageAPI
from config import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Мой создатель - rfgfgfgfgf. Мои команды: /help, /start, /command_text")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Привет, проверь мои команды: /help, /start, /command_text')
    
@bot.message_handler(commands=['generate'])
def generate_image(message):
    prompt = message.text.replace('/generate', '')

    if not prompt:
        bot.reply_to(message, "Пожалуйста, введите описание изображения после команды /generate.")
        return

    bot.reply_to(message, "Генерирую изображение, подождите...")

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]

    file_path = 'generated_image.jpg'
    api.save_image(images, file_path)

    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

# Запускаем бота
bot.polling()
