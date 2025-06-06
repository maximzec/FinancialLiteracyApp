<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Шапка -->
    <header class="px-6 py-4 bg-white border-b border-neutral-200 flex items-center">
      <button 
        class="p-2 rounded-full hover:bg-neutral-100 transition-colors mr-2"
        @click="goBack"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-900" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
      </button>
      <h1 class="text-xl font-bold text-neutral-900">Индивидуальный план</h1>
    </header>

    <div class="flex-1 px-6 py-6 overflow-auto">
      <!-- Прогресс обучения -->
      <div class="mb-6">
        <h2 class="text-lg font-medium text-neutral-900 mb-4">Ваш прогресс обучения</h2>
        <div class="p-5 bg-neutral-50 rounded-xl border border-neutral-200">
          <div class="flex justify-between items-center mb-3">
            <div>
              <h3 class="text-sm font-medium text-neutral-900">Общий прогресс</h3>
              <p class="text-sm text-neutral-600">4 из 12 уроков пройдено</p>
            </div>
            <div class="bg-alpha-500 text-white h-10 w-10 rounded-full flex items-center justify-center text-sm font-medium">
              33%
            </div>
          </div>
          <div class="h-2 w-full bg-neutral-200 rounded-full overflow-hidden">
            <div class="h-2 bg-alpha-500 rounded-full" style="width: 33%"></div>
          </div>
        </div>
      </div>

      <!-- Рекомендуемые следующие шаги -->
      <div class="mb-6">
        <h2 class="text-lg font-medium text-neutral-900 mb-4">Рекомендуемые шаги</h2>
        <div class="space-y-4">
          <div 
            v-for="(step, index) in recommendedSteps" 
            :key="index"
            class="p-4 bg-white border border-neutral-200 rounded-xl hover:border-alpha-300 transition-colors cursor-pointer shadow-sm"
            @click="handleStepClick(step)"
          >
            <div class="flex items-start">
              <div class="h-8 w-8 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mr-3 mt-1">
                <span class="text-sm font-medium">{{ index + 1 }}</span>
              </div>
              <div>
                <h3 class="text-base font-medium text-neutral-900 mb-1">{{ step.title }}</h3>
                <p class="text-sm text-neutral-600 mb-2">{{ step.description }}</p>
                <div class="flex items-center">
                  <span class="text-xs text-neutral-500 mr-2">{{ step.type }}</span>
                  <span class="text-xs text-neutral-500">{{ step.duration }} мин</span>
                  <div class="ml-auto flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-alpha-500 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- План на месяц -->
      <div class="mb-6">
        <h2 class="text-lg font-medium text-neutral-900 mb-4">Ваш план на месяц</h2>
        <div class="bg-white border border-neutral-200 rounded-xl p-5">
          <div class="mb-4">
            <h3 class="text-base font-medium text-neutral-900 mb-2">Цели обучения</h3>
            <ul class="space-y-2">
              <li v-for="(goal, index) in monthlyGoals" :key="index" class="flex items-start">
                <div class="h-5 w-5 rounded-full border border-alpha-500 flex items-center justify-center mr-2 mt-0.5">
                  <svg v-if="goal.completed" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-alpha-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span class="text-sm" :class="goal.completed ? 'text-neutral-500 line-through' : 'text-neutral-900'">{{ goal.text }}</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-base font-medium text-neutral-900 mb-2">Награда за выполнение</h3>
            <div class="flex items-center bg-neutral-50 p-3 rounded-lg">
              <div class="h-8 w-8 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <div class="flex items-center">
                  <span class="text-sm font-medium text-neutral-900 mr-2">50</span>
                  <div class="px-2 py-0.5 rounded-lg bg-blue-100 text-blue-600 text-xs font-medium flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-0.5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd" />
                    </svg>
                    коины
                  </div>
                </div>
                <p class="text-xs text-neutral-600">Бонус за выполнение всех целей</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Панель навигации -->
    <nav class="border-t border-neutral-200 bg-white py-3 px-6">
      <div class="flex justify-around">
        <button class="flex flex-col items-center text-neutral-500" @click="goToHome">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span class="text-xs mt-1">Главная</span>
        </button>
        <button class="flex flex-col items-center text-neutral-500" @click="goToLessons">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span class="text-xs mt-1">Уроки</span>
        </button>
        <button class="flex flex-col items-center text-neutral-500" @click="goToProfile">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="text-xs mt-1">Профиль</span>
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const recommendedSteps = ref([
  {
    id: 1,
    title: "Основы инвестирования",
    description: "Изучите основные принципы инвестирования и различные типы инвестиционных инструментов",
    type: "Урок",
    duration: 15
  },
  {
    id: 2,
    title: "Практика: составление бюджета",
    description: "Практическое задание по составлению личного или семейного бюджета",
    type: "Практика",
    duration: 20
  },
  {
    id: 3,
    title: "Финансовые риски",
    description: "Узнайте о различных финансовых рисках и методах их минимизации",
    type: "Урок",
    duration: 12
  }
]);

const monthlyGoals = ref([
  {
    text: "Пройти 3 урока по основам инвестирования",
    completed: true
  },
  {
    text: "Составить личный финансовый план",
    completed: false
  },
  {
    text: "Пройти тест по финансовым рискам",
    completed: false
  },
  {
    text: "Создать первый инвестиционный портфель",
    completed: false
  }
]);

const goBack = () => {
  router.go(-1);
};

const goToHome = () => {
  router.push('/');
};

const goToLessons = () => {
  router.push('/lessons');
};

const goToProfile = () => {
  router.push('/profile');
};

const handleStepClick = (step) => {
  if (step.type === "Урок") {
    router.push(`/lesson/${step.id}`);
  } else {
    router.push(`/practice/${step.id}`);
  }
};
</script> 