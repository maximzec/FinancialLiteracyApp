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

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  background-color: var(--app-background-color, #f5f7fa);
  color: var(--app-text-color, #333333);
}

#app {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Стили для Telegram Mini Apps */
.telegram-app {
  background-color: var(--app-background-color);
  color: var(--app-text-color);
}

/* Медиа-запросы для адаптивности */
@media screen and (max-width: 768px) {
  #app {
    max-width: 100vw;
    overflow-x: hidden;
  }
}
</style> 