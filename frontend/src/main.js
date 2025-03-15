import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// Bootstrap & Icons
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'

// Axios 기본 설정
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Axios 인터셉터 설정
axios.interceptors.request.use(
  config => {
    const token = store.state.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('요청 오류:', error)
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        store.dispatch('logout')
        router.push('/login')
      }
      console.error('API 오류:', error.response.data)
    }
    return Promise.reject(error)
  }
)

// Vue 앱 생성
const app = createApp(App)

// 글로벌 프로퍼티
app.config.globalProperties.$axios = axios

// 플러그인 등록
app.use(store)
app.use(router)

// 앱 마운트
app.mount('#app')
