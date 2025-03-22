<template>
  <div class="min-h-screen bg-indigo-50 flex flex-col justify-center items-center p-6">
    <div class="w-full max-w-md bg-white rounded-lg shadow-sm border border-indigo-100 p-8">
      <!-- Логотип и заголовок -->
      <div class="text-center mb-8">
        <div class="inline-block bg-indigo-100 rounded-full p-3 mb-3">
          <div class="text-indigo-500 text-3xl">💰</div>
        </div>
        <h1 class="text-2xl font-bold text-indigo-900 mb-2">Финансовая грамотность</h1>
        <p class="text-indigo-600">Инвестируйте в свои знания</p>
      </div>
      
      <!-- Формы входа/регистрации -->
      <div class="mb-6">
        <div class="flex border-b border-indigo-100 mb-6">
          <button 
            :class="['flex-1 py-2 text-center text-sm font-medium', isLogin ? 'text-indigo-500 border-b-2 border-indigo-500' : 'text-indigo-300']"
            @click="isLogin = true"
          >
            Вход
          </button>
          <button 
            :class="['flex-1 py-2 text-center text-sm font-medium', !isLogin ? 'text-indigo-500 border-b-2 border-indigo-500' : 'text-indigo-300']"
            @click="isLogin = false"
          >
            Регистрация
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit">
          <!-- Форма входа -->
          <div v-if="isLogin">
            <div class="mb-4">
              <label class="block text-xs font-medium text-indigo-900 mb-1" for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                class="w-full p-3 text-sm border border-indigo-100 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-200"
                placeholder="example@mail.com"
                required
              />
            </div>
            
            <div class="mb-4">
              <label class="block text-xs font-medium text-indigo-900 mb-1" for="password">Пароль</label>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                class="w-full p-3 text-sm border border-indigo-100 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-200"
                placeholder="Ваш пароль"
                required
              />
            </div>
            
            <div class="flex justify-between items-center mb-6">
              <div class="flex items-center">
                <input type="checkbox" id="remember" class="mr-2 h-4 w-4 text-indigo-500" />
                <label for="remember" class="text-xs text-indigo-600">Запомнить меня</label>
              </div>
              <a href="#" class="text-xs text-indigo-500 hover:text-indigo-700">Забыли пароль?</a>
            </div>
          </div>
          
          <!-- Форма регистрации -->
          <div v-else>
            <div class="mb-4">
              <label class="block text-xs font-medium text-indigo-900 mb-1" for="reg-name">Имя</label>
              <input 
                type="text" 
                id="reg-name" 
                v-model="name" 
                class="w-full p-3 text-sm border border-indigo-100 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-200"
                placeholder="Ваше имя"
                required
              />
            </div>
            
            <div class="mb-4">
              <label class="block text-xs font-medium text-indigo-900 mb-1" for="reg-email">Email</label>
              <input 
                type="email" 
                id="reg-email" 
                v-model="email" 
                class="w-full p-3 text-sm border border-indigo-100 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-200"
                placeholder="example@mail.com"
                required
              />
            </div>
            
            <div class="mb-4">
              <label class="block text-xs font-medium text-indigo-900 mb-1" for="reg-password">Пароль</label>
              <input 
                type="password" 
                id="reg-password" 
                v-model="password" 
                class="w-full p-3 text-sm border border-indigo-100 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-200"
                placeholder="Минимум 8 символов"
                required
              />
            </div>
            
            <div class="flex items-center mb-6">
              <input type="checkbox" id="terms" class="mr-2 h-4 w-4 text-indigo-500" required />
              <label for="terms" class="text-xs text-indigo-600">
                Я принимаю <a href="#" class="text-indigo-500 hover:text-indigo-700">условия использования</a>
              </label>
            </div>
          </div>
          
          <button 
            type="submit" 
            class="w-full bg-indigo-500 text-white px-4 py-3 rounded-md hover:bg-indigo-600 transition-colors font-medium"
          >
            {{ isLogin ? 'Войти' : 'Создать аккаунт' }}
          </button>
        </form>
      </div>
      
      <!-- Разделитель -->
      <div class="flex items-center justify-center mb-6">
        <div class="flex-1 h-px bg-indigo-100"></div>
        <div class="px-4 text-xs text-indigo-400">или</div>
        <div class="flex-1 h-px bg-indigo-100"></div>
      </div>
      
      <!-- Социальные сети -->
      <div class="space-y-3 mb-6">
        <button class="w-full flex items-center justify-center border border-indigo-100 rounded-md p-3 hover:bg-indigo-50 transition-colors">
          <span class="mr-2">G</span>
          <span class="text-sm text-indigo-900">Продолжить с Google</span>
        </button>
        
        <button class="w-full flex items-center justify-center border border-indigo-100 rounded-md p-3 hover:bg-indigo-50 transition-colors">
          <span class="mr-2">f</span>
          <span class="text-sm text-indigo-900">Продолжить с Facebook</span>
        </button>
      </div>
      
      <!-- Подсказка -->
      <div v-if="isLogin" class="text-center text-xs text-indigo-400">
        Нет аккаунта? <button @click="isLogin = false" class="text-indigo-500 hover:text-indigo-700">Зарегистрироваться</button>
      </div>
      <div v-else class="text-center text-xs text-indigo-400">
        Уже есть аккаунт? <button @click="isLogin = true" class="text-indigo-500 hover:text-indigo-700">Войти</button>
      </div>
    </div>
    
    <!-- Преимущества приложения -->
    <div class="w-full max-w-md mt-8 grid grid-cols-2 gap-4">
      <div class="bg-white p-4 rounded-lg border border-indigo-100 text-center">
        <div class="text-indigo-500 text-xl mb-2">📚</div>
        <div class="text-sm font-medium text-indigo-900 mb-1">Учитесь в своем темпе</div>
        <div class="text-xs text-indigo-600">Более 20 уроков по финансовой грамотности</div>
      </div>
      
      <div class="bg-white p-4 rounded-lg border border-indigo-100 text-center">
        <div class="text-indigo-500 text-xl mb-2">🏆</div>
        <div class="text-sm font-medium text-indigo-900 mb-1">Получайте награды</div>
        <div class="text-xs text-indigo-600">Зарабатывайте опыт и достижения</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLogin = ref(true);
const email = ref('');
const password = ref('');
const name = ref('');

const handleSubmit = () => {
  // В реальном приложении здесь была бы логика авторизации/регистрации
  console.log('Форма отправлена:', { 
    isLogin: isLogin.value, 
    email: email.value,
    password: password.value,
    name: !isLogin.value ? name.value : undefined
  });
  
  // Перенаправляем пользователя на главную страницу
  router.push('/');
};
</script> 