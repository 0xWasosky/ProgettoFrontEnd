const LOCAL_API_PORT = 5000

/*const getLocalApiHost = () => {
  if (typeof window === 'undefined') {
    return 'localhost'
  }

  return window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost'
}*/

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  `http://80.211.24.126:${LOCAL_API_PORT}`

export const buildApiUrl = (path) =>
  `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
//80.211.24.126:5000