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
            <li class="nav-item">
              <router-link class="nav-link" to="/content-optimization">콘텐츠 최적화</router-link>
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
              <button class="nav-link dropdown-toggle btn btn-link" @click="toggleDropdown">
                <i class="bi bi-person-circle me-1"></i>
                {{ user?.username || '사용자' }}
              </button>
              <div class="dropdown-menu dropdown-menu-end" :class="{ show: isDropdownOpen }" @click.stop>
                <router-link class="dropdown-item" to="/dashboard" @click="closeDropdown">
                  <i class="bi bi-speedometer2 me-2"></i>개인 대시보드
                </router-link>
                <router-link class="dropdown-item" to="/profile" @click="closeDropdown">
                  <i class="bi bi-person-circle me-2"></i>내 정보
                </router-link>
                <router-link class="dropdown-item" to="/ai-tools" @click="closeDropdown">
                  <i class="bi bi-tools me-2"></i>내 AI 도구함
                </router-link>
                <router-link class="dropdown-item" to="/support" @click="closeDropdown">
                  <i class="bi bi-question-circle me-2"></i>문의사항
                </router-link>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">
                  <i class="bi bi-box-arrow-right me-2"></i>로그아웃
                </a>
              </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'



export default {
  name: 'App',

  setup() {
    const router = useRouter()
    const store = useStore()
    const isDropdownOpen = ref(false)

    const user = computed(() => store.getters.currentUser)
    const isLoggedIn = computed(() => store.getters.isAuthenticated)

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const closeDropdown = () => {
      isDropdownOpen.value = false
    }

    const handleClickOutside = (event) => {
      const dropdown = document.querySelector('.dropdown')
      if (dropdown && !dropdown.contains(event.target)) {
        closeDropdown()
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    const handleLogout = async () => {
      try {
        await store.dispatch('logout')
        closeDropdown()
        router.push('/login')
      } catch (err) {
        console.error('로그아웃 오류:', err)
      }
    }



    return {
      user,
      isLoggedIn,
      isDropdownOpen,
      toggleDropdown,
      closeDropdown,
      handleLogout
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

/* 드롭다운 메뉴 스타일 */
.dropdown {
  position: relative;
}

.dropdown-toggle {
  background: none;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
}

.dropdown-toggle:hover,
.dropdown-toggle:focus {
  color: rgba(255, 255, 255, 0.8);
}

.dropdown-menu {
  display: none;
  position: absolute;
  right: 0;
  top: 100%;
  min-width: 200px;
  padding: 0.5rem 0;
  margin: 0.125rem 0 0;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  color: #212529;
  text-decoration: none;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.dropdown-item.text-danger:hover {
  background-color: #dc3545;
  color: white;
}

.dropdown-divider {
  border-top: 1px solid #e9ecef;
  margin: 0.5rem 0;
}
</style>
