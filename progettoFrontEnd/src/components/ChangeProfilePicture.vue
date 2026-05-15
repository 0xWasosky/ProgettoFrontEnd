<script>
import { onMounted, ref } from 'vue'
import { isDarkMode, toggleTheme, username, initTheme } from '../jsGraphicManaging/toggleLDModeButton.js'
import { buildApiUrl } from '../utils/api'
import { handleUnauthorizedResponse } from '../utils/session'
import { cacheProfilePictureBlob, getCachedProfilePicture, setCachedProfilePicture } from '../utils/profilePictureCache'
import defaultPreviewImage from '../../assets/default_profile_pictures/default.jpg'
import defaultImage0 from '../../assets/default_profile_pictures/default.jpg'
import defaultImage1 from '../../assets/default_profile_pictures/default1.jpg'
import defaultImage2 from '../../assets/default_profile_pictures/default2.jpg'
import defaultImage3 from '../../assets/default_profile_pictures/default3.jpg'
import defaultImage4 from '../../assets/default_profile_pictures/default4.jpg'
import homeImage from '../../assets/images/home.png'


export default {
  setup() {
    const iconContainer = ref(null)
    const fileInput = ref(null)

    const  convertToJPG = (file, quality = 0.9) => {
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

    const renderPreview = (src) => {
      const img = document.createElement('img')
      img.src = src
      img.style.width = '100%'
      img.style.height = '100%'
      img.style.objectFit = 'cover'

      if (iconContainer.value) {
        iconContainer.value.innerHTML = ''
        iconContainer.value.appendChild(img)
      }
    }

    const loadProfileImage = async () => {
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
          renderPreview(cachedProfilePicture || defaultPreviewImage)
          return
        }

        const blob = await response.blob()
        const cachedImage = await cacheProfilePictureBlob(blob)
        renderPreview(cachedImage || cachedProfilePicture || defaultPreviewImage)
      } catch {
        renderPreview(cachedProfilePicture || defaultPreviewImage)
      }
    }

    onMounted(() => {
      initTheme()
      renderPreview(getCachedProfilePicture() || defaultPreviewImage)
      loadProfileImage()
    })

    const openFilePicker = () => {
      if (fileInput.value) {
        fileInput.value.click()
      }
    }

    const handleFileChange = async (event) => {
        const file = event.target.files[0]
        const conferma = confirm("Vuoi usare questa immagine come profilo?")

        if(!conferma){
            event.target.value = '' // resetta input file
            return
        }

        if(file){
            let fileUpload = file

            try {
                if(file.type !== 'image/jpeg'){
                    fileUpload = await convertToJPG(file)
                }
            } catch (error){
                alert("Errore nella conversione dell'immagine")
                return 
            }
            

            // Preview the image
            const previewURL = URL.createObjectURL(fileUpload)
            renderPreview(previewURL)

            //Upload
            const formData = new FormData()
            formData.append('file', fileUpload, 'file.jpeg')

            /*const reader = new FileReader()
            reader.onload = (e) => {
                renderPreview(e.target.result)
            }
            reader.readAsDataURL(file)

            // Upload to server
            const formData = new FormData()
            formData.append('file', file, 'file.jpeg')*/

            try {
                const response = await fetch(buildApiUrl('/files/image/add'), {
                    method: 'PUT',
                    body: formData,
                    credentials: 'include'
                })

                if (handleUnauthorizedResponse(response)) {
                    return
                }

                const result = await response.json()
                if (response.ok) {
                    const cachedImage = await cacheProfilePictureBlob(fileUpload)
                    renderPreview(cachedImage || previewURL)
                    alert('Immagine caricata con successo!')
                } else {
                    alert('Errore nel caricamento: ' + (result?.data?.message ?? result?.message ?? 'Upload failed'))
                    loadProfileImage()
                }
            } catch (error) {
                alert('Errore di rete: ' + error.message)
                loadProfileImage()
            }
        }
    }
    
    const selectDefault = (imgSrc) => {
        const conferma = confirm("Vuoi davvero cambiare immagine profilo?")

        if (iconContainer.value && conferma) {
            renderPreview(imgSrc)
            setCachedProfilePicture(imgSrc)
        }
    }

    return {
        isDarkMode,
        toggleTheme,
        username,
        homeImage,
        iconContainer,
        fileInput,
        openFilePicker,
        handleFileChange,
        selectDefault,
        defaultImage0,
        defaultImage1,
        defaultImage2,
        defaultImage3,
        defaultImage4
    }
  }
}
</script>

<template>
    <button class="theme-toggle" @click="toggleTheme">
        {{ isDarkMode ? '☼' : '☀︎' }}
    </button>

    <div id="accountIcon">
        <router-link to="/settings">
            <img :src="homeImage" width="50px"/>
        </router-link>
    </div>

    <h1 class="centered">Cambia foto profilo</h1>

    <div ref="iconContainer" class="circle1" id="preview" @click="openFilePicker"></div>
    <input type="file" ref="fileInput" @change="handleFileChange" style="display:none" accept="image/*"/>
    
    <div class="choiceContainer">
        <div class="card"><img :src="defaultImage0" alt="Default Profile Picture" @click="selectDefault(defaultImage0)"></div>
        <div class="card"><img :src="defaultImage1" alt="Default Profile Picture 1" @click="selectDefault(defaultImage1)"></div>
        <div class="card"><img :src="defaultImage2" alt="Default Profile Picture 2" @click="selectDefault(defaultImage2)"></div>
        <div class="card"><img :src="defaultImage3" alt="Default Profile Picture 3" @click="selectDefault(defaultImage3)"></div>
        <div class="card"><img :src="defaultImage4" alt="Default Profile Picture 4" @click="selectDefault(defaultImage4)"></div>
    </div>

    <!--<input type="file" id="fileInput"/>-->

</template>

<style src="../stylesheets/defaultStyle.css"></style>
<style>
.choiceContainer {
    width: min(100%, 1200px);
    padding: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin: 30px auto 0;
}

.circle1{
    width: 125px;
    height: 125px;
    border-radius: 50%;
    position: relative;
    left: 50%;
    margin-bottom: 25px;
    transform: translateX(-50%);
    overflow: hidden;
    border: 2px solid var(--borders);
    transition: 0.33s ease;
}

.circle1:hover{
    transform: translateX(-50%) scale(1.1);
    cursor: pointer;
    border-color: var(--borders-hover);
}

.circle1 img {
    justify-content: center;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card{
    width: 100%; 
    aspect-ratio: 1 / 1;
    min-height: 180px;
    background-color: var(--card-bg);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 20px auto;
    transition: 0.5s ease;
    box-shadow: 0 2px 4px 2px var(--borders);
    overflow: hidden;
}

.card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card:hover {
    transform: translateY(-5px);
    cursor: pointer;
    box-shadow: 0 4px 8px 4px var(--borders);
}

@media (max-width: 600px) {
    .choiceContainer {
        padding: 16px;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
    }

    .card {
        min-height: 140px;
    }
}
</style>
