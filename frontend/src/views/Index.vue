<template>
  <div class="grid md:grid-cols-3 gap-8">
    <!-- === Производные === -->
    <div class="shadow-lg rounded-2xl p-6 text-center transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Производные</h2>
      <RouterLink
          to="/derivative-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Производная
      </RouterLink>
    </div>

    <!-- === Интегралы === -->
    <div class="shadow-lg rounded-2xl p-6 text-center transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Интегралы</h2>
      <RouterLink
          to="/integral-solver"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Определённый интеграл
      </RouterLink>
      <RouterLink
          to="/fractional-integral"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Дробный интеграл
      </RouterLink>
    </div>

    <!-- === Параболические уравнения === -->
    <div class="shadow-lg rounded-2xl p-6 text-center transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Параболические уравнения</h2>
      <RouterLink
          to="/parabolic-1d"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Одномерное
      </RouterLink>
      <RouterLink
          to="/parabolic-2d"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Двумерное
      </RouterLink>
      <RouterLink
          to="/fractional-parabolic"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        С дробным производным
      </RouterLink>
      <RouterLink
          to="/inverse-parabolic"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Обратная задача восстановления функции правой части
      </RouterLink>
    </div>

    <!-- === Гиперболические === -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Гиперболические уравнения</h2>
      <RouterLink
          to="/hyperbolic-1d"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        Одномерное
      </RouterLink>
    </div>

    <!-- Эллиптические уравнения -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Эллиптические уравнения</h2>
      <RouterLink
          to="/elliptic-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        Одномерное
      </RouterLink>
    </div>

    <!-- дифференциальные уравнения -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Обыкновенные дифференциальные уравнения</h2>
      <RouterLink
          to="/odefirstorder-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        Дифференциальное уравнение 1-го порядка
      </RouterLink>
      <RouterLink
          to="/odesecondorder-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        Дифференциальное уравнение 2-го порядка
      </RouterLink>
    </div>

    <!-- другие уравнения -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">Другие уравнения</h2>
      <RouterLink
          to="/elliptic-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        Численное моделирование процесса биологической очистки сточных вод
      </RouterLink>
      <RouterLink
          to="/elliptic-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        Модель роста солидной опухоли без диффузии и химиотерапии
      </RouterLink>
      <RouterLink
          to="/nonlinear-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        Нелинейное уравнение
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { inject } from 'vue'

// Получаем состояние темы из родительского компонента
const isDark = inject('isDark', false)
</script>