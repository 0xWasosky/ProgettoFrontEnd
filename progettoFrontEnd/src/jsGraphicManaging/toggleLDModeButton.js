import { ref } from 'vue'

export const username = ref(localStorage.getItem('username') || 'Guest')

export const isDarkMode = ref(false)

export const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

export const initTheme = () => {
  isDarkMode.value = localStorage.getItem('theme') === 'dark'
  document.documentElement.setAttribute(
    'data-theme',
    isDarkMode.value ? 'dark' : 'light'
  )
}