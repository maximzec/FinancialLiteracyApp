<template>
  <div class="min-h-screen bg-white flex flex-col">
    <div class="flex-1 flex flex-col px-6 pt-8 pb-4">
      <!-- Заголовок -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-neutral-900">Магазин коинов</h2>
        <p class="text-neutral-600 mt-1">Пополните баланс для доступа к премиум-контенту</p>
      </div>

      <!-- Баланс -->
      <div class="bg-gradient-to-r from-alpha-500 to-alpha-600 rounded-xl p-6 mb-8">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-white/80 text-sm">Текущий баланс</p>
            <p class="text-3xl font-bold text-white">{{ balance }} коинов</p>
          </div>
          <div class="h-12 w-12 bg-white/20 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Пакеты коинов -->
      <div class="space-y-4">
        <div class="p-4 border border-neutral-200 rounded-xl">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-medium text-neutral-900">Базовый пакет</h3>
              <p class="text-sm text-neutral-600">100 коинов</p>
            </div>
            <div class="text-right">
              <p class="font-medium text-neutral-900">99 ₽</p>
              <p class="text-sm text-neutral-600">0.99 ₽ за коин</p>
            </div>
          </div>
          <button class="w-full bg-alpha-500 text-white py-3 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors">
            Купить
          </button>
        </div>

        <div class="p-4 border border-alpha-500 rounded-xl bg-alpha-50">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-medium text-neutral-900">Популярный пакет</h3>
              <p class="text-sm text-neutral-600">500 коинов</p>
            </div>
            <div class="text-right">
              <p class="font-medium text-neutral-900">399 ₽</p>
              <p class="text-sm text-neutral-600">0.80 ₽ за коин</p>
            </div>
          </div>
          <button class="w-full bg-alpha-500 text-white py-3 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors">
            Купить
          </button>
        </div>

        <div class="p-4 border border-neutral-200 rounded-xl">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-medium text-neutral-900">Премиум пакет</h3>
              <p class="text-sm text-neutral-600">1000 коинов</p>
            </div>
            <div class="text-right">
              <p class="font-medium text-neutral-900">699 ₽</p>
              <p class="text-sm text-neutral-600">0.70 ₽ за коин</p>
            </div>
          </div>
          <button class="w-full bg-alpha-500 text-white py-3 rounded-xl text-base font-medium hover:bg-alpha-600 transition-colors">
            Купить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const balance = ref(25);
</script>

<style scoped>
/* Дополнительные стили если потребуются */
</style> 