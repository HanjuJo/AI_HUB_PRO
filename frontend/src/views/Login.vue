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
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const isLoading = ref(false)
    const error = ref('')

    const handleSubmit = async () => {
      try {
        isLoading.value = true
        error.value = ''

        // 실제 구현에서는 백엔드 API를 호출합니다
        // const response = await axios.post('/api/v1/auth/login/access-token', {
        //   username: email.value,
        //   password: password.value
        // })
        
        // 테스트용 모의 응답
        const response = { data: { access_token: 'test_token', token_type: 'bearer' } }
        
        // 토큰 저장
        const token = response.data.access_token
        localStorage.setItem('token', token)
        
        // 사용자 정보 가져오기 (실제 구현에서는 API 호출)
        // const userResponse = await axios.get('/api/v1/users/me', {
        //   headers: { Authorization: `Bearer ${token}` }
        // })
        
        // 로그인 성공 후 대시보드로 이동
        router.push('/dashboard')
      } catch (err) {
        console.error('로그인 오류:', err)
        error.value = '이메일 또는 비밀번호가 올바르지 않습니다.'
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
