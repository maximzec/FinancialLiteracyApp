<template>
  <div class="min-h-screen bg-white flex flex-col">
    <div class="flex-1 flex flex-col px-6 pt-8 pb-4">
      <div class="mb-6">
        <h2 class="text-2xl font-semibold text-neutral-900 mb-1">Привет 👋</h2>
        <p class="text-neutral-600">Изучайте финансы без стресса</p>
      </div>
      
      <!-- Секция с балансом знаний -->
      <div class="mb-6">
        <!-- Карточка коинов в стиле Альфа-Банка -->
        <div class="p-6 rounded-xl mb-2 relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-purple-700 h-48">
          <!-- Декоративные элементы с анимацией -->
          <div class="absolute bottom-[-10%] right-[-5%] w-32 h-32 rounded-full bg-red-500 opacity-20 animate-pulse-slow"></div>
          <div class="absolute top-[-10%] left-[-5%] w-40 h-40 rounded-full bg-yellow-300 opacity-10 animate-pulse-medium"></div>
          <div class="absolute bottom-[-30%] left-[20%] w-60 h-60 rounded-full bg-green-400 opacity-10 animate-float-slow"></div>
          
          <!-- Основное содержимое -->
          <div class="flex flex-col h-full justify-center items-center relative z-10">
            <div class="text-center mb-5">
              <h3 class="text-base font-medium text-white/80 mb-1">У вас</h3>
              <p class="text-5xl font-bold text-white">25 коинов</p>
            </div>
            
            <button 
              class="bg-white/20 hover:bg-white/30 transition-colors text-white py-2 px-6 rounded-lg text-sm font-medium flex items-center backdrop-blur-sm"
              @click="handleCoinShopClick"
            >
              В магазин
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <div 
          class="p-5 border border-neutral-200 rounded-xl shadow-sm hover:border-alpha-300 transition-colors cursor-pointer bg-white"
          tabindex="0"
          aria-label="Перейти к текущему уроку"
          @click="handleLessonClick"
          @keydown.enter="handleLessonClick"
          @keydown.space="handleLessonClick"
        >
          <div class="flex items-center mb-3">
            <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
              </svg>
            </div>
            <div>
              <h3 class="text-base font-medium text-neutral-900">{{ currentLesson.title }}</h3>
              <p class="text-sm text-neutral-500">{{ currentLesson.description }}</p>
            </div>
          </div>
          <button class="w-full bg-alpha-500 text-white py-3 rounded-lg text-sm font-medium hover:bg-alpha-600 transition-colors">
            Продолжить обучение
          </button>
        </div>
      </div>

      <!-- Секция "Быстрый доступ" -->
      <div class="mb-6">
        <h3 class="text-base font-medium text-neutral-900 mb-4">Быстрый доступ</h3>
        <div class="grid grid-cols-2 gap-4">
          <div 
            class="p-4 border border-neutral-200 rounded-xl shadow-sm hover:border-alpha-300 transition-colors cursor-pointer flex flex-col items-center justify-center bg-white"
            tabindex="0"
            aria-label="Перейти к профилю"
            @click="handleProfileClick"
            @keydown.enter="handleProfileClick"
            @keydown.space="handleProfileClick"
          >
            <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-sm font-medium text-neutral-900">Мой профиль</span>
          </div>
          
          <div 
            class="p-4 border border-neutral-200 rounded-xl shadow-sm hover:border-alpha-300 transition-colors cursor-pointer flex flex-col items-center justify-center bg-white"
            tabindex="0"
            aria-label="Перейти ко всем урокам"
            @click="handleAllLessonsClick"
            @keydown.enter="handleAllLessonsClick"
            @keydown.space="handleAllLessonsClick"
          >
            <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
              </svg>
            </div>
            <span class="text-sm font-medium text-neutral-900">Все уроки</span>
          </div>
          
          <div 
            class="p-4 border border-neutral-200 rounded-xl shadow-sm hover:border-alpha-300 transition-colors cursor-pointer flex flex-col items-center justify-center bg-white"
            tabindex="0"
            aria-label="Перейти к индивидуальному плану обучения"
            @click="handleIndividualPlanClick"
            @keydown.enter="handleIndividualPlanClick"
            @keydown.space="handleIndividualPlanClick"
          >
            <div class="h-10 w-10 bg-alpha-100 text-alpha-500 rounded-full flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
              </svg>
            </div>
            <span class="text-sm font-medium text-neutral-900">Индивидуальный план</span>
          </div>
        </div>
      </div>

      <!-- Совет дня -->
      <div class="p-5 border border-neutral-100 rounded-xl bg-neutral-50 mb-6">
        <div class="flex items-center mb-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
          </svg>
          <h3 class="text-sm font-medium text-neutral-900">Совет дня</h3>
        </div>
        <p class="text-sm text-neutral-600">{{ randomFact }}</p>
      </div>

    </div>

    <!-- Панель навигации в стиле Альфа-Банка -->
    <nav class="border-t border-neutral-200 bg-white py-3 px-6">
      <div class="flex justify-around">
        <button class="flex flex-col items-center text-alpha-500" @click="handleHomeClick">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span class="text-xs mt-1">Главная</span>
        </button>
        <button class="flex flex-col items-center text-neutral-500" @click="handleAllLessonsClick">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span class="text-xs mt-1">Уроки</span>
        </button>
        <button class="flex flex-col items-center text-neutral-500" @click="handleProfileClick">
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

const router = useRouter();

const currentLesson = ref({
  id: 1,
  title: "Основы личного бюджета",
  description: "Научитесь правильно планировать свои доходы и расходы",
  progress: 25
});

const facts = ref([
  "70% людей, ведущих бюджет, достигают финансовых целей быстрее",
  "Регулярные инвестиции даже небольших сумм могут принести значительный доход через 10-15 лет",
  "Финансовая грамотность помогает снизить стресс и улучшить качество жизни",
  "Более 60% миллионеров — обычные люди, которые грамотно управляют своими финансами"
]);

const randomFact = computed(() => {
  const randomIndex = Math.floor(Math.random() * facts.value.length);
  return facts.value[randomIndex];
});

onMounted(() => {
  // Здесь будет запрос к API для получения текущего урока пользователя
  fetchCurrentLesson();
});

const fetchCurrentLesson = () => {
  // Здесь будет логика для получения текущего урока с сервера
};

const handleHomeClick = () => {
  router.push('/');
};

const handleLessonClick = () => {
  router.push(`/lessons/${currentLesson.value.id}`);
};

const handleAllLessonsClick = () => {
  router.push('/lessons');
};

const handleProfileClick = () => {
  router.push('/profile');
};

const handleIndividualPlanClick = () => {
  router.push('/individual-plan');
};

const handleCoinShopClick = () => {
  router.push('/coin-shop');
};
</script>

<style scoped>
/* Base styles */
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 24px;
  background-color: #f8faff;
  position: relative;
  overflow: hidden;
}

/* Анимации для эмодзи и фоновых элементов */
.coin-emoji {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

@keyframes float-medium {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-8px) rotate(-5deg); }
}

@keyframes float-fast {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-12px) rotate(8deg); }
}

@keyframes pulse-slow {
  0%, 100% { transform: scale(1); opacity: 0.2; }
  50% { transform: scale(1.1); opacity: 0.25; }
}

@keyframes pulse-medium {
  0%, 100% { transform: scale(1); opacity: 0.1; }
  50% { transform: scale(1.15); opacity: 0.15; }
}

.animate-float-slow {
  animation: float-slow 5s ease-in-out infinite;
}

.animate-float-medium {
  animation: float-medium 4s ease-in-out infinite;
}

.animate-float-fast {
  animation: float-fast 3s ease-in-out infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 8s ease-in-out infinite;
}

.animate-pulse-medium {
  animation: pulse-medium 6s ease-in-out infinite;
}

/* Background decorations */
.bg-decoration {
  position: absolute;
  z-index: 0;
  pointer-events: none;
}

.bg-circle-1 {
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.1), rgba(74, 144, 226, 0));
  top: -100px;
  right: -100px;
}

.bg-circle-2 {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(97, 218, 251, 0.1), rgba(97, 218, 251, 0));
  bottom: 20%;
  left: -50px;
}

.bg-pattern {
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 36px;
  position: relative;
  z-index: 2;
}

.welcome-message {
  font-size: 28px;
  background: linear-gradient(135deg, #4A90E2, #61DAFB);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 800;
  margin: 0;
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.welcome-message:hover {
  transform: scale(1.03);
}

.profile-link {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4A90E2, #61DAFB);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(74, 144, 226, 0.2);
  transition: all 0.3s ease;
  position: relative;
}

.profile-link:hover, .profile-link:focus {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(74, 144, 226, 0.3);
}

.profile-icon {
  font-size: 24px;
  color: white;
}

.profile-tooltip {
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.profile-link:hover .profile-tooltip, .profile-link:focus .profile-tooltip {
  opacity: 1;
  visibility: visible;
}

/* Section headers */
.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  position: relative;
}

h2 {
  color: #333;
  font-size: 20px;
  margin: 0;
  z-index: 1;
  position: relative;
}

.ribbon {
  height: 2px;
  background: linear-gradient(90deg, #4A90E2, rgba(97, 218, 251, 0));
  margin-left: 12px;
  flex-grow: 1;
}

/* Current lesson section */
.current-lesson, .all-lessons-section, .quick-facts {
  margin-bottom: 36px;
  position: relative;
  z-index: 1;
}

.lesson-card {
  background: linear-gradient(135deg, white, #f8faff);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(74, 144, 226, 0.07);
  display: flex;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(74, 144, 226, 0.1);
  position: relative;
  overflow: hidden;
}

.lesson-card:hover, .lesson-card:focus {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(74, 144, 226, 0.1);
}

.lesson-card:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, #4A90E2, #61DAFB);
}

.lesson-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.1), rgba(97, 218, 251, 0.1));
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
  flex-shrink: 0;
}

.icon {
  font-size: 30px;
}

.lesson-content {
  flex: 1;
}

.lesson-content h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 18px;
  font-weight: 700;
}

.lesson-content p {
  margin: 0 0 16px 0;
  color: #666;
  font-size: 15px;
  line-height: 1.5;
}

.lesson-progress {
  margin-bottom: 16px;
}

.progress-text {
  display: block;
  margin-top: 5px;
  color: #4A90E2;
  font-size: 14px;
  font-weight: 600;
}

.start-btn {
  background: linear-gradient(135deg, #4A90E2, #61DAFB);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 12px 20px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
  width: 100%;
  box-shadow: 0 4px 10px rgba(74, 144, 226, 0.3);
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(74, 144, 226, 0.4);
  background: linear-gradient(135deg, #3a80d2, #51CAEB);
}

.btn-icon {
  font-size: 18px;
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.start-btn:hover .btn-icon {
  transform: translateX(5px);
}

/* All lessons button */
.all-lessons-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border: none;
  border-radius: 16px;
  padding: 20px;
  width: 100%;
  box-shadow: 0 10px 25px rgba(74, 144, 226, 0.07);
  font-size: 16px;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  border: 1px solid rgba(74, 144, 226, 0.1);
}

.all-lessons-btn:hover, .all-lessons-btn:focus {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(74, 144, 226, 0.1);
}

.btn-content {
  display: flex;
  align-items: center;
}

.btn-icon-left {
  font-size: 22px;
  margin-right: 12px;
}

.arrow {
  color: #4A90E2;
  font-weight: bold;
  font-size: 20px;
  transition: transform 0.3s ease;
}

.all-lessons-btn:hover .arrow {
  transform: translateX(5px);
}

/* Quick facts section */
.quick-facts {
  margin-top: auto;
  padding-top: 20px;
}

.fact-card {
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.05), rgba(97, 218, 251, 0.05));
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  border: 1px solid rgba(74, 144, 226, 0.1);
  box-shadow: 0 5px 15px rgba(74, 144, 226, 0.05);
  position: relative;
  overflow: hidden;
}

.fact-card:before {
  content: '';
  position: absolute;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(97, 218, 251, 0.1), transparent);
  top: -50px;
  right: -50px;
  border-radius: 50%;
}

.fact-icon {
  font-size: 24px;
  margin-right: 16px;
  flex-shrink: 0;
}

.fact-text {
  font-size: 15px;
  color: #555;
  line-height: 1.5;
  font-style: italic;
  margin: 0;
}

/* Animation for page loading */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.home-container > * {
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}

.header {
  animation-delay: 0.1s;
}

.current-lesson {
  animation-delay: 0.2s;
}

.all-lessons-section {
  animation-delay: 0.3s;
}

.quick-facts {
  animation-delay: 0.4s;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .lesson-card {
    flex-direction: column;
  }
  
  .lesson-icon {
    margin-right: 0;
    margin-bottom: 16px;
  }
}
</style> 