<script setup>
import { ref, onMounted } from 'vue'

const username = ref('')
const password = ref('')
const showPassword = ref(false)

const errors = ref({
  username: '',
  password: '',
})

const emit = defineEmits(['login', 'clearAuthError'])

// Login form
const handleLogin = () => {
  errors.value = { username: '', password: '' }
  let isValid = true

  if (!username.value) {
    errors.value.username = 'Nome utente obbligatorio'
    isValid = false
  }
  if (!password.value) {
    errors.value.password = 'Password obbligatoria'
    isValid = false
  }

  if (!isValid) return

  emit('clearAuthError')
  emit('login', { username: username.value, password: password.value })
}

// Theme toggle
const isDarkMode = ref(false)

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

// Load saved theme on mount
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  } else {
    document.documentElement.setAttribute('data-theme', 'light')
  }
})
</script>

<template>
  <button type="button" class="theme-toggle" @click="toggleTheme">
    {{ isDarkMode ? '☼' : '☀︎' }}
  </button>

  <div class="top-nav">
    <router-link to="/about">Info</router-link>
  </div>

  <div class="login-container">
    <div class="login-card">
      <div class="logoEU"><img src="../../assets/images/logoEU.jpg"></div>
      <h1>Login</h1>

      <form @submit.prevent="handleLogin" class="login-form" novalidate>
        <div>
          <label for="username" class="required">Nome utente:</label>
          <input type="text" id="username" v-model="username" />
          <p v-if="errors.username" class="error">{{ errors.username }}</p>
        </div>

        <div>
          <label for="password" class="required">Password:</label>
          <div style="display:flex; gap:8px; align-items:center;">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
            />
            <button
              type="button"
              style="width:auto; min-width: fit-content;"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? 'Nascondi' : 'Mostra' }}
            </button>
          </div>
          <p v-if="errors.password" class="error">{{ errors.password }}</p>
        </div>

        <button type="submit">Accedi</button>

        <!--<div class="register-link">
          <p>
            Non hai un account?
            <router-link to="/register"><br />Registrati qui</router-link>
          </p>
        </div>-->

        <div class=register-link>
          <router-link to="/">Ritorna all'indice</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<style src="../stylesheets/logoEU.css"></style>
<style>
/* Theme variables */
:root {
  --bg-color: #f5f0f0;
  --card-bg: #fff;
  --text-color: #2c3e50;
  --input-bg: #fff;
  --input-border: #ccc;
  --button-bg: #3490dc;
  --button-hover: #2176b8;
}

[data-theme='dark'] {
  --bg-color: #1e1e2f;
  --card-bg: #2c2c3a;
  --text-color: #f5f5f5;
  --input-bg: #3a3a4a;
  --input-border: #555;
  --button-bg: #ff932f;
  --button-hover: #ff9e0c;
}

.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--bg-color);
}

.login-card {
  background: var(--card-bg);
  padding: clamp(1.5rem, 4vw, 2.5rem);
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: min(100% - 2rem, 350px);
  text-align: center;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease,
    color 0.2s ease;
}

.login-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.login-card h1 {
  margin-bottom: 15px;
  font-size: 28px;
  color: var(--text-color);
}

.login-form div {
  margin-bottom: 15px;
  text-align: left;
}

.login-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: var(--text-color);
}

.login-form input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid var(--input-border);
  font-size: 16px;
  box-sizing: border-box;
  background: var(--input-bg);
  color: var(--text-color);
}

.login-form button {
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  border: none;
  background-color: var(--button-bg);
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: 0.5s ease;
}

.login-form button:hover {
  background-color: var(--button-hover);
}


theme-toggle {
  margin-bottom: 20px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background-color: var(--button-bg);
  color: white;
  font-size: 14px;
  transition: background-color 0.2s ease;
}

.theme-toggle:hover {
  background-color: var(--button-hover);
}

.login-form .register-link {
  margin-top: 15px;
  text-align: center;
}


.login-form .register-link a {
  color: var(--button-bg);
  font-weight: bold;
  text-decoration: none;
}

.login-form .register-link a:hover {
  text-decoration: underline;
}

.login-form .error {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 4px;
}

@media (max-width: 600px) {
  .login-container {
    padding: 1rem;
  }

  .login-form div > div {
    flex-direction: column;
    align-items: stretch !important;
  }

  .login-form div > div button {
    width: 100% !important;
  }
}

.logoEU{
    position: relative;
    top: 0px;
    display: flex;
    max-width: 75px;
    border-radius: 24px;
    overflow: hidden;
    margin: 0 auto 0 auto;
}

.logoEU img{
    width: 100%;
}
</style>
