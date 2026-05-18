<script>
//`
import { onMounted, ref } from 'vue'
import { isDarkMode, toggleTheme, initTheme } from '../jsGraphicManaging/toggleLDModeButton.js'
import { buildApiUrl } from '../utils/api'
import { handleUnauthorizedResponse } from '../utils/session'

const REQUIRED_STUDENT_HEADERS = ['classe_desc', 'cognome', 'nome', 'email']

export default {
  setup() {
    const fileInput = ref(null)
    const studentFileInput = ref(null)
    const selectedClass = ref('')
    const classes = ref([])
    const uploadStatus = ref('')
    const previewUrl = ref('')
    const imageAccessPassword = ref('')
    const showImageAccessPassword = ref(false)

    // Student creation form
    const studentName = ref('')
    const studentSurname = ref('')
    const studentEmail = ref('')
    const studentClass = ref('')
    const studentStatus = ref('')
    const studentAccessPassword = ref('')
    const showStudentAccessPassword = ref(false)
    const studentImportStatus = ref('')
    const studentImportAccessPassword = ref('')
    const showStudentImportAccessPassword = ref(false)

    const getApiMessage = (result) =>
      result?.data?.message ?? result?.message ?? 'Richiesta fallita'

    const isSessionErrorMessage = (message) =>
      ['Token not found', 'Invalid token', 'The token is expired'].includes(message)

    const isErrorMessage = (message) => {
      const normalizedMessage = String(message ?? '').toLowerCase()

      return [
        'error',
        'failed',
        'required',
        'not accepted',
        'missing',
        'invalid',
        'unsupported',
        'expired',
        'not correct'
      ].some((fragment) => normalizedMessage.includes(fragment))
    }

    const classOptions = () =>
      classes.value
        .map((classSummary) => classSummary?.name)
        .filter((className) => typeof className === 'string' && className.length > 0)

    const normalizeCellValue = (value) => String(value ?? '').trim()

    const normalizeHeader = (value) => normalizeCellValue(value).replace(/^\uFEFF/, '').toLowerCase()

    const getFileExtension = (fileName) => {
      const lastDotIndex = fileName.lastIndexOf('.')

      if (lastDotIndex === -1) {
        return ''
      }

      return fileName.slice(lastDotIndex + 1).toLowerCase()
    }

    const clearStudentImportFile = () => {
      if (studentFileInput.value) {
        studentFileInput.value.value = ''
      }
    }

    const readFileAsText = (file) =>
      new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = () => {
          resolve(String(reader.result ?? ''))
        }

        reader.onerror = () => {
          reject(new Error('Impossibile leggere il file.'))
        }

        reader.readAsText(file, 'utf-8')
      })

    const readFileAsArrayBuffer = (file) =>
      new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = () => {
          resolve(reader.result)
        }

        reader.onerror = () => {
          reject(new Error('Impossibile leggere il file.'))
        }

        reader.readAsArrayBuffer(file)
      })

    const parseDelimitedRows = (text, delimiter) => {
      const rows = []
      let currentRow = []
      let currentValue = ''
      let insideQuotes = false

      for (let index = 0; index < text.length; index += 1) {
        const character = text[index]

        if (character === '"') {
          if (insideQuotes && text[index + 1] === '"') {
            currentValue += '"'
            index += 1
          } else {
            insideQuotes = !insideQuotes
          }

          continue
        }

        if (!insideQuotes && character === delimiter) {
          currentRow.push(currentValue)
          currentValue = ''
          continue
        }

        if (!insideQuotes && (character === '\n' || character === '\r')) {
          if (character === '\r' && text[index + 1] === '\n') {
            index += 1
          }

          currentRow.push(currentValue)
          rows.push(currentRow)
          currentRow = []
          currentValue = ''
          continue
        }

        currentValue = currentValue + character
      }

      if (currentValue.length > 0 || currentRow.length > 0) {
        currentRow.push(currentValue)
        rows.push(currentRow)
      }

      return rows.map((row) => row.map((value) => normalizeCellValue(value).replace(/^\uFEFF/, '')))
    }

    const scoreParsedRows = (rows) => {
      const headerRow =
        rows.find((row) => row.some((cell) => normalizeCellValue(cell).length > 0)) ?? []
      const normalizedHeaders = headerRow.map((header) => normalizeHeader(header))

      return {
        headerMatches: REQUIRED_STUDENT_HEADERS.filter((header) =>
          normalizedHeaders.includes(header)
        ).length,
        columnCount: headerRow.length
      }
    }

    const parseCsvRows = (text) => {
      const commaRows = parseDelimitedRows(text, ',')
      const semicolonRows = parseDelimitedRows(text, ';')
      const commaScore = scoreParsedRows(commaRows)
      const semicolonScore = scoreParsedRows(semicolonRows)

      if (semicolonScore.headerMatches > commaScore.headerMatches) {
        return semicolonRows
      }

      if (commaScore.headerMatches > semicolonScore.headerMatches) {
        return commaRows
      }

      if (semicolonScore.columnCount > commaScore.columnCount) {
        return semicolonRows
      }

      return commaRows
    }

    const buildStudentsFromRows = (rows) => {
      const headerRowIndex = rows.findIndex((row) =>
        row.some((cell) => normalizeCellValue(cell).length > 0)
      )

      if (headerRowIndex === -1) {
        throw new Error('Il file è vuoto.')
      }

      const headerRow = rows[headerRowIndex]
      const headerIndexes = new Map(
        headerRow.map((header, index) => [normalizeHeader(header), index])
      )
      const missingHeaders = REQUIRED_STUDENT_HEADERS.filter((header) => !headerIndexes.has(header))

      if (missingHeaders.length > 0) {
        throw new Error(`Mancano le colonne obbligatorie: ${missingHeaders.join(', ')}`)
      }

      const students = rows
        .slice(headerRowIndex + 1)
        .filter((row) => row.some((cell) => normalizeCellValue(cell).length > 0))
        .map((row, index) => {
          const className = normalizeCellValue(row[headerIndexes.get('classe_desc')])
          const surname = normalizeCellValue(row[headerIndexes.get('cognome')])
          const name = normalizeCellValue(row[headerIndexes.get('nome')])
          const email = normalizeCellValue(row[headerIndexes.get('email')])
          const rowNumber = headerRowIndex + index + 2

          if (!className || !surname || !name || !email) {
            throw new Error(
              `Row ${rowNumber} is missing one of the required values: classe_desc, cognome, nome, email.`
            )
          }

          return {
            name,
            surname,
            email,
            class: className
          }
        })

      if (students.length === 0) {
        throw new Error('Il file non contiene studenti da importare.')
      }

      return students
    }

    const extractStudentRowsFromFile = async (file) => {
      const fileExtension = getFileExtension(file.name)

      if (fileExtension === 'csv') {
        return parseCsvRows(await readFileAsText(file))
      }

      if (fileExtension === 'xls') {
        try {
          const { read, utils } = await import('xlsx')
          const workbook = read(await readFileAsArrayBuffer(file), { type: 'array' })
          const firstSheetName = workbook.SheetNames[0]

          if (!firstSheetName) {
            throw new Error('The .xls file does not contain any sheets.')
          }

          return utils.sheet_to_json(workbook.Sheets[firstSheetName], {
            header: 1,
            raw: false,
            defval: '',
            blankrows: false
          })
        } catch (error) {
          console.error('XLS conversion error:', error)
          throw new Error('Impossibile convertire il file .xls.')
        }
      }

      throw new Error('Il file selezionato non è accettato. Carica un file .csv o .xls.')
    }

    const convertToJPG = (file, quality = 0.9) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        const img = new Image()

        reader.onload = (e) => {
          img.src = e.target.result
        }

        reader.readAsDataURL(file)

        img.onload = () => {
          let canvas = document.createElement('canvas')
          canvas.width = img.width
          canvas.height = img.height

          const ctx = canvas.getContext('2d')
          ctx.fillStyle = '#fff'
          ctx.fillRect(0, 0, canvas.width, canvas.height)
          ctx.drawImage(img, 0, 0)

          canvas.toBlob((blob) => {
            resolve(blob)
          }, 'image/jpeg', quality)
        }

        img.onerror = (err) => {
          reject(err)
        }
      })
    }

    const fetchClasses = async () => {
      try {
        const response = await fetch(buildApiUrl('/class/getClasses'), {
          method: 'GET',
          credentials: 'include'
        })

        if (handleUnauthorizedResponse(response)) {
          uploadStatus.value = 'La sessione è scaduta. Effettua di nuovo il login.'
          studentStatus.value = 'La sessione è scaduta. Effettua di nuovo il login.'
          return
        }

        const result = await response.json()

        if (!response.ok) {
          throw new Error(getApiMessage(result))
        }

        classes.value = result?.data?.message?.classes || []
      } catch (error) {
        console.error('Error fetching classes:', error)
        const message = error instanceof Error ? error.message : 'Errore durante il caricamento delle classi'
        uploadStatus.value = message
      }
    }

    const openFilePicker = () => {
      if (fileInput.value) {
        fileInput.value.click()
      }
    }

    const openStudentFilePicker = () => {
      if (studentFileInput.value) {
        studentFileInput.value.click()
      }
    }

    const handleFileChange = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      if (!selectedClass.value) {
        uploadStatus.value = 'Seleziona prima una classe'
        return
      }

      if (!imageAccessPassword.value.trim()) {
        uploadStatus.value = 'La password per le immagini è obbligatoria'
        event.target.value = ''
        return
      }

      try {
        let fileUpload = file

        if (file.type !== 'image/jpeg') {
            uploadStatus.value = "Conversione dell'immagine in JPEG in corso..."
        }

        if (previewUrl.value) {
          URL.revokeObjectURL(previewUrl.value)
        }
        previewUrl.value = URL.createObjectURL(fileUpload)

        // Upload to server
        const formData = new FormData()
        formData.append('file', fileUpload, 'file.jpeg')
        formData.append('access_password', imageAccessPassword.value)

        uploadStatus.value = 'Caricamento in corso...'

        const response = await fetch(
          buildApiUrl(`/admin/addImage?class=${encodeURIComponent(selectedClass.value)}`),
          {
            method: 'PUT',
            body: formData,
            credentials: 'include'
          }
        )

        const result = await response.json()

        if (response.status === 401 && isSessionErrorMessage(getApiMessage(result))) {
          handleUnauthorizedResponse(response)
          uploadStatus.value = 'La sessione è scaduta. Effettua di nuovo il login.'
          return
        }

        if (!response.ok) {
          throw new Error(getApiMessage(result))
        }

        uploadStatus.value = `Immagine caricata con successo per la classe ${selectedClass.value}`
        imageAccessPassword.value = ''
        event.target.value = ''

      } catch (error) {
        console.error('Upload error:', error)
        uploadStatus.value = `Caricamento fallito: ${error.message}`
      }
    }

    const submitStudents = async (students, accessPassword) => {
      const response = await fetch(buildApiUrl('/admin/add'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          access_password: accessPassword,
          students
        }),
        credentials: 'include'
      })

      const result = await response.json()

      if (response.status === 401 && isSessionErrorMessage(getApiMessage(result))) {
        handleUnauthorizedResponse(response)
        throw new Error('La sessione è scaduta. Effettua di nuovo il login.')
      }

      if (!response.ok) {
        throw new Error(getApiMessage(result))
      }
    }

    const addStudent = async () => {
      const normalizedName = studentName.value.trim()
      const normalizedSurname = studentSurname.value.trim()
      const normalizedEmail = studentEmail.value.trim()
      const normalizedClass = studentClass.value.trim()
      const normalizedAccessPassword = studentAccessPassword.value.trim()

      if (!normalizedName || !normalizedSurname || !normalizedEmail || !normalizedClass || !normalizedAccessPassword) {
        studentStatus.value = 'Tutti i campi sono obbligatori'
        return
      }

      try {
        studentStatus.value = 'Aggiunta studente in corso...'

        await submitStudents(
          [
            {
              name: normalizedName,
              surname: normalizedSurname,
              email: normalizedEmail,
              class: normalizedClass
            }
          ],
          normalizedAccessPassword
        )

        studentStatus.value = `Studente ${normalizedName} ${normalizedSurname} aggiunto con successo. Credenziali salvate sul server.`

        studentName.value = ''
        studentSurname.value = ''
        studentEmail.value = ''
        studentClass.value = ''
        studentAccessPassword.value = ''

        await fetchClasses()
      } catch (error) {
        console.error('Add student error:', error)
        const message = error instanceof Error ? error.message : 'Aggiunta studente fallita.'
        studentStatus.value = `Impossibile aggiungere lo studente: ${message}`
      }
    }

    const handleStudentImportFileChange = async (event) => {
      const file = event.target.files[0]
      if (!file) {
        return
      }

      const normalizedAccessPassword = studentImportAccessPassword.value.trim()

      if (!normalizedAccessPassword) {
        studentImportStatus.value = 'La password di importazione è obbligatoria.'
        clearStudentImportFile()
        return
      }

      const fileExtension = getFileExtension(file.name)

      if (!['csv', 'xls'].includes(fileExtension)) {
        studentImportStatus.value =
          'Il file selezionato non è accettato. Carica un file .csv o .xls.'
        clearStudentImportFile()
        return
      }

      try {
        studentImportStatus.value =
          fileExtension === 'xls'
            ? `Conversione di ${file.name} in corso...`
            : `Lettura di ${file.name} in corso...`

        const rows = await extractStudentRowsFromFile(file)
        const students = buildStudentsFromRows(rows)

        studentImportStatus.value = `Importazione di ${students.length} studenti in corso...`

        await submitStudents(students, normalizedAccessPassword)

        studentImportStatus.value = `${students.length} studenti importati con successo da ${file.name}. Credenziali salvate sul server.`
        studentImportAccessPassword.value = ''
        clearStudentImportFile()

        await fetchClasses()
      } catch (error) {
        console.error('Student import error:', error)
        const message = error instanceof Error ? error.message : 'Importazione studenti fallita.'
        studentImportStatus.value =
          message.startsWith('Il file selezionato non è accettato')
            ? message
            : `Importazione fallita: ${message}`
        clearStudentImportFile()
      }
    }

    onMounted(() => {
      initTheme()
      fetchClasses()
    })

    return {
      fileInput,
      studentFileInput,
      selectedClass,
      classes,
      uploadStatus,
      previewUrl,
      imageAccessPassword,
      showImageAccessPassword,
      classOptions,
      isErrorMessage,
      studentName,
      studentSurname,
      studentEmail,
      studentClass,
      studentStatus,
      studentAccessPassword,
      showStudentAccessPassword,
      studentImportStatus,
      studentImportAccessPassword,
      showStudentImportAccessPassword,
      openFilePicker,
      openStudentFilePicker,
      handleFileChange,
      addStudent,
      handleStudentImportFileChange,
      isDarkMode,
      toggleTheme
    }
  }
}
</script>

<template>
  <div class="admin-container">
    <div class="top-nav-single">
      <router-link to="/home">Torna alla home</router-link>
    </div>

    <h1 class="page-title">Admin</h1>
    
    <div class="upload-section">
      <div class="form-group">
        <label for="class-select">Seleziona classe:</label>
        <select id="class-select" v-model="selectedClass" class="class-select">
          <option value="">Scegli una classe...</option>
          <option v-for="className in classOptions()" :key="className" :value="className">
            {{ className }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="image-access-password">Password accesso immagini:</label>
        <div class="password-toggle-row">
          <input
            id="image-access-password"
            v-model="imageAccessPassword"
            :type="showImageAccessPassword ? 'text' : 'password'"
            class="form-input"
            autocomplete="off"
            placeholder="Inserisci la password immagini"
          />
          <button
            type="button"
            class="password-toggle-btn"
            @click="showImageAccessPassword = !showImageAccessPassword"
          >
            {{ showImageAccessPassword ? 'Nascondi' : 'Mostra' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label>Carica immagine della classe:</label>
        <input 
          ref="fileInput"
          type="file" 
          accept="image/*"
          @change="handleFileChange"
          style="display: none"
        />
        <button @click="openFilePicker" class="upload-btn" :disabled="!selectedClass || !imageAccessPassword">
          Scegli immagine
        </button>
      </div>

      <div v-if="previewUrl" class="preview-section">
        <h3>Anteprima:</h3>
        <img :src="previewUrl" alt="Anteprima" class="preview-image" />
      </div>

      <div v-if="uploadStatus" class="status-message" :class="{ error: isErrorMessage(uploadStatus) }">
        {{ uploadStatus }}
      </div>
    </div>

    <div class="student-section">
      <h3 style="color: black;">Aggiungi studente</h3>

      <div class="form-group">
        <label for="student-name">Nome studente:</label>
        <input 
          id="student-name"
          v-model="studentName" 
          type="text" 
          class="form-input"
          placeholder="Inserisci nome studente"
        />
      </div>

      <div class="form-group">
        <label for="student-surname">Cognome studente:</label>
        <input 
          id="student-surname"
          v-model="studentSurname" 
          type="text" 
          class="form-input"
          placeholder="Inserisci cognome studente"
        />
      </div>

      <div class="form-group">
        <label for="student-email">Email studente:</label>
        <input 
          id="student-email"
          v-model="studentEmail" 
          type="email" 
          class="form-input"
          placeholder="Inserisci email studente"
        />
      </div>

      <div class="form-group">
        <label for="student-class">Classe:</label>
        <input 
          id="student-class"
          v-model="studentClass" 
          type="text" 
          class="form-input"
          list="class-options"
          placeholder="Inserisci classe (es. 1A)"
        />
        <datalist id="class-options">
          <option v-for="className in classOptions()" :key="`student-${className}`" :value="className" />
        </datalist>
      </div>

      <div class="form-group">
        <label for="student-access-password">Password accesso studenti:</label>
        <div class="password-toggle-row">
          <input
            id="student-access-password"
            v-model="studentAccessPassword"
            :type="showStudentAccessPassword ? 'text' : 'password'"
            class="form-input"
            autocomplete="off"
            placeholder="Inserisci la password studenti"
          />
          <button
            type="button"
            class="password-toggle-btn"
            @click="showStudentAccessPassword = !showStudentAccessPassword"
          >
            {{ showStudentAccessPassword ? 'Nascondi' : 'Mostra' }}
          </button>
        </div>
      </div>

      <button @click="addStudent" class="add-student-btn" :disabled="!studentName || !studentSurname || !studentClass || !studentAccessPassword">
        Aggiungi studente
      </button>

      <div v-if="studentStatus" class="status-message" :class="{ error: isErrorMessage(studentStatus) }">
        {{ studentStatus }}
      </div>

      <div class="student-import-section">
        <h3 style="color: black;">Importa studenti</h3>

        <p class="helper-text">
          File accettati: .csv e .xls. Colonne richieste: classe_desc, cognome, nome, email.
          Sono supportati separatori virgola e punto e virgola.
        </p>

        <div class="form-group">
          <label for="student-import-access-password">Password importazione:</label>
          <div class="password-toggle-row">
            <input
              id="student-import-access-password"
              v-model="studentImportAccessPassword"
              :type="showStudentImportAccessPassword ? 'text' : 'password'"
              class="form-input"
              autocomplete="off"
              placeholder="Inserisci la password di importazione"
            />
            <button
              type="button"
              class="password-toggle-btn"
              @click="showStudentImportAccessPassword = !showStudentImportAccessPassword"
            >
              {{ showStudentImportAccessPassword ? 'Nascondi' : 'Mostra' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Carica file studenti:</label>
          <input
            ref="studentFileInput"
            type="file"
            accept=".csv,.xls,text/csv,application/vnd.ms-excel"
            @change="handleStudentImportFileChange"
            style="display: none"
          />
          <button
            @click="openStudentFilePicker"
            class="add-student-btn"
            :disabled="!studentImportAccessPassword"
          >
            Scegli file CSV/XLS
          </button>
        </div>

        <div
          v-if="studentImportStatus"
          class="status-message"
          :class="{ error: isErrorMessage(studentImportStatus) }"
        >
          {{ studentImportStatus }}
        </div>
      </div>
    </div>

    <button class="theme-toggle" @click="toggleTheme">
      {{ isDarkMode ? '☼' : '☀︎' }}
    </button>
  </div>
</template>

<style src="../stylesheets/defaultStyle.css"></style>
<style scoped>
.top-nav-single {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;

  background: var(--card-bg);
  border: 1px solid var(--borders);
  border-radius: 10px;
  padding: 10px 20px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.top-nav-single a {
  text-decoration: none;
  color: var(--text-color);
  font-size: 18px;
  padding: 6px 12px;
  border-radius: 6px;
  transition: 0.3s ease;
}

.top-nav-single a:hover {
  background: var(--button-bg);
  color: white;
  transform: scale(1.05);
}

.page-title {
  text-align: center;
  margin-top: 70px; /* spazio per la navbar fixed */
  margin-bottom: 20px;
  color: var(--text-color);
}

.admin-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

.upload-section {
  background: var(--bg-secondary, #f5f5f5);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.student-section {
  background: var(--bg-secondary, #f5f5f5);
  padding: 2rem;
  border-radius: 8px;
}

.student-import-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color, #ddd);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: var(--text-primary, #333);
}

.helper-text {
  margin: 0 0 1rem;
  color: var(--text-secondary, #666);
  line-height: 1.5;
}

.class-select,
.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 4px;
  background: var(--bg-primary, #fff);
  color: var(--text-primary, #333);
  font-size: 1rem;
}

.password-toggle-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.password-toggle-btn {
  width: auto;
  max-width: 67px;
  min-width: fit-content;
  background: var(--accent-color, #007bff);
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.upload-btn,
.add-student-btn {
  background: var(--accent-color, #007bff);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.upload-btn:hover:not(:disabled),
.add-student-btn:hover:not(:disabled),
.password-toggle-btn:hover {
  background: var(--accent-hover, #0056b3);
}

.upload-btn:disabled,
.add-student-btn:disabled {
  background: var(--disabled-color, #ccc);
  cursor: not-allowed;
}

.preview-section {
  margin: 1.5rem 0;
  text-align: center;
}

.preview-section h3 {
  margin-bottom: 1rem;
  color: var(--text-primary, #333);
}

.preview-image {
  max-width: 300px;
  max-height: 300px;
  border: 2px solid var(--border-color, #ddd);
  border-radius: 8px;
  object-fit: cover;
}

.status-message {
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  background: var(--success-bg, #d4edda);
  color: var(--success-text, #155724);
  border: 1px solid var(--success-border, #c3e6cb);
}

.status-message.error {
  background: var(--error-bg, #f8d7da);
  color: var(--error-text, #721c24);
  border: 1px solid var(--error-border, #f5c6cb);
}

/* Dark mode support */
/*@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --bg-tertiary: #404040;
    --text-primary: #ffffff;
    --text-secondary: #b3b3b3;
    --border-color: #404040;
    --accent-color: #0066cc;
    --accent-hover: #0052a3;
    --disabled-color: #666666;
    --success-bg: #1e3a1e;
    --success-text: #90ee90;
    --success-border: #2d5a2d;
    --error-bg: #3a1e1e;
    --error-text: #ff6b6b;
    --error-border: #5a2d2d;
  }
}*/
</style>
