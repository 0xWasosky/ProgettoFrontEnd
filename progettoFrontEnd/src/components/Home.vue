<script setup>
import { ref, onMounted } from 'vue'

const username = ref(localStorage.getItem('username') || 'Guest')
const greeting = ref('')

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

// Fetch existing audio on mount
onMounted(async () => {
  greeting.value = username.value

  //In questa parte di codice viene fatto il fetch ogni volta che l'utente esegue il login e di conseguenza
  //se è presente ricaricherà il file e rigenererà il qr per scaricare il file
  try{
    const response=await fetch("http://localhost:5000/files/get", {
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

      generateQR("http://localhost:5000/files/get")
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

      //Viene creato il file mp3 e vine inviato al server
      const formData = new FormData()
      formData.append('file', audio, 'recording.mp3')

      await fetch("http://localhost:5000/files/add", {
        method: "PUT",
        body: formData,
        credentials: "include"
      })

      generateQR("http://localhost:5000/files/get") //in questo QR vi è l'URL che permetterà di scaricare l'audio una vola che il server sarà attivo
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
        <img src="../../assets/images/icon.png" width="100%" />
      </router-link>
    </div>
  </nav>

  <button class="theme-toggle" @click="toggleTheme">
    {{ isDarkMode ? '☼' : '☀︎' }}
  </button>

  <h1 id="greeting">Hello {{ greeting }}</h1>

  <div class="container">
    <div class="QRcontainer">
      <div class="containerV">
        <h1>Record Voice & Generate QR</h1>

        <button @click="toggleRecording" class="voice-btn">
          {{ isRecording ? 'Stop Recording' : 'Start Recording' }}
        </button>

        <audio ref="audioPlayer" controls style="display:none;"></audio>

        <a v-if="downloadUrl" :href="downloadUrl" :download="`recording_${username.value}.mp3`" class="download-btn">
          Download Audio
        </a>

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
  transition: 0.5s ease;
}

#greeting{
  position: absolute;
  top: 75px;
  left: 42%;
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
}

.QRcontainer {
  margin-top: 100px;
  background: var(--card-bg);
  padding: 100px;
  border-radius: 16px;
  width: 75%;
  display: flex;
  align-items: center;
  border: 1px solid var(--borders);
  transition: 0.5s ease;
}

.containerV {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  color: var(--min);
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
  position: absolute;
  left: 550px;
  top: 240px;
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
</style>
