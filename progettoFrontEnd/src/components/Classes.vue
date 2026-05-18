<script setup>
import { computed, onMounted, ref } from 'vue'
import QRCode from 'qrcode'
import { buildApiUrl } from '@/utils/api'
import { handleUnauthorizedResponse } from '@/utils/session'

const defaultStudentProfileImage = new URL(
  '../../assets/default_profile_pictures/default.jpg',
  import.meta.url
).href

const classes = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const detailsErrorMessage = ref('')
const yearbookErrorMessage = ref('')
const selectedClass = ref('')
const classStudents = ref([])
const studentProfileImages = ref({})
const isDetailsLoading = ref(false)
const audioActionErrorMessage = ref('')
const downloadingStudent = ref('')
const classImageActionMessage = ref('')
const classImageActionErrorMessage = ref('')
const downloadingClassImage = ref('')
const isDownloadingAllClassImages = ref(false)

const getApiMessage = (result) =>
  result?.data?.message ?? result?.message ?? 'Richiesta fallita'

const classImageUrl = (className) =>
  buildApiUrl(`/files/class-image/get?class=${encodeURIComponent(className)}`)

const studentAudioUrl = (student) => {
  if (!student?.username) {
    return ''
  }

  return buildApiUrl(`/files/audio/student?username=${encodeURIComponent(student.username)}`)
}

const downloadableClasses = computed(() =>
  classes.value.filter((classSummary) => classSummary?.hasImage)
)

const clearClassImageActionMessages = () => {
  classImageActionMessage.value = ''
  classImageActionErrorMessage.value = ''
}

const revokeStudentProfileImageUrls = () => {
  Object.values(studentProfileImages.value).forEach((url) => {
    try {
      URL.revokeObjectURL(url)
    } catch {
      // ignore invalid urls
    }
  })
  studentProfileImages.value = {}
}

const studentProfileImageUrl = (student) =>
  student?.username ? studentProfileImages.value[student.username] : ''

const loadStudentProfileImages = async () => {
  revokeStudentProfileImageUrls()

  const images = {}

  for (const student of classStudents.value) {
    if (!student?.username) {
      continue
    }

    try {
      const response = await fetch(
        buildApiUrl(
          `/files/image/student?username=${encodeURIComponent(student.username)}`
        ),
        {
          method: 'GET',
          credentials: 'include',
        }
      )

      if (!response.ok) {
        continue
      }

      const blob = await response.blob()
      images[student.username] = URL.createObjectURL(blob)
    } catch {
      continue
    }
  }

  studentProfileImages.value = images
}

const studentQrDataUrls = ref({})

const loadStudentQrCodes = async () => {
  const qrUrls = {}

  for (const student of classStudents.value) {
    if (!student?.hasAudio || !student?.username) {
      continue
    }

    try {
      qrUrls[student.username] = await QRCode.toDataURL(studentAudioUrl(student), {
        width: 160,
        margin: 1,
      })
    } catch (error) {
      console.error('Error generating QR code for student:', student, error)
    }
  }

  studentQrDataUrls.value = qrUrls
}

const triggerBlobDownload = (blob, fileName) => {
  const objectUrl = URL.createObjectURL(blob)
  const link = document.createElement('a')

  link.href = objectUrl
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  link.remove()

  window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1000)
}

const fetchClassImageBlob = async (className) => {
  const response = await fetch(classImageUrl(className), {
    method: 'GET',
    credentials: 'include',
  })

  if (handleUnauthorizedResponse(response)) {
    throw new Error('La sessione è scaduta. Effettua di nuovo il login.')
  }

  if (!response.ok) {
    const result = await response.json().catch(() => null)
    throw new Error(getApiMessage(result))
  }

  return response.blob()
}

onMounted(async () => {
    try {
        const res = await fetch(buildApiUrl('/class/getClasses'), {
            method: 'GET',
            credentials: 'include'
        })

        if (handleUnauthorizedResponse(res)) {
          errorMessage.value = 'La sessione è scaduta. Effettua di nuovo il login.'
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
          err instanceof Error ? err.message : 'Impossibile caricare le classi in questo momento.'
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
      revokeStudentProfileImageUrls()
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
      detailsErrorMessage.value = 'La sessione è scaduta. Effettua di nuovo il login.'
      return
    }

    const result = await response.json()

    if (!response.ok) {
      throw new Error(getApiMessage(result))
    }

    selectedClass.value = className
    classStudents.value = result?.data?.message?.students ?? []
    await loadStudentQrCodes()
    await loadStudentProfileImages()
  } catch (err) {
    console.error('Error in class details fetch:', err)
    detailsErrorMessage.value =
      err instanceof Error ? err.message : 'Impossibile caricare i dettagli della classe in questo momento.'
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
      audioActionErrorMessage.value = 'La sessione è scaduta. Effettua di nuovo il login.'
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
      err instanceof Error ? err.message : "Impossibile scaricare l'audio in questo momento."
  } finally {
    downloadingStudent.value = ''
  }
}

const downloadClassImage = async (className) => {
  if (!className) {
    return
  }

  clearClassImageActionMessages()
  downloadingClassImage.value = className

  try {
    const blob = await fetchClassImageBlob(className)

    triggerBlobDownload(blob, `${className}.jpeg`)
    classImageActionMessage.value = `Foto della classe ${className} scaricata con successo.`
  } catch (err) {
    console.error('Error downloading class image:', err)
    classImageActionErrorMessage.value =
      err instanceof Error ? err.message : "Impossibile scaricare l'immagine della classe in questo momento."
  } finally {
    downloadingClassImage.value = ''
  }
}

const downloadAllClassImages = async () => {
  if (!downloadableClasses.value.length) {
    clearClassImageActionMessages()
    classImageActionErrorMessage.value = 'Nessuna foto di classe disponibile per il download.'
    return
  }

  clearClassImageActionMessages()
  isDownloadingAllClassImages.value = true

  try {
    const downloadedImages = []
    const failedClasses = []

    for (const classSummary of downloadableClasses.value) {
      try {
        const blob = await fetchClassImageBlob(classSummary.name)
        downloadedImages.push({
          name: classSummary.name,
          blob,
        })
      } catch (err) {
        if (err instanceof Error && err.message === 'Your session expired. Please log in again.') {
          throw err
        }

        failedClasses.push(classSummary.name)
      }
    }

    if (!downloadedImages.length) {
      throw new Error(
        failedClasses.length
          ? `Impossibile scaricare le foto di classe per: ${failedClasses.join(', ')}.`
          : 'Nessuna foto di classe disponibile per il download.'
      )
    }

    const { default: JSZip } = await import('jszip')
    const zip = new JSZip()

    downloadedImages.forEach((image) => {
      zip.file(`${image.name}.jpeg`, image.blob)
    })

    const zipBlob = await zip.generateAsync({ type: 'blob' })

    triggerBlobDownload(zipBlob, 'class-images.zip')
    classImageActionMessage.value = failedClasses.length
      ? `Scaricate ${downloadedImages.length} foto di classe. Saltate: ${failedClasses.join(', ')}.`
      : `Scaricate ${downloadedImages.length} foto di classe con successo.`
  } catch (err) {
    console.error('Error downloading all class images:', err)
    classImageActionErrorMessage.value =
      err instanceof Error ? err.message : 'Impossibile scaricare le foto delle classi in questo momento.'
  } finally {
    isDownloadingAllClassImages.value = false
  }
}

const downloadYearbook = async () => {
  yearbookErrorMessage.value = ''

  try {
    const response = await fetch(buildApiUrl('/files/yearbook'), {
      method: 'GET',
      credentials: 'include'
    })

    if (handleUnauthorizedResponse(response)) {
      throw new Error('La sessione è scaduta. Effettua di nuovo il login.')
    }

    if (!response.ok) {
      const result = await response.json().catch(() => null)
      throw new Error(getApiMessage(result))
    }

    const blob = await response.blob()
    triggerBlobDownload(blob, 'annuario.pdf')
  } catch (err) {
    console.error('Error downloading yearbook:', err)
    yearbookErrorMessage.value =
      err instanceof Error ? err.message : 'Impossibile scaricare l\'annuario in questo momento.'
  }
}
</script>

<template>
  <h1 class="centered">Classi</h1>

  <div class="top-nav-single">
    <router-link to="/home">Torna alla home</router-link>
  </div>

  <h1 class="page-title">Classi</h1>

  <div v-if="!isLoading && classes.length" class="classes-actions">
    <button
      class="download-all-images-btn"
      :disabled="!downloadableClasses.length || isDownloadingAllClassImages"
      @click="downloadAllClassImages"
    >
      {{
        isDownloadingAllClassImages
          ? 'Download delle foto di classe in corso...'
          : 'Scarica tutte le foto di classe'
      }}
    </button>
    <button
      class="download-all-images-btn download-yearbook-btn"
      @click="downloadYearbook"
    >
      Scarica annuario
    </button>
  </div>
  <p v-if="yearbookErrorMessage" class="status-message error-text">
    {{ yearbookErrorMessage }}
  </p>

  <p v-if="isLoading" class="status-message">Caricamento classi...</p>
  <p v-else-if="errorMessage" class="status-message error-text">{{ errorMessage }}</p>
  <template v-else>
    <p v-if="classImageActionErrorMessage" class="action-status-message error-text">
      {{ classImageActionErrorMessage }}
    </p>
    <p v-else-if="classImageActionMessage" class="action-status-message">
      {{ classImageActionMessage }}
    </p>

    <div class="classes-container">
      <div 
        v-for="classe in classes" 
        :key="classe.id" 
        :class="['class-card', { 'class-card--expanded': selectedClass === classe.name }]"
      >
        <img
          v-if="classe.hasImage"
          :src="classImageUrl(classe.name)"
          :alt="`${classe.name} immagine di classe`"
          class="class-image"
          loading="lazy"
        >

        <h2>{{ classe.name }}</h2>
        <p>Studenti: {{ classe.students }}</p>

        <button @click="loadClassDetails(classe.name)">
          {{ selectedClass === classe.name ? 'Nascondi dettagli' : 'Mostra dettagli' }}
        </button>

        <button
          v-if="classe.hasImage"
          class="download-class-image-btn"
          :disabled="
            downloadingClassImage === classe.name || isDownloadingAllClassImages
          "
          @click="downloadClassImage(classe.name)"
        >
          {{
            downloadingClassImage === classe.name
              ? 'Scaricamento immagine in corso...'
              : 'Scarica foto classe'
          }}
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
            <img
              :src="studentProfileImageUrl(student) || defaultStudentProfileImage"
              :alt="`Foto profilo di ${student.name}`"
              class="student-profile-image"
              loading="lazy"
            />
            <h3>{{ student.name }}</h3>
            <p v-if="student.username" class="student-username">
              {{ student.username }}
            </p>

            <div v-if="student.hasAudio && student.username" class="student-qr">
              <img
                v-if="studentQrDataUrls[student.username]"
                :src="studentQrDataUrls[student.username]"
                :alt="`QR code audio per ${student.name}`"
                class="student-qr-image"
              />
            </div>

            <p v-else class="student-audio-status">
              Nessun audio caricato ancora.
            </p>

            <button
              v-if="student.hasAudio && student.username"
              class="download-audio-btn"
              :disabled="downloadingStudent === student.username"
              @click="downloadStudentAudio(student)"
            >
              {{ downloadingStudent === student.username ? 'Scaricamento in corso...' : 'Scarica audio' }}
            </button>
          </article>
        </div>

        <p
          v-else-if="selectedClass === classe.name"
          class="empty-state"
        >
          Nessuno studente trovato per questa classe.
        </p>
      </div>
    </div>
  </template>
</template>

<style src="../stylesheets/defaultStyle.css"></style>

<style scoped>
.top-nav-single {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: min(calc(100% - 2rem), 22rem);

  background: var(--card-bg);
  border: 1px solid var(--borders);
  border-radius: 10px;
  padding: 10px 16px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.top-nav-single a {
  width: 100%;
  text-decoration: none;
  color: var(--text-color);
  font-size: clamp(1rem, 2vw, 1.125rem);
  padding: 6px 12px;
  border-radius: 6px;
  transition: 0.3s ease;
  text-align: center;
}

.top-nav-single a:hover {
  background: var(--button-bg);
  color: white;
  transform: scale(1.05);
}

.page-title {
  text-align: center;
  margin-top: 5.5rem;
  margin-bottom: 1.25rem;
  padding: 0 1rem;
  color: var(--text-color);
  overflow-wrap: anywhere;
}

.classes-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  width: min(100%, 1280px);
  margin: 0 auto;
  padding: 1rem 1rem 2rem;
}

.status-message {
  padding: 1rem 1rem 2rem;
  text-align: center;
  color: var(--text-color);
}

.classes-actions {
  display: flex;
  justify-content: center;
  padding: 0 1rem;
}

.action-status-message {
  padding: 0.75rem 1rem 0;
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
  display: flex;
  flex-direction: column;
  text-align: center;
  transition: 0.3s ease;
  min-width: 0;
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
  margin-top: 0;
  margin-bottom: 10px;
  color: var(--text-color);
  overflow-wrap: anywhere;
}

.class-card p {
  margin-bottom: 15px;
  overflow-wrap: anywhere;
}

.class-card button {
  width: 100%;
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

.download-all-images-btn,
.download-class-image-btn {
  margin-top: 10px;
}

.download-all-images-btn,
.download-yearbook-btn {
  margin-top: 10px;
  width: min(100%, 24rem);
}

.download-yearbook-btn {
  margin-left: 1rem;
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
  min-width: 0;
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

.student-profile-image {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--borders);
  background: var(--card-bg);
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
  .page-title {
    margin-top: 5rem;
  }

  .classes-container {
    grid-template-columns: 1fr;
  }

  .class-card--expanded {
    grid-column: auto;
  }

  .class-card {
    padding: 18px 16px;
  }

  .students-grid {
    grid-template-columns: 1fr;
  }

  .student-qr {
    width: min(100%, 180px);
  }
}

@media (max-width: 480px) {
  .top-nav-single {
    top: 12px;
    width: min(calc(100% - 1rem), 22rem);
    padding: 8px 12px;
  }

  .top-nav-single a {
    padding: 8px 10px;
  }

  .page-title {
    margin-top: 4.75rem;
    font-size: 1.7rem;
  }

  .classes-container,
  .status-message,
  .classes-actions,
  .action-status-message {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }

  .class-image {
    height: 160px;
  }

  .student-card {
    padding: 16px 14px;
  }

  .student-qr {
    min-height: 150px;
    padding: 8px;
  }
}
</style>
