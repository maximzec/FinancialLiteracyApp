<template>
  <div id="app">
    <UserOnboarding v-if="showOnboarding" @onboarding-completed="completeOnboarding" />
    <HomePage v-else />
  </div>
</template>

<script>
import UserOnboarding from './components/UserOnboarding.vue';
import HomePage from './components/HomePage.vue';

export default {
  components: {
    UserOnboarding,
    HomePage
  },
  data() {
    return {
      showOnboarding: true,
      telegramUser: null
    };
  },
  methods: {
    completeOnboarding() {
      this.showOnboarding = false;
      // Здесь можно добавить сохранение состояния в localStorage, чтобы не показывать онбординг при повторном посещении
      localStorage.setItem('onboardingCompleted', 'true');
      
      // Если приложение запущено в Telegram, показываем главную кнопку
      this.setupTelegramMainButton();
    },
    
    // Методы для работы с Telegram Mini Apps
    setupTelegramMainButton() {
      if (this.isTelegramApp) {
        this.$telegram.showMainButton('Продолжить обучение', () => {
          console.log('Нажата главная кнопка Telegram');
          // Здесь можно добавить логику для перехода к обучению
        });
      }
    },
    
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
    // Проверяем, был ли уже пройден онбординг
    const onboardingCompleted = localStorage.getItem('onboardingCompleted');
    if (onboardingCompleted === 'true') {
      this.showOnboarding = false;
    }
    
    // Если приложение запущено в Telegram
    if (this.isTelegramApp) {
      // Получаем данные пользователя
      this.getTelegramUserData();
      
      // Запрашиваем полноэкранный режим
      this.$telegram.requestFullScreen();
      
      // Скрываем элементы управления Telegram
      this.$telegram.hideBackButton();
      
      // Если онбординг уже пройден, показываем главную кнопку
      if (!this.showOnboarding) {
        this.setupTelegramMainButton();
      }
    }
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
}

#app {
  width: 100%;
  height: 100%;
}

/* Добавляем мета-тег для корректного отображения в мобильных браузерах */
@media screen and (max-width: 768px) {
  #app {
    max-width: 100vw;
    overflow-x: hidden;
  }
}
</style> 