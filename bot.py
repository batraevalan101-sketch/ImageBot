import telebot
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши описание картинки на английском 🎨\nПример: beautiful sunset over mountains")

@bot.message_handler(func=lambda m: True)
def generate(message):
    prompt = message.text
    bot.reply_to(message, "⏳ Генерирую, подожди...")
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true"
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
        else:
            bot.reply_to(message, "❌ Ошибка, попробуй ещё раз")
    except Exception as e:
        bot.reply_to(message, "❌ Сервис недоступен, попробуй позже")

bot.infinity_polling()
