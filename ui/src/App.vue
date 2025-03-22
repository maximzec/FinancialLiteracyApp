<template>
  <div id="app" :class="{ 'telegram-app': isTelegramApp }">
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      telegramUser: null
    };
  },
  methods: {
    // Получение данных пользователя из Telegram
    getTelegramUserData() {
      if (this.isTelegramApp) {
        this.telegramUser = this.$telegram.getUserData();
        console.log('Данные пользователя Telegram:', this.telegramUser);
      }
    }
  },
  computed: {
    // Проверка, запущено ли приложение в Telegram
    isTelegramApp() {
      return this.$telegram && this.$telegram.isRunningInTelegram();
    }
  },
  created() {
    // Создаем метод для обработки изменения размера окна
    this.handleResize = () => {
      if (this.isTelegramApp && !this.$telegram.isFullScreen()) {
        this.$telegram.requestFullScreen();
      }
    };
    
    // Если приложение запущено в Telegram
    if (this.isTelegramApp) {
      // Получаем данные пользователя
      this.getTelegramUserData();
      
      // Запрашиваем полноэкранный режим
      this.$telegram.requestFullScreen();
      
      // Скрываем элементы управления Telegram
      this.$telegram.hideBackButton();
    }
  },
  beforeUnmount() {
    // Удаляем обработчик события resize
    window.removeEventListener('resize', this.handleResize);
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --alpha-red: #EF3124;
  --alpha-red-light: #FF8185;
  --alpha-red-dark: #CF2A1E;
  --alpha-gray-50: #F8F9FA;
  --alpha-gray-100: #F1F3F5;
  --alpha-gray-200: #E9ECEF;
  --alpha-gray-300: #DEE2E6;
  --alpha-gray-400: #CED4DA;
  --alpha-gray-500: #ADB5BD;
  --alpha-gray-600: #6C757D;
  --alpha-gray-700: #495057;
  --alpha-gray-800: #343A40;
  --alpha-gray-900: #212529;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'SF Pro Display', 'Styrene A LC', 'Inter', sans-serif;
  background-color: var(--alpha-gray-50);
  color: var(--alpha-gray-900);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Кнопки в стиле Альфа-Банка */
.alpha-button {
  background-color: var(--alpha-red);
  color: white;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.alpha-button:hover {
  background-color: var(--alpha-red-dark);
}

.alpha-button-outline {
  border: 1px solid var(--alpha-red);
  color: var(--alpha-red);
  background-color: transparent;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.alpha-button-outline:hover {
  background-color: rgba(239, 49, 36, 0.05);
}

/* Стили для Telegram Mini Apps */
.telegram-app {
  background-color: var(--alpha-gray-50);
  color: var(--alpha-gray-900);
}

/* Медиа-запросы для адаптивности */
@media screen and (max-width: 768px) {
  #app {
    max-width: 100vw;
    overflow-x: hidden;
  }
}
</style> 