export const SESSION_EXPIRED_EVENT = 'session-expired'

export const isUnauthorizedResponse = (response) =>
  response.status === 401 || response.status === 403

export const notifySessionExpired = () => {
  window.dispatchEvent(new CustomEvent(SESSION_EXPIRED_EVENT))
}

export const handleUnauthorizedResponse = (response) => {
  if (isUnauthorizedResponse(response)) {
    notifySessionExpired()
    return true
  }

  return false
}
