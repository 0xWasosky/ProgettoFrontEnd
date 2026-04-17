/**
 * Shared theme toggle helper.
 * Uses `localStorage.theme` and the `data-theme` attribute on `documentElement`.
 */

export function initLightDarkMode() {
  const stored = localStorage.getItem('theme')
  const isDark = stored == 'dark'
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light')
  return isDark
}

export function toggleLightDarkMode() {
  const stored = localStorage.getItem('theme')
  const current = stored == 'dark' ? 'dark' : 'light'
  const next = current == 'dark' ? 'light' : 'dark'

  document.documentElement.setAttribute('data-theme', next)
  localStorage.setItem('theme', next)
  return next == 'dark'
}

