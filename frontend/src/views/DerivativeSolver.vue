<template>
  <div :class="[
    'min-h-screen transition-colors duration-300',
    darkMode
      ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900'
      : 'bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'
  ]">
    <div class="container mx-auto px-4 py-8 md:py-12 max-w-4xl">
      <!-- Header with Theme Toggle -->
      <div class="flex justify-between items-center mb-8">
        <div class="flex items-center gap-3">
          <svg class="w-8 h-8" :class="darkMode ? 'text-blue-400' : 'text-blue-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
          <h1 :class="[
            'text-2xl md:text-3xl font-bold',
            darkMode ? 'text-white' : 'text-gray-800'
          ]">
            {{ $t('derivative.calculatingTheDerivative') }}
          </h1>
        </div>
        <button
            @click="toggleTheme"
            :class="[
            'p-3 rounded-full transition-all duration-300',
            darkMode
              ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400'
              : 'bg-white hover:bg-gray-100 text-gray-700 shadow-md'
          ]"
            aria-label="Toggle theme"
        >
          <svg v-if="darkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>
      </div>

      <!-- Main Card -->
      <div :class="[
        'rounded-3xl shadow-2xl p-6 md:p-8 transition-colors duration-300',
        darkMode ? 'bg-gray-800/50 backdrop-blur-sm' : 'bg-white/80 backdrop-blur-sm'
      ]">
        <!-- Form -->
        <form @submit.prevent="solve" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- L parameter -->
            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                {{ $t('derivative.value') }}
              </label>
              <input
                  v-model.number="params.x"
                  type="number"
                  step="1.0"
                  :class="inputClasses"
              />
            </div>

            <!-- M parameter -->
            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                {{ $t('derivative.step') }}
              </label>
              <input
                  v-model.number="params.h"
                  type="number"
                  step="0.01"
                  min="0"
                  :class="inputClasses"
                  @input="params.h = Math.max(0, params.h)"
              />
            </div>

            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                {{ $t('derivative.method') }}
              </label>
              <select v-model="params.method" :class="inputClasses">
                <option value="left-derivative">Левая производная</option>
                <option value="central-derivative">Центральная производная</option>
                <option value="right-derivative">Правая производная</option>
              </select>

            </div>
          </div>

          <!-- f_expr -->
          <div class="space-y-2">
            <label :class="[
              'block text-sm font-semibold',
              darkMode ? 'text-gray-300' : 'text-gray-700'
            ]">
              {{ $t('derivative.function') }}
            </label>
            <input
                v-model="params.f_expr"
                type="text"
                placeholder="sin(pi * x * x)"
                :class="[inputClasses, 'font-mono text-sm']"
            />
          </div>

          <!-- Submit Button -->
          <button
              type="submit"
              :disabled="loading"
              :class="[
              'w-full py-4 px-6 rounded-2xl font-semibold text-white text-lg transition-all duration-300 shadow-lg hover:shadow-xl',
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-[1.02] active:scale-[0.98]'
            ]"
          >
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Вычисление...
            </span>
            <span v-else>{{ $t('derivative.calculateTheDerivative') }}</span>
          </button>
        </form>

        <!-- Error Message -->
        <div v-if="error" class="mt-6 p-4 rounded-2xl bg-red-100 border border-red-300 text-red-700 animate-fade-in">
          <p class="font-semibold">Ошибка:</p>
          <p class="text-sm">{{ error }}</p>
        </div>

        <!-- Results -->
        <div v-if="result && !loading" class="mt-8 space-y-6 animate-fade-in">
          <div :class="[
            'p-6 rounded-2xl',
            darkMode ? 'bg-gray-700/50' : 'bg-gradient-to-br from-green-50 to-emerald-50'
          ]">
            <h2 :class="[
              'text-xl font-bold mb-4 flex items-center gap-2',
              darkMode ? 'text-green-400' : 'text-green-700'
            ]">
              <span class="inline-block w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              Результаты решения
            </h2>

            <div :class="[
              'text-sm p-4 rounded-xl overflow-x-auto font-mono',
              darkMode ? 'bg-gray-800 text-gray-300' : 'bg-white text-gray-700'
            ]">
              <p class="mb-2 text-xl">
                <strong :class="darkMode ? 'text-blue-400' : 'text-blue-600'"></strong>
                \(\frac{df({{x}})}{dx} = {{ result }}\)
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div :class="[
        'text-center mt-8 text-sm',
        darkMode ? 'text-gray-400' : 'text-gray-600'
      ]">
        <p>Численное решение производной</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, onUpdated, nextTick, watch, provide} from "vue";
import { useI18n } from 'vue-i18n'
import axios from "axios";

const { locale } = useI18n()
const language = ref(locale.value)
const darkMode = ref(false);
const x = ref(1.0);
const params = ref({
  x: 1.0,
  h: 0.01,
  method: "left-derivative",
  f_expr: "sin(pi*x*x)",
});

const result = ref(null);
const error = ref("");
const loading = ref(false);

watch(language, (lang) => {
  locale.value = lang
  localStorage.setItem('lang', lang)
})

// Load theme from localStorage on mount
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    darkMode.value = savedTheme === 'dark';
  } else {
    // Check system preference
    darkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
});

// Toggle theme and save to localStorage
function toggleTheme() {
  darkMode.value = !darkMode.value;
  localStorage.setItem('theme', darkMode.value ? 'dark' : 'light');
}

// Dynamic input classes
const inputClasses = computed(() => [
  'w-full px-4 py-3 rounded-2xl transition-all duration-300 focus:outline-none focus:ring-2',
  darkMode.value
      ? 'bg-gray-700 text-white border border-gray-600 focus:ring-blue-500 focus:border-transparent'
      : 'bg-gray-50 text-gray-900 border border-gray-200 focus:ring-blue-500 focus:bg-white shadow-sm hover:shadow-md'
]);

// Format array for display
function formatArray(arr) {
  if (!arr || !arr.length) return '';
  return arr.slice(0, 10).map(v => v.toFixed(4)).join(', ') + ' ...';
}

async function solve() {
  result.value = null;
  error.value = "";
  loading.value = true;

  try {
    const res = await axios.post("http://127.0.0.1:5000/api/derivative/solve", params.value);
    result.value = res.data.result;  // res.data = { result: число }
    x.value = params.value.x;
  } catch (err) {
    error.value = err.response?.data?.detail || err.message;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  if (window.MathJax) window.MathJax.typesetPromise()
})

onUpdated(() => {
  if (window.MathJax) window.MathJax.typesetPromise()
})

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}
</style>