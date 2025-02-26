import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles/telegram-theme.css'

// Импортируем сервис для работы с Telegram
import telegramService from './services/TelegramService'

// Создаем экземпляр приложения
const app = createApp(App)

// Добавляем сервис Telegram в глобальные свойства
app.config.globalProperties.$telegram = telegramService

// Проверяем, запущено ли приложение в Telegram
const isTelegramApp = telegramService.isRunningInTelegram()

// Добавляем класс для стилизации, если приложение запущено в Telegram
if (isTelegramApp) {
    document.body.classList.add('telegram-app')
}

// Монтируем приложение
app.mount('#app')
