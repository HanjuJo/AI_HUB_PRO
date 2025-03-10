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
                <li><router-link class="dropdown-item" to="/profile">프로필</router-link></li>
                <li><router-link class="dropdown-item" to="/dashboard">대시보드</router-link></li>
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
        <span class="text-muted">© 2025 AI 콘텐츠 제작 지원 플랫폼. All rights reserved.</span>
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

    // 실제 구현에서는 Pinia 스토어를 사용하여 인증 상태를 관리할 것입니다
    const logout = () => {
      user.value = null
      localStorage.removeItem('token')
      router.push('/login')
    }

    // 컴포넌트 마운트 시 로컬 스토리지에서 토큰 확인
    const checkAuth = () => {
      const token = localStorage.getItem('token')
      if (token) {
        // 실제 구현에서는 토큰을 검증하고 사용자 정보를 가져옵니다
        user.value = { username: '사용자' }
      }
    }

    checkAuth()

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
