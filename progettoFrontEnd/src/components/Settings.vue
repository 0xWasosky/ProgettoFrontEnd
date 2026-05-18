<script setup>
import { ref, onMounted } from 'vue'
import { notifySessionExpired } from '../utils/session'
import defaultProfileImage from '../../assets/images/icon.png'
import { getCachedProfilePicture } from '../utils/profilePictureCache'

const username = ref(localStorage.getItem('username') || 'Guest')
const profileImageSrc = ref(getCachedProfilePicture() || defaultProfileImage)

const isDarkMode = ref(false)

onMounted(() => {
  isDarkMode.value = localStorage.getItem('theme') === 'dark'
  document.documentElement.setAttribute(
    'data-theme',
    isDarkMode.value ? 'dark' : 'light'
  )
  profileImageSrc.value = getCachedProfilePicture() || defaultProfileImage
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

const handleLogout = () => {
  notifySessionExpired()
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

    <div class="centered"><h1>Informazioni utente</h1></div>

    <router-link to="/change_profile_picture" >
      <div class="circle moveUp">
        <img :src="profileImageSrc" alt="User profile picture" class="profile-picture">
      </div>
    </router-link>

    <!--<div class="container seeBorder">
        <div class="containerV seeBorder">
            <div class="containerB">
                <div class="containerV">
                    <h3>User Name: {{ username }}</h3>
                    <h3>Class: </h3>
                    
                    <router-link to="/change_password">
                      <button>Change Password</button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>-->

    <div class="containerV1 seeBorder">
        <h3>Nome utente: {{ username }}</h3>
        
        <router-link to="/change_password">
          <button>Cambia password</button>
        </router-link>

        <button @click="handleLogout">Esci</button>
    </div>

</template>

<style src="../stylesheets/defaultStyle.css"></style>
<style>
.circle{
  margin: 5px;
  height: 125px;
  width: 125px;
  border-radius: 50%;
  border: 2px solid black;
  overflow: hidden;
  margin-left: auto;
  margin-right: auto;
  transition: 0.2s ease;
}

.circle:hover{
  transform: scale(1.1);
  cursor: pointer;
}

.profile-picture{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

button{
  max-width: 200px;
}

@media (max-width: 600px) {
  button {
    max-width: none;
    width: 100%;
  }
}
</style>
