<template>
  <div class="login-page">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">로그인</h4>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="email" class="form-label">이메일</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="email"
                  required
                  placeholder="이메일을 입력하세요"
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">비밀번호</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  required
                  placeholder="비밀번호를 입력하세요"
                />
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="rememberMe" v-model="rememberMe">
                <label class="form-check-label" for="rememberMe">로그인 상태 유지</label>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                로그인
              </button>
            </form>
            <div class="mt-3 text-center">
              <p>계정이 없으신가요? <router-link to="/register">회원가입</router-link></p>
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
import { auth } from '@/api'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const isLoading = ref(false)
    const error = ref('')
    const store = useStore()

    const handleSubmit = async () => {
      try {
        isLoading.value = true
        error.value = ''

        // OAuth2 형식에 맞게 form-urlencoded 형식으로 데이터 전송
        // 로그인 시도 로그 추가
        console.log('로그인 시도:', { email: email.value })
        
        const formData = new URLSearchParams()
        formData.append('username', email.value)
        formData.append('password', password.value)
        
        // 로그인 요청 전송
        const response = await auth.login(formData)
        console.log('로그인 응답:', response.data)
        
        const token = response.data.access_token
        if (!token) {
          throw new Error('토큰이 없습니다')
        }
        
        // 토큰 저장
        localStorage.setItem('token', token)
        
        // 사용자 정보 요청
        const userResponse = await auth.getCurrentUser()
        console.log('사용자 정보:', userResponse.data)
        
        // 상태 관리
        await store.dispatch('login', {
          user: userResponse.data,
          token: token
        })
        
        // 네비게이션 메뉴 상태 초기화
        await store.dispatch('setMenuState', true)
        
        router.push('/dashboard')
      } catch (err) {
        console.error('로그인 오류:', err)
        
        if (err.response) {
          console.error('서버 응답:', err.response.data)
          
          if (err.response.status === 401) {
            error.value = '이메일 또는 비밀번호가 올바르지 않습니다.'
          } else if (err.response.status === 422) {
            error.value = '입력 데이터가 유효하지 않습니다.'
          } else if (err.response.status === 400) {
            error.value = '비활성화된 사용자입니다.'
          } else {
            error.value = '서버 오류가 발생했습니다. 다시 시도해주세요.'
          }
        } else if (err.message === '토큰이 없습니다') {
          error.value = '로그인에 실패했습니다. 다시 시도해주세요.'
        } else {
          error.value = '서버에 연결할 수 없습니다.'
        }
      } finally {
        isLoading.value = false
      }
    }

    return {
      email,
      password,
      rememberMe,
      isLoading,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.login-page {
  margin-top: 2rem;
}
</style>
