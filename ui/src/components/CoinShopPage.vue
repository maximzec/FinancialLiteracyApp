<template>
  <div class="min-h-screen bg-alpha-gray-50 flex flex-col">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <button @click="handleGoBack" class="text-alpha-red flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            Назад
          </button>
          <h1 class="text-xl font-semibold text-alpha-gray-900">Магазин предметов</h1>
          <div class="w-10"></div> <!-- Spacer for centering title -->
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 py-8 px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto">
        <!-- User Balance -->
        <div class="mb-8 p-6 rounded-xl bg-gradient-to-r from-alpha-red to-red-600 text-white shadow-lg">
          <div class="flex justify-between items-center">
            <div>
              <p class="text-sm opacity-80">Ваш баланс</p>
              <p class="text-3xl font-bold">{{ userCoins }} коинов</p>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 opacity-50" viewBox="0 0 20 20" fill="currentColor">
              <path d="M8.433 7.418c.158-.103.335-.166.534-.185.261-.023.529-.015.792.016.183.021.361.058.532.109.17.051.33.118.481.198.151.08.292.174.422.279.13.105.248.224.354.354.105.13.198.271.279.422.081.15.149.31.198.481.051.171.088.349.109.532.021.183.029.351.016.512a2.162 2.162 0 01-.185.534c-.103.158-.222.304-.354.434s-.276.251-.434.354a2.162 2.162 0 01-.534.185c-.183.021-.37.029-.554.016-.183-.013-.365-.046-.546-.097a3.518 3.518 0 01-.504-.159 3.518 3.518 0 01-.463-.236c-.14-.092-.27-.2-.39-.318a3.518 3.518 0 01-.318-.39c-.082-.13-.15-.267-.204-.409-.055-.141-.097-.284-.126-.43a2.162 2.162 0 01-.016-.554c.013-.184.046-.366.097-.546.051-.18.118-.351.198-.512.08-.162.174-.312.279-.451.105-.14.224-.268.354-.386.13-.119.271-.224.422-.318.151-.093.311-.174.481-.243zM10 2a8 8 0 100 16 8 8 0 000-16z" />
            </svg>
          </div>
        </div>

        <!-- Items Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="item in shopItems" 
            :key="item.id"
            class="bg-white rounded-xl shadow-md overflow-hidden flex flex-col hover:shadow-lg transition-shadow duration-300"
          >
            <div class="h-40 bg-alpha-gray-100 flex items-center justify-center p-4">
              <!-- Replace with actual item.icon or a placeholder -->
              <span class="text-4xl">{{ item.iconPlaceholder || '🛍️' }}</span>
            </div>
            <div class="p-5 flex flex-col flex-grow">
              <h2 class="text-lg font-semibold text-alpha-gray-900 mb-1">{{ item.name }}</h2>
              <p class="text-sm text-alpha-gray-600 mb-3 flex-grow">{{ item.description }}</p>
              <div class="flex justify-between items-center mt-auto">
                <p class="text-xl font-bold text-alpha-red">{{ item.price }} <span class="text-sm font-normal">коинов</span></p>
                <button 
                  @click="handleBuyItemClick(item)"
                  :disabled="userCoins < item.price"
                  class="alpha-button px-4 py-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  :aria-label="'Купить ' + item.name + ' за ' + item.price + ' коинов'"
                >
                  Купить
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="shopItems.length === 0" class="text-center py-10">
          <p class="text-xl text-alpha-gray-500">Магазин пока пуст, но скоро здесь появятся крутые предметы!</p>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-alpha-gray-300 mx-auto mt-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
          </svg>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userCoins = ref(1500); // Пример баланса пользователя

const shopItems = ref([
  {
    id: 'badge_beginner_financer',
    name: 'Бейдж "Новичок Финансист"',
    description: 'Покажите всем, что вы начали свой путь в мир финансов!',
    price: 100,
    type: 'badge',
    iconPlaceholder: '🔰', // Placeholder icon
  },
  {
    id: 'virtual_mascot_alpha_cat',
    name: 'Маскот "Альфа-Котик"',
    description: 'Милый виртуальный котик, который будет поднимать вам настроение.',
    price: 300,
    type: 'virtual_item',
    iconPlaceholder: '😼',
  },
  {
    id: 'badge_budget_master',
    name: 'Бейдж "Магистр Бюджета"',
    description: 'За проявленное мастерство в планировании личного бюджета.',
    price: 500,
    type: 'badge',
    iconPlaceholder: '🏆',
  },
  {
    id: 'theme_space_voyager',
    name: 'Тема "Космический Путешественник"',
    description: 'Новое оформление для вашего профиля в стиле космоса.',
    price: 750,
    type: 'theme',
    iconPlaceholder: '🚀',
  },
  {
    id: 'sound_pack_relax',
    name: 'Набор звуков "Релакс"',
    description: 'Успокаивающие звуки для концентрации во время обучения.',
    price: 250,
    type: 'sound_pack',
    iconPlaceholder: '🎧',
  },
  {
    id: 'avatar_frame_golden',
    name: 'Золотая рамка для аватара',
    description: 'Выделите свой аватар эксклюзивной золотой рамкой.',
    price: 1000,
    type: 'avatar_customization',
    iconPlaceholder: '🌟',
  }
]);

const handleGoBack = () => {
  router.back();
};

const handleBuyItemClick = (item) => {
  if (userCoins.value >= item.price) {
    // В будущем здесь будет логика покупки:
    // 1. Списать коины у пользователя
    // 2. Добавить предмет в инвентарь пользователя
    // 3. Показать уведомление об успешной покупке
    userCoins.value -= item.price; // Временно для демонстрации
    console.log(`Покупка: ${item.name}, Цена: ${item.price} коинов. Остаток: ${userCoins.value}`);
    alert(`Вы купили "${item.name}"!`);
  } else {
    console.log('Недостаточно средств для покупки');
    alert('У вас недостаточно коинов для покупки этого предмета.');
  }
};
</script>

<style scoped>
/* Styles for CoinShopPage */
/* Using Tailwind utility classes, so no specific scoped styles are needed beyond those implied by the classes. */
/* However, you can add custom animations or very specific element styles here if necessary. */

.alpha-button:disabled {
  background-color: var(--alpha-gray-300);
  border-color: var(--alpha-gray-300);
  color: var(--alpha-gray-500);
}
</style> 