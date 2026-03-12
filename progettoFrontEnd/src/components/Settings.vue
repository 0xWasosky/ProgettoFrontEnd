<script setup>
import { ref, inject, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const username = ref(localStorage.getItem('username') || 'Guest')

const isDarkMode = ref(false)
//const user = ref({ id: null, username: '' })

onMounted(() => {
  isDarkMode.value = localStorage.getItem('theme') === 'dark'
  document.documentElement.setAttribute(
    'data-theme',
    isDarkMode.value ? 'dark' : 'light'
  )

})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}
</script>

<template>
    <nav>
        <div id="accountIcon">
            <router-link to="/home">
                <img src="../../assets/images/home.png" width="100%">
            </router-link>
        </div>
    </nav>

    <button class="theme-toggle" @click="toggleTheme">
        {{ isDarkMode ? '☼' : '☀︎' }}
    </button>

    <div class="container">
        <div class="containerV">
            <div class="centered"><h1>User Information</h1></div>
            <div class="containerB">
                <div class="containerV">
                    <h3>User Name: {{ username }}</h3>
                    <h3>Password: </h3>
                    <h3>Class: </h3>
                </div>
            </div>
        </div>
    </div>

</template>

<style>
:root {
  --bg-color: #f5f0f0;
  --card-bg: #fff;
  --text-color: #2c3e50;
  --input-bg: #fff;
  --input-border: #ccc;
  --button-bg: #3490dc;
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
  --button-bg: #ff932f;
  --button-hover: #ff9e0c;
  --nav-bg: #333;
  --borders: #fff;
  --empty: #3a3a3a;
  --max: #000;
  --min: #ffffff;
}

body {
  background: var(--bg-color);
  margin: 0;
}

#accountIcon {
  border-radius: 50%;
  border: 2px solid var(--borders);
  overflow: hidden;
  max-width: 50px;
  max-height: 50px;
  position: fixed;
  right: 15px;
  top: 15px;
  cursor: pointer;
  transition: 0.5s ease;
}

#accountIcon:hover {
  transform: scale(1.1);
}

.centered{
    min-width: 100%;
    display: flex;
    /*border: 1px solid black;*/
    justify-content: center;
}

.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.containerB{
  background: var(--card-bg);
  padding: 50px;
  border-radius: 16px;
  min-width: 75%;
  display: flex;
  align-items: center;
  border: 1px solid var(--borders);
  margin-left: 10%;
}

.containerV {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  color: var(--min);
  min-width: 100%;
}

input {
  width: 250px;
  padding: 12px;
  margin-bottom: 20px;
  border-radius: 8px;
  border: 1px solid var(--input-border);
  background: var(--input-bg);
  color: var(--text-color);
}

button {
  padding: 10px 20px;
  background-color: var(--button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.5s;
  margin-bottom: 15px;
}

button:hover {
  background-color: var(--button-hover);
  transform: scale(1.04);
}

.voice-btn {
  width: 250px;
}

.drop-zone {
  padding: 35px;
  border: 2px dashed var(--input-border);
  border-radius: 14px;
  text-align: center;
  cursor: pointer;
  background: var(--empty);
  color: var(--text-color);
  width: 250px;
  transition: 0.5s;
}

.drop-zone:hover {
  border: 2px dashed var(--button-hover);
  transform: scale(1.03);
}

.drop-zone.dragging {
  border-color: var(--button-bg);
  background: var(--button-bg);
  color: white;
}

#qrcode {
  margin-left: 400px;
  border: 5px solid var(--borders);
  border-radius: 12px;
  min-height: 250px;
  min-width: 250px;
  background-color: var(--empty);
}

.theme-toggle {
  position: absolute;
  left: 10px;
  top: 10px;
  min-height: 40px;
  min-width: 40px;
  background-color: var(--min);
  color: var(--max);
  border-radius: 6px;
  cursor: pointer;
  transition: 0.5s;
}

.theme-toggle:hover {
  transform: scale(1.04);
}
</style>