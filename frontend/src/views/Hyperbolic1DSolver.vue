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
            Решение 1D гиперболического уравнения
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
        <div class="mb-6 p-4 rounded-2xl bg-white/70 backdrop-blur-sm shadow-sm"
             :class="darkMode ? 'bg-gray-800/50 text-gray-200' : 'bg-white text-gray-800'">
          <h2 class="text-xl font-semibold mb-3 text-blue-600 dark:text-blue-400">
            Постановка задачи
          </h2>
          <p>
            Рассматривается одномерное гиперболическое уравнение:
          </p>
          <p class="text-center my-4 font-mono text-lg italic">
            \(\frac{\partial^2 u}{\partial t^2} = a \frac{\partial^2u}{\partial x^2} + f(x), \quad 0 < x < L, \quad 0 < t < T \)
          </p>
          <p>
            с начальными условиями:
          </p>
          <p class="text-center my-4 font-mono text-lg italic">
            \(u(x, 0) = u_0(x), \quad 0 < x < L \)
            \(\frac{\partial u(x, 0)}{\partial t} = u_1(x), \quad 0 < x < L \)
          </p>
          <p>
            с граничными условиями:
          </p>
          <p class="text-center my-4 font-mono text-lg italic">
            \(u(0, t) = \mu_1(t), \quad u(L, t) = \mu_2(t), \quad 0 < t < T \)
          </p>
          <p>
            Здесь \(a > 0\) — коэффициент теплопроводности (или аналогичный параметр в физической постановке),
            \(f(x)\) — правая часть, задающая распределение источников.
          </p>
        </div>
        <div class="mb-6 p-4 rounded-2xl bg-white/70 backdrop-blur-sm shadow-sm"
             :class="darkMode ? 'bg-gray-800/50 text-gray-200' : 'bg-white text-gray-800'">
          <h2 class="text-xl font-semibold mb-3 text-indigo-600 dark:text-indigo-400">
            Метод решения
          </h2>
          <p>
            Для численного решения используется <strong>метод конечных разностей</strong>.
            Вторая производная аппроксимируется по схеме:
          </p>
          <p class="text-center my-4 font-mono text-lg italic">
            \(\frac{\partial^2u}{\partial x^2} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{h^2}\),
          </p>
          <p>
            где \(h = \frac{L}{M}\) — шаг сетки.
            В результате получаем систему линейных алгебраических уравнений, решаемую методом прогонки.
          </p>
        </div>
        <div class="mb-6 p-4 rounded-2xl bg-white/70 backdrop-blur-sm shadow-sm"
             :class="darkMode ? 'bg-gray-800/50 text-gray-200' : 'bg-white text-gray-800'">
          <h2 class="text-xl font-semibold mb-3 text-purple-600 dark:text-purple-400">
            Физическая интерпретация
          </h2>
          <p>
            Уравнение теплопроводности описывает установившееся распределение температуры,
            электрического потенциала или концентрации вещества в однородной среде.
            Заданные граничные условия определяют значение функции \(u(x)\) на концах области.
          </p>
        </div>
        <form @submit.prevent="solve" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- L parameter -->
            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Длина времени (T)
              </label>
              <input
                  v-model.number="params.T"
                  type="number"
                  step="1.0"
                  :class="inputClasses"
              />
            </div>
            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Длина области (L)
              </label>
              <input
                  v-model.number="params.L"
                  type="number"
                  step="1.0"
                  :class="inputClasses"
              />
            </div>

            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Количество разбиений (N)
              </label>
              <input
                  v-model.number="params.N"
                  type="number"
                  step="1"
                  :class="inputClasses"
              />
            </div>

            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Количество разбиений (M)
              </label>
              <input
                  v-model.number="params.M"
                  type="number"
                  step="1"
                  :class="inputClasses"
              />
            </div>

            <!-- a parameter -->
            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Коэффициент (a)
              </label>
              <input
                  v-model.number="params.a"
                  type="number"
                  step="1.0"
                  :class="inputClasses"
              />
            </div>

            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Начальное условие u(x, 0)
              </label>
              <input
                  v-model="params.init_cond"
                  type="text"
                  placeholder="x+1"
                  :class="[inputClasses, 'font-mono text-sm']"
              />
            </div>

            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Начальная скорость u'(x, 0)
              </label>
              <input
                  v-model="params.init_velocity"
                  type="text"
                  placeholder="x**2"
                  :class="[inputClasses, 'font-mono text-sm']"
              />
            </div>

            <div class="space-y-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Граничное условие u(0, t)
              </label>
              <input
                  v-model="params.left_bc"
                  type="text"
                  placeholder="t"
                  :class="[inputClasses, 'font-mono text-sm']"
              />
            </div>

            <!-- right_bc -->
            <div class="space-y-2 md:col-span-2">
              <label :class="[
                'block text-sm font-semibold',
                darkMode ? 'text-gray-300' : 'text-gray-700'
              ]">
                Граничное условие u(L, t)
              </label>
              <input
                  v-model="params.right_bc"
                  type="text"
                  placeholder="cos(pi*t)"
                  :class="[inputClasses, 'font-mono text-sm']"
              />
            </div>
          </div>

          <!-- f_expr -->
          <div class="space-y-2">
            <label :class="[
              'block text-sm font-semibold',
              darkMode ? 'text-gray-300' : 'text-gray-700'
            ]">
              Функция правой части f(x)
            </label>
            <input
                v-model="params.f_expr"
                type="text"
                placeholder="sin(pi*x)"
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
            <span v-else>Решить уравнение</span>
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

          </div>

          <!-- Charts -->
          <div class="space-y-6">
            <div v-if="result.img_line" :class="[
              'p-4 rounded-2xl',
              darkMode ? 'bg-gray-700/30' : 'bg-white shadow-md'
            ]">
              <img
                  :src="result.img_line"
                  alt="График решения"
                  class="w-full h-auto rounded-xl"
              />
            </div>

            <div v-if="result.img_heat" :class="[
              'p-4 rounded-2xl',
              darkMode ? 'bg-gray-700/30' : 'bg-white shadow-md'
            ]">
              <img
                  :src="result.img_heat"
                  alt="Тепловая карта"
                  class="w-full h-auto rounded-xl"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div :class="[
        'text-center mt-8 text-sm',
        darkMode ? 'text-gray-400' : 'text-gray-600'
      ]">
        <p>Численное решение гиперболического уравнения методом конечных разностей</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, onUpdated} from "vue";
import axios from "axios";

const darkMode = ref(false);

const params = ref({
  T: 1.0,
  L: 1.0,
  N: 100,
  M: 50,
  a: 1.0,
  init_cond: "x+1",
  init_velocity: "x**2",
  left_bc: "t",
  right_bc: "cos(pi*t)",
  f_expr: "sin(pi*x)",
});

const result = ref(null);
const error = ref("");
const loading = ref(false);

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
const formatArray = (arr) => {
  if (!arr) return "[]";
  return arr.map(v => {
    const n = Number(v);
    return isFinite(n) ? n.toFixed(4) : "NaN";
  });
}

async function solve() {
  result.value = null;
  error.value = "";
  loading.value = true;

  try {
    const res = await axios.post("http://127.0.0.1:5000/api/hyperbolic1d/solve", params.value);
    result.value = res.data;
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