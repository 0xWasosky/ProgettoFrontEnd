<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { buildApiUrl } from '../utils/api'
import { handleUnauthorizedResponse } from '../utils/session'
import {
  initLightDarkMode,
  toggleLightDarkMode,
} from '../jsGraphicManaging/toggleLightDarkMode'

const isDarkMode = ref(false)

onMounted(() => {
  isDarkMode.value = initLightDarkMode()
})

const onToggleTheme = () => {
  isDarkMode.value = toggleLightDarkMode()
}

const oldPassword = ref('')
const newPassword = ref('')
const showOldPassword = ref(false)
const showNewPassword = ref(false)

const apiMessage = ref('')
const apiError = ref('')

const getApiMessage = (result) =>
  result?.data?.message ?? result?.message ?? 'Richiesta fallita'

const submitChangePassword = async () => {
  apiMessage.value = ''
  apiError.value = ''

  if (!oldPassword.value || !newPassword.value) {
    apiError.value = 'Password attuale e nuova password sono obbligatorie'
    return
  }

  try {
    const response = await fetch(buildApiUrl('/user/change_password'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        old_password: oldPassword.value,
        new_password: newPassword.value,
      }),
    })

    if (handleUnauthorizedResponse(response)) {
      return
    }

    const result = await response.json().catch(() => null)

    if (!response.ok) {
      apiError.value = getApiMessage(result)
      return
    }

    apiMessage.value = 'Password aggiornata con successo'
    oldPassword.value = ''
    newPassword.value = ''
  } catch (e) {
    apiError.value = 'Aggiornamento password fallito'
    console.error(e)
  }
}
</script>

<template>
  <nav>
    <div id="accountIcon">
      <router-link to="/settings">
        <img src="../../assets/images/home.png" width="100%" />
      </router-link>
    </div>
  </nav>

  <button class="theme-toggle" @click="onToggleTheme">
    {{ isDarkMode ? '☼' : '☀︎' }}
  </button>

  <div class="container">
    <div class="containerV">
      <div class="centered">
          <h1>Cambia password</h1>

      <div class="containerB">
        <form @submit.prevent="submitChangePassword" class="register-form">
          <div>
            <label>Password attuale:</label>
            <div style="display:flex; gap:8px; align-items:center;">
              <input
                :type="showOldPassword ? 'text' : 'password'"
                v-model="oldPassword"
              />
              <button
                type="button"
                style="width:auto;"
                @click="showOldPassword = !showOldPassword"
              >
                {{ showOldPassword ? 'Nascondi' : 'Mostra' }}
              </button>
            </div>
          </div>

          <div>
            <label>Nuova password:</label>
            <div style="display:flex; gap:8px; align-items:center;">
              <input
                :type="showNewPassword ? 'text' : 'password'"
                v-model="newPassword"
              />
              <button
                type="button"
                style="width:auto;"
                @click="showNewPassword = !showNewPassword"
              >
                {{ showNewPassword ? 'Nascondi' : 'Mostra' }}
              </button>
            </div>
          </div>

          <button type="submit">Aggiorna password</button>

          <p v-if="apiError" class="error">{{ apiError }}</p>
          <p v-if="apiMessage" class="success">{{ apiMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<style src="../stylesheets/defaultStyle.css"></style>
