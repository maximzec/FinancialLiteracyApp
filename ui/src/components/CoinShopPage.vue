<!-- Текущий баланс -->
<div class="mb-6">
  <div class="p-5 rounded-xl relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-purple-700">
    <!-- Декоративные элементы с анимацией -->
    <div class="absolute bottom-[-20%] right-[-5%] w-32 h-32 rounded-full bg-red-500 opacity-20 animate-pulse-slow"></div>
    <div class="absolute top-[-10%] left-[-5%] w-40 h-40 rounded-full bg-yellow-300 opacity-10 animate-pulse-medium"></div>
    <div class="absolute bottom-[-30%] left-[20%] w-60 h-60 rounded-full bg-green-400 opacity-10 animate-float-slow"></div>
    
    <!-- Основное содержимое -->
    <div class="flex items-center justify-center relative z-10 py-3">
      <div class="text-center">
        <h3 class="text-sm font-medium text-white/80 mb-1">Баланс</h3>
        <p class="text-3xl font-bold text-white">25 коинов</p>
      </div>
    </div>
  </div>
</div>

<style scoped>
.bg-pattern {
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
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

.animate-pulse-slow {
  animation: pulse-slow 8s ease-in-out infinite;
}

.animate-pulse-medium {
  animation: pulse-medium 6s ease-in-out infinite;
}
</style> 