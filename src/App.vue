<script setup>
import router from './router'

const handleLogin = (data) => {
  console.log('Received in App.vue:', data)

  try {
    //Il trasferimento dati verra' fatto presto ho voluto pensare prima di aggiustare i bug della registrazione
    //vocale perché richiedono molto tempo

    router.push('/home')
  } catch (error) {
    console.log('Login failed')
  }
}

const handleRegister = (data) => {
  console.log('Register received in App.vue:', data)

  try {
    //trasferimento dati all'API

    router.push('/home')
  } catch (error) {
    console.log('Registration failed')
  }
}
</script>

<template>
  <div class="app">
    <!--<h3>APP NAME</h3>-->

    <!--<p>
      Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
      documentation
    </p>-->
    <!--<Login @login="handleLogin"></Login>-->
    <router-view v-slot="{ Component }">
      <component :is="Component" @login="handleLogin" @register="handleRegister" />
    </router-view>
  </div>
</template>

<style scoped>
/*Write here the style of App.vue*/
</style>
