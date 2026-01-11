<template>
  <div class="min-h-screen flex flex-col transition-colors duration-300" :class="isDark ? 'bg-gray-900' : 'bg-gray-100'">
    <!-- === Header === -->
    <header class="py-4 shadow-md transition-colors duration-300" :class="isDark ? 'bg-indigo-700 text-white' : 'bg-indigo-600 text-white'">
      <div class="container mx-auto flex justify-between items-center px-6">
        <h1 class="text-2xl font-bold">{{ $t('menu.title') }}</h1>

        <nav class="space-x-6 hidden md:flex items-center">
          <RouterLink to="/" class="hover:text-gray-200 transition">{{ $t('menu.home') }}</RouterLink>
          <RouterLink to="/about" class="hover:text-gray-200 transition">{{ $t('menu.about') }}</RouterLink>
          <RouterLink to="/contacts" class="hover:text-gray-200 transition">{{ $t('menu.contacts') }}</RouterLink>

          <!-- Theme Toggle Button -->
          <button
              @click="toggleTheme"
              class="p-2 rounded-lg transition-colors duration-300 hover:bg-indigo-500"
              :title="isDark ? 'Светлая тема' : 'Темная тема'"
          >
            <!-- Sun Icon (Light Mode) -->
            <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <!-- Moon Icon (Dark Mode) -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
        </nav>

        <select
            v-model="language"
            class="ml-4 px-2 py-1 rounded-md border focus:ring-2 focus:ring-indigo-400 transition-colors duration-300"
            :class="isDark ? 'bg-gray-700 text-white border-gray-600' : 'bg-white text-gray-700'"
        >
          <option value="ru">Русский</option>
          <option value="en">English</option>
        </select>
      </div>
    </header>

    <!-- === Main Content === -->
    <main class="flex-1 container mx-auto p-6 transition-colors duration-300" :class="isDark ? 'text-gray-100' : 'text-gray-900'">
      <RouterView />
    </main>

    <!-- === Footer === -->
    <footer class="py-4 text-center text-sm transition-colors duration-300" :class="isDark ? 'bg-gray-800 text-gray-400' : 'bg-gray-200 text-gray-600'">
      © 2025 NumMethods Solver
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch , provide} from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const language = ref(locale.value)
const isDark = ref(false)

provide('isDark', isDark)

// Load theme preference from localStorage
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  isDark.value = savedTheme === 'dark'
})

watch(language, (lang) => {
  locale.value = lang
  localStorage.setItem('lang', lang)
})

// Toggle theme function
const toggleTheme = () => {
  isDark.value = !isDark.value
}

watch(isDark, (val) => {
  localStorage.setItem('theme', val ? 'dark' : 'light')
})
</script>