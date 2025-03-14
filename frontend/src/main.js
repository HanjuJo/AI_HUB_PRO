import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from './store'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import * as bootstrap from 'bootstrap'

// Bootstrap 초기화
const initBootstrap = () => {
  // 드롭다운 초기화
  const dropdownElementList = document.querySelectorAll('.dropdown-toggle')
  const dropdownList = [...dropdownElementList].map(dropdownToggleEl => new bootstrap.Dropdown(dropdownToggleEl))
}

// 페이지 로드 후 Bootstrap 초기화
document.addEventListener('DOMContentLoaded', initBootstrap)

// Axios 기본 설정
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8004/api/v1'

// Axios 인터셉터 설정
axios.interceptors.request.use(request => {
  const token = store.getters.token
  if (token) {
    request.headers.Authorization = `Bearer ${token}`
  }
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
app.use(store)

app.mount('#app')
