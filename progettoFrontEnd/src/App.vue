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
  result?.data?.message ?? result?.message ?? 'Richiesta fallita'

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
      redirectToLogin('Sessione scaduta. Effettua di nuovo il login.')
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
  redirectToLogin('Sessione scaduta. Effettua di nuovo il login.')
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
      error instanceof Error ? error.message : 'Accesso fallito'
    console.error('Login fallito', error)
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
      error instanceof Error ? error.message : 'Registrazione fallita'
    console.error('Registrazione fallita', error)
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
  <p v-if="!isAuthReady" class="auth-status">Verifica sessione...</p>
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
    <footer class="footer">Progetto scolastico presentato dal prof. Nicola M. nell'a.s. 2025/2026 a cui hanno lavorato gli alunni Jacopo Seglie della 4E info e Adriano Loiero 4C info</footer>
</template>

<style scoped>
/*Write here the style of App.vue*/
:root {
  --bg-color: #f5f0f0;
  --card-bg: #fff;
  --text-color: #2c3e50;
  --input-bg: #fff;
  --input-border: #ccc;
  --button-bg: #1c99ff;
  --button-hover: #2176b8;
  --nav-bg: #ddd;
  --borders: #000;
  --empty: #f2f2f2;
  --max: #ffffff;
  --min: #000;
}

[data-theme='dark'] {
  --bg-color: #1e1e2f;
  --card-bg: #2c2c3a;
  --text-color: #f5f5f5;
  --input-bg: #3a3a4a;
  --input-border: #555;
  --button-bg: #038f6e;
  --button-hover: #2d76ff;
  --nav-bg: #333;
  --borders: #fff;
  --empty: #3a3a3a;
  --max: #000;
  --min: #ffffff;
}

.auth-status{
  padding: 1rem;
}
.footer {  background: transparent;  color: var(--min);  text-align: center;  padding: 0.75rem 0;  width: 100%;}
</style>
