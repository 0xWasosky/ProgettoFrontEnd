<script setup>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'

const isDarkMode = ref(false)
const router = useRouter()

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

const goTo = (routeName) => {
  router.push({name: routeName})
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

    <div class="centered" id="title"><br>Annuario scolastico del I.I.S. Europa Unita di Chivasso</div>

    <div class="container" style=" margin: 0px; padding: 0px;">

        <div class="image" style="margin: 0 auto 0 auto; position: relative; top: -50px;">
            <img src="../../assets/images/logoEU.jpg" width="100%">
        </div>

        <div class="paragraph">
            <p style="font-weight: bold;">Gli alunni e il personale scolastico potrà accedere alla propria area riservata e inserire il contenuto multimediale facolativo (audio).
             E' possibile anche scaricare gratuitamente l'annuario.
            </p>
        </div>

        <button type="button" class="index-btn" @click="goTo('Login')">
            Accedi all'annuario
        </button>

        <button type="button" class="index-btn" @click="goTo('About')">
            Istruzioni
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
    max-width: 850px;
    text-align: center;
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

.container{
    /*border: 1px solid black;*/
    margin: 10px;
    display:flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    padding: 0px;
}

.image{
    /*border: 1px solid var(--min);*/
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

#title{
    margin: 20px auto 0 auto;
    padding: 0px; 
    /*border: 1px solid black;*/ 
    max-height: fit-content;
    font-size: xx-large;
    font-weight: bold;
    color: var(--min);
}
</style>
