<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Шапка в стиле Альфа-Банка -->
    <header class="px-6 py-4 bg-white border-b border-neutral-200 flex items-center">
      <button 
        class="p-2 rounded-full hover:bg-neutral-100 transition-colors mr-2"
        @click="handleBackClick"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-900" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
      </button>
      <h1 class="text-xl font-bold text-neutral-900">{{ lesson?.title || 'Загрузка урока...' }}</h1>
    </header>

    <!-- Загрузка -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="flex flex-col items-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-alpha-500 mb-2"></div>
        <p class="text-sm text-neutral-500">Загрузка урока...</p>
      </div>
    </div>

    <!-- Содержимое урока -->
    <div v-else class="flex-1 px-6 py-4 overflow-auto">
      <!-- Прогресс урока -->
      <div class="mb-6 bg-white rounded-xl border border-neutral-200 p-5">
        <div class="flex justify-between mb-4">
          <div>
            <h3 class="text-sm font-medium text-neutral-500 mb-1">Прогресс урока</h3>
            <p class="text-xl font-semibold text-neutral-900">{{ currentStep + 1 }} из {{ lesson.steps.length }}</p>
          </div>
          <div class="h-12 w-12 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
        <div class="h-2 w-full bg-neutral-100 rounded-full">
          <div 
            class="h-2 bg-alpha-500 rounded-full transition-all duration-300" 
            :style="{ width: `${((currentStep + 1) / lesson.steps.length) * 100}%` }"
          ></div>
        </div>
      </div>

      <!-- Содержимое текущего шага -->
      <div class="bg-white rounded-xl border border-neutral-200 p-5 mb-6">
        <h2 class="text-lg font-semibold text-neutral-900 mb-4">{{ currentStepContent.title }}</h2>
        <div class="prose prose-neutral max-w-none text-neutral-600">
          <div v-html="currentStepContent.content"></div>
        </div>
      </div>

      <!-- Интерактивные элементы текущего шага -->
      <div v-if="currentStepContent.hasQuiz" class="bg-white rounded-xl border border-neutral-200 p-5 mb-6">
        <h3 class="text-base font-medium text-neutral-900 mb-4">{{ currentStepContent.quizQuestion }}</h3>
        
        <div class="space-y-3">
          <div 
            v-for="(option, index) in currentStepContent.quizOptions" 
            :key="index"
            class="border rounded-xl p-4 cursor-pointer transition-colors"
            :class="[
              selectedOption === index 
                ? 'border-alpha-500 bg-alpha-50' 
                : 'border-neutral-200 hover:border-alpha-300'
            ]"
            @click="selectedOption = index"
          >
            <div class="flex items-center">
              <div 
                class="w-5 h-5 rounded-full border flex items-center justify-center mr-3"
                :class="[
                  selectedOption === index 
                    ? 'border-alpha-500 bg-alpha-500' 
                    : 'border-neutral-300'
                ]"
              >
                <svg v-if="selectedOption === index" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <span class="text-sm text-neutral-700">{{ option }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Управление навигацией -->
      <div class="flex justify-between mt-6">
        <button 
          class="w-14 h-14 rounded-full border border-neutral-200 flex items-center justify-center hover:border-alpha-300 transition-colors"
          :disabled="currentStep === 0"
          :class="{ 'opacity-50 cursor-not-allowed': currentStep === 0 }"
          @click="handlePreviousStep"
          aria-label="Предыдущий шаг"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-700" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          class="w-14 h-14 rounded-full bg-alpha-500 flex items-center justify-center hover:bg-alpha-600 transition-colors"
          @click="!isLastStep ? handleNextStep() : completeLesson()"
          aria-label="Следующий шаг"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
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
import { LessonService } from '../services/LessonService';

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

const handleNextStep = async () => {
  if (currentStepContent.value.hasQuiz && selectedOption.value === null) {
    // Если есть тест, и ответ не выбран
    alert('Пожалуйста, выберите ответ на вопрос');
    return;
  }
  
  if (!isLastStep.value) {
    // Если есть тест, отправляем ответ
    if (currentStepContent.value.hasQuiz) {
      await LessonService.submitQuizAnswer(lesson.value.id, currentStep.value, selectedOption.value);
    }
    
    currentStep.value++;
    updateCurrentStepContent();
    selectedOption.value = null; // Сбрасываем выбранный ответ
  }
};

const completeLesson = async () => {
  if (currentStepContent.value.hasQuiz && selectedOption.value === null) {
    // Если есть тест, и ответ не выбран
    alert('Пожалуйста, выберите ответ на вопрос');
    return;
  }
  
  // Отправляем ответ на последний тест, если он есть
  if (currentStepContent.value.hasQuiz) {
    await LessonService.submitQuizAnswer(lesson.value.id, currentStep.value, selectedOption.value);
  }
  
  // Отмечаем урок как завершенный
  await LessonService.completeLesson(lesson.value.id);
  
  // Переходим на страницу успеха
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
    lesson.value = await LessonService.getLesson(Number(route.params.id));
    updateCurrentStepContent();
  } catch (error) {
    console.error('Ошибка при загрузке урока:', error);
    alert('Произошла ошибка при загрузке урока. Пожалуйста, попробуйте позже.');
  } finally {
    loading.value = false;
  }
};

// Загружаем урок при монтировании компонента
onMounted(() => {
  fetchLesson();
});

// Следим за изменением ID урока в URL
watch(() => route.params.id, () => {
  fetchLesson();
});
</script> 