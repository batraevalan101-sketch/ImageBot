import telebot
import requests
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши описание картинки на английском 🎨\nПример: beautiful sunset over mountains")

@bot.message_handler(func=lambda m: True)
def generate(message):
    prompt = message.text
    msg = bot.reply_to(message, "⏳ Генерирую...")
    
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true"
    
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=90)
            if response.status_code == 200:
                bot.delete_message(message.chat.id, msg.message_id)
                bot.send_photo(message.chat.id, response.content)
                return
        except:
            if attempt < 2:
                bot.edit_message_text(f"⏳ Попытка {attempt+2} из 3...",
                                       message.chat.id, msg.message_id)
                time.sleep(5)
    
    bot.edit_message_text("❌ Сервис недоступен, попробуй через минуту",
                           message.chat.id, msg.message_id)

bot.infinity_polling()
