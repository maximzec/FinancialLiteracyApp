<template>
  <div class="min-h-screen bg-white flex flex-col">
    <div class="flex-1 flex flex-col px-6 pt-8 pb-4">
      <!-- Прогресс-бар -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-medium text-neutral-600">Шаг {{ currentStep }} из {{ totalSteps }}</span>
          <span class="text-sm font-medium text-alpha-500">{{ Math.round((currentStep / totalSteps) * 100) }}%</span>
        </div>
        <div class="h-2 bg-neutral-100 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-alpha-500 to-alpha-600 transition-all duration-300"
            :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
          ></div>
        </div>
      </div>

      <!-- Основной контент -->
      <div class="flex-1">
        <!-- Шаг 1: Приветствие -->
        <div v-if="currentStep === 1" class="text-center">
          <h2 class="text-2xl font-semibold text-neutral-900 mb-4">Добро пожаловать 👋</h2>
          <p class="text-neutral-600 mb-8">Давайте сделаем ваше обучение максимально эффективным</p>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors"
            @click="nextStep"
          >
            Начать
          </button>
        </div>

        <!-- Шаг 2: Финансовые цели -->
        <div v-if="currentStep === 2">
          <h2 class="text-xl font-semibold text-neutral-900 mb-6">Какие у вас финансовые цели?</h2>
          <div class="space-y-4">
            <div 
              v-for="goal in financialGoals" 
              :key="goal.id"
              class="p-4 border border-neutral-200 rounded-xl cursor-pointer transition-all"
              :class="{ 'border-alpha-500 bg-alpha-50': selectedGoals.includes(goal.id) }"
              @click="toggleGoal(goal.id)"
            >
              <div class="flex items-center">
                <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mr-3">
                  <component :is="goal.icon" class="h-5 w-5" />
                </div>
                <div>
                  <h3 class="font-medium text-neutral-900">{{ goal.title }}</h3>
                  <p class="text-sm text-neutral-600">{{ goal.description }}</p>
                </div>
              </div>
            </div>
          </div>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors mt-8"
            @click="nextStep"
            :disabled="selectedGoals.length === 0"
          >
            Продолжить
          </button>
        </div>

        <!-- Шаг 3: Уровень знаний -->
        <div v-if="currentStep === 3">
          <h2 class="text-xl font-semibold text-neutral-900 mb-6">Как бы вы оценили свой уровень финансовой грамотности?</h2>
          <div class="space-y-4">
            <div 
              v-for="level in knowledgeLevels" 
              :key="level.id"
              class="p-4 border border-neutral-200 rounded-xl cursor-pointer transition-all"
              :class="{ 'border-alpha-500 bg-alpha-50': selectedKnowledgeLevel === level.id }"
              @click="selectedKnowledgeLevel = level.id"
            >
              <div class="flex items-center">
                <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mr-3">
                  <component :is="level.icon" class="h-5 w-5" />
                </div>
                <div>
                  <h3 class="font-medium text-neutral-900">{{ level.title }}</h3>
                  <p class="text-sm text-neutral-600">{{ level.description }}</p>
                </div>
              </div>
            </div>
          </div>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors mt-8"
            @click="nextStep"
            :disabled="!selectedKnowledgeLevel"
          >
            Продолжить
          </button>
        </div>

        <!-- Шаг 4: Возраст -->
        <div v-if="currentStep === 4">
          <h2 class="text-xl font-semibold text-neutral-900 mb-6">Сколько вам лет?</h2>
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">Ваш возраст</label>
              <div class="relative">
                <input 
                  type="number" 
                  v-model="userAge"
                  min="18"
                  max="100"
                  class="w-full px-4 py-3 border border-neutral-200 rounded-xl focus:border-alpha-500 focus:ring-1 focus:ring-alpha-500"
                  placeholder="Введите ваш возраст"
                >
              </div>
            </div>
          </div>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors mt-8"
            @click="nextStep"
            :disabled="!userAge || userAge < 18 || userAge > 100"
          >
            Продолжить
          </button>
        </div>

        <!-- Шаг 5: Финансовое положение -->
        <div v-if="currentStep === 5">
          <h2 class="text-xl font-semibold text-neutral-900 mb-6">Расскажите о своем финансовом положении</h2>
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">Ежемесячный доход</label>
              <div class="relative">
                <input 
                  type="number" 
                  v-model="financialInfo.income"
                  class="w-full px-4 py-3 border border-neutral-200 rounded-xl focus:border-alpha-500 focus:ring-1 focus:ring-alpha-500"
                  placeholder="Введите сумму"
                >
                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-500">₽</span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">Ежемесячные расходы</label>
              <div class="relative">
                <input 
                  type="number" 
                  v-model="financialInfo.expenses"
                  class="w-full px-4 py-3 border border-neutral-200 rounded-xl focus:border-alpha-500 focus:ring-1 focus:ring-alpha-500"
                  placeholder="Введите сумму"
                >
                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-500">₽</span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-neutral-700 mb-2">Сбережения</label>
              <div class="relative">
                <input 
                  type="number" 
                  v-model="financialInfo.savings"
                  class="w-full px-4 py-3 border border-neutral-200 rounded-xl focus:border-alpha-500 focus:ring-1 focus:ring-alpha-500"
                  placeholder="Введите сумму"
                >
                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-500">₽</span>
              </div>
            </div>
          </div>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors mt-8"
            @click="nextStep"
            :disabled="!isFinancialInfoValid"
          >
            Продолжить
          </button>
        </div>

        <!-- Шаг 6: Инвестиционные предпочтения -->
        <div v-if="currentStep === 6">
          <h2 class="text-xl font-semibold text-neutral-900 mb-6">Какие инвестиционные инструменты вас интересуют?</h2>
          <div class="space-y-4">
            <div 
              v-for="instrument in investmentInstruments" 
              :key="instrument.id"
              class="p-4 border border-neutral-200 rounded-xl cursor-pointer transition-all"
              :class="{ 'border-alpha-500 bg-alpha-50': selectedInstruments.includes(instrument.id) }"
              @click="toggleInstrument(instrument.id)"
            >
              <div class="flex items-center">
                <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mr-3">
                  <component :is="instrument.icon" class="h-5 w-5" />
                </div>
                <div>
                  <h3 class="font-medium text-neutral-900">{{ instrument.title }}</h3>
                  <p class="text-sm text-neutral-600">{{ instrument.description }}</p>
                </div>
              </div>
            </div>
          </div>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors mt-8"
            @click="nextStep"
            :disabled="selectedInstruments.length === 0"
          >
            Продолжить
          </button>
        </div>

        <!-- Шаг 7: Завершение -->
        <div v-if="currentStep === 7" class="text-center">
          <div class="mb-8">
            <div class="h-20 w-20 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <h2 class="text-2xl font-semibold text-neutral-900 mb-4">Отлично! 🎉</h2>
            <p class="text-neutral-600">Мы подготовили персонализированный план обучения для вас</p>
          </div>
          <button 
            class="w-full bg-alpha-500 text-white py-4 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors"
            @click="completeOnboarding"
          >
            Начать обучение
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const currentStep = ref(1);
const totalSteps = 7;

// Финансовые цели
const financialGoals = [
  {
    id: 1,
    title: 'Создание подушки безопасности',
    description: 'Накопить резервный фонд на случай непредвиденных ситуаций',
    icon: 'svg',
    iconPath: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  },
  {
    id: 2,
    title: 'Инвестиции',
    description: 'Научиться инвестировать и приумножать капитал',
    icon: 'svg',
    iconPath: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6'
  },
  {
    id: 3,
    title: 'Покупка жилья',
    description: 'Подготовиться к приобретению собственного жилья',
    icon: 'svg',
    iconPath: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6'
  }
];

// Уровни знаний
const knowledgeLevels = [
  {
    id: 1,
    title: 'Начинающий',
    description: 'Имею базовые представления о финансах',
    icon: 'svg',
    iconPath: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'
  },
  {
    id: 2,
    title: 'Средний',
    description: 'Понимаю основные финансовые концепции',
    icon: 'svg',
    iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
  },
  {
    id: 3,
    title: 'Продвинутый',
    description: 'Имею опыт инвестирования и управления финансами',
    icon: 'svg',
    iconPath: 'M13 10V3L4 14h7v7l9-11h-7z'
  }
];

// Инвестиционные инструменты
const investmentInstruments = [
  {
    id: 1,
    title: 'Акции',
    description: 'Инвестиции в доли компаний',
    icon: 'svg',
    iconPath: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  },
  {
    id: 2,
    title: 'Облигации',
    description: 'Долговые ценные бумаги',
    icon: 'svg',
    iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
  },
  {
    id: 3,
    title: 'Криптовалюты',
    description: 'Цифровые активы',
    icon: 'svg',
    iconPath: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
];

// Состояние формы
const selectedGoals = ref([]);
const selectedKnowledgeLevel = ref(null);
const selectedInstruments = ref([]);
const financialInfo = ref({
  income: '',
  expenses: '',
  savings: ''
});

// Добавляем возраст в состояние формы
const userAge = ref('');

// Валидация финансовой информации
const isFinancialInfoValid = computed(() => {
  return financialInfo.value.income && 
         financialInfo.value.expenses && 
         financialInfo.value.savings;
});

// Методы
const nextStep = () => {
  if (currentStep.value < totalSteps) {
    currentStep.value++;
  }
};

const toggleGoal = (goalId) => {
  const index = selectedGoals.value.indexOf(goalId);
  if (index === -1) {
    selectedGoals.value.push(goalId);
  } else {
    selectedGoals.value.splice(index, 1);
  }
};

const toggleInstrument = (instrumentId) => {
  const index = selectedInstruments.value.indexOf(instrumentId);
  if (index === -1) {
    selectedInstruments.value.push(instrumentId);
  } else {
    selectedInstruments.value.splice(index, 1);
  }
};

const completeOnboarding = () => {
  // Здесь будет логика сохранения данных пользователя
  router.push('/');
};
</script>

<style scoped>
/* Анимации для переходов между шагами */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Стили для прогресс-бара */
.progress-bar {
  transition: width 0.3s ease;
}

/* Стили для кнопок */
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Стили для карточек */
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style> 