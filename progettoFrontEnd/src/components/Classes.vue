<script setup>
import { nextTick, onMounted, ref } from 'vue'
import { buildApiUrl } from '@/utils/api'
import { handleUnauthorizedResponse } from '@/utils/session'

// dati di esempio (poi li colleghi alla tua API)
/*const classes = ref([
  { id: 1, name: '1A', students: 22 },
  { id: 2, name: '2B', students: 18 },
  { id: 3, name: '3C', students: 25 },
  { id: 4, name: '4A', students: 20 },
  { id: 5, name: '5B', students: 19 }
])*/

const classes = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const detailsErrorMessage = ref('')
const selectedClass = ref('')
const classStudents = ref([])
const isDetailsLoading = ref(false)
const audioActionErrorMessage = ref('')
const downloadingStudent = ref('')

const getApiMessage = (result) =>
  result?.data?.message ?? result?.message ?? 'Request failed'

const classImageUrl = (className) =>
  buildApiUrl(`/files/class-image/get?class=${encodeURIComponent(className)}`)

const studentAudioUrl = (student) => {
  if (!student?.username) {
    return ''
  }

  return buildApiUrl(`/files/audio/student?username=${encodeURIComponent(student.username)}`)
}

const sanitizeForDomId = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, '-')

const studentQrId = (student) =>
  `student-audio-qr-${sanitizeForDomId(
    `${selectedClass.value}-${student.username ?? student.name ?? 'student'}`
  )}`

const renderStudentQRCodes = async () => {
  await nextTick()

  classStudents.value.forEach((student) => {
    const qrContainer = document.getElementById(studentQrId(student))

    if (!qrContainer) {
      return
    }

    qrContainer.innerHTML = ''

    if (!student.hasAudio || !student.username) {
      return
    }

    new QRCode(qrContainer, {
      text: studentAudioUrl(student),
      width: 160,
      height: 160,
    })
  })
}

onMounted(async () => {
    try {
        const res = await fetch(buildApiUrl('/class/getClasses'), {
            method: 'GET',
            credentials: 'include'
        })

        if (handleUnauthorizedResponse(res)) {
          errorMessage.value = 'Your session expired. Please log in again.'
          return
        }

        const data = await res.json()

        if (!res.ok) {
          throw new Error(getApiMessage(data))
        }

        classes.value = data.data.message.classes
    } catch(err) {
        console.error('Error in fetch: ', err);
        errorMessage.value =
          err instanceof Error ? err.message : 'Unable to load classes right now.'
    } finally {
        isLoading.value = false
    }
})

const loadClassDetails = async (className) => {
  try {
    detailsErrorMessage.value = ''
    audioActionErrorMessage.value = ''

    if (selectedClass.value === className) {
      selectedClass.value = ''
      classStudents.value = []
      return
    }

    isDetailsLoading.value = true

    const response = await fetch(
      buildApiUrl(`/class/getClass?class=${encodeURIComponent(className)}`),
      {
        method: 'GET',
        credentials: 'include'
      }
    )

    if (handleUnauthorizedResponse(response)) {
      detailsErrorMessage.value = 'Your session expired. Please log in again.'
      return
    }

    const result = await response.json()

    if (!response.ok) {
      throw new Error(getApiMessage(result))
    }

    selectedClass.value = className
    classStudents.value = result?.data?.message?.students ?? []
    await renderStudentQRCodes()
  } catch (err) {
    console.error('Error in class details fetch:', err)
    detailsErrorMessage.value =
      err instanceof Error ? err.message : 'Unable to load class details right now.'
  } finally {
    isDetailsLoading.value = false
  }
}

const downloadStudentAudio = async (student) => {
  if (!student?.hasAudio || !student?.username) {
    return
  }

  audioActionErrorMessage.value = ''
  downloadingStudent.value = student.username

  try {
    const response = await fetch(studentAudioUrl(student), {
      method: 'GET',
      credentials: 'include',
    })

    if (handleUnauthorizedResponse(response)) {
      audioActionErrorMessage.value = 'Your session expired. Please log in again.'
      return
    }

    if (!response.ok) {
      const result = await response.json().catch(() => null)
      throw new Error(getApiMessage(result))
    }

    const blob = await response.blob()
    const objectUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')

    link.href = objectUrl
    link.download = `${student.username}.mp3`
    document.body.appendChild(link)
    link.click()
    link.remove()

    window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1000)
  } catch (err) {
    console.error('Error downloading student audio:', err)
    audioActionErrorMessage.value =
      err instanceof Error ? err.message : 'Unable to download audio right now.'
  } finally {
    downloadingStudent.value = ''
  }
}
</script>

<template>
  <h1 class="centered">Classes</h1>

  <div id="classes-btn">
    <router-link to="/home">
      Back to home page
    </router-link>
  </div>

  <p v-if="isLoading" class="status-message">Loading classes...</p>
  <p v-else-if="errorMessage" class="status-message error-text">{{ errorMessage }}</p>

  <div v-else class="classes-container">
    <div 
      v-for="classe in classes" 
      :key="classe.id" 
      :class="['class-card', { 'class-card--expanded': selectedClass === classe.name }]"
    >
      <img
        v-if="classe.hasImage"
        :src="classImageUrl(classe.name)"
        :alt="`${classe.name} class image`"
        class="class-image"
        loading="lazy"
      >

      <h2>{{ classe.name }}</h2>
      <p>Students: {{ classe.students }}</p>

      <button @click="loadClassDetails(classe.name)">
        {{ selectedClass === classe.name ? 'Hide details' : 'View details' }}
      </button>

      <p
        v-if="selectedClass === classe.name && isDetailsLoading"
        class="empty-state"
      >
        Loading students...
      </p>

      <p
        v-else-if="selectedClass === classe.name && detailsErrorMessage"
        class="empty-state error-text"
      >
        {{ detailsErrorMessage }}
      </p>

      <p
        v-if="selectedClass === classe.name && audioActionErrorMessage"
        class="empty-state error-text"
      >
        {{ audioActionErrorMessage }}
      </p>

      <div
        v-else-if="selectedClass === classe.name && classStudents.length"
        class="students-grid"
      >
        <article
          v-for="student in classStudents"
          :key="student.username ?? student.name"
          class="student-card"
        >
          <h3>{{ student.name }}</h3>
          <p v-if="student.username" class="student-username">
            {{ student.username }}
          </p>

          <div
            v-if="student.hasAudio && student.username"
            :id="studentQrId(student)"
            class="student-qr"
          ></div>

          <p v-else class="student-audio-status">
            No audio uploaded yet.
          </p>

          <button
            v-if="student.hasAudio && student.username"
            class="download-audio-btn"
            :disabled="downloadingStudent === student.username"
            @click="downloadStudentAudio(student)"
          >
            {{ downloadingStudent === student.username ? 'Downloading...' : 'Download audio' }}
          </button>
        </article>
      </div>

      <p
        v-else-if="selectedClass === classe.name"
        class="empty-state"
      >
        No students found for this class.
      </p>
    </div>
  </div>
</template>

<style src="../stylesheets/defaultStyle.css"></style>

<style scoped>
.classes-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  padding: 80px 20px 20px;
}

.status-message {
  padding: 80px 20px 20px;
  text-align: center;
  color: var(--text-color);
}

.error-text {
  color: #e74c3c;
}

.class-card {
  background: var(--card-bg);
  border: 1px solid var(--borders);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  transition: 0.3s ease;
}

.class-card:hover {
  transform: scale(1.05);
}

.class-card--expanded {
  grid-column: 1 / -1;
}

.class-card--expanded:hover {
  transform: none;
}

.class-image {
  width: 100%;
  height: 180px;
  margin-bottom: 16px;
  border: 1px solid var(--borders);
  border-radius: 10px;
  object-fit: cover;
}

.class-card h2 {
  margin-bottom: 10px;
  color: var(--text-color);
}

.class-card p {
  margin-bottom: 15px;
}

.class-card button {
  padding: 10px 18px;
  background: var(--button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.class-card button:hover:not(:disabled) {
  transform: translateY(-1px);
}

.class-card button:disabled {
  cursor: wait;
  opacity: 0.7;
}

.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.student-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 18px;
  border: 1px solid var(--borders);
  border-radius: 12px;
  background: color-mix(in srgb, var(--card-bg) 88%, var(--bg-color) 12%);
}

.student-card h3 {
  margin: 0;
  color: var(--text-color);
}

.student-username {
  margin: 0;
  font-size: 0.95rem;
  word-break: break-word;
}

.student-qr {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 180px;
  min-height: 180px;
  padding: 10px;
  border: 1px solid var(--borders);
  border-radius: 12px;
  background: white;
}

.student-qr :deep(canvas),
.student-qr :deep(img),
.student-qr :deep(table) {
  max-width: 100%;
  height: auto;
}

.student-audio-status {
  margin: 0;
  color: var(--text-color);
}

.download-audio-btn {
  width: 100%;
}

.empty-state {
  margin-top: 15px;
  color: var(--text-color);
}

@media (max-width: 720px) {
  .class-card--expanded {
    grid-column: auto;
  }

  .student-qr {
    width: min(100%, 180px);
  }
}
</style>
