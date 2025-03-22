<template>
  <div class="h-1 w-full bg-gray-100 rounded-none">
    <div 
      class="h-1 bg-indigo-500 rounded-none transition-all duration-300" 
      :style="{ width: `${progress}%` }"
    ></div>
  </div>
</template>

<script setup>
import { toRef } from 'vue';

/* eslint-disable no-undef */
const props = defineProps({
  progress: {
    type: Number,
    default: 0
  }
});
/* eslint-enable no-undef */

const progress = toRef(props, 'progress');
</script> 