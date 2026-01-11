<template>
  <div class="grid md:grid-cols-3 gap-8">
    <!-- === Производные === -->
    <div class="shadow-lg rounded-2xl p-6 text-center transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.derivatives') }}</h2>
      <RouterLink
          to="/derivative-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.derivatives') }}
      </RouterLink>
    </div>

    <!-- === Интегралы === -->
    <div class="shadow-lg rounded-2xl p-6 text-center transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.integrals') }}</h2>
      <RouterLink
          to="/integral-solver"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.definiteIntegral') }}
      </RouterLink>
      <RouterLink
          to="/fractional-integral"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.fractionalIntegral') }}
      </RouterLink>
    </div>

    <!-- === Параболические уравнения === -->
    <div class="shadow-lg rounded-2xl p-6 text-center transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.parabolicEquations')}}</h2>
      <RouterLink
          to="/parabolic-1d"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.oneDim') }}
      </RouterLink>
      <RouterLink
          to="/parabolic-2d"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.twoDim') }}
      </RouterLink>
      <RouterLink
          to="/fractional-parabolic"
          class="block bg-indigo-500 text-white py-2 mb-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.withFractionalDerivative') }}
      </RouterLink>
      <RouterLink
          to="/inverse-parabolic"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.inverseProblem') }}
      </RouterLink>
    </div>

    <!-- === Гиперболические === -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.hyperbolicEquations') }}</h2>
      <RouterLink
          to="/hyperbolic-1d"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
      >
        {{ $t('index.oneDim') }}
      </RouterLink>
    </div>

    <!-- Эллиптические уравнения -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.ellipticEquations') }}</h2>
      <RouterLink
          to="/elliptic-1d"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.oneDim') }}
      </RouterLink>
      <RouterLink
          to="/elliptic-2d"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.twoDim') }}
      </RouterLink>
      <RouterLink
          to="/inverse-elliptic"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.inverseProblem') }}
      </RouterLink>
    </div>

    <!-- дифференциальные уравнения -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.ordinaryDifferentialEquations') }}</h2>
      <RouterLink
          to="/odefirstorder-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.firstOrderDifferentialEquation') }}
      </RouterLink>
      <RouterLink
          to="/odesecondorder-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.secondOrderDifferentialEquation') }}
      </RouterLink>
    </div>

    <!-- другие уравнения -->
    <div class="shadow-lg rounded-2xl p-6 text-center md:col-span-3 lg:col-span-1 transition-colors duration-300" :class="isDark ? 'bg-gray-800' : 'bg-white'">
      <h2 class="text-xl font-bold mb-4" :class="isDark ? 'text-gray-100' : 'text-gray-900'">{{ $t('index.otherEquations') }}</h2>
      <RouterLink
          to="/wastewater-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.wastewater') }}
      </RouterLink>
      <RouterLink
          to="/stg-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.solidTumorGrowth') }}
      </RouterLink>
      <RouterLink
          to="/nonlinear-solver"
          class="block bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition mt-2"
      >
        {{ $t('index.nonlinearEquation') }}
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { inject } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Получаем состояние темы из родительского компонента
const isDark = inject('isDark', false)
</script>