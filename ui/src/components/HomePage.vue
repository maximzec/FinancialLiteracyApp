<template>
  <div class="home-page">
    <header class="app-header">
      <div class="logo">FinLit</div>
      <button class="menu-button" @click="toggleMenu" v-if="!isTelegramApp">
        <span class="menu-icon"></span>
      </button>
    </header>

    <div class="sidebar" :class="{ 'sidebar-open': menuOpen }">
      <div class="sidebar-header">
        <div class="user-profile">
          <div class="user-avatar">
            <img :src="userAvatar" alt="Аватар пользователя" />
          </div>
          <div class="user-info">
            <h3>{{ userName }}</h3>
            <p>Начинающий</p>
          </div>
        </div>
        <button class="close-menu" @click="toggleMenu">×</button>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li><a href="#" class="active">Главная</a></li>
          <li><a href="#">Мой профиль</a></li>
          <li><a href="#">Курсы</a></li>
          <li><a href="#">Достижения</a></li>
          <li><a href="#">Настройки</a></li>
          <li><a href="#">Помощь</a></li>
        </ul>
      </nav>
    </div>

    <div class="overlay" v-if="menuOpen" @click="toggleMenu"></div>

    <main class="content">
      <section class="welcome-section">
        <h1>Добро пожаловать в FinLit!</h1>
        <p>Ваш персональный помощник в мире финансовой грамотности</p>
      </section>

      <section class="cards-section">
        <h2>Рекомендуемые действия</h2>
        <div class="cards-grid">
          <div class="card course-card" @click="startCourse">
            <div class="card-icon">📚</div>
            <div class="card-content">
              <h3>Начать обучение</h3>
              <p>Пройдите первый урок по основам финансовой грамотности</p>
              <button class="card-button">Начать</button>
            </div>
          </div>

          <div class="card news-card" @click="openNews">
            <div class="card-icon">📰</div>
            <div class="card-content">
              <h3>Новости</h3>
              <p>Актуальные новости из мира финансов</p>
              <button class="card-button">Читать</button>
            </div>
          </div>

          <div class="card schedule-card" @click="viewSchedule">
            <div class="card-icon">📅</div>
            <div class="card-content">
              <h3>Расписание занятий</h3>
              <p>Запланированные уроки и вебинары</p>
              <button class="card-button">Посмотреть</button>
            </div>
          </div>

          <div class="card quiz-card" @click="startQuiz">
            <div class="card-icon">🧩</div>
            <div class="card-content">
              <h3>Тест дня</h3>
              <p>Проверьте свои знания в коротком тесте</p>
              <button class="card-button">Пройти тест</button>
            </div>
          </div>
        </div>
      </section>

      <section class="progress-section">
        <h2>Ваш прогресс</h2>
        <div class="progress-container">
          <div class="progress-info">
            <span>Основы финансов</span>
            <span>30%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: 30%"></div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      menuOpen: false
    };
  },
  computed: {
    // Проверка, запущено ли приложение в Telegram
    isTelegramApp() {
      return this.$telegram && this.$telegram.isRunningInTelegram();
    },
    // Получение имени пользователя
    userName() {
      if (this.isTelegramApp && this.$telegram.getUserData()) {
        const user = this.$telegram.getUserData();
        return user.first_name || 'Пользователь';
      }
      return 'Пользователь';
    },
    // Получение аватара пользователя
    userAvatar() {
      if (this.isTelegramApp && this.$telegram.getUserData() && this.$telegram.getUserData().photo_url) {
        return this.$telegram.getUserData().photo_url;
      }
      return require('../assets/logo.png');
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
      if (this.menuOpen) {
        document.body.classList.add('no-scroll');
      } else {
        document.body.classList.remove('no-scroll');
      }
    },
    // Методы для обработки нажатий на карточки
    startCourse() {
      console.log('Начать обучение');
      if (this.isTelegramApp) {
        this.$telegram.showMainButton('Начать урок', () => {
          // Логика для начала урока
          console.log('Начинаем урок через Telegram MainButton');
        });
      }
      // Здесь будет логика для начала обучения
    },
    openNews() {
      console.log('Открыть новости');
      // Здесь будет логика для открытия новостей
    },
    viewSchedule() {
      console.log('Посмотреть расписание');
      // Здесь будет логика для просмотра расписания
    },
    startQuiz() {
      console.log('Начать тест');
      if (this.isTelegramApp) {
        this.$telegram.showMainButton('Начать тест', () => {
          // Логика для начала теста
          console.log('Начинаем тест через Telegram MainButton');
        });
      }
      // Здесь будет логика для начала теста
    }
  },
  beforeUnmount() {
    // Удаляем обработчик события resize
    window.removeEventListener('resize', this.handleResize);
  },
  created() {
    // Создаем метод для обработки изменения размера окна
    this.handleResize = () => {
      if (this.isTelegramApp && !this.$telegram.isFullScreen()) {
        this.$telegram.requestFullScreen();
      }
    };
  },
  mounted() {
    // Если приложение запущено в Telegram, настраиваем интерфейс
    if (this.isTelegramApp) {
      // Запрашиваем полноэкранный режим
      this.$telegram.requestFullScreen();
      
      // Скрываем элементы управления Telegram
      this.$telegram.hideBackButton();
      
      // Добавляем обработчик для повторного запроса полноэкранного режима
      window.addEventListener('resize', this.handleResize);
      
      // Добавляем класс для полноэкранного режима
      document.body.classList.add('fullscreen-active');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.home-page {
  font-family: 'Inter', sans-serif;
  background-color: var(--app-background-color, #f5f7fa);
  min-height: 100vh;
  color: var(--app-text-color, #333);
  position: relative;
}

/* Заголовок */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: var(--app-header-background, #ffffff);
  box-shadow: 0 2px 10px var(--app-shadow-color, rgba(0, 0, 0, 0.05));
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: var(--app-link-color, #1a73e8);
}

.menu-button {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.menu-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.menu-icon {
  position: relative;
  width: 24px;
  height: 2px;
  background-color: var(--app-text-color, #333);
}

.menu-icon::before,
.menu-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background-color: var(--app-text-color, #333);
  transition: transform 0.3s;
}

.menu-icon::before {
  top: -6px;
}

.menu-icon::after {
  top: 6px;
}

/* Боковое меню */
.sidebar {
  position: fixed;
  top: 0;
  right: -280px;
  width: 280px;
  height: 100vh;
  background-color: var(--app-background-color, #ffffff);
  box-shadow: -2px 0 10px var(--app-shadow-color, rgba(0, 0, 0, 0.1));
  z-index: 1000;
  transition: right 0.3s ease;
  overflow-y: auto;
}

.sidebar-open {
  right: 0;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--app-border-color, #eaeaea);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--app-text-color, #333);
}

.user-info p {
  margin: 5px 0 0;
  font-size: 14px;
  color: var(--app-hint-color, #666);
}

.close-menu {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--app-hint-color, #666);
}

.sidebar-nav {
  padding: 20px 0;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav li {
  margin-bottom: 5px;
}

.sidebar-nav a {
  display: block;
  padding: 12px 20px;
  color: var(--app-text-color, #333);
  text-decoration: none;
  transition: background-color 0.3s;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  background-color: var(--app-card-background, #f0f7ff);
  color: var(--app-link-color, #1a73e8);
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* Основной контент */
.content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 30px;
}

.welcome-section h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: var(--app-link-color, #1a73e8);
}

.welcome-section p {
  font-size: 16px;
  color: var(--app-hint-color, #666);
}

.cards-section {
  margin-bottom: 30px;
}

.cards-section h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: var(--app-text-color, #333);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.card {
  background-color: var(--app-card-background, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 12px var(--app-shadow-color, rgba(0, 0, 0, 0.05));
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px var(--app-shadow-color, rgba(0, 0, 0, 0.1));
}

.card-icon {
  font-size: 32px;
  padding: 20px;
  text-align: center;
  background-color: var(--app-card-background, #f0f7ff);
}

.course-card .card-icon {
  background-color: #e8f0fe;
}

.news-card .card-icon {
  background-color: #fef8e8;
}

.schedule-card .card-icon {
  background-color: #e8f5e9;
}

.quiz-card .card-icon {
  background-color: #f3e5f5;
}

.card-content {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.card-content h3 {
  font-size: 18px;
  margin: 0 0 10px;
  color: var(--app-text-color, #333);
}

.card-content p {
  font-size: 14px;
  color: var(--app-hint-color, #666);
  margin: 0 0 15px;
  flex-grow: 1;
}

.card-button {
  background-color: var(--app-button-color, #1a73e8);
  color: var(--app-button-text-color, white);
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  align-self: flex-start;
}

.card-button:hover {
  background-color: #1669d8;
}

/* Секция прогресса */
.progress-section {
  margin-bottom: 30px;
}

.progress-section h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: var(--app-text-color, #333);
}

.progress-container {
  background-color: var(--app-card-background, #ffffff);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px var(--app-shadow-color, rgba(0, 0, 0, 0.05));
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--app-text-color, #333);
}

.progress-bar {
  height: 10px;
  background-color: var(--app-border-color, #f0f0f0);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--app-button-color, #1a73e8);
  border-radius: 5px;
}

/* Стили для предотвращения прокрутки при открытом меню */
.no-scroll {
  overflow: hidden;
}

/* Медиа-запросы для адаптивности */
@media (max-width: 768px) {
  .welcome-section h1 {
    font-size: 24px;
  }
  
  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style> 