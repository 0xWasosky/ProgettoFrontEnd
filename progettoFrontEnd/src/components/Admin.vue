<script>
//`
import { onMounted, ref } from 'vue'
import { isDarkMode, toggleTheme, initTheme } from '../jsGraphicManaging/toggleLDModeButton.js'
import { buildApiUrl } from '../utils/api'
import { handleUnauthorizedResponse } from '../utils/session'

export default {
  setup() {
    const ADMIN_ACCESS_KEY =
      import.meta.env.VITE_ADMIN_ACCESS_KEY || 'eqvU148VnKHornxdmaUX08ElRsj6tDkVMqpUksf4qdM'
    const IMAGE_ACCESS_KEY =
      import.meta.env.VITE_IMAGE_ACCESS_KEY || 'ZaE86wpZMl8lAjpMI7yezFaSNIUv4yS84LzWoEOdcPI'

    const fileInput = ref(null)
    const selectedClass = ref('')
    const classes = ref([])
    const uploadStatus = ref('')
    const previewUrl = ref('')

    // Student creation form
    const studentName = ref('')
    const studentSurname = ref('')
    const studentClass = ref('')
    const studentStatus = ref('')

    const getApiMessage = (result) =>
      result?.data?.message ?? result?.message ?? 'Request failed'

    const classOptions = () =>
      classes.value
        .map((classSummary) => classSummary?.name)
        .filter((className) => typeof className === 'string' && className.length > 0)

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
          uploadStatus.value = 'Your session expired. Please log in again.'
          studentStatus.value = 'Your session expired. Please log in again.'
          return
        }

        const result = await response.json()

        if (!response.ok) {
          throw new Error(getApiMessage(result))
        }

        classes.value = result?.data?.message?.classes || []
      } catch (error) {
        console.error('Error fetching classes:', error)
        const message = error instanceof Error ? error.message : 'Error loading classes'
        uploadStatus.value = message
      }
    }

    const openFilePicker = () => {
      if (fileInput.value) {
        fileInput.value.click()
      }
    }

    const handleFileChange = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      if (!selectedClass.value) {
        uploadStatus.value = 'Please select a class first'
        return
      }

      try {
        let fileUpload = file

        // Convert to JPEG if needed
        if (file.type !== 'image/jpeg') {
          uploadStatus.value = 'Converting image to JPEG...'
          fileUpload = await convertToJPG(file)
        }

        // Create preview
        if (previewUrl.value) {
          URL.revokeObjectURL(previewUrl.value)
        }
        previewUrl.value = URL.createObjectURL(fileUpload)

        // Upload to server
        const formData = new FormData()
        formData.append('file', fileUpload, 'file.jpeg')

        uploadStatus.value = 'Uploading...'

        const response = await fetch(
          buildApiUrl(`/admin/addImage?class=${encodeURIComponent(selectedClass.value)}`),
          {
            method: 'PUT',
            headers: {
              'access': IMAGE_ACCESS_KEY
            },
            body: formData,
            credentials: 'include'
          }
        )

        if (handleUnauthorizedResponse(response)) {
          uploadStatus.value = 'Authentication failed'
          return
        }

        const result = await response.json()

        if (!response.ok) {
          throw new Error(getApiMessage(result))
        }

        uploadStatus.value = `Image uploaded successfully for class ${selectedClass.value}`
        event.target.value = '' // Reset file input

      } catch (error) {
        console.error('Upload error:', error)
        uploadStatus.value = `Upload failed: ${error.message}`
      }
    }

    const addStudent = async () => {
      const normalizedName = studentName.value.trim()
      const normalizedSurname = studentSurname.value.trim()
      const normalizedClass = studentClass.value.trim()

      if (!normalizedName || !normalizedSurname || !normalizedClass) {
        studentStatus.value = 'All fields are required'
        return
      }

      try {
        studentStatus.value = 'Adding student...'

        const response = await fetch(buildApiUrl('/admin/add'), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'access': ADMIN_ACCESS_KEY
          },
          body: JSON.stringify({
            students: [{
              name: normalizedName,
              surname: normalizedSurname,
              class: normalizedClass
            }]
          }),
          credentials: 'include'
        })

        if (handleUnauthorizedResponse(response)) {
          studentStatus.value = 'Authentication failed'
          return
        }

        const result = await response.json()

        if (!response.ok) {
          throw new Error(getApiMessage(result))
        }

        studentStatus.value = `Student ${normalizedName} ${normalizedSurname} added successfully. Credentials saved on the server.`
        
        // Reset form
        studentName.value = ''
        studentSurname.value = ''
        studentClass.value = ''
        
        // Refresh classes list
        await fetchClasses()

      } catch (error) {
        console.error('Add student error:', error)
        studentStatus.value = `Failed to add student: ${error.message}`
      }
    }

    onMounted(() => {
      initTheme()
      fetchClasses()
    })

    return {
      fileInput,
      selectedClass,
      classes,
      uploadStatus,
      previewUrl,
      classOptions,
      studentName,
      studentSurname,
      studentClass,
      studentStatus,
      openFilePicker,
      handleFileChange,
      addStudent,
      isDarkMode,
      toggleTheme
    }
  }
}
</script>

<template>
  <div class="admin-container">
    <h2>Admin - Class Image Management</h2>
    
    <div class="upload-section">
      <div class="form-group">
        <label for="class-select">Select Class:</label>
        <select id="class-select" v-model="selectedClass" class="class-select">
          <option value="">Choose a class...</option>
          <option v-for="className in classOptions()" :key="className" :value="className">
            {{ className }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Upload Class Image:</label>
        <input 
          ref="fileInput"
          type="file" 
          accept="image/*"
          @change="handleFileChange"
          style="display: none"
        />
        <button @click="openFilePicker" class="upload-btn" :disabled="!selectedClass">
          Choose Image
        </button>
      </div>

      <div v-if="previewUrl" class="preview-section">
        <h3>Preview:</h3>
        <img :src="previewUrl" alt="Preview" class="preview-image" />
      </div>

      <div v-if="uploadStatus" class="status-message" :class="{ 'error': uploadStatus.includes('Error') || uploadStatus.includes('failed') }">
        {{ uploadStatus }}
      </div>
    </div>

    <!-- Student Creation Section -->
    <div class="student-section">
      <h3>Add Student</h3>
      <div class="form-group">
        <label for="student-name">Student Name:</label>
        <input 
          id="student-name"
          v-model="studentName" 
          type="text" 
          class="form-input"
          placeholder="Enter student name"
        />
      </div>

      <div class="form-group">
        <label for="student-surname">Student Surname:</label>
        <input 
          id="student-surname"
          v-model="studentSurname" 
          type="text" 
          class="form-input"
          placeholder="Enter student surname"
        />
      </div>

      <div class="form-group">
        <label for="student-class">Class:</label>
        <input 
          id="student-class"
          v-model="studentClass" 
          type="text" 
          class="form-input"
          list="class-options"
          placeholder="Enter class name (e.g., 1A)"
        />
        <datalist id="class-options">
          <option v-for="className in classOptions()" :key="`student-${className}`" :value="className" />
        </datalist>
      </div>

      <button @click="addStudent" class="add-student-btn" :disabled="!studentName || !studentSurname || !studentClass">
        Add Student
      </button>

      <div v-if="studentStatus" class="status-message" :class="{ 'error': studentStatus.includes('Error') || studentStatus.includes('failed') || studentStatus.includes('required') }">
        {{ studentStatus }}
      </div>
    </div>

    <div class="theme-toggle">
      <button @click="toggleTheme" class="theme-btn">
        {{ isDarkMode ? '☀️ Light' : '🌙 Dark' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: var(--text-primary, #333);
}

.class-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 4px;
  background: var(--bg-primary, #fff);
  color: var(--text-primary, #333);
  font-size: 1rem;
}

.upload-btn {
  background: var(--accent-color, #007bff);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.upload-btn:hover:not(:disabled) {
  background: var(--accent-hover, #0056b3);
}

.upload-btn:disabled {
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

.theme-toggle {
  text-align: center;
  margin-top: 2rem;
}

.theme-btn {
  background: var(--bg-secondary, #f5f5f5);
  border: 1px solid var(--border-color, #ddd);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.theme-btn:hover {
  background: var(--bg-tertiary, #e9ecef);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
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
}
</style>
