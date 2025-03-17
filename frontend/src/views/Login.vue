<template>
  <div class="login-modal">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">선택의 신에 오신 것을 환영합니다!</h4>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <div v-if="successMessage" class="alert alert-success" role="alert">
              <i class="bi bi-check-circle-fill me-2"></i>{{ successMessage }}
            </div>
            
            <!-- 단계 표시기 -->
            <div class="progress mb-4">
              <div class="progress-bar" :style="{ width: step === 1 ? '30%' : '100%' }"></div>
            </div>
            
            <!-- 단계 1: 이름 입력 -->
            <form v-if="step === 1" @submit.prevent="goToStep2">
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
                  입력하신 이름으로 선택의 신의 모든 기능을 이용하실 수 있습니다.
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-lg w-100" :disabled="!username.trim()">
                다음 단계로
              </button>
            </form>
            
            <!-- 단계 2: 생년월일, 시간, 성별 입력 -->
            <form v-if="step === 2" @submit.prevent="handleSubmit">
              <h5 class="mb-3">안녕하세요, <strong>{{ username }}</strong>님!</h5>
              <p class="text-muted mb-4">더 정확한 사주 분석을 위해 아래 정보를 입력해주세요.</p>
              
              <div class="mb-3">
                <label for="birthdate" class="form-label">생년월일</label>
                <input
                  type="date"
                  class="form-control"
                  id="birthdate"
                  v-model="birthdate"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="birthtime" class="form-label">태어난 시간</label>
                <input
                  type="time"
                  class="form-control"
                  id="birthtime"
                  v-model="birthtime"
                />
                <div class="form-text text-muted">
                  정확한 시간을 모르시면 비워두셔도 됩니다.
                </div>
              </div>
              
              <div class="mb-4">
                <label class="form-label d-block">성별</label>
                <div class="btn-group w-100" role="group">
                  <input type="radio" class="btn-check" name="gender" id="male" value="남자" v-model="gender" required>
                  <label class="btn btn-outline-primary" for="male">남자</label>
                  
                  <input type="radio" class="btn-check" name="gender" id="female" value="여자" v-model="gender" required>
                  <label class="btn btn-outline-primary" for="female">여자</label>
                </div>
              </div>
              
              <div class="d-flex gap-2">
                <button type="button" class="btn btn-outline-secondary btn-lg flex-grow-1" @click="step = 1">
                  이전으로
                </button>
                <button type="submit" class="btn btn-primary btn-lg flex-grow-1" :disabled="isLoading || !isFormValid">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ isLoading ? '처리 중...' : '로그인' }}
                </button>
              </div>
            </form>
            
            <div class="mt-4 text-center">
              <p class="text-muted">
                * 입력하신 정보는 로그아웃 전까지 세션에 유지됩니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'Login',
  emits: ['login-success'],
  setup(props, { emit }) {
    const router = useRouter()
    const store = useStore()
    
    // 폼 입력 데이터
    const username = ref('')
    const birthdate = ref('')
    const birthtime = ref('')
    const gender = ref('')
    const step = ref(1)
    
    const isLoading = ref(false)
    const error = ref('')
    const successMessage = ref('')

    // 컴포넌트 로드 시 사용자 세션 확인
    onMounted(() => {
      // 이미 로그인 상태인 경우 대시보드로 이동
      if (store.getters.isLoggedIn) {
        router.push('/dashboard')
        return
      }
      
      // 세션 스토리지에서 사용자 정보 복원 시도
      const restored = store.dispatch('initUserSession')
      if (restored) {
        router.push('/dashboard')
      }
    })
    
    // 폼 유효성 검사
    const isFormValid = computed(() => {
      return username.value.trim() && birthdate.value && gender.value
    })
    
    // 2단계로 이동
    const goToStep2 = () => {
      if (!username.value.trim()) {
        error.value = '이름을 입력해주세요.'
        return
      }
      
      error.value = ''
      successMessage.value = ''
      step.value = 2
    }

    const handleSubmit = async () => {
      try {
        if (!isFormValid.value) {
          error.value = '모든 필수 정보를 입력해주세요.'
          return
        }

        isLoading.value = true
        error.value = ''
        successMessage.value = ''

        // 현재 날짜 및 시간 정보
        const now = new Date()
        
        // 사용자 정보를 세션 스토리지에 저장
        const birthInfo = {
          birthdate: birthdate.value,
          birthtime: birthtime.value,
          gender: gender.value
        }
        
        sessionStorage.setItem('userBirthInfo', JSON.stringify(birthInfo))
        console.log('저장된 사용자 정보:', {
          username: username.value,
          birthInfo
        })
        
        // 잠시 대기하여 사용자에게 로딩 상태를 보여줌
        await new Promise(resolve => setTimeout(resolve, 800))
        
        // Vuex 스토어에 사용자 정보 저장
        await store.dispatch('login', {
          user: {
            username: username.value,
            isGuest: false,
            created_at: now.toISOString(),
            // 프로필 정보 저장
            profile: {
              birthdate: birthdate.value,
              birthtime: birthtime.value,
              gender: gender.value
            }
          }
        })

        // 네비게이션 메뉴 상태 초기화
        await store.dispatch('setMenuState', true)

        // 성공 메시지 표시
        successMessage.value = '로그인 성공! 잠시 후 대시보드로 이동합니다.'
        
        console.log('로그인 성공 이벤트 발생')
        // 로그인 성공 이벤트 발생 - 상위 컴포넌트에서 처리
        emit('login-success')
      } catch (err) {
        console.error('로그인 오류:', err)
        error.value = '오류가 발생했습니다. 다시 시도해주세요.'
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      birthdate,
      birthtime,
      gender,
      step,
      isLoading,
      error,
      successMessage,
      isFormValid,
      goToStep2,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.login-modal {
  margin-top: 3rem;
  margin-bottom: 3rem;
}

.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
  padding: 1.5rem;
  background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important;
  text-align: center;
}

.card-body {
  padding: 2.5rem;
}

.form-control {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 10px;
  border: 1px solid #e1e1e1;
  background-color: #f8f9fa;
}

.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(108, 92, 231, 0.25);
  border-color: #a29bfe;
}

.btn-primary {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3);
}

.btn-outline-secondary {
  border-color: #ced4da;
  color: #6c757d;
}

.btn-outline-primary {
  border-color: #6c5ce7;
  color: #6c5ce7;
}

.btn-outline-primary:hover {
  background-color: #6c5ce7;
  color: white;
}

.btn-check:checked + .btn-outline-primary {
  background-color: #6c5ce7;
  color: white;
  border-color: #6c5ce7;
}

.progress {
  height: 8px;
  border-radius: 4px;
  background-color: #e9ecef;
}

.progress-bar {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  transition: width 0.3s ease;
}
</style>
