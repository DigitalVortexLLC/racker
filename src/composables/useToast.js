import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

export function useToast() {
  const addToast = (type, message, detail = '', duration = 3000) => {
    const id = nextId++
    const toast = {
      id,
      type,
      message,
      detail,
      duration
    }
    
    toasts.value.push(toast)
    
    // Auto remove after duration
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const showSuccess = (message, detail = '') => {
    addToast('success', message, detail, 3000)
  }

  const showError = (message, detail = '') => {
    addToast('error', message, detail, 5000)
  }

  const showInfo = (message, detail = '') => {
    addToast('info', message, detail, 3000)
  }

  const showWarn = (message, detail = '') => {
    addToast('warning', message, detail, 4000)
  }

  // Generic showToast function that maps severity to specific functions
  const showToast = (severity, message, detail = '') => {
    const severityMap = {
      'success': showSuccess,
      'error': showError,
      'info': showInfo,
      'warn': showWarn,
      'warning': showWarn
    }

    const toastFn = severityMap[severity] || showInfo
    toastFn(message, detail)
  }

  return {
    toasts,
    showSuccess,
    showError,
    showInfo,
    showWarn,
    showToast,
    removeToast
  }
}