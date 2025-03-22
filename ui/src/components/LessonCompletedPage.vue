<template>
  <div class="min-h-screen bg-indigo-50 flex flex-col justify-center items-center p-6">
    <div class="w-full max-w-md bg-white rounded-lg shadow-sm border border-indigo-100 p-8 text-center">
      <!-- Анимированная иконка -->
      <div class="mb-6 relative">
        <div class="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto">
          <span class="text-indigo-500 text-3xl">🎉</span>
        </div>
        <div class="absolute -top-2 -right-2 w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center text-white font-bold">
          <span>+{{ xpEarned }}</span>
        </div>
      </div>
      
      <h1 class="text-2xl font-bold text-indigo-900 mb-3">Урок завершен!</h1>
      <p class="text-indigo-600 mb-6">Поздравляем! Вы успешно освоили урок "{{ lessonTitle }}"</p>
      
      <!-- Прогресс уровня -->
      <div class="mb-6">
        <div class="flex justify-between items-center mb-1">
          <span class="text-xs text-indigo-500 font-medium">Уровень {{ currentLevel }}</span>
          <span class="text-xs text-indigo-500 font-medium">{{ xpProgress }}/{{ xpNeeded }} XP</span>
        </div>
        <div class="relative pt-1">
          <div class="overflow-hidden h-2 text-xs flex rounded-full bg-indigo-50">
            <div :style="{ width: `${progressPercent}%` }" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500 transition-all duration-500"></div>
          </div>
        </div>
      </div>
      
      <!-- Достижения -->
      <div v-if="unlockedAchievement" class="mb-6 p-4 bg-indigo-50 rounded-lg border border-indigo-100">
        <div class="text-sm font-medium text-indigo-900 mb-1">🏆 Новое достижение!</div>
        <div class="flex items-center">
          <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-500 mr-3">
            <span class="text-xl">{{ unlockedAchievement.icon }}</span>
          </div>
          <div class="text-left">
            <div class="text-sm font-medium text-indigo-900">{{ unlockedAchievement.title }}</div>
            <div class="text-xs text-indigo-600">{{ unlockedAchievement.description }}</div>
          </div>
          <div class="ml-auto text-xs font-medium text-indigo-500">+{{ unlockedAchievement.xp }} XP</div>
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="space-y-3">
        <button 
          class="w-full bg-indigo-500 text-white px-4 py-3 rounded-md hover:bg-indigo-600 transition-colors font-medium"
          @click="goToNextLesson"
        >
          Продолжить обучение
        </button>
        
        <button 
          class="w-full bg-white text-indigo-500 border border-indigo-100 px-4 py-3 rounded-md hover:border-indigo-300 transition-colors"
          @click="goToHome"
        >
          Вернуться на главную
        </button>
      </div>
      
      <!-- Интересный факт -->
      <div class="mt-6 text-xs text-indigo-400 p-3 border-t border-indigo-50">
        <div class="font-medium mb-1">💡 Знаете ли вы?</div>
        <p>{{ randomFact }}</p>
      </div>
    </div>
    
    <!-- Заметка внизу страницы -->
    <div class="text-xs text-indigo-400 mt-6">
      Продолжайте обучение регулярно для лучших результатов!
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Предполагаем, что мы получаем ID урока из параметров маршрута
const lessonId = computed(() => route.params.id || 1);

// Моковые данные для демонстрации
const lessonTitle = ref('Основы личного бюджета');
const xpEarned = ref(50);
const currentLevel = ref(3);
const xpProgress = ref(350);
const xpNeeded = ref(800);
const unlockedAchievement = ref({
  icon: '📚',
  title: 'Финансовый ученик',
  description: 'Пройдите 5 уроков по финансовой грамотности',
  xp: 25
});

const facts = [
  'Регулярные инвестиции даже небольших сумм могут привести к значительному накоплению благодаря сложному проценту.',
  'Более 30% людей не имеют никаких сбережений на случай чрезвычайных ситуаций.',
  'Финансово грамотные люди в среднем накапливают на 25% больше средств к пенсии.',
  'Ведение бюджета помогает сократить импульсивные траты на 20-30%.',
  'Люди, которые ставят конкретные финансовые цели, достигают их в 2 раза чаще.'
];

const randomFact = ref('');

const progressPercent = computed(() => {
  return Math.min((xpProgress.value / xpNeeded.value) * 100, 100);
});

const goToNextLesson = () => {
  // Логика для перехода к следующему уроку
  router.push('/lessons');
};

const goToHome = () => {
  router.push('/');
};

onMounted(() => {
  // Выбираем случайный факт при монтировании компонента
  const randomIndex = Math.floor(Math.random() * facts.length);
  randomFact.value = facts[randomIndex];
  
  // В реальном приложении здесь бы загружались данные по API
  fetchLessonCompletionData(lessonId.value);
});

// Заглушка для будущей функции получения данных о завершенном уроке
const fetchLessonCompletionData = (id) => {
  console.log(`Загрузка данных для завершенного урока с ID: ${id}`);
  // Здесь будет реальный запрос к API
};
</script> 