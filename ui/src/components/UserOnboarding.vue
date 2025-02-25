<template>
  <div class="onboarding-fullscreen">
    <div class="onboarding-content">
      <div class="progress-bar-wrapper">
        <div class="progress-bar-container">
          <div class="progress-bar-fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
      <transition name="fade-slide" mode="out-in">
        <div class="step-content" :key="step">
          <div v-if="step === 1">
            <div class="image-container">
              <img src="path/to/image1.jpg" alt="Изображение 1" />
            </div>
            <h1>Добро пожаловать!</h1>
            <p>Рассказ про преимущества продукта...</p>
          </div>
          <div v-else-if="step === 2">
            <div class="image-container">
              <img src="path/to/image2.jpg" alt="Изображение 2" />
            </div>
            <h2>Выберите ваш возраст</h2>
          </div>
          <div v-else-if="step === 3">
            <div class="image-container">
              <img src="path/to/image3.jpg" alt="Изображение 3" />
            </div>
            <h2>Выберите ваши финансовые накопления</h2>
          </div>
          <div v-else-if="step === 4">
            <div class="image-container">
              <img src="path/to/image4.jpg" alt="Изображение 4" />
            </div>
            <h2>Выберите цель обучения</h2>
          </div>
        </div>
      </transition>
    </div>
    <div class="onboarding-button-container">
      <button class="onboarding-button" @click="step < 4 ? nextStep() : finishOnboarding()">
        {{ step < 4 ? 'Далее' : 'Завершить' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserOnboarding',
  components: {
    // ProgressBar,
  },
  data() {
    return {
      step: 1,
      styleInterval: null
    };
  },
  computed: {
    progress() {
      return (this.step / 4) * 100;
    },
  },
  methods: {
    nextStep() {
      if (this.step < 4) {
        this.step++;
      }
    },
    finishOnboarding() {
      // Логика завершения онбординга
      console.log('Онбординг завершен');
    },
    forceBlackBackground() {
      document.body.classList.add('onboarding-active');
      
      // Создаем глобальные стили
      const styleElement = document.createElement('style');
      styleElement.id = 'onboarding-global-styles';
      styleElement.textContent = `
        body.onboarding-active {
          background-color: #000000 !important;
          overflow: hidden !important;
          position: fixed !important;
          width: 100% !important;
          height: 100% !important;
        }
        
        html {
          background-color: #000000 !important;
        }
      `;
      document.head.appendChild(styleElement);
      
      // Устанавливаем метатеги
      const themeColorMeta = document.createElement('meta');
      themeColorMeta.name = 'theme-color';
      themeColorMeta.content = '#000000';
      document.head.appendChild(themeColorMeta);
      
      // Запускаем интервал для постоянного применения стилей
      this.styleInterval = setInterval(() => {
        document.body.style.backgroundColor = '#000000';
        document.documentElement.style.backgroundColor = '#000000';
      }, 100);
    },
    removeBlackBackground() {
      document.body.classList.remove('onboarding-active');
      
      // Удаляем глобальные стили
      const styleElement = document.getElementById('onboarding-global-styles');
      if (styleElement) {
        styleElement.remove();
      }
      
      // Удаляем метатеги
      document.querySelectorAll('meta[name="theme-color"]').forEach(meta => {
        meta.remove();
      });
      
      // Останавливаем интервал
      clearInterval(this.styleInterval);
    }
  },
  mounted() {
    this.forceBlackBackground();
  },
  beforeUnmount() {
    this.removeBlackBackground();
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.onboarding-fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #ffffff;
  background-image: radial-gradient(circle at center, rgba(0, 0, 0, 0.05) 0%, rgba(255, 255, 255, 1) 70%);
  background-attachment: fixed;
  background-size: cover;
  background-position: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  z-index: 9999;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  font-family: 'Inter', sans-serif;
  color: #333333;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.onboarding-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.progress-bar-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 30px;
  padding: 0 20px;
  box-sizing: border-box;
}

.progress-bar-container {
  width: 100%;
  max-width: 300px;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), inset 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.progress-bar-fill {
  height: 100%;
  background-color: #1a73e8;
  background-image: linear-gradient(45deg, #1a73e8, #4285f4);
  border-radius: 10px;
  transition: width 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 0 10px rgba(26, 115, 232, 0.5);
}

.step-content {
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  flex: 1;
  margin: 0;
  padding-top: 0;
}

.image-container {
  width: 100%;
  max-width: 300px;
  height: 150px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-left: auto;
  margin-right: auto;
  margin-top: 0;
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.onboarding-button-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  padding: 20px;
  padding-bottom: calc(20px + env(safe-area-inset-bottom));
  text-align: center;
  background: transparent;
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.onboarding-button-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 100%);
  z-index: -1;
}

.onboarding-button {
  position: relative;
  display: inline-block;
  background: #1a73e8;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 15px 30px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s;
  width: 80%;
  max-width: 300px;
  margin: 0 auto;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.02em;
}

.onboarding-button:hover {
  background: #1669d8;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.onboarding-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

h1, h2 {
  color: #333333;
  margin-bottom: 15px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.02em;
  font-weight: 700;
}

h1 {
  font-size: 32px;
  letter-spacing: 0.01em;
}

h2 {
  font-size: 28px;
  letter-spacing: 0.02em;
}

p {
  color: rgba(0, 0, 0, 0.8);
  text-align: center;
  margin-bottom: 20px;
  font-weight: 400;
  line-height: 1.5;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
  letter-spacing: 0.03em;
}

/* Анимации */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.6s cubic-bezier(0.33, 1, 0.68, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

/* Медиа-запрос для маленьких экранов */
@media screen and (max-height: 600px) {
  .onboarding-content {
    justify-content: flex-start;
  }
  
  .image-container {
    height: 100px;
    margin-bottom: 10px;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  h2 {
    font-size: 20px;
    margin-bottom: 10px;
  }
  
  p {
    margin-bottom: 10px;
    font-size: 14px;
  }
  
  .onboarding-button {
    padding: 12px 24px;
    font-size: 16px;
  }
}

/* Стили для прогресс-бара */
.progress-bar-container {
  width: 100%;
  max-width: 300px;
  height: 20px;
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Стиль для заполняющей части прогресс-бара */
.progress-bar,
.progress-fill,
.progress-value,
[class*="progress-fill"],
[class*="progress-value"],
[class*="progress-bar-fill"] {
  height: 100% !important;
  background-color: #1a73e8 !important;
  border-radius: 10px !important;
  transition: width 0.3s linear !important;
  position: relative !important;
  overflow: hidden !important;
  animation: none !important;
  -webkit-animation: none !important;
}

/* Полностью отключаем все анимации и эффекты для прогресс-бара */
.progress-bar::before,
.progress-bar::after,
.progress-fill::before,
.progress-fill::after,
.progress-value::before,
.progress-value::after,
[class*="progress-fill"]::before,
[class*="progress-fill"]::after,
[class*="progress-value"]::before,
[class*="progress-value"]::after,
[class*="progress-bar-fill"]::before,
[class*="progress-bar-fill"]::after {
  display: none !important;
  opacity: 0 !important;
  content: none !important;
}

/* Скрываем все возможные анимированные элементы */
.progress-bar-pulse,
.progress-bar-shine,
.progress-bar-glow,
.progress-bar-highlight,
.progress-bar-overlay,
.progress-bar-animation,
.progress-bar-animated,
[class*="progress-bar-anim"],
[class*="progress-shine"],
[class*="progress-glow"],
[class*="progress-highlight"] {
  display: none !important;
  opacity: 0 !important;
  visibility: hidden !important;
}

/* Отключаем любые эффекты мерцания */
@keyframes none {
  0% { opacity: 1; }
  100% { opacity: 1; }
}
</style> 