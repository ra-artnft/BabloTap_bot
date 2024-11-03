let clickCount = 0;

document.getElementById('bablo-button').addEventListener('click', function() {
    clickCount++;

    if (clickCount % 10 === 0) {
        triggerMoneyAnimation();
    }
});

document.getElementById('start-bot-button').addEventListener('click', function() {
    startBot();
});

function startBot() {
    fetch('/start-bot', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);  // Уведомление об успешном запуске бота
            } else {
                alert(data.message);  // Уведомление об ошибке запуска бота
            }
        })
        .catch(error => {
            console.error('Ошибка при запуске бота:', error);
        });
}

function triggerMoneyAnimation() {
    for (let i = 0; i < 50; i++) {
        setTimeout(createFallingMoney, i * 100); // Разница в 100 мс между падениями купюр
    }
}

function createFallingMoney() {
    const money = document.createElement('img');
    money.src = '/static/money.png';
    money.classList.add('money');

    // Случайное положение и скорость падения
    money.style.left = `${Math.random() * 100}vw`;
    money.style.setProperty('--fall-duration', `${Math.random() * 2 + 2}s`); // Время падения от 2 до 4 секунд

    document.body.appendChild(money);

    setTimeout(() => {
        money.remove();
    }, 4000); // Удаление через 4 секунды
}
