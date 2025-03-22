import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles/telegram-theme.css'
import './assets/styles/tailwind.css'
import './assets/styles/base.css'
import './assets/styles/app-styles.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
