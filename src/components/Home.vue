<script setup>
import { ref, onMounted, watch } from 'vue'

const qrText = ref('')
let qrInstance = null

const generateQR = () => {
  if (!qrText.value) return

  const qrContainer = document.getElementById('qrcode')
  qrContainer.innerHTML = ''

  qrInstance = new QRCode(qrContainer, {
    text: qrText.value,
    width: 250,
    height: 250,
  })
}

/* Aggiorna QR automaticamente nel momento in cui cambia il testo */
watch(qrText, () => {
  generateQR()
})

const isRecording = ref(false)
let recognition = null

onMounted(() => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

  if (SpeechRecognition) {
    recognition = new SpeechRecognition()
    recognition.lang = 'en-US'
    recognition.continuous = true
    recognition.interimResults = true

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript
      }
      qrText.value = transcript
    }

    recognition.onend = () => {
      if (isRecording.value) {
        recognition.start()
      }
    }
  } else {
    alert('This browser does not suppor vocal recognition.')
  }

  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  }
})

const toggleRecording = () => {
  if (!recognition) return

  if (!isRecording.value) {
    recognition.start()
    isRecording.value = true
  } else {
    recognition.stop()
    isRecording.value = false
  }
}

const isDarkMode = ref(false)

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

const selectedFile = ref(null)
const isDragging = ref(false)
const fileInput = ref(null)

const handleFile = (event) => {
  const file = event.target.files[0]
  if (file) selectedFile.value = file
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) selectedFile.value = file
}

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const openFileDialog = () => {
  fileInput.value.click()
}
</script>

<template>
  <nav>
    <div id="accountIcon">
      <img src="../../assets/images/icon.png" width="100%" />
    </div>
  </nav>

  <button class="theme-toggle" @click="toggleTheme">
    {{ isDarkMode ? '☼' : '☀︎' }}
  </button>

  <div class="container">
    <div class="QRcontainer">
      <div class="containerV">
        <h1>Generate QR Code</h1>

        <input v-model="qrText" placeholder="Insert your text or use voice..." />

        <button @click="toggleRecording" class="voice-btn">
          {{ isRecording ? 'Stop' : 'Registra voce' }}
        </button>

        <!--È possibile caricare i file ma ancora non vengono letti-->
        <div
          class="drop-zone"
          :class="{ dragging: isDragging }"
          @click="openFileDialog"
          @dragover.prevent="handleDragOver"
          @dragleave="handleDragLeave"
          @drop.prevent="handleDrop"
        >
          <p v-if="!selectedFile">Click or drag file here</p>
          <p v-else>{{ selectedFile.name }}</p>

          <input type="file" ref="fileInput" @change="handleFile" hidden />
        </div>
      </div>

      <div id="qrcode"></div>
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

.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.QRcontainer {
  background: var(--card-bg);
  padding: 50px;
  border-radius: 16px;
  width: 75%;
  display: flex;
  align-items: center;
  border: 1px solid var(--borders);
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
