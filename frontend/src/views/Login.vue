<template>
  <div class="welcome-page">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">AI HUB에 오신 것을 환영합니다!</h4>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            <form @submit.prevent="handleSubmit">
              <div class="mb-4">
                <label for="username" class="form-label">사용하실 이름을 입력해주세요</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="username"
                  v-model="username"
                  required
                  placeholder="이름을 입력하세요"
                  :class="{ 'is-invalid': error }"
                />
                <div class="form-text text-muted">
                  입력하신 이름으로 AI HUB의 모든 기능을 무료로 이용하실 수 있습니다.
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-lg w-100" :disabled="isLoading || !username.trim()">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                시작하기
              </button>
            </form>
            <div class="mt-4 text-center">
              <p class="text-muted">
                * 세션이 종료되면 입력하신 정보는 초기화됩니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const store = useStore()
    const username = ref('')
    const isLoading = ref(false)
    const error = ref('')

    const handleSubmit = async () => {
      try {
        if (!username.value.trim()) {
          error.value = '이름을 입력해주세요.'
          return
        }

        isLoading.value = true
        error.value = ''

        // 세션 스토리지에 사용자 이름 저장
        sessionStorage.setItem('guestName', username.value)

        // Vuex 스토어에 게스트 사용자 정보 저장
        await store.dispatch('login', {
          user: {
            username: username.value,
            isGuest: true,
            created_at: new Date().toISOString()
          }
        })

        // 네비게이션 메뉴 상태 초기화
        await store.dispatch('setMenuState', true)

        // 대시보드로 이동
        router.push('/dashboard')
      } catch (err) {
        console.error('오류:', err)
        error.value = '오류가 발생했습니다. 다시 시도해주세요.'
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      isLoading,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.welcome-page {
  margin-top: 3rem;
}

.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
  padding: 1.5rem;
}

.card-body {
  padding: 2rem;
}

.form-control {
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
  border-radius: 10px;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
  border-radius: 10px;
}

.text-muted {
  font-size: 0.9rem;
}
</style>
