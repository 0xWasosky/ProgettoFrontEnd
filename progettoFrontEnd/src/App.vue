<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import router from './router'
import { buildApiUrl } from './utils/api'
import {
  SESSION_EXPIRED_EVENT,
  handleUnauthorizedResponse,
} from './utils/session'

/** API wraps messages in { status, data: { message } } — not top-level message. */
const getApiMessage = (result) =>
  result?.data?.message ?? result?.message ?? 'Request failed'

const authError = ref('')
const isAuthenticated = ref(false)
const isAuthReady = ref(false)

const redirectToLogin = (message = '') => {
  isAuthenticated.value = false
  authError.value = message
  localStorage.removeItem('username')

  if (router.currentRoute.value.path !== '/') {
    router.replace('/')
  }
}

const checkAuthentication = async () => {
  try {
    //Utilizzo dell'end point classes per verificre se la sessione è ancora valida dal momento che
    //per accedere all'endpoint è necessario un JWT valido
    const response = await fetch(buildApiUrl('/class/getClasses'), {
      method: 'GET',
      credentials: 'include'
    })

    if (handleUnauthorizedResponse(response)) {
      redirectToLogin('Session expired. Please log in again.')
      return false
    }

    if(!response.ok) {
      isAuthenticated.value = false
      localStorage.removeItem('username')
      return false
    }

    isAuthenticated.value = true
    return true
  } catch(error){
    isAuthenticated.value = false
    return false
  } finally{
    isAuthReady.value = true
  }
}

const onSessionExpired = () => {
  redirectToLogin('Session expired. Please log in again.')
}

const handleLogin = async (data) => {
  authError.value = ''
  try {
    const response = await fetch(buildApiUrl('/auth/login'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        username: data.username,
        password: data.password
      })
    })

    const result = await response.json()

    if (!response.ok) {
      throw new Error(getApiMessage(result))
    }

    isAuthenticated.value = true
    localStorage.setItem('username', data.username)
    router.push('/home')
  } catch (error) {
    isAuthenticated.value = false
    authError.value =
      error instanceof Error ? error.message : 'Login failed'
    console.error('Login failed', error)
  }
}

const handleRegister = async (data) => {
  authError.value = ''
  try {
    //Comunicazione con l'API
    //la parte "localhost:5000" verrà modificata con l'IP del server
    const response = await fetch(buildApiUrl('/auth/register'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include', // per i cookie JWT
      body: JSON.stringify({
        username: data.username,
        password: data.password
      })
    })

    const result = await response.json()

    if (!response.ok) {
      throw new Error(getApiMessage(result))
    }

    isAuthenticated.value = true
    localStorage.setItem('username', data.username)
    router.push('/home')
  } catch (error) {
    isAuthenticated.value = false
    authError.value =
      error instanceof Error ? error.message : 'Registration failed'
    console.error('Registration failed', error)
  }
}

onMounted(() => {
  window.addEventListener(SESSION_EXPIRED_EVENT, onSessionExpired)
  checkAuthentication()
})

onUnmounted(() => {
  window.removeEventListener(SESSION_EXPIRED_EVENT, onSessionExpired)
})
</script>

<template>
  <p v-if="!isAuthReady" class="auth-status">Checking session...</p>
  <div class="app">
    <p v-if="authError" class="auth-error" role="alert">{{ authError }}</p>
    <router-view
      v-if="isAuthReady"
      v-slot="{ Component }"
      :key="$route.fullPath"
    >
      <component
        :is="Component"
        :is-authenticated="isAuthenticated"
        @login="handleLogin"
        @register="handleRegister"
        @clear-auth-error="authError = ''"
      />
    </router-view>
  </div>
</template>

<style scoped>
/*Write here the style of App.vue*/

.auth-status{
  padding: 1rem;
}
</style>
