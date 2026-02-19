<script setup>
import { ref, onMounted } from 'vue'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const errors = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

const emit = defineEmits(['register'])

// Form registration
const handleRegister = () => {
  errors.value = { username: '', password: '', confirmPassword: '' }
  let isValid = true

  if (!username.value) {
    errors.value.username = 'Username is required'
    isValid = false
  }

  if (!password.value) {
    errors.value.password = 'Password is required'
    isValid = false
  }

  if (password.value !== confirmPassword.value) {
    errors.value.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  if (!isValid) return

  emit('register', {
    username: username.value,
    password: password.value,
  })

  username.value = ''
  password.value = ''
  confirmPassword.value = ''
}

// Theme toggle
const isDarkMode = ref(false)

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

// Load theme on mount
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
  <button type="button" @click="toggleTheme" class="theme-toggle">
    {{ isDarkMode ? '🌙 Dark Mode' : '☀️ Light Mode' }}
  </button>

  <div class="register-container">
    <div class="register-card">
      <h1>Register</h1>

      <form @submit.prevent="handleRegister" class="register-form">
        <div>
          <label>Username:</label>
          <input type="text" v-model="username" />
          <p v-if="errors.username" class="error">{{ errors.username }}</p>
        </div>

        <div>
          <label>Password:</label>
          <input type="password" v-model="password" />
          <p v-if="errors.password" class="error">{{ errors.password }}</p>
        </div>

        <div>
          <label>Confirm Password:</label>
          <input type="password" v-model="confirmPassword" />
          <p v-if="errors.confirmPassword" class="error">{{ errors.confirmPassword }}</p>
        </div>

        <button type="submit">Register</button>
      </form>

      <div class="register-link">
        <p>
          Already have an account?
          <router-link to="/">Login here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style>
:root {
  --bg-color: #f0f2f5;
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

.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--bg-color);
}

.register-card {
  background: var(--card-bg);
  padding: 40px 50px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease,
    color 0.2s ease;
}

.register-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.register-card h1 {
  margin-bottom: 15px;
  font-size: 28px;
  color: var(--text-color);
}

.register-form div {
  margin-bottom: 15px;
  text-align: left;
}

.register-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: var(--text-color);
}

.register-form input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid var(--input-border);
  font-size: 16px;
  box-sizing: border-box;
  background: var(--input-bg);
  color: var(--text-color);
}

.register-form button {
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

.register-form button:hover {
  background-color: var(--button-hover);
}

.theme-toggle {
  margin-bottom: 20px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background-color: var(--button-bg);
  color: white;
  font-size: 14px;
  transition: 0.5s ease;
}

.theme-toggle:hover {
  background-color: var(--button-hover);
}

.register-card .register-link {
  margin-top: 15px;
  text-align: center;
}

.register-card .register-link a {
  color: var(--button-bg);
  font-weight: bold;
  text-decoration: none;
}

.register-card .register-link a:hover {
  text-decoration: underline;
}

.register-form .error {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 4px;
}
</style>
