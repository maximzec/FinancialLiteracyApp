<template>
  <div class="progress-container">
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',
  props: {
    progress: {
      type: Number,
      required: true,
      default: 0
    }
  }
}
</script>

<style scoped>
.progress-container {
  width: 100%;
  max-width: 300px;
  margin: 20px 0;
}

.progress-bar {
  height: 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) inset;
  backdrop-filter: blur(5px);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #00c6ff, #0072ff);
  border-radius: 3px;
  transition: width 0.5s ease;
  position: relative;
  box-shadow: 0 0 8px rgba(0, 198, 255, 0.5);
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0.1)
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style> 