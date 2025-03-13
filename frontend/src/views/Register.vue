<template>
  <div class="register-page">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">회원가입</h4>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="username" class="form-label">사용자 이름</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="username"
                  required
                  placeholder="사용자 이름을 입력하세요"
                />
              </div>
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
                <div class="form-text">비밀번호는 최소 8자 이상이어야 합니다.</div>
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">비밀번호 확인</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="confirmPassword"
                  required
                  placeholder="비밀번호를 다시 입력하세요"
                />
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="termsAgreed" v-model="termsAgreed" required>
                <label class="form-check-label" for="termsAgreed">
                  <a href="#" @click.prevent="showTerms = true">이용약관</a>에 동의합니다
                </label>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="isLoading || !isFormValid">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                회원가입
              </button>
            </form>
            <div class="mt-3 text-center">
              <p>이미 계정이 있으신가요? <router-link to="/login">로그인</router-link></p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 이용약관 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showTerms }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">이용약관</h5>
            <button type="button" class="btn-close" @click="showTerms = false"></button>
          </div>
          <div class="modal-body">
            <h6>AI 콘텐츠 제작 지원 플랫폼 이용약관</h6>
            <p>본 약관은 AI 콘텐츠 제작 지원 플랫폼 서비스 이용에 관한 조건 및 절차, 이용자와 당사의 권리, 의무, 책임사항을 규정함을 목적으로 합니다.</p>
            <p>1. 서비스 이용 목적</p>
            <p>2. 개인정보 수집 및 이용</p>
            <p>3. 이용자의 의무</p>
            <p>4. 서비스 제공자의 의무</p>
            <p>5. 서비스 이용 제한</p>
            <p>6. 저작권 및 지적재산권</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showTerms = false">닫기</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ 'show': showTerms }" v-if="showTerms"></div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const termsAgreed = ref(false)
    const isLoading = ref(false)
    const error = ref('')
    const showTerms = ref(false)

    const isFormValid = computed(() => {
      return (
        username.value.length > 0 &&
        email.value.length > 0 &&
        password.value.length >= 8 &&
        password.value === confirmPassword.value &&
        termsAgreed.value
      )
    })

    const handleSubmit = async () => {
      if (!isFormValid.value) {
        if (password.value !== confirmPassword.value) {
          error.value = '비밀번호가 일치하지 않습니다.'
        } else if (password.value.length < 8) {
          error.value = '비밀번호는 최소 8자 이상이어야 합니다.'
        }
        return
      }

      try {
        isLoading.value = true
        error.value = ''

        console.log('회원가입 시도 중...')

        // 백엔드 API 호출 - 기본 요청
        const userData = {
          username: username.value,
          email: email.value,
          password: password.value
        }

        console.log('요청 URL:', 'http://localhost:8000/api/v1/users/')
        
        // 직접 서버 URL을 사용하여 요청
        const response = await axios.post('http://localhost:8000/api/v1/users/', userData, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        console.log('회원가입 성공:', response.data)
        
        // 회원가입 성공 후 로그인 페이지로 이동
        router.push('/login')
      } catch (err) {
        console.error('회원가입 오류:', err)
        if (err.response) {
          console.error('서버 응답:', err.response.status, err.response.data)
          error.value = err.response.data.detail || '회원가입 중 오류가 발생했습니다.'
        } else if (err.request) {
          console.error('서버에서 응답이 없습니다:', err.request)
          error.value = '서버에 연결할 수 없습니다.'
        } else {
          console.error('요청 설정 오류:', err.message)
          error.value = '회원가입 중 오류가 발생했습니다.'
        }
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      email,
      password,
      confirmPassword,
      termsAgreed,
      isLoading,
      error,
      showTerms,
      isFormValid,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.register-page {
  margin-top: 2rem;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: #000;
}

.modal-backdrop.fade {
  opacity: 0;
}

.modal-backdrop.show {
  opacity: 0.5;
}

.modal.fade {
  z-index: 1050;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal.show {
  display: block;
}
</style>
