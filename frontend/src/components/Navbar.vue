<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        AI HUB
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        @click="toggleMenu"
        :aria-expanded="isMenuOpen"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div
        class="collapse navbar-collapse"
        :class="{ 'show': isMenuOpen }"
        id="navbarNav"
      >
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <router-link class="nav-link" to="/dashboard">
              <i class="bi bi-speedometer2"></i> Personal Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/ai-tools">
              <i class="bi bi-tools"></i> AI Tools
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/youtube-analysis">
              <i class="bi bi-youtube"></i> YouTube Analysis
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/support">
              <i class="bi bi-question-circle"></i> Support/Inquiries
            </router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle d-flex align-items-center"
              href="#"
              @click.prevent="toggleUserMenu"
              :class="{ 'show': isUserMenuOpen }"
            >
              <i class="bi bi-person-circle me-1"></i>
              {{ currentUser.username }}
            </a>
            <ul
              class="dropdown-menu dropdown-menu-end"
              :class="{ 'show': isUserMenuOpen }"
            >
              <li>
                <router-link class="dropdown-item" to="/profile">
                  <i class="bi bi-person"></i> User Profile
                </router-link>
              </li>
              <template v-if="currentUser.role === 'guest'">
                <li><hr class="dropdown-divider"></li>
                <li>
                  <router-link class="dropdown-item" to="/login">
                    <i class="bi bi-box-arrow-in-right"></i> Login
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/register">
                    <i class="bi bi-person-plus"></i> Register
                  </router-link>
                </li>
              </template>
              <template v-else>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">
                    <i class="bi bi-box-arrow-right"></i> Exit Session
                  </a>
                </li>
              </template>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const store = useStore()
    const router = useRouter()
    const isUserMenuOpen = ref(false)

    const currentUser = computed(() => store.getters.currentUser)
    const isMenuOpen = computed(() => store.getters.isMenuOpen)

    const toggleMenu = () => {
      store.dispatch('setMenuState', !isMenuOpen.value)
    }

    const toggleUserMenu = () => {
      isUserMenuOpen.value = !isUserMenuOpen.value
    }

    const handleLogout = () => {
      store.dispatch('logout')
      router.push('/')
    }

    // 클릭 이벤트 리스너 추가
    const closeMenus = (event) => {
      if (!event.target.closest('.dropdown')) {
        isUserMenuOpen.value = false
      }
      if (!event.target.closest('.navbar-collapse') && !event.target.closest('.navbar-toggler')) {
        store.dispatch('setMenuState', false)
      }
    }

    // 컴포넌트 마운트 시 이벤트 리스너 추가
    onMounted(() => {
      document.addEventListener('click', closeMenus)
    })

    // 컴포넌트 언마운트 시 이벤트 리스너 제거
    onUnmounted(() => {
      document.removeEventListener('click', closeMenus)
    })

    return {
      currentUser,
      isMenuOpen,
      isUserMenuOpen,
      toggleMenu,
      toggleUserMenu,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.nav-link {
  font-size: 1rem;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
}

.nav-link i {
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.dropdown-item {
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
}

.dropdown-item i {
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

@media (max-width: 991.98px) {
  .navbar-collapse {
    padding: 1rem 0;
  }
  
  .dropdown-menu {
    border: none;
    box-shadow: none;
    padding: 0;
    margin: 0;
  }
  
  .dropdown-item {
    padding: 0.5rem 1rem;
  }
}
</style>
