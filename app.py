from flask import Flask, render_template, request, jsonify
import os
import requests

# Ваш токен бота
TOKEN = '7518885686:AAHpUsAwSnnW0HD3DzoGoRruTADzaS6dq50'
URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
webhook_url = 'https://api.vercel.com/v1/integrations/deploy/prj_V60mLrw1lD8ydkVEeTltwtc31dmu/vyxMLgYyJm'  # URL вебхука вашего приложения

# Установка вебхука при запуске приложения
response = requests.post(URL, data={'url': webhook_url})
print(response.json())

app = Flask(__name__)
@app.route('/test')
def test():
    return 'Test route is working!'
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
    # Обработка обновления от Telegram
    print(update)  # Для отладки

    return '', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
