from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from flask import Flask, render_template, request, jsonify
import os
import requests
# Ваш токен бота
TOKEN = '7518885686:AAHpUsAwSnnW0HD3DzoGoRruTADzaS6dq50'
URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
webhook_url = 'https://api.vercel.com/v1/integrations/deploy/prj_V60mLrw1lD8ydkVEeTltwtc31dmu/vyxMLgYyJm'  # Замените на ваш домен

bot = Bot(token="TOKEN")
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    web_app_button = types.InlineKeyboardButton(
        text="Запустить BabloTap",
        web_app=types.WebAppInfo(url="https://bablo-tap-bot.vercel.app/")
    )
    keyboard.add(web_app_button)
    await message.reply("Нажмите кнопку ниже, чтобы запустить игру!", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp)

# Установка вебхука при запуске приложения
response = requests.post(URL, data={'url': webhook_url})
print(response.json())

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с кнопкой для запуска бота."""
    return render_template('index.html')

@app.route('/start-bot', methods=['POST'])
def start_bot():
    """Маршрут для запуска бота (установка вебхука)."""
    response = requests.post(URL, data={'url': webhook_url})

    if response.ok:
        return jsonify({'status': 'success', 'message': 'Бот запущен!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Ошибка запуска бота'}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Маршрут для обработки обновлений от Telegram."""
    update = request.json
    print(update)  # Для отладки

    chat_id = update['message']['chat']['id']
    if 'text' in update['message']:
        if update['message']['text'] == '/start':
            send_welcome_message(chat_id)

    return '', 300

def send_welcome_message(chat_id):
    """Отправка приветственного сообщения с кнопкой 'Запустить'."""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Запустить", "callback_data": "start_game"}
            ]
        ]
    }
    message = "Добро пожаловать! Нажмите кнопку ниже, чтобы начать."
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={
        'chat_id': chat_id,
        'text': message,
        'reply_markup': keyboard
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
