import WebApp from '@twa-dev/sdk';

class TelegramService {
    constructor() {
        this.webApp = WebApp;
        this.isInitialized = false;
        this.initTelegramApp();
    }

    initTelegramApp() {
        if (this.webApp && !this.isInitialized) {
            try {
                // Инициализация Telegram WebApp
                this.webApp.ready();
                this.isInitialized = true;
                console.log('Telegram WebApp initialized successfully');

                // Настройка темы
                this.applyTelegramTheme();

                // Настройка основных параметров
                this.setupMainButton();

                // Настройка обработчиков событий
                this.setupEventHandlers();
            } catch (error) {
                console.error('Failed to initialize Telegram WebApp:', error);
            }
        } else if (this.isInitialized) {
            console.log('Telegram WebApp already initialized');
        } else {
            console.warn('Telegram WebApp SDK not available');
        }
    }

    applyTelegramTheme() {
        if (!this.isInitialized) return;

        try {
            // Получаем цвета темы из Telegram
            const colorScheme = this.webApp.colorScheme;
            document.documentElement.setAttribute('data-theme', colorScheme);

            // Устанавливаем цвет фона
            if (this.webApp.backgroundColor) {
                document.body.style.backgroundColor = this.webApp.backgroundColor;
            }

            console.log('Telegram theme applied:', colorScheme);
        } catch (error) {
            console.error('Failed to apply Telegram theme:', error);
        }
    }

    setupMainButton() {
        if (!this.isInitialized) return;

        try {
            // Настройка главной кнопки Telegram
            const mainButton = this.webApp.MainButton;

            if (mainButton) {
                // Скрываем кнопку по умолчанию, будем показывать её при необходимости
                mainButton.hide();
            }
        } catch (error) {
            console.error('Failed to setup main button:', error);
        }
    }

    setupEventHandlers() {
        if (!this.isInitialized) return;

        try {
            // Обработчик изменения темы
            this.webApp.onEvent('themeChanged', () => {
                this.applyTelegramTheme();
            });

            // Обработчик закрытия приложения
            this.webApp.onEvent('viewportChanged', () => {
                console.log('Viewport changed');
            });
        } catch (error) {
            console.error('Failed to setup event handlers:', error);
        }
    }

    // Методы для работы с главной кнопкой
    showMainButton(text, callback) {
        if (!this.isInitialized) return;

        try {
            const mainButton = this.webApp.MainButton;

            if (mainButton) {
                mainButton.setText(text);

                if (callback) {
                    mainButton.onClick(callback);
                }

                mainButton.show();
            }
        } catch (error) {
            console.error('Failed to show main button:', error);
        }
    }

    hideMainButton() {
        if (!this.isInitialized) return;

        try {
            const mainButton = this.webApp.MainButton;

            if (mainButton) {
                mainButton.hide();
            }
        } catch (error) {
            console.error('Failed to hide main button:', error);
        }
    }

    // Методы для работы с данными пользователя
    getUserData() {
        if (!this.isInitialized) return null;

        try {
            return this.webApp.initDataUnsafe?.user || null;
        } catch (error) {
            console.error('Failed to get user data:', error);
            return null;
        }
    }

    // Метод для закрытия приложения
    closeApp() {
        if (!this.isInitialized) return;

        try {
            this.webApp.close();
        } catch (error) {
            console.error('Failed to close app:', error);
        }
    }

    // Метод для проверки, запущено ли приложение в Telegram
    isRunningInTelegram() {
        return this.isInitialized && this.webApp.isExpanded;
    }

    // Метод для отправки данных в Telegram бота
    sendData(data) {
        if (!this.isInitialized) return;

        try {
            this.webApp.sendData(JSON.stringify(data));
        } catch (error) {
            console.error('Failed to send data:', error);
        }
    }

    // Метод для расширения окна приложения на весь экран
    expandApp() {
        if (!this.isInitialized) return;

        try {
            this.webApp.expand();
        } catch (error) {
            console.error('Failed to expand app:', error);
        }
    }
}

// Создаем и экспортируем экземпляр сервиса
const telegramService = new TelegramService();
export default telegramService; 