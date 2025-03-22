<template>
  <div class="flex flex-col min-h-screen bg-black text-white">
    <!-- Верхняя панель -->
    <header class="px-5 py-4 flex items-center">
      <button 
        class="p-2 rounded-full"
        tabindex="0"
        aria-label="Вернуться назад"
        @click="handleBackClick"
        @keydown.enter="handleBackClick"
        @keydown.space="handleBackClick"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    </header>

    <!-- Загрузка -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="flex flex-col items-center">
        <svg class="animate-spin h-8 w-8 text-blue-500 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-sm text-gray-400">Загрузка урока...</p>
      </div>
    </div>

    <!-- Содержимое урока -->
    <div v-else class="flex-1 px-6 py-4">
      <!-- Заголовок урока -->
      <h1 class="text-2xl font-bold mb-8">{{ lesson?.title || 'Загрузка урока...' }}</h1>
      
      <!-- Карточка с суммой -->
      <div class="bg-gray-900 rounded-3xl p-6 mb-8">
        <div class="text-center">
          <div class="text-3xl font-bold mb-1">{{ currentStepContent.title }}</div>
          <div class="text-gray-400 text-sm">{{ currentStep + 1 }} из {{ lesson.steps.length }}</div>
        </div>
      </div>

      <!-- Содержимое текущего шага -->
      <div class="mb-8">
        <div class="prose prose-invert max-w-none text-gray-300">
          <div v-html="currentStepContent.content"></div>
        </div>
      </div>

      <!-- Интерактивные элементы текущего шага -->
      <div v-if="currentStepContent.hasQuiz" class="mb-10">
        <h3 class="text-base font-medium mb-4">{{ currentStepContent.quizQuestion }}</h3>
        
        <div class="space-y-3">
          <div 
            v-for="(option, index) in currentStepContent.quizOptions" 
            :key="index"
            class="border border-gray-800 rounded-2xl p-4 cursor-pointer transition-colors"
            :class="selectedOption === index ? 'border-blue-500 bg-gray-900' : 'hover:border-gray-700'"
            @click="selectedOption = index"
          >
            <div class="flex items-center">
              <div 
                class="w-5 h-5 rounded-full border flex items-center justify-center mr-3"
                :class="selectedOption === index ? 'border-blue-500 bg-blue-500' : 'border-gray-700'"
              >
                <svg v-if="selectedOption === index" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <span class="text-sm">{{ option }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Прогресс бар -->
      <div class="mb-8">
        <div class="h-1 bg-gray-800 rounded-full overflow-hidden">
          <div 
            class="h-1 bg-blue-500 rounded-full" 
            :style="{ width: `${((currentStep + 1) / lesson.steps.length) * 100}%` }"
          ></div>
        </div>
      </div>

      <!-- Управление навигацией -->
      <div class="flex justify-between">
        <button 
          class="w-14 h-14 rounded-full border border-gray-800 flex items-center justify-center"
          :disabled="currentStep === 0"
          :class="{ 'opacity-50 cursor-not-allowed': currentStep === 0 }"
          @click="handlePreviousStep"
          aria-label="Предыдущий шаг"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          class="w-14 h-14 rounded-full bg-blue-500 flex items-center justify-center"
          @click="!isLastStep ? handleNextStep() : completeLesson()"
          aria-label="Следующий шаг"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Реактивные свойства
const loading = ref(true);
const lesson = ref(null);
const currentStep = ref(0);
const currentStepContent = ref({});
const selectedOption = ref(null);

// Вычисляемые свойства
const isLastStep = computed(() => {
  if (!lesson.value) return false;
  return currentStep.value === lesson.value.steps.length - 1;
});

// Методы
const handleBackClick = () => {
  router.push({ name: 'Lessons' });
};

const handlePreviousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--;
    updateCurrentStepContent();
  }
};

const handleNextStep = () => {
  if (currentStepContent.value.hasQuiz && selectedOption.value === null) {
    // Если есть тест, и ответ не выбран
    alert('Пожалуйста, выберите ответ на вопрос');
    return;
  }
  
  if (!isLastStep.value) {
    currentStep.value++;
    updateCurrentStepContent();
    selectedOption.value = null; // Сбрасываем выбранный ответ
  }
};

const completeLesson = () => {
  if (currentStepContent.value.hasQuiz && selectedOption.value === null) {
    // Если есть тест, и ответ не выбран
    alert('Пожалуйста, выберите ответ на вопрос');
    return;
  }
  
  // Здесь будет логика для отправки статуса завершения на сервер
  // После успешного завершения переходим на страницу успеха
  router.push({ 
    name: 'LessonCompleted',
    params: { 
      id: route.params.id
    }
  });
};

const updateCurrentStepContent = () => {
  if (!lesson.value || !lesson.value.steps) return;
  
  currentStepContent.value = lesson.value.steps[currentStep.value];
};

const fetchLesson = async () => {
  try {
    loading.value = true;
    
    // Имитация загрузки данных с сервера
    setTimeout(() => {
      // Здесь будет запрос к API для получения данных урока
      lesson.value = {
        id: Number(route.params.id),
        title: 'Основы личного бюджета',
        description: 'Научитесь планировать и вести учет доходов и расходов',
        steps: [
          {
            title: 'Что такое личный бюджет?',
            content: `
              <p>Личный бюджет — это план управления вашими доходами и расходами за определенный период времени. Это инструмент, который помогает вам контролировать свои финансы и достигать финансовых целей.</p>
              <p>Основные компоненты личного бюджета:</p>
              <ul>
                <li>Доходы — все источники поступления денег</li>
                <li>Расходы — все направления трат денег</li>
                <li>Сбережения — часть доходов, которую вы откладываете</li>
              </ul>
            `,
            hasQuiz: false
          },
          {
            title: 'Почему важно вести бюджет?',
            content: `
              <p>Ведение бюджета дает вам множество преимуществ:</p>
              <ul>
                <li>Полный контроль над своими финансами</li>
                <li>Возможность выявить и сократить ненужные расходы</li>
                <li>Способность быстрее достигать финансовых целей</li>
                <li>Снижение стресса и беспокойства о деньгах</li>
                <li>Возможность создать финансовую подушку безопасности</li>
              </ul>
            `,
            hasQuiz: true,
            quizQuestion: 'Какое из следующих утверждений НЕ является преимуществом ведения личного бюджета?',
            quizOptions: [
              'Выявление лишних расходов',
              'Увеличение доходов без дополнительной работы',
              'Снижение финансового стресса',
              'Ускорение достижения финансовых целей'
            ]
          },
          {
            title: 'Как составить личный бюджет?',
            content: `
              <p>Для составления эффективного личного бюджета следуйте этим шагам:</p>
              <ol>
                <li>Определите период бюджетирования (неделя, месяц, год)</li>
                <li>Запишите все источники дохода за этот период</li>
                <li>Перечислите все ваши расходы, разбив их на категории</li>
                <li>Вычтите расходы из доходов</li>
                <li>Проанализируйте результат и скорректируйте при необходимости</li>
              </ol>
              <p>Важно быть честными с собой и записывать абсолютно все траты, даже мелкие.</p>
            `,
            hasQuiz: true,
            quizQuestion: 'Что является первым шагом при составлении личного бюджета?',
            quizOptions: [
              'Выбор периода бюджетирования',
              'Запись всех расходов',
              'Анализ предыдущих трат',
              'Определение финансовых целей'
            ]
          }
        ]
      };
      
      updateCurrentStepContent();
      loading.value = false;
    }, 800);
  } catch (error) {
    console.error('Ошибка при загрузке урока:', error);
    loading.value = false;
  }
};

// Наблюдатели
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchLesson();
  }
});

// Хуки жизненного цикла
onMounted(() => {
  fetchLesson();
});
</script> 