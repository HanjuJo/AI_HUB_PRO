<template>
  <div class="app-container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">AI 콘텐츠 제작 지원 플랫폼</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">홈</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/ai-tools">AI 도구</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/tool-combinations">도구 조합</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/youtube-data">유튜브 데이터</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link class="nav-link" to="/login">로그인</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link class="nav-link" to="/register">회원가입</router-link>
            </li>
            <li class="nav-item dropdown" v-if="isLoggedIn">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                {{ user.username }}
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><router-link class="dropdown-item" to="/dashboard">내 대시보드</router-link></li>
                <li><router-link class="dropdown-item" to="/profile">내 정보</router-link></li>
                <li><router-link class="dropdown-item" to="/ai-tools">내 도구함</router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click.prevent="logout">로그아웃</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container">
      <router-view />
    </div>

    <footer class="footer mt-5 py-3 bg-light">
      <div class="container text-center">
        <span class="text-muted"> 2025 AI . All rights reserved.</span>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const user = ref(null)
    const isLoggedIn = computed(() => !!user.value)

    const logout = async () => {
      try {
        const token = localStorage.getItem('token')
        if (token) {
          // 백엔드에 로그아웃 요청 전송 (실제 구현 시 사용)
          // await axios.post('http://localhost:8000/api/v1/auth/logout', {}, {
          //   headers: { Authorization: `Bearer ${token}` }
          // })
        }
      } catch (err) {
        console.error('로그아웃 오류:', err)
      } finally {
        // 로컬 상태 초기화
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      }
    }

    const checkAuth = () => {
      const token = localStorage.getItem('token')
      if (token) {
        const userData = localStorage.getItem('user')
        if (userData) {
          user.value = JSON.parse(userData)
        }
      }
    }

    checkAuth()

    // Add route guard to prevent access to dashboard without authentication
    router.beforeEach((to, from, next) => {
      if (to.path === '/dashboard' && !isLoggedIn.value) {
        next('/login')
      } else {
        next()
      }
    })

    return {
      user,
      isLoggedIn,
      logout
    }
  }
}
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  flex: 1;
}

.footer {
  margin-top: auto;
}
</style>
