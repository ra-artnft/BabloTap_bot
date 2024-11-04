from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from flask import Flask, render_template, request, jsonify
import os
import requests

# Ваш токен бота
TOKEN = '7518885686:AAHpUsAwSnnW0HD3DzoGoRruTADzaS6dq50'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

app = Flask(__name__)


@app.route('/')
def index():
    """Главная страница с кнопкой для запуска бота."""
    return render_template('index.html')


@app.route('/start-bot', methods=['POST'])
def start_bot():
    """Маршрут для запуска бота (установка вебхука)."""
    webhook_url = f'https://bablo-tap-bot.vercel.app/webhook'  # Замените на ваш домен
    URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'

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

    if 'message' in update:
        chat_id = update['message']['chat']['id']
        if 'text' in update['message'] and update['message']['text'] == '/start':
            send_welcome_message(chat_id)

    return '', 200


def send_welcome_message(chat_id):
    """Отправка приветственного сообщения с кнопкой 'Запустить'."""
    keyboard = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton(
        text="Запустить BabloTap",
        web_app={"url": "https://bablo-tap-bot.vercel.app/"}
    )
    keyboard.add(web_app_button)

    message = "Добро пожаловать! Нажмите кнопку ниже, чтобы начать."
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={
        'chat_id': chat_id,
        'text': message,
        'reply_markup': keyboard
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
