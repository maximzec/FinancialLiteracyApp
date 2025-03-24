<template>
  <div class="min-h-screen bg-white flex flex-col">
    <div class="flex-1 flex flex-col px-6 pt-8 pb-4">
      <!-- Заголовок урока -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-semibold text-neutral-900">Основы инвестирования</h2>
          <div class="flex items-center space-x-2">
            <span class="text-sm font-medium text-neutral-600">Урок 3 из 10</span>
            <div class="h-2 w-24 bg-neutral-100 rounded-full overflow-hidden">
              <div class="h-full bg-alpha-500" style="width: 30%"></div>
            </div>
          </div>
        </div>
        <p class="text-neutral-600">Научитесь разбираться в основных инвестиционных инструментах и стратегиях</p>
      </div>

      <!-- Основной контент -->
      <div class="flex-1">
        <!-- Видео или изображение -->
        <div class="aspect-video bg-neutral-100 rounded-xl mb-8 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-neutral-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
        </div>

        <!-- Текст урока -->
        <div class="prose max-w-none mb-8">
          <h3>Что такое инвестиции?</h3>
          <p>Инвестиции — это вложение денег с целью получения дохода в будущем. Основные принципы инвестирования:</p>
          <ul>
            <li>Диверсификация — распределение средств между разными активами</li>
            <li>Долгосрочность — инвестиции работают лучше всего на длительном горизонте</li>
            <li>Регулярность — постоянные инвестиции помогают сгладить риски</li>
          </ul>

          <h3>Основные инвестиционные инструменты</h3>
          <p>Существует множество способов инвестирования. Рассмотрим основные:</p>
          
          <div class="bg-neutral-50 p-4 rounded-xl mb-4">
            <h4 class="text-lg font-medium text-neutral-900 mb-2">Акции</h4>
            <p class="text-neutral-600">Доля в собственности компании. При покупке акций вы становитесь совладельцем бизнеса и можете получать:</p>
            <ul>
              <li>Дивиденды — часть прибыли компании</li>
              <li>Доход от роста стоимости акций</li>
            </ul>
          </div>

          <div class="bg-neutral-50 p-4 rounded-xl mb-4">
            <h4 class="text-lg font-medium text-neutral-900 mb-2">Облигации</h4>
            <p class="text-neutral-600">Долговые ценные бумаги. При покупке облигаций вы даете деньги в долг:</p>
            <ul>
              <li>Государству (гос. облигации)</li>
              <li>Компаниям (корпоративные облигации)</li>
              <li>Получаете фиксированный доход</li>
            </ul>
          </div>

          <div class="bg-neutral-50 p-4 rounded-xl">
            <h4 class="text-lg font-medium text-neutral-900 mb-2">ETF</h4>
            <p class="text-neutral-600">Биржевые инвестиционные фонды. Позволяют инвестировать в:</p>
            <ul>
              <li>Индексы (например, S&P 500)</li>
              <li>Отрасли экономики</li>
              <li>Страны и регионы</li>
            </ul>
          </div>
        </div>

        <!-- Тест -->
        <div class="bg-neutral-50 rounded-xl p-6 mb-8">
          <h3 class="text-lg font-medium text-neutral-900 mb-4">Проверьте свои знания</h3>
          <p class="text-neutral-600 mb-4">Ответьте на вопросы, чтобы закрепить материал</p>
          <button 
            class="w-full bg-alpha-500 text-white py-3 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors"
            @click="startTest"
          >
            Начать тест
          </button>
        </div>

        <!-- Навигация по урокам -->
        <div class="flex items-center justify-between">
          <button 
            class="flex items-center text-neutral-600 hover:text-alpha-500 transition-colors"
            :disabled="!hasPreviousLesson"
            @click="goToPreviousLesson"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            Предыдущий урок
          </button>
          <button 
            class="flex items-center text-neutral-600 hover:text-alpha-500 transition-colors"
            :disabled="!hasNextLesson"
            @click="goToNextLesson"
          >
            Следующий урок
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
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
const currentLesson = ref(3);
const totalLessons = ref(10);

const hasPreviousLesson = computed(() => currentLesson.value > 1);
const hasNextLesson = computed(() => currentLesson.value < totalLessons.value);

const startTest = () => {
  // Здесь будет логика начала теста
  console.log('Начало теста');
};

const goToPreviousLesson = () => {
  if (hasPreviousLesson.value) {
    currentLesson.value--;
    // Здесь будет логика загрузки предыдущего урока
  }
};

const goToNextLesson = () => {
  if (hasNextLesson.value) {
    currentLesson.value++;
    // Здесь будет логика загрузки следующего урока
  }
};
</script>

<style scoped>
.prose {
  max-width: 65ch;
}

.prose h3 {
  @apply text-xl font-semibold text-neutral-900 mb-4;
}

.prose p {
  @apply text-neutral-600 mb-4;
}

.prose ul {
  @apply list-disc list-inside text-neutral-600 mb-4;
}

.prose li {
  @apply mb-2;
}

button:disabled {
  @apply opacity-50 cursor-not-allowed;
}
</style> 