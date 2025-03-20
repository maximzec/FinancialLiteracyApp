<template>
  <div class="onboarding-container">
    <!-- Шаг 1: Финансовое будущее -->
    <div v-if="currentStep === 1" class="onboarding-step tbank-slide-up">
      <div class="step-content">
        <h1>Каким вы видите своё финансовое будущее?</h1>
        <p>Выберите один или несколько вариантов, которые соответствуют вашим целям</p>
        
        <div class="options-grid">
          <button @click="toggleOption(1, 1)" class="tbank-option" :class="{ 'option-selected': selectedOptions[1].includes(1) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/money-growth-5160611-4311081.png" alt="Финансовая независимость">
            </div>
            <div class="option-text">
              <h3>Финансовая независимость</h3>
              <p>Создать капитал, который будет приносить пассивный доход</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[1].includes(1) }"></div>
          </button>
          
          <button @click="toggleOption(1, 2)" class="tbank-option" :class="{ 'option-selected': selectedOptions[1].includes(2) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/money-saving-5045069-4200007.png" alt="Крупные покупки">
            </div>
            <div class="option-text">
              <h3>Крупные покупки</h3>
              <p>Накопить на жильё, автомобиль или другие значимые приобретения</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[1].includes(2) }"></div>
          </button>
          
          <button @click="toggleOption(1, 3)" class="tbank-option" :class="{ 'option-selected': selectedOptions[1].includes(3) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/investment-5740487-4805717.png" alt="Инвестиции">
            </div>
            <div class="option-text">
              <h3>Инвестиции</h3>
              <p>Научиться грамотно вкладывать деньги и получать прибыль</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[1].includes(3) }"></div>
          </button>
          
          <button @click="toggleOption(1, 4)" class="tbank-option" :class="{ 'option-selected': selectedOptions[1].includes(4) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/budget-5045052-4199990.png" alt="Управление бюджетом">
            </div>
            <div class="option-text">
              <h3>Управление бюджетом</h3>
              <p>Научиться эффективно планировать доходы и расходы</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[1].includes(4) }"></div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Шаг 2: Возрастная категория -->
    <div v-if="currentStep === 2" class="onboarding-step tbank-slide-up">
      <div class="step-content">
        <h1>К какой возрастной категории вы относитесь?</h1>
        <p>Эта информация поможет нам подобрать подходящие материалы</p>
        
        <div class="options-column">
          <button @click="toggleOption(2, 1)" class="tbank-option" :class="{ 'option-selected': selectedOptions[2].includes(1) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/student-5044999-4199937.png" alt="До 25 лет">
            </div>
            <div class="option-text">
              <h3>До 25 лет</h3>
              <p>Начало карьеры, первые шаги в финансовой грамотности</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[2].includes(1) }"></div>
          </button>
          
          <button @click="toggleOption(2, 2)" class="tbank-option" :class="{ 'option-selected': selectedOptions[2].includes(2) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/work-from-home-5047290-4210174.png" alt="25-40 лет">
            </div>
            <div class="option-text">
              <h3>25-40 лет</h3>
              <p>Активное построение карьеры, создание семьи, накопления</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[2].includes(2) }"></div>
          </button>
          
          <button @click="toggleOption(2, 3)" class="tbank-option" :class="{ 'option-selected': selectedOptions[2].includes(3) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/business-management-5740458-4805693.png" alt="40-55 лет">
            </div>
            <div class="option-text">
              <h3>40-55 лет</h3>
              <p>Пик карьеры, планирование пенсии, инвестиции</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[2].includes(3) }"></div>
          </button>
          
          <button @click="toggleOption(2, 4)" class="tbank-option" :class="{ 'option-selected': selectedOptions[2].includes(4) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/investor-5045146-4200084.png" alt="Старше 55 лет">
            </div>
            <div class="option-text">
              <h3>Старше 55 лет</h3>
              <p>Предпенсионный и пенсионный возраст, сохранение средств</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[2].includes(4) }"></div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Шаг 3: Финансовые накопления -->
    <div v-if="currentStep === 3" class="onboarding-step tbank-slide-up">
      <div class="step-content">
        <h1>Есть ли у вас финансовые накопления?</h1>
        <p>Выберите наиболее подходящий вариант</p>
        
        <div class="options-column">
          <button @click="toggleOption(3, 1)" class="tbank-option" :class="{ 'option-selected': selectedOptions[3].includes(1) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/wallet-5045123-4200061.png" alt="Нет накоплений">
            </div>
            <div class="option-text">
              <h3>Нет накоплений</h3>
              <p>Пока не получается откладывать деньги</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[3].includes(1) }"></div>
          </button>
          
          <button @click="toggleOption(3, 2)" class="tbank-option" :class="{ 'option-selected': selectedOptions[3].includes(2) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/savings-5045089-4200027.png" alt="Небольшие накопления">
            </div>
            <div class="option-text">
              <h3>Небольшие накопления</h3>
              <p>Есть подушка безопасности на 1-3 месяца</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[3].includes(2) }"></div>
          </button>
          
          <button @click="toggleOption(3, 3)" class="tbank-option" :class="{ 'option-selected': selectedOptions[3].includes(3) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/money-5160610-4311080.png" alt="Средние накопления">
            </div>
            <div class="option-text">
              <h3>Средние накопления</h3>
              <p>Есть накопления на 4-6 месяцев жизни</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[3].includes(3) }"></div>
          </button>
          
          <button @click="toggleOption(3, 4)" class="tbank-option" :class="{ 'option-selected': selectedOptions[3].includes(4) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/money-savings-5740564-4805788.png" alt="Крупные накопления">
            </div>
            <div class="option-text">
              <h3>Крупные накопления</h3>
              <p>Есть значительные сбережения и/или инвестиции</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[3].includes(4) }"></div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Шаг 4: Цели обучения -->
    <div v-if="currentStep === 4" class="onboarding-step tbank-slide-up">
      <div class="step-content">
        <h1>Чему вы хотите научиться в первую очередь?</h1>
        <p>Выберите темы, которые вам наиболее интересны</p>
        
        <div class="options-grid">
          <button @click="toggleOption(4, 1)" class="tbank-option" :class="{ 'option-selected': selectedOptions[4].includes(1) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/budget-planning-5554869-4639076.png" alt="Планирование бюджета">
            </div>
            <div class="option-text">
              <h3>Планирование бюджета</h3>
              <p>Контроль доходов и расходов, экономия</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[4].includes(1) }"></div>
          </button>
          
          <button @click="toggleOption(4, 2)" class="tbank-option" :class="{ 'option-selected': selectedOptions[4].includes(2) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/loan-payment-5740548-4805772.png" alt="Избавление от долгов">
            </div>
            <div class="option-text">
              <h3>Избавление от долгов</h3>
              <p>Стратегии погашения кредитов и займов</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[4].includes(2) }"></div>
          </button>
          
          <button @click="toggleOption(4, 3)" class="tbank-option" :class="{ 'option-selected': selectedOptions[4].includes(3) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/investment-5045041-4199979.png" alt="Инвестирование">
            </div>
            <div class="option-text">
              <h3>Инвестирование</h3>
              <p>Фондовый рынок, активы, стратегии</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[4].includes(3) }"></div>
          </button>
          
          <button @click="toggleOption(4, 4)" class="tbank-option" :class="{ 'option-selected': selectedOptions[4].includes(4) }">
            <div class="option-icon">
              <img src="https://cdn3d.iconscout.com/3d/premium/thumb/passive-income-5045078-4200016.png" alt="Пассивный доход">
            </div>
            <div class="option-text">
              <h3>Пассивный доход</h3>
              <p>Создание источников пассивного дохода</p>
            </div>
            <div class="option-checkbox" :class="{ 'checkbox-selected': selectedOptions[4].includes(4) }"></div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Декоративные элементы -->
    <div class="decorative-3d-elements">
      <div class="coin coin-1"></div>
      <div class="coin coin-2"></div>
      <div class="chart-element"></div>
    </div>

    <!-- Навигационные кнопки -->
    <div class="navigation-buttons">
      <button 
        v-if="currentStep > 1" 
        @click="prevStep" 
        class="back-arrow">
        ←
      </button>
      <button 
        v-if="currentStep < totalSteps" 
        @click="nextStep" 
        class="tbank-button tbank-button--blue tbank-wide-button"
        :class="{ 'active': canProceedToNextStep }"
        :disabled="!canProceedToNextStep">
        Продолжить
      </button>
      <button 
        v-if="currentStep === totalSteps" 
        @click="finishOnboarding" 
        class="tbank-button tbank-button--blue tbank-wide-button"
        :class="{ 'active': canProceedToNextStep }"
        :disabled="!canProceedToNextStep">
        Начать обучение
        <span class="button-icon">→</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserOnboarding',
  data() {
    return {
      currentStep: 1,
      totalSteps: 4,
      styleInterval: null,
      selectedOptions: {
        1: [], // Финансовое будущее
        2: [], // Возрастная категория
        3: [], // Финансовые накопления
        4: []  // Цели обучения
      }
    }
  },
  computed: {
    progressPercent() {
      return (this.currentStep / this.totalSteps) * 100;
    },
    isTelegramApp() {
      return this.$telegram && this.$telegram.isRunningInTelegram();
    },
    canProceedToNextStep() {
      // Проверяем, выбран ли хотя бы один вариант для текущего шага
      return this.selectedOptions[this.currentStep].length > 0;
    }
  },
  methods: {
    toggleOption(step, optionId) {
      // Если выбор возрастной категории (шаг 2) или накоплений (шаг 3), то только один вариант
      if (step === 2 || step === 3) {
        this.selectedOptions[step] = [optionId];
      } else {
        // Для остальных шагов - множественный выбор
        const index = this.selectedOptions[step].indexOf(optionId);
        if (index > -1) {
          this.selectedOptions[step].splice(index, 1);
        } else {
          this.selectedOptions[step].push(optionId);
        }
      }
    },
    nextStep() {
      if (this.currentStep < this.totalSteps && this.canProceedToNextStep) {
        this.currentStep++;
      }
    },
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },
    finishOnboarding() {
      // Сохраняем выборы пользователя
      localStorage.setItem('userSelections', JSON.stringify(this.selectedOptions));
      localStorage.setItem('onboardingCompleted', 'true');
      this.$router.push('/home');
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
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.onboarding-container {
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 100vh;
  font-family: 'Roboto', sans-serif;
}

/* Кнопка назад в левом верхнем углу */
.back-arrow {
  position: fixed;
  top: 20px;
  left: 20px;
  width: 40px;
  height: 40px;
  border-radius: 5px;
  background-color: transparent;
  color: #4A90E2;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  z-index: 100;
  border: none;
  transition: all 0.3s ease;
}

.back-arrow:hover {
  color: #3A7BC8;
  transform: translateX(-3px);
}

/* Шаги онбординга */
.onboarding-step {
  max-width: 800px;
  margin: 0 auto;
}

.step-content {
  text-align: center;
}

.step-content h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--tbank-black);
  margin-top: 20px;
}

.step-content p {
  font-size: 16px;
  color: var(--tbank-mid-gray);
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Опции выбора */
.options-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 30px;
}

.options-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 30px;
}

.tbank-option {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 16px;
  background-color: white;
  border: 2px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  text-align: left;
}

.tbank-option:hover, .tbank-option:focus {
  border-color: var(--tbank-yellow);
  box-shadow: 0 8px 16px rgba(255, 221, 45, 0.15);
  transform: translateY(-4px);
}

.option-icon {
  width: 60px;
  height: 60px;
  margin-right: 16px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-icon img {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.option-text {
  flex: 1;
}

.option-text h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--tbank-black);
}

.option-text p {
  font-size: 14px;
  color: var(--tbank-mid-gray);
  margin: 0;
}

/* 3D Декоративные элементы */
.decorative-3d-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
}

.coin {
  position: absolute;
  width: 40px;
  height: 40px;
  background-image: url('https://cdn3d.iconscout.com/3d/premium/thumb/bitcoin-5044920-4199858.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.15;
  z-index: -1;
}

.coin-1 {
  top: 15%;
  right: 10%;
  animation: floatCoin 12s ease-in-out infinite;
}

.coin-2 {
  bottom: 20%;
  left: 8%;
  width: 30px;
  height: 30px;
  animation: floatCoin 10s ease-in-out infinite 1s;
}

.chart-element {
  position: absolute;
  bottom: 15%;
  right: 12%;
  width: 50px;
  height: 50px;
  background-image: url('https://cdn3d.iconscout.com/3d/premium/thumb/financial-growth-5044949-4199887.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.15;
  z-index: -1;
  animation: floatSlow 15s ease-in-out infinite;
}

/* Анимации */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
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
    transform: translateY(-10px) rotate(5deg);
  }
  50% {
    transform: translateY(0) rotate(10deg);
  }
  75% {
    transform: translateY(10px) rotate(5deg);
  }
}

/* Навигационные кнопки */
.navigation-buttons {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 10;
  background: linear-gradient(to top, rgba(255, 255, 255, 1) 60%, rgba(255, 255, 255, 0));
  padding-top: 40px;
}

.tbank-button--secondary {
  background-color: white;
  color: var(--tbank-black);
  border: 2px solid rgba(0, 0, 0, 0.1);
  position: absolute;
  left: 20px;
}

.tbank-button--secondary:hover {
  border-color: var(--tbank-yellow);
}

.tbank-button--primary {
  background-color: var(--tbank-yellow);
  font-weight: 600;
}

.tbank-button--transparent {
  background-color: #4A90E2;
  color: white;
  border: none;
  box-shadow: none;
  font-weight: 500;
}

.tbank-button--transparent:hover {
  background-color: #3A7BC8;
}

.tbank-button--yellow {
  background-color: var(--tbank-yellow, #FFDD2D);
  color: var(--tbank-black, #333333);
  border: none;
  box-shadow: 0 4px 12px rgba(255, 221, 45, 0.25);
  font-weight: 500;
}

.tbank-button--yellow:hover {
  background-color: var(--tbank-yellow-hover, #FFCC00);
}

.tbank-wide-button {
  width: 80%;
  max-width: 300px;
  border-radius: 16px;
  padding: 12px 20px;
}

.tbank-button {
  background-color: var(--tbank-yellow);
  color: var(--tbank-black);
  font-weight: 500;
}

.tbank-button:hover {
  background-color: var(--tbank-yellow-hover);
}

.button-icon {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.button-icon-left {
  margin-right: 8px;
  transition: transform 0.3s ease;
}

.tbank-button:hover .button-icon {
  transform: translateX(4px);
}

.tbank-button:hover .button-icon-left {
  transform: translateX(-4px);
}

/* Адаптивность */
@media (min-width: 768px) {
  .onboarding-container {
    padding: 40px;
  }
  
  .options-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .step-content h1 {
    font-size: 32px;
  }
  
  .step-content p {
    font-size: 18px;
  }

  .navigation-buttons {
    padding: 20px 40px;
    margin: 40px -40px 0;
  }
}

.tbank-button--blue {
  background-color: #4A90E2;
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.25);
  font-weight: 500;
}

.tbank-button--blue:hover {
  background-color: #3A7BC8;
}

/* Чекбоксы для опций */
.option-checkbox {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #e0e0e0;
  margin-left: 16px;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.checkbox-selected {
  border-color: #4A90E2;
  background-color: #4A90E2;
}

.checkbox-selected:after {
  content: '';
  position: absolute;
  width: 12px;
  height: 6px;
  border-left: 2px solid white;
  border-bottom: 2px solid white;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-45deg);
}

.option-selected {
  box-shadow: 0 8px 16px rgba(74, 144, 226, 0.15);
}

.tbank-button {
  opacity: 0.7;
  pointer-events: none;
}

.tbank-button.active {
  opacity: 1;
  pointer-events: auto;
}

.tbank-button--blue[disabled] {
  background-color: #a0bfe8;
  cursor: not-allowed;
}
</style> 