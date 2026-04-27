const PROFILE_PICTURE_CACHE_KEY = 'profilePictureCache'
const PROFILE_PICTURE_PREVIEW_SIZE = 256

export const getCachedProfilePicture = () => {
  return localStorage.getItem(PROFILE_PICTURE_CACHE_KEY)
}

export const setCachedProfilePicture = (src) => {
  if (!src) {
    localStorage.removeItem(PROFILE_PICTURE_CACHE_KEY)
    return null
  }

  try {
    localStorage.setItem(PROFILE_PICTURE_CACHE_KEY, src)
    return src
  } catch (error) {
    console.warn('Unable to cache profile picture locally:', error)
    return src
  }
}

const loadImageFromBlob = (blob) => {
  return new Promise((resolve, reject) => {
    const imageUrl = URL.createObjectURL(blob)
    const image = new Image()

    image.onload = () => {
      URL.revokeObjectURL(imageUrl)
      resolve(image)
    }

    image.onerror = (error) => {
      URL.revokeObjectURL(imageUrl)
      reject(error)
    }

    image.src = imageUrl
  })
}

const createPreviewDataUrl = (image) => {
  const sourceWidth = image.naturalWidth || image.width
  const sourceHeight = image.naturalHeight || image.height
  const largestSide = Math.max(sourceWidth, sourceHeight)
  const scale = largestSide > PROFILE_PICTURE_PREVIEW_SIZE
    ? PROFILE_PICTURE_PREVIEW_SIZE / largestSide
    : 1

  const targetWidth = Math.max(1, Math.round(sourceWidth * scale))
  const targetHeight = Math.max(1, Math.round(sourceHeight * scale))

  const canvas = document.createElement('canvas')
  canvas.width = targetWidth
  canvas.height = targetHeight

  const context = canvas.getContext('2d')
  if (!context) {
    return null
  }

  context.drawImage(image, 0, 0, targetWidth, targetHeight)
  return canvas.toDataURL('image/jpeg', 0.88)
}

export const cacheProfilePictureBlob = async (blob) => {
  try {
    const image = await loadImageFromBlob(blob)
    const previewDataUrl = createPreviewDataUrl(image)

    if (!previewDataUrl) {
      return null
    }

    return setCachedProfilePicture(previewDataUrl)
  } catch (error) {
    console.warn('Unable to prepare cached profile picture:', error)
    return null
  }
}
