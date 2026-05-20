<script setup>
//eqvU148VnKHornxdmaUX08ElRsj6tDkVMqpUksf4qdM Admin
import { ref, onMounted } from 'vue'
import { buildApiUrl } from '@/utils/api'
import { handleUnauthorizedResponse } from '@/utils/session'
import defaultProfileImage from '../../assets/images/icon.png'
import { cacheProfilePictureBlob, getCachedProfilePicture } from '../utils/profilePictureCache'

const username = ref(localStorage.getItem('username') || 'Guest')
const greeting = ref('')
const accountIconSrc = ref(getCachedProfilePicture() || defaultProfileImage)

const audioPlayer = ref(null)
const downloadUrl = ref('')

const isRecording = ref(false)
let mediaRecorder = null
let audioChunks = []

let qrInstance = null

// Generate QR code
const generateQR = (text) => {
  const qrContainer = document.getElementById('qrcode')
  qrContainer.innerHTML = ''
  if (!text) return

  qrInstance = new QRCode(qrContainer, {
    text: text,
    width: 250,
    height: 250,
  })
}

const loadProfilePicture = async () => {
  const cachedProfilePicture = getCachedProfilePicture()

  try {
    const response = await fetch(buildApiUrl('/files/image/get'), {
      method: 'GET',
      credentials: 'include'
    })

    if (handleUnauthorizedResponse(response)) {
      return
    }

    if (!response.ok) {
      accountIconSrc.value = cachedProfilePicture || defaultProfileImage
      return
    }

    const blob = await response.blob()
    accountIconSrc.value =
      (await cacheProfilePictureBlob(blob)) ||
      cachedProfilePicture ||
      defaultProfileImage
  } catch {
    accountIconSrc.value = cachedProfilePicture || defaultProfileImage
  }
}

// Fetch existing audio on mount
onMounted(async () => {
  greeting.value = username.value
  isDarkMode.value = localStorage.getItem('theme') === 'dark'
  document.documentElement.setAttribute(
    'data-theme',
    isDarkMode.value ? 'dark' : 'light'
  )

  await loadProfilePicture()

  try{
    const response=await fetch(buildApiUrl('/files/audio/get'), {
      credentials: "include"
    })

    if(response.ok){
      const blob = await response.blob()
      const audioURL = URL.createObjectURL(blob)

      downloadUrl.value = audioURL
      if (audioPlayer.value) {
        audioPlayer.value.src = audioURL
        audioPlayer.value.style.display = "block"
      }

      generateQR(buildApiUrl('/files/audio/get'))
    }
  }
  catch(err){
    console.log("No saved audio for this user")
  }
})

// Toggle recording
const toggleRecording = async () => {
  if (!isRecording.value) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data)

    mediaRecorder.onstop = async () => {
      const audio = new Blob(audioChunks, { type: 'audio/mp3' })

      const audioUrl = URL.createObjectURL(audio)
      downloadUrl.value = audioUrl

      if (audioPlayer.value) {
        audioPlayer.value.src = audioUrl
        audioPlayer.value.style.display = 'block'
      }

      const formData = new FormData()
      formData.append('file', audio, 'recording.mp3')

      await fetch(buildApiUrl('/files/audio/add'), {
        method: "PUT",
        body: formData,
        credentials: "include"
      })

      generateQR(buildApiUrl('/files/audio/get'))
    }

    mediaRecorder.start()
    isRecording.value = true
  } else {
    mediaRecorder.stop()
    isRecording.value = false
  }
}

// Theme toggle
const isDarkMode = ref(false)
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
      <router-link to="/settings">
        <img :src="accountIconSrc" alt="User profile picture" width="100%" />
      </router-link>
    </div>
  </nav>

  <!--<div id="classes-btn">
    <router-link to="/classes">
      See All classes
    </router-link>
  </div>

  <router-link to="admin">
    Admin
  </router-link>

  <router-link to="presentation">Presentation</router-link>-->
  <div class="top-nav">
    <router-link to="/classes">Classi</router-link>
    <router-link to="/admin">Admin</router-link>
    <router-link to="/presentation">Presentazione</router-link>
  </div>

  <button class="theme-toggle" @click="toggleTheme">
    {{ isDarkMode ? '☼' : '☀︎' }}
  </button>

  <h1 id="greeting">Ciao {{ greeting }}!</h1>
  <div class="logoEU"><img src="../../assets/images/logoEU.jpg"></div>

  <div class="container" style="position: relative; top: -120px">
    <div class="QRcontainer">
      <div class="home-content">
        <div class="containerV">
          <h1>Registra audio e genera QR</h1>

          <button @click="toggleRecording" class="voice-btn" id="recording-btn">
            {{ isRecording ? 'Interrompi registrazione' : 'Avvia registrazione' }}
          </button>

          <audio ref="audioPlayer" controls style="display:none;"></audio>

          <a v-if="downloadUrl" :href="downloadUrl" :download="`recording_${username}.mp3`" class="download-btn">
            Scarica audio
          </a>
        </div>

        <div id="qrcode"></div>
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
  --button-bg: #ff1717;
  --button-hover: #ff9e0c;
  --nav-bg: #333;
  --borders: #fff;
  --empty: #3a3a3a;
  --max: #000;
  --min: #ffffff;
}

.top-nav {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  align-items: center;
  padding: 10px 20px;
  background: var(--card-bg);
  border: 1px solid var(--borders);
  border-radius: 10px;
  z-index: 1000;
}

.top-nav a {
  text-decoration: none;
  color: var(--text-color);
  font-size: 18px;
  padding: 6px 12px;
  border-radius: 6px;
  transition: 0.3s ease;
}

.top-nav a:hover {
  background: var(--button-bg);
  color: white;
  transform: scale(1.05);
}

body {
  background: var(--bg-color);
  margin: 0;
  transition: 0.5s ease;
}

#greeting{
  margin: 5.5rem auto 0;
  padding: 0 1rem;
  text-align: center;
  color: var(--min);
  transition: 0.5s ease;
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

.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1.5rem 1rem 2rem;
}

.QRcontainer {
  margin-top: 1rem;
  background: var(--card-bg);
  padding: clamp(1.5rem, 5vw, 4rem);
  border-radius: 16px;
  width: min(100%, 1100px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: clamp(1.5rem, 5vw, 4rem);
  border: 1px solid var(--borders);
  transition: 0.5s ease;
}

.home-content {
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: clamp(1.5rem, 5vw, 4rem);
}

.containerV {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  color: var(--min);
  width: 100%;
  min-width: 0;
}

input {
  width: min(100%, 320px);
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
  width: min(100%, 320px);
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
  border: 5px solid var(--borders);
  border-radius: 12px;
  min-height: 250px;
  min-width: 250px;
  width: 250px;
  background-color: var(--empty);
  align-self: center;
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

.download-btn {
  padding: 10px 20px;
  margin: 10px 0;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  text-decoration: none;
  display: inline-block;
  background-color: #28a745; /* verde per distinguere il download */
  color: white;
  cursor: pointer;
  transition: 0.3s;
}

.download-btn:hover {
  background-color: #218838;
  transform: scale(1.03);
}

#classes-btn{
  position: fixed;
  text-decoration: none;
  border: 1px solid var(--min);
  border-radius: 7px;
  top: 10px;
  color: var(--min);
  padding: 10px;
  font-size: 20px;
  background-color: var(--button-bg);
  transition: 0.5s ease;
  left: 40%;
  text-decoration: none;
}

#classes-btn:hover{
  cursor: pointer;
  transform: scale(1.04);
}

@media (max-width: 900px) {
  #greeting {
    margin-top: 5rem;
  }

  .container {
    align-items: flex-start;
  }

  .QRcontainer,
  .home-content {
    flex-direction: column;
    align-items: stretch;
  }

  .containerV {
    align-items: stretch;
  }

  #qrcode {
    width: min(100%, 250px);
    min-width: 0;
  }
}

@media (max-width: 600px) {
  .voice-btn,
  button,
  .download-btn {
    width: 100%;
    text-align: center;
  }

  audio {
    width: 100%;
  }
}

@media (max-width: 500px){
  .containerV {
    font-size: 20px;
  }

  #recording-btn {
    font-size: 18px;
  }
}

.logoEU{
    display: flex;
    max-width: 12%;
    min-width: 100px;
    border-radius: 24px;
    overflow: hidden;
    margin: 0 auto 0 auto;
}

.logoEU img{
    width: 100%;
}
</style>
