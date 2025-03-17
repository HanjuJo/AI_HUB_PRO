<template>
  <div class="app-container">
    <header>
      <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
          <router-link to="/" class="navbar-brand">
            <span class="brand-text">선택의 신</span>
          </router-link>
          <button 
            class="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
            aria-controls="navbarNav" 
            aria-expanded="false" 
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
              <li class="nav-item" v-if="isLoggedIn">
                <router-link to="/dashboard" class="nav-link dashboard-link">
                  <i class="bi bi-speedometer2 me-1"></i>내 대시보드
                </router-link>
              </li>
              <li class="nav-item" v-else>
                <router-link to="/login" class="nav-link dashboard-login-link">
                  <i class="bi bi-speedometer2 me-1"></i>대시보드 로그인
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/choice-helper" class="nav-link">
                  <i class="bi bi-shuffle me-1"></i>선택 도우미
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/daily-fortune" class="nav-link">
                  <i class="bi bi-stars me-1"></i>오늘의 운세
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/naming" class="nav-link">
                  <i class="bi bi-cursor-text me-1"></i>AI 작명
                </router-link>
              </li>
              <li class="nav-item dropdown">
                <a 
                  class="nav-link dropdown-toggle" 
                  href="#" 
                  id="navbarDropdown" 
                  role="button" 
                  data-bs-toggle="dropdown" 
                  aria-expanded="false"
                >
                  <i class="bi bi-gem me-1"></i>운세 보기
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <li>
                    <router-link to="/fortune/love" class="dropdown-item">
                      <i class="bi bi-heart me-1 text-danger"></i>연애운
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/fortune/money" class="dropdown-item">
                      <i class="bi bi-coin me-1 text-warning"></i>금전운
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/fortune/business" class="dropdown-item">
                      <i class="bi bi-briefcase me-1 text-success"></i>사업운
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/fortune/health" class="dropdown-item">
                      <i class="bi bi-activity me-1 text-info"></i>건강운
                    </router-link>
                  </li>
                </ul>
              </li>
            </ul>
            
            <ul class="navbar-nav">
              <li class="nav-item" v-if="!isLoggedIn">
                <a href="#" class="nav-link" @click.prevent="showLoginForm">
                  <i class="bi bi-box-arrow-in-right me-1"></i>로그인
                </a>
              </li>
              <li class="nav-item" v-if="!isLoggedIn">
                <button @click="showServiceModal" class="btn btn-outline-primary btn-sm membership-btn ms-2">
                  <i class="bi bi-gem me-1"></i>회원 서비스 준비중
                </button>
              </li>
              <li class="nav-item dropdown" v-if="isLoggedIn">
                <a 
                  class="nav-link dropdown-toggle" 
                  href="#" 
                  id="userDropdown" 
                  role="button" 
                  data-bs-toggle="dropdown" 
                  aria-expanded="false"
                >
                  <i class="bi bi-person-circle me-1"></i>{{ user.username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                  <li>
                    <router-link to="/dashboard" class="dropdown-item">
                      <i class="bi bi-speedometer2 me-1"></i>나의 대시보드
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/profile" class="dropdown-item">
                      <i class="bi bi-person me-1"></i>내 프로필
                    </router-link>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a href="#" class="dropdown-item" @click.prevent="logout">
                      <i class="bi bi-box-arrow-right me-1"></i>로그아웃
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
    
    <main class="py-4">
      <router-view/>
    </main>

    <footer class="bg-light py-4 mt-auto">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5 class="mb-3">선택의 신</h5>
            <p class="text-muted">
              사주팔자 기반 AI 선택 도우미로 더 나은 결정을 내리세요.
            </p>
          </div>
          <div class="col-md-3">
            <h5 class="mb-3">서비스</h5>
            <ul class="list-unstyled">
              <li><router-link to="/choice-helper" class="text-decoration-none">선택 도우미</router-link></li>
              <li><router-link to="/daily-fortune" class="text-decoration-none">오늘의 운세</router-link></li>
              <li><router-link to="/naming" class="text-decoration-none">AI 작명</router-link></li>
            </ul>
          </div>
          <div class="col-md-3">
            <h5 class="mb-3">고객지원</h5>
            <ul class="list-unstyled">
              <li><router-link to="/support" class="text-decoration-none">고객 센터</router-link></li>
              <li><a href="#" class="text-decoration-none">개인정보처리방침</a></li>
              <li><a href="#" class="text-decoration-none">이용약관</a></li>
            </ul>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-md-6">
            <p class="small text-muted mb-0">
              &copy; 2023 선택의 신. All rights reserved.
            </p>
          </div>
          <div class="col-md-6 text-md-end">
            <ul class="list-inline mb-0">
              <li class="list-inline-item">
                <a href="#" class="text-muted">
                  <i class="bi bi-instagram"></i>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="#" class="text-muted">
                  <i class="bi bi-facebook"></i>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="#" class="text-muted">
                  <i class="bi bi-twitter"></i>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
    
    <!-- 회원 서비스 안내 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showModal }" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-info-circle me-2"></i>회원 서비스 안내
            </h5>
            <button type="button" class="btn-close" @click="hideModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="text-center mb-4">
              <i class="bi bi-hourglass-split display-4 text-primary"></i>
            </div>
            <p class="text-center fs-5 mb-4">
              회원가입시 더 많은 서비스를 사용할 수 있도록 준비 중에 있습니다.
            </p>
            <p class="text-center fs-6 text-muted">
              감사합니다.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="hideModal">확인</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 로그인 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showLoginModal }" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-person-circle me-2"></i>선택의 신 로그인
            </h5>
            <button type="button" class="btn-close" @click="hideLoginModal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-0">
            <Login @login-success="loginSuccessHandler" />
          </div>
        </div>
      </div>
    </div>

    <!-- 모달 배경 오버레이 -->
    <div class="modal-backdrop fade show" v-if="showModal" @click="hideModal"></div>

    <!-- 모달 배경 오버레이 (로그인) -->
    <div class="modal-backdrop fade show" v-if="showLoginModal" @click="hideLoginModal"></div>
  </div>
</template>

<script>
import { defineComponent, computed, ref, onMounted, provide } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Login from './views/Login.vue'

export default defineComponent({
  name: 'App',
  components: {
    Navbar,
    Login
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isLoggedIn = computed(() => store.getters.isLoggedIn)
    const user = computed(() => store.getters.currentUser)
    
    // 모달 상태 관리
    const showModal = ref(false)
    const showLoginModal = ref(false)
    
    // provide를 사용하여 자식 컴포넌트에 showLoginForm 함수 제공
    provide('showLoginModal', () => {
      showLoginModal.value = true
      document.body.classList.add('modal-open')
    })
    
    // 컴포넌트 마운트 시 사용자 세션 복원
    onMounted(() => {
      // 세션 스토리지에서 사용자 정보 복원 시도
      store.dispatch('initUserSession')
      
      // 로컬 스토리지에서 사주 정보 확인
      const userBirthInfo = sessionStorage.getItem('userBirthInfo')
      if (userBirthInfo && store.getters.isLoggedIn) {
        store.dispatch('updateUserProfile', JSON.parse(userBirthInfo))
      }
    })
    
    // 회원 서비스 모달 표시 함수
    const showServiceModal = () => {
      showModal.value = true
      document.body.classList.add('modal-open')
    }
    
    // 로그인 모달 표시 함수
    const showLoginForm = () => {
      showLoginModal.value = true
      document.body.classList.add('modal-open')
    }
    
    // 모달 숨김 함수
    const hideModal = () => {
      showModal.value = false
      document.body.classList.remove('modal-open')
    }
    
    // 로그인 모달 숨김 함수
    const hideLoginModal = () => {
      showLoginModal.value = false
      document.body.classList.remove('modal-open')
    }
    
    // 로그인 성공 핸들러
    const loginSuccessHandler = () => {
      console.log('로그인 성공 이벤트 수신')
      
      // 모달 닫기 전 상태 체크
      const loginState = store.getters.isLoggedIn
      const currentUser = store.getters.currentUser
      console.log('로그인 상태:', loginState)
      console.log('사용자 정보:', currentUser)
      
      // 모달 먼저 닫기
      hideLoginModal()
      
      // 약간의 지연 후 대시보드로 이동 (모달 닫히는 애니메이션 처리 위함)
      setTimeout(() => {
        console.log('대시보드로 이동 시도')
        router.push({
          path: '/dashboard',
          // 캐시 방지 쿼리 추가
          query: { t: Date.now() }
        }).catch(err => {
          console.error('라우팅 오류:', err)
          // 오류 발생 시 대안으로 페이지 새로고침
          window.location.href = '/dashboard'
        })
      }, 500)
    }
    
    const logout = async () => {
      await store.dispatch('logout')
      router.push('/')
    }
    
    return {
      isLoggedIn,
      user,
      logout,
      showModal,
      showLoginModal,
      showServiceModal,
      showLoginForm,
      hideModal,
      hideLoginModal,
      loginSuccessHandler
    }
  }
})
</script>

<style>
/* 기본 스타일 초기화 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f8f9fa;
  color: #343a40;
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 레이아웃 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px 0;
}

/* 푸터 */
.footer {
  margin-top: auto;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

/* 드롭다운 메뉴 */
.dropdown-item {
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  transform: translateX(5px);
  background-color: #e9ecef;
}

.dropdown-item.text-danger:hover {
  background-color: #dc3545;
  color: white;
}

.dropdown-divider {
  border-top: 1px solid #e9ecef;
  margin: 0.5rem 0;
}

/* 유틸리티 클래스 */
.text-muted {
  color: #6c757d !important;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.brand-text {
  font-weight: 700;
  font-size: 1.5rem;
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-link {
  padding: 0.5rem 1rem;
  transition: all 0.3s;
}

.nav-link:hover {
  color: #6c5ce7;
}

/* 대시보드 링크 스타일 */
.dashboard-link {
  font-weight: 600;
  color: #6c5ce7 !important;
  background-color: rgba(108, 92, 231, 0.1);
  border-radius: 10px;
  padding: 0.5rem 1rem !important;
  margin-right: 0.5rem;
  transition: all 0.3s;
}

.dashboard-link:hover, 
.dashboard-link.router-link-active {
  background-color: rgba(108, 92, 231, 0.2);
  transform: translateY(-2px);
}

.dashboard-login-link {
  font-weight: 600;
  color: #6c5ce7 !important;
  border: 1px dashed rgba(108, 92, 231, 0.5);
  border-radius: 10px;
  padding: 0.5rem 1rem !important;
  margin-right: 0.5rem;
  transition: all 0.3s;
}

.dashboard-login-link:hover {
  background-color: rgba(108, 92, 231, 0.05);
  transform: translateY(-2px);
}

/* 회원 서비스 버튼 스타일 */
.membership-btn {
  font-weight: 600;
  border-radius: 50px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  border-color: #6c5ce7;
  color: #6c5ce7;
  transition: all 0.3s;
}

.membership-btn:hover {
  background-color: #6c5ce7;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(108, 92, 231, 0.3);
}

/* 모달 스타일 */
.modal.show {
  display: block;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.modal {
  z-index: 1050;
}

.modal-content {
  border: none;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.modal-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #a29bfe, #6c5ce7);
  color: white;
  border-radius: 15px 15px 0 0;
}

.modal-body {
  padding: 2rem 1.5rem;
}

.modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1rem 1.5rem;
}

.modal-title {
  font-weight: 600;
}

.btn-primary {
  background: linear-gradient(135deg, #a29bfe, #6c5ce7);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #6c5ce7, #5b52d1);
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(108, 92, 231, 0.3);
}

/* body 스타일 */
body.modal-open {
  overflow: hidden;
}
</style>
