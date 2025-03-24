<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Шапка в стиле Альфа-Банка -->
    <header class="px-6 py-4 bg-white border-b border-neutral-200 flex items-center justify-between">
      <div class="flex items-center">
        <button 
          class="p-2 rounded-full hover:bg-neutral-100 transition-colors mr-2"
          @click="goBack"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-900" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
        </button>
        <h1 class="text-xl font-bold text-neutral-900">Уроки</h1>
      </div>
      <button class="p-2 rounded-full hover:bg-neutral-100 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-900" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
        </svg>
      </button>
    </header>
    
    <div class="flex-1 px-6 py-4 overflow-auto">
      <!-- Фильтры категорий -->
      <div class="mb-6 overflow-x-auto">
        <div class="flex space-x-2 pb-2">
          <button 
            v-for="category in categories" 
            :key="category.id"
            @click="selectCategory(category.id)"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors',
              selectedCategory === category.id ? 
                'bg-alpha-500 text-white' : 
                'bg-white border border-neutral-200 text-neutral-700 hover:bg-neutral-50'
            ]"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
      
      <!-- Прогресс обучения -->
      <div class="mb-6 bg-white rounded-xl border border-neutral-200 p-5">
        <div class="flex justify-between mb-4">
          <div>
            <h3 class="text-sm font-medium text-neutral-500 mb-1">Общий прогресс обучения</h3>
            <p class="text-xl font-semibold text-neutral-900">{{ overallProgress }}%</p>
          </div>
          <div class="h-12 w-12 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
        <div class="h-2 w-full bg-neutral-100 rounded-full">
          <div class="h-2 bg-alpha-500 rounded-full" :style="{ width: `${overallProgress}%` }"></div>
        </div>
      </div>
      
      <!-- Список уроков -->
      <h3 class="text-lg font-semibold text-neutral-900 mb-4">Все уроки</h3>
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-alpha-500"></div>
      </div>
      <div v-else class="space-y-4">
        <div 
          v-for="(lesson, index) in filteredLessons" 
          :key="lesson.id"
          class="bg-white rounded-xl border border-neutral-200 p-5 cursor-pointer hover:border-alpha-300 transition-colors"
          @click="openLesson(lesson)"
        >
          <div class="flex justify-between mb-3">
            <div class="flex items-center">
              <div :class="[
                'h-10 w-10 rounded-full flex items-center justify-center mr-3',
                lesson.completed ? 'bg-green-100 text-green-600' : 'bg-alpha-100 text-alpha-500'
              ]">
                <svg v-if="lesson.completed" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-else class="text-sm font-medium">{{ index + 1 }}</span>
              </div>
              <div>
                <h4 class="text-base font-medium text-neutral-900">{{ lesson.title }}</h4>
                <p class="text-sm text-neutral-500">{{ lesson.duration }} мин • {{ lesson.category }}</p>
              </div>
            </div>
            <div class="flex items-center">
              <div v-if="lesson.progress > 0 && !lesson.completed" class="mr-4">
                <span class="text-xs font-medium text-neutral-500">{{ lesson.progress }}%</span>
              </div>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-neutral-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          <p class="text-sm text-neutral-600 mb-3">{{ lesson.description }}</p>
          <div v-if="lesson.progress > 0 && !lesson.completed" class="h-1.5 w-full bg-neutral-100 rounded-full">
            <div class="h-1.5 bg-alpha-500 rounded-full" :style="{ width: `${lesson.progress}%` }"></div>
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
        <button class="flex flex-col items-center text-alpha-500" @click="goToLessons">
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { LessonService } from '../services/LessonService';

const router = useRouter();

// Категории уроков
const categories = ref([
  { id: 'all', name: 'Все' },
  { id: 'budget', name: 'Бюджет' },
  { id: 'savings', name: 'Накопления' },
  { id: 'investing', name: 'Инвестиции' },
  { id: 'credit', name: 'Кредиты' },
  { id: 'taxes', name: 'Налоги' }
]);

// Выбранная категория (по умолчанию - все)
const selectedCategory = ref('all');

// Данные уроков
const lessons = ref([]);
const loading = ref(true);

// Загрузка уроков
const fetchLessons = async () => {
  try {
    loading.value = true;
    const fetchedLessons = await LessonService.getLessons();
    lessons.value = fetchedLessons.map(lesson => ({
      ...lesson,
      category: getLessonCategory(lesson.id),
      duration: calculateLessonDuration(lesson),
      progress: 0, // Здесь можно добавить логику расчета прогресса
      completed: false // Здесь можно добавить логику проверки завершения
    }));
  } catch (error) {
    console.error('Ошибка при загрузке уроков:', error);
  } finally {
    loading.value = false;
  }
};

// Определение категории урока по ID
const getLessonCategory = (lessonId) => {
  const categoryMap = {
    1: 'Бюджет',
    2: 'Инвестиции',
    3: 'Накопления',
    4: 'Кредиты',
    5: 'Налоги',
    6: 'Накопления'
  };
  return categoryMap[lessonId] || 'Другое';
};

// Расчет длительности урока
const calculateLessonDuration = (lesson) => {
  return lesson.steps.length * 5; // Примерная длительность: 5 минут на шаг
};

// Отфильтрованные уроки
const filteredLessons = computed(() => {
  if (selectedCategory.value === 'all') {
    return lessons.value;
  }
  
  return lessons.value.filter(lesson => {
    const categoryName = categories.value.find(c => c.id === selectedCategory.value)?.name;
    return lesson.category === categoryName;
  });
});

// Общий прогресс обучения
const overallProgress = computed(() => {
  const totalLessons = lessons.value.length;
  if (totalLessons === 0) return 0;
  
  const completedLessons = lessons.value.filter(l => l.completed).length;
  const inProgressLessons = lessons.value.filter(l => !l.completed && l.progress > 0);
  const progressSum = inProgressLessons.reduce((sum, lesson) => sum + lesson.progress, 0);
  
  return Math.round((completedLessons * 100 + progressSum) / totalLessons);
});

// Действия
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId;
};

const openLesson = (lesson) => {
  router.push(`/lesson/${lesson.id}`);
};

const goBack = () => {
  router.go(-1);
};

const goToHome = () => {
  router.push('/');
};

const goToLessons = () => {
  // Уже на странице уроков, поэтому ничего не делаем
};

const goToProfile = () => {
  router.push('/profile');
};

// Загружаем уроки при монтировании компонента
onMounted(() => {
  fetchLessons();
});
</script> 