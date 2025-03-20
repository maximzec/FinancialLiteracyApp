<template>
  <div class="home-container">
    <!-- Навигация -->
    <div class="tbank-navigation">
      <div class="tbank-navigation__brand">Финансовая грамотность</div>
      <div class="tbank-navigation__menu">
        <a href="#" class="tbank-navigation__link">Главная</a>
        <a href="#" class="tbank-navigation__link">Курсы</a>
        <a href="#" class="tbank-navigation__link">Статьи</a>
        <a href="#" class="tbank-navigation__link">Профиль</a>
      </div>
    </div>

    <!-- Главный баннер -->
    <div class="main-banner tbank-slide-up">
      <div class="main-banner__content">
        <h1>Финансовая грамотность</h1>
        <p class="main-banner__subtitle">Начните свой путь к финансовой независимости вместе с нами</p>
        <button class="tbank-button">Начать обучение</button>
      </div>
      <div class="main-banner__image">
        <img src="https://cdn3d.iconscout.com/3d/premium/thumb/finance-management-5740461-4805695.png" alt="Финансовая грамотность">
      </div>
    </div>

    <!-- Раздел курсов -->
    <section class="section tbank-fade-in">
      <div class="section__header">
        <h2>Популярные курсы</h2>
        <a href="#" class="section__more">Все курсы</a>
      </div>
      
      <div class="tbank-grid">
        <!-- Карточка курса 1 -->
        <div class="tbank-card course-card">
          <div class="tbank-badge">Популярно</div>
          <div class="course-card__image">
            <img src="https://cdn3d.iconscout.com/3d/premium/thumb/budget-planning-5554869-4639076.png" alt="Основы финансов">
          </div>
          <h3 class="tbank-card__title">Основы личных финансов</h3>
          <p class="tbank-card__text">Научитесь базовым принципам управления личными финансами и создания бюджета</p>
          <div class="course-card__footer">
            <span class="course-card__info">8 уроков • 2 часа</span>
            <button class="tbank-button">Перейти</button>
          </div>
        </div>

        <!-- Карточка курса 2 -->
        <div class="tbank-card course-card">
          <div class="tbank-badge tbank-badge--new">Новый</div>
          <div class="course-card__image">
            <img src="https://cdn3d.iconscout.com/3d/premium/thumb/investment-5740487-4805717.png" alt="Инвестиции">
          </div>
          <h3 class="tbank-card__title">Основы инвестирования</h3>
          <p class="tbank-card__text">Изучите базовые принципы инвестирования и стратегии формирования инвестиционного портфеля</p>
          <div class="course-card__footer">
            <span class="course-card__info">10 уроков • 3 часа</span>
            <button class="tbank-button">Перейти</button>
          </div>
        </div>

        <!-- Карточка курса 3 -->
        <div class="tbank-card course-card">
          <div class="course-card__image">
            <img src="https://cdn3d.iconscout.com/3d/premium/thumb/money-savings-5740564-4805788.png" alt="Сбережения">
          </div>
          <h3 class="tbank-card__title">Накопления и сбережения</h3>
          <p class="tbank-card__text">Узнайте, как правильно формировать финансовую подушку безопасности и копить на важные цели</p>
          <div class="course-card__footer">
            <span class="course-card__info">6 уроков • 1.5 часа</span>
            <button class="tbank-button">Перейти</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Промо-блок -->
    <div class="promo-block tbank-slide-up">
      <div class="promo-block__content">
        <div class="promo-block__image">
          <img src="https://cdn3d.iconscout.com/3d/premium/thumb/financial-growth-5044949-4199887.png" alt="Финансовый план">
        </div>
        <div class="promo-block__text">
          <h2>Рассчитайте свой финансовый план</h2>
          <p>Получите персональные рекомендации для достижения финансовых целей</p>
          <button class="tbank-button">Рассчитать</button>
        </div>
      </div>
    </div>

    <!-- Раздел полезных статей -->
    <section class="section tbank-fade-in">
      <div class="section__header">
        <h2>Полезные статьи</h2>
        <a href="#" class="section__more">Все статьи</a>
      </div>
      
      <div class="tbank-grid">
        <!-- Статья 1 -->
        <div class="tbank-card article-card">
          <div class="article-card__image">
            <img src="https://cdn3d.iconscout.com/3d/premium/thumb/money-growth-5160611-4311081.png" alt="Пассивный доход">
          </div>
          <div class="article-card__content">
            <div class="article-card__category">Инвестиции</div>
            <h3 class="tbank-card__title">Как создать пассивный доход</h3>
            <p class="tbank-card__text">Узнайте о различных способах создания пассивного дохода и начните путь к финансовой свободе</p>
            <div class="article-card__footer">
              <span class="article-card__info">7 мин. чтения</span>
              <a href="#" class="article-card__link">Читать</a>
            </div>
          </div>
        </div>

        <!-- Статья 2 -->
        <div class="tbank-card article-card">
          <div class="article-card__image">
            <img src="https://cdn3d.iconscout.com/3d/premium/thumb/budget-calculator-5744026-4808975.png" alt="Правило 50/30/20">
          </div>
          <div class="article-card__content">
            <div class="article-card__category">Бюджет</div>
            <h3 class="tbank-card__title">Правило 50/30/20</h3>
            <p class="tbank-card__text">Простая и эффективная система распределения доходов для достижения финансовых целей</p>
            <div class="article-card__footer">
              <span class="article-card__info">5 мин. чтения</span>
              <a href="#" class="article-card__link">Читать</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3D декоративные элементы -->
    <div class="decorative-3d-elements">
      <div class="coin coin-1"></div>
      <div class="coin coin-2"></div>
      <div class="coin coin-3"></div>
      <div class="coin coin-4"></div>
      <div class="chart-element"></div>
      <div class="wallet-element"></div>
    </div>

    <!-- Кнопка возврата к онбордингу -->
    <div class="back-button-container">
      <button @click="restartOnboarding" class="tbank-button tbank-button--secondary">Вернуться к онбордингу</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      styleInterval: null
    }
  },
  computed: {
    isTelegramApp() {
      return this.$telegram && this.$telegram.isRunningInTelegram();
    }
  },
  methods: {
    restartOnboarding() {
      localStorage.removeItem('onboardingCompleted');
      this.$router.push('/');
    }
  },
  mounted() {
    document.body.classList.add('telegram-app');
    
    if (this.isTelegramApp) {
      this.$telegram.requestFullScreen();
      this.$telegram.hideBackButton();
    }
  },
  beforeUnmount() {
    if (this.styleInterval) {
      clearInterval(this.styleInterval);
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  padding-bottom: 60px;
  box-sizing: border-box;
  background-color: var(--tbank-light-gray);
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 100vh;
}

/* Главный баннер */
.main-banner {
  display: flex;
  align-items: center;
  padding: 40px 24px;
  background: var(--app-gradient);
  margin-bottom: 40px;
  border-radius: 0 0 30px 30px;
  position: relative;
  overflow: hidden;
}

.main-banner__content {
  flex: 1;
  padding-right: 20px;
  position: relative;
  z-index: 2;
}

.main-banner__image {
  flex: 1;
  max-width: 50%;
  display: none;
  position: relative;
  z-index: 2;
}

.main-banner__image img {
  width: 100%;
  height: auto;
  max-width: 300px;
  filter: drop-shadow(0 10px 15px rgba(0, 0, 0, 0.1));
  transform: scale(1.2);
  animation: float 6s ease-in-out infinite;
}

.main-banner h1 {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 16px;
  color: var(--tbank-black);
}

.main-banner__subtitle {
  font-size: 18px;
  margin-bottom: 24px;
  color: var(--tbank-dark-gray);
  max-width: 500px;
}

/* Секции */
.section {
  padding: 0 24px;
  margin-bottom: 50px;
}

.section__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section__more {
  font-size: 16px;
  color: var(--app-secondary-color);
  text-decoration: none;
  font-weight: 500;
}

.section__more:hover {
  text-decoration: underline;
}

/* Карточки курсов */
.course-card {
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.course-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1);
}

.course-card__image {
  height: 180px;
  margin: -24px -24px 16px -24px;
  overflow: hidden;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-card__image img {
  width: 60%;
  height: auto;
  object-fit: contain;
  transition: transform 0.4s ease;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.1));
}

.course-card:hover .course-card__image img {
  transform: scale(1.05) translateY(-5px);
}

.tbank-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1;
}

.course-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.course-card__info {
  font-size: 14px;
  color: var(--app-hint-color);
}

/* Статьи */
.article-card__image {
  height: 180px;
  margin: -24px -24px 16px -24px;
  overflow: hidden;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.article-card__image img {
  width: 60%;
  height: auto;
  object-fit: contain;
  transition: transform 0.4s ease;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.1));
}

.article-card:hover .article-card__image img {
  transform: scale(1.05) translateY(-5px);
}

.article-card__category {
  display: inline-block;
  font-size: 14px;
  font-weight: 600;
  color: var(--app-secondary-color);
  margin-bottom: 8px;
}

.article-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-card__info {
  font-size: 14px;
  color: var(--app-hint-color);
}

.article-card__link {
  color: var(--app-secondary-color);
  font-weight: 600;
  text-decoration: none;
}

.article-card__link:hover {
  text-decoration: underline;
}

/* Промо-блок */
.promo-block {
  background: var(--app-gradient);
  padding: 40px 24px;
  margin: 0 24px 50px;
  border-radius: var(--app-radius-large);
}

.promo-block__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.promo-block__image {
  width: 150px;
  height: 150px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.promo-block__image img {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.1));
  animation: floatSlow 8s ease-in-out infinite;
}

.promo-block__text {
  max-width: 600px;
}

.promo-block h2 {
  font-size: 28px;
  margin-bottom: 16px;
  color: var(--tbank-black);
}

.promo-block p {
  font-size: 18px;
  margin-bottom: 24px;
  color: var(--tbank-dark-gray);
}

/* 3D Декоративные элементы */
.decorative-3d-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.coin {
  position: absolute;
  width: 50px;
  height: 50px;
  background-image: url('https://cdn3d.iconscout.com/3d/premium/thumb/bitcoin-5044920-4199858.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.2;
  z-index: -1;
}

.coin-1 {
  top: 15%;
  left: 10%;
  animation: floatCoin 10s ease-in-out infinite;
}

.coin-2 {
  bottom: 20%;
  right: 5%;
  width: 40px;
  height: 40px;
  animation: floatCoin 12s ease-in-out infinite 1s;
}

.coin-3 {
  top: 60%;
  left: 7%;
  width: 30px;
  height: 30px;
  animation: floatCoin 9s ease-in-out infinite 2s;
}

.coin-4 {
  top: 30%;
  right: 10%;
  width: 25px;
  height: 25px;
  animation: floatCoin 11s ease-in-out infinite 3s;
}

.chart-element {
  position: absolute;
  bottom: 10%;
  left: 15%;
  width: 60px;
  height: 60px;
  background-image: url('https://cdn3d.iconscout.com/3d/premium/thumb/financial-growth-5045003-4199941.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.2;
  z-index: -1;
  animation: floatSlow 15s ease-in-out infinite;
}

.wallet-element {
  position: absolute;
  top: 40%;
  right: 20%;
  width: 55px;
  height: 55px;
  background-image: url('https://cdn3d.iconscout.com/3d/premium/thumb/wallet-5045123-4200061.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.2;
  z-index: -1;
  animation: floatSlow 13s ease-in-out infinite 2s;
}

/* Кнопка возврата */
.back-button-container {
  text-align: center;
  margin-top: 40px;
}

/* Анимации */
@keyframes float {
  0%, 100% {
    transform: scale(1.2) translateY(0);
  }
  50% {
    transform: scale(1.2) translateY(-10px);
  }
}

@keyframes floatSlow {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-15px) rotate(5deg);
  }
}

@keyframes floatCoin {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-15px) rotate(5deg);
  }
  50% {
    transform: translateY(0) rotate(10deg);
  }
  75% {
    transform: translateY(15px) rotate(5deg);
  }
}

/* Адаптивность */
@media (min-width: 768px) {
  .main-banner {
    padding: 60px 40px;
  }
  
  .main-banner__image {
    display: block;
  }
  
  .main-banner h1 {
    font-size: 48px;
  }
  
  .section, .promo-block {
    padding: 0 40px;
    margin-left: 40px;
    margin-right: 40px;
  }

  .promo-block__content {
    flex-direction: row;
    text-align: left;
  }

  .promo-block__image {
    margin-bottom: 0;
    margin-right: 40px;
  }
}
</style> 