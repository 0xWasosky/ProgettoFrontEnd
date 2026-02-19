<script setup>
import router from './router'

const handleLogin = async (data) => {
  console.log('Received in App.vue:', data)

  try {
    //Comunicazione con l'API
    //la parte "localhost:5000" verrà modificata con l'IP del server
    const response = await fetch('http://localhost:5000/auth/login', {
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
      throw new Error(result.message || 'Login failed')
    }


    //Visuallizza la scheramata di home
    router.push('/home')
  } catch (error) {
    console.log('Login failed')
  }
}

const handleRegister = async (data) => {
  console.log('Register received in App.vue:', data)

  try {
    //trasferimento dati all'API
    //la parte "localhost:5000" verrà modificata con l'IP del server
    const response = await fetch('http://localhost:5000/auth/register', {
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
      console.log('Backend error:', result.data?.message)
      throw new Error(result.data?.message || 'Registration failed')
    }


    //Visualizza schermata home
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
