<script setup>
import {ref, onMounted} from 'vue'

const isDarkMode = ref(false)

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

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

    <div class="centered"><h1>Benvenuto nell'annuario del I.I.S Europa Unita di Chivasso</h1></div>

    <div class="container">

        <div class="image" style="margin: auto;">
            <img src="../../assets/images/logoEU.jpg" width="100%">
        </div>

        <div class="paragraph">
            <h2>Primo annuario dell'Europa Unita</h2>
            <p>Questo è il primo annuario scolastico dell'europa unita nel quale vengono caricate le 
                immagini delle foto di classe e gli studenti possono condividere la loro
                esepreinza sull'anno corrente
            </p>
        </div>

        <button class="index-btn">
            <router-link to="/login">Login</router-link>
        </button>

        <button class="index-btn">
            <router-link to="/about">Info</router-link>
        </button>
    </div>
    
    


</template>

<style>
body{
    display: flex;
    align-items: center;
    justify-content: center;
}

#title{
    margin: auto;
    max-width: fit-content;
}

.paragraph{
    display: flex;
    flex-direction: column;
    color: var(--min);
    max-width: 450px;
}

.paragraph h2{
    margin: 20px 0 5px 0;
}

.paragraph p{
    margin-top: 5px;
}

.index-btn{
    margin: 20px 10px 5px 10px;
    min-width: 300px;
}

.index-btn a{
    text-decoration: none;
    color: #fff;
}

.container{
    /*border: 1px solid black;*/
    margin: 20px;
    display:flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}

.image{
    border: 1px solid var(--min);
    max-width: 45%;
    border-radius: 24px;
    overflow: hidden;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.image img{
    align-self: center;
}
</style>
