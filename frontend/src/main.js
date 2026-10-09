import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'
import { definePreset } from '@primevue/themes'
import Aura from '@primevue/themes/aura'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'

import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'

import 'primeicons/primeicons.css'
import './assets/main.css'

// Preset com a paleta corporativa do Roadmap (Roxo #3E2666 / #6D56A0 e Rosa #ED1E81)
const AppPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '#F6F3FB',
      100: '#EEEAF5',
      200: '#DDD5EC',
      300: '#C2B4DE',
      400: '#9E8CC9',
      500: '#6D56A0',
      600: '#5C448D',
      700: '#4B3576',
      800: '#3E2666',
      900: '#2C194D',
      950: '#1B0E33'
    }
  }
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: AppPreset,
    options: {
      prefix: 'p',
      darkModeSelector: false,
      cssLayer: false
    }
  }
})
app.use(ToastService)
app.use(ConfirmationService)

// Registra globalmente componentes essenciais de feedback
app.component('Toast', Toast)
app.component('ConfirmDialog', ConfirmDialog)

app.mount('#app')
