import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

// Axios 기본 설정
axios.defaults.baseURL = ''
axios.interceptors.request.use(request => {
  console.log('Starting Request', request.url)
  return request
})

axios.interceptors.response.use(
  response => {
    console.log('Response:', response.status, response.data)
    return response
  },
  error => {
    console.error('Axios 오류:', error.message)
    if (error.response) {
      console.error('Response Error:', error.response.status, error.response.data)
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
