<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Шапка в стиле Альфа-Банка -->
    <header class="px-6 py-4 bg-white border-b border-neutral-200 flex items-center">
      <button 
        class="p-2 rounded-full hover:bg-neutral-100 transition-colors mr-2"
        @click="goBack"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-900" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
      </button>
      <h1 class="text-xl font-bold text-neutral-900">Профиль</h1>
    </header>

    <div class="flex-1 px-6 py-6 overflow-auto">
      <!-- Профиль пользователя -->
      <div class="bg-white rounded-xl border border-neutral-200 p-6 mb-6">
        <div class="flex items-center mb-4">
          <div class="w-16 h-16 rounded-full bg-alpha-100 flex items-center justify-center text-alpha-500 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-neutral-900">{{ profile.name }}</h2>
            <p class="text-neutral-500">{{ profile.email }}</p>
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div class="bg-neutral-50 p-4 rounded-lg">
            <h3 class="text-xs font-medium text-neutral-500 mb-1">Пройдено уроков</h3>
            <p class="text-2xl font-semibold text-neutral-900">{{ profile.lessonsCompleted }}</p>
          </div>
          <div class="bg-neutral-50 p-4 rounded-lg">
            <h3 class="text-xs font-medium text-neutral-500 mb-1">Уровень знаний</h3>
            <p class="text-2xl font-semibold text-neutral-900">{{ profile.level }}</p>
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <button class="bg-alpha-500 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-alpha-600 transition-colors">
            Редактировать профиль
          </button>
          <button class="border border-neutral-200 text-neutral-700 py-2 px-4 rounded-lg text-sm font-medium hover:bg-neutral-50 transition-colors">
            Настройки
          </button>
        </div>
      </div>

      <!-- Прогресс обучения -->
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-neutral-900 mb-4">Прогресс обучения</h3>
        <div class="bg-white rounded-xl border border-neutral-200 p-4">
          <div class="mb-4">
            <div class="flex justify-between mb-1">
              <span class="text-sm font-medium text-neutral-700">Общий прогресс</span>
              <span class="text-sm font-medium text-neutral-700">{{ profile.progress }}%</span>
            </div>
            <div class="h-2 w-full bg-neutral-100 rounded-full">
              <div class="h-2 bg-alpha-500 rounded-full" :style="{ width: `${profile.progress}%` }"></div>
            </div>
          </div>
          
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-sm font-medium text-neutral-700">Опыт</span>
              <span class="text-sm font-medium text-neutral-700">{{ profile.experience }} XP</span>
            </div>
            <div class="h-2 w-full bg-neutral-100 rounded-full">
              <div class="h-2 bg-amber-500 rounded-full" :style="{ width: `${(profile.experience / profile.maxExperience) * 100}%` }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Достижения -->
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-neutral-900 mb-4">Достижения</h3>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="(achievement, index) in profile.achievements" :key="index" 
               class="bg-white rounded-xl border border-neutral-200 p-4 flex flex-col items-center">
            <div :class="`h-12 w-12 rounded-full flex items-center justify-center mb-2 ${achievement.unlocked ? 'bg-alpha-100 text-alpha-500' : 'bg-neutral-100 text-neutral-400'}`">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                <path v-if="achievement.unlocked" fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                <path v-else fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <h4 class="text-sm font-medium text-neutral-900 text-center mb-1">{{ achievement.name }}</h4>
            <p class="text-xs text-neutral-500 text-center">{{ achievement.description }}</p>
          </div>
        </div>
      </div>

      <!-- История активности -->
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-neutral-900 mb-4">История активности</h3>
        <div class="bg-white rounded-xl border border-neutral-200 divide-y divide-neutral-100">
          <div v-for="(activity, index) in profile.activities" :key="index" class="p-4">
            <div class="flex items-center">
              <div class="h-8 w-8 rounded-full bg-alpha-100 text-alpha-500 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="flex-1">
                <h4 class="text-sm font-medium text-neutral-900">{{ activity.title }}</h4>
                <p class="text-xs text-neutral-500">{{ activity.date }}</p>
              </div>
              <span class="text-xs font-medium px-2 py-1 rounded-full" 
                    :class="activity.type === 'completed' ? 'bg-green-100 text-green-800' : 'bg-alpha-100 text-alpha-800'">
                {{ activity.type === 'completed' ? 'Завершен' : 'Начат' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Панель навигации в стиле Альфа-Банка -->
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
        <button class="flex flex-col items-center text-alpha-500" @click="goToProfile">
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

const profile = ref({
  name: 'Иван Иванов',
  email: 'ivan@example.com',
  lessonsCompleted: 5,
  level: 'Новичок',
  progress: 35,
  experience: 250,
  maxExperience: 500,
  achievements: [
    {
      name: 'Первый урок',
      description: 'Завершите свой первый урок',
      unlocked: true
    },
    {
      name: 'Бюджетный эксперт',
      description: 'Пройдите модуль по личному бюджету',
      unlocked: true
    },
    {
      name: 'Инвестор',
      description: 'Изучите основы инвестирования',
      unlocked: false
    },
    {
      name: 'Финансовый гуру',
      description: 'Пройдите все уроки в приложении',
      unlocked: false
    },
  ],
  activities: [
    {
      title: 'Урок "Основы личного бюджета"',
      date: 'Сегодня, 14:25',
      type: 'completed'
    },
    {
      title: 'Урок "Экономия и накопления"',
      date: 'Вчера, 18:30',
      type: 'completed'
    },
    {
      title: 'Урок "Кредиты и займы"',
      date: '10 марта, 12:15',
      type: 'started'
    }
  ]
});

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
  // Уже на странице профиля, поэтому ничего не делаем
};
</script> 