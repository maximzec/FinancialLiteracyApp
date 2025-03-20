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

                // Запрашиваем полноэкранный режим
                this.requestFullScreen();

                // Скрываем элементы управления Telegram
                this.hideBackButton();
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

            // Обработчик изменения полноэкранного режима
            this.webApp.onEvent('fullscreenChanged', (isFullscreen) => {
                console.log('Fullscreen mode changed:', isFullscreen);
            });

            // Обработчик ошибки полноэкранного режима
            this.webApp.onEvent('fullscreenFailed', () => {
                console.error('Failed to enter fullscreen mode');
            });

            // Обработчик изменения безопасной области
            this.webApp.onEvent('safeAreaChanged', () => {
                console.log('Safe area changed');
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

    // Метод для обратной совместимости с isAvailable()
    isAvailable() {
        return this.isRunningInTelegram();
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

    // Метод для запроса полноэкранного режима (новый метод из Bot API 8.0)
    requestFullScreen() {
        if (!this.isInitialized) return;

        try {
            // Используем новый метод requestFullscreen из Bot API 8.0
            if (typeof this.webApp.requestFullscreen === 'function') {
                this.webApp.requestFullscreen();
                console.log('Requested full screen mode using new API');
            } else {
                // Для обратной совместимости используем старый метод
                this.webApp.expand();
                console.log('Requested expanded mode (fallback)');
            }
        } catch (error) {
            console.error('Failed to request full screen:', error);
        }
    }

    // Метод для выхода из полноэкранного режима (новый метод из Bot API 8.0)
    exitFullScreen() {
        if (!this.isInitialized) return;

        try {
            // Используем новый метод exitFullscreen из Bot API 8.0
            if (typeof this.webApp.exitFullscreen === 'function') {
                this.webApp.exitFullscreen();
                console.log('Exited full screen mode');
            }
        } catch (error) {
            console.error('Failed to exit full screen:', error);
        }
    }

    // Метод для проверки, находится ли приложение в полноэкранном режиме
    isFullScreen() {
        if (!this.isInitialized) return false;

        try {
            // Используем новое свойство isFullscreen из Bot API 8.0
            if (typeof this.webApp.isFullscreen !== 'undefined') {
                return this.webApp.isFullscreen;
            }
            // Для обратной совместимости
            return this.webApp.isExpanded;
        } catch (error) {
            console.error('Failed to check full screen status:', error);
            return false;
        }
    }

    // Метод для скрытия кнопки "Назад" в Telegram
    hideBackButton() {
        if (!this.isInitialized) return;

        try {
            // Скрываем кнопку "Назад"
            this.webApp.BackButton.hide();

            // Отключаем стандартное поведение при свайпе назад
            this.webApp.disableClosingConfirmation();

            console.log('Back button hidden');
        } catch (error) {
            console.error('Failed to hide back button:', error);
        }
    }

    // Метод для показа кнопки "Назад" в Telegram
    showBackButton(callback) {
        if (!this.isInitialized) return;

        try {
            const backButton = this.webApp.BackButton;

            if (backButton) {
                if (callback) {
                    backButton.onClick(callback);
                }

                backButton.show();
            }

            console.log('Back button shown');
        } catch (error) {
            console.error('Failed to show back button:', error);
        }
    }
}

// Создаем и экспортируем экземпляр сервиса
const telegramService = new TelegramService();
export default telegramService; 