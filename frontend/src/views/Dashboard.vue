<template>
  <div class="dashboard">
    <!-- 환영 배너 -->
    <div class="welcome-banner mb-4">
      <div class="row align-items-center">
        <div class="col-lg-9">
      <h2 class="welcome-title">
        <i class="bi bi-person-circle me-2"></i>
            {{ currentUser?.username }}님의 선택 대시보드
      </h2>
      <p class="text-muted mb-0">
        <i class="bi bi-clock-history me-1"></i>
            최근 접속 시간: {{ formatDate(sessionStartTime) }}
      </p>
        </div>
        <div class="col-lg-3 text-end">
          <div class="fortune-pill">
            <span>오늘의 운세 지수: {{ todayLuckLevel }}%</span>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-6 mb-4">
        <div class="card card-fortune h-100">
          <div class="card-header">
            <h5 class="mb-0"><i class="bi bi-stars me-2"></i>최근 본 운세</h5>
          </div>
          <div class="card-body">
            <div v-if="recentFortunes.length === 0" class="text-center py-4">
              <p>최근 본 운세가 없습니다.</p>
              <router-link to="/daily-fortune" class="btn btn-primary">오늘의 운세 보기</router-link>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="fortune in recentFortunes" :key="fortune.id" class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ fortune.type }}</h6>
                    <small>{{ formatDate(fortune.date) }}</small>
                  </div>
                  <p class="mb-1">{{ fortune.summary }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                  <div>
                      <span class="badge bg-primary me-1">행운지수: {{ fortune.luckScore }}%</span>
                    </div>
                    <router-link :to="fortune.link" class="btn btn-sm btn-outline-primary">다시 보기</router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 mb-4">
        <div class="card card-choice h-100">
          <div class="card-header">
            <h5 class="mb-0"><i class="bi bi-shuffle me-2"></i>최근 선택 기록</h5>
          </div>
          <div class="card-body">
            <div v-if="recentChoices.length === 0" class="text-center py-4">
              <p>최근 선택 기록이 없습니다.</p>
              <router-link to="/choice-helper" class="btn btn-primary">선택 도우미 사용하기</router-link>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="choice in recentChoices" :key="choice.id" class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ choice.category }}</h6>
                    <small>{{ formatDate(choice.date) }}</small>
                  </div>
                  <p class="mb-1"><strong>질문:</strong> {{ choice.question }}</p>
                  <p class="mb-0"><strong>선택된 답변:</strong> <span class="text-success">{{ choice.selectedOption }}</span></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-12">
        <div class="card card-profile">
          <div class="card-header">
            <h5 class="mb-0"><i class="bi bi-person me-2"></i>나의 사주 정보</h5>
          </div>
          <div class="card-body">
            <div v-if="!userBirthInfo.birthdate" class="text-center py-4">
              <p>등록된 사주 정보가 없습니다.</p>
              <button @click="showBirthInfoModal" class="btn btn-primary">사주 정보 입력하기</button>
            </div>
            <div v-else class="row">
              <div class="col-md-4">
                <div class="birth-info p-3 border rounded mb-3">
                  <h6 class="mb-3 text-center">기본 정보</h6>
                  <p><strong>생년월일:</strong> {{ formatBirthdate(userBirthInfo.birthdate) }}</p>
                  <p><strong>태어난 시간:</strong> {{ userBirthInfo.birthtime || '미입력' }}</p>
                  <p><strong>성별:</strong> {{ userBirthInfo.gender === 'male' ? '남성' : '여성' }}</p>
                  <button @click="showBirthInfoModal" class="btn btn-sm btn-outline-primary w-100">
                    <i class="bi bi-pencil me-1"></i>정보 수정
                  </button>
                </div>
              </div>
              <div class="col-md-4">
                <div class="saju-chart p-3 border rounded mb-3">
                  <h6 class="mb-3 text-center">사주팔자</h6>
                  <div class="saju-grid mb-3">
                    <div class="row text-center mb-2">
                      <div class="col">시주</div>
                      <div class="col">일주</div>
                      <div class="col">월주</div>
                      <div class="col">년주</div>
                    </div>
                    <div class="row text-center mb-1">
                      <div class="col saju-cell">{{ sajuInfo.hour.heaven }}</div>
                      <div class="col saju-cell">{{ sajuInfo.day.heaven }}</div>
                      <div class="col saju-cell">{{ sajuInfo.month.heaven }}</div>
                      <div class="col saju-cell">{{ sajuInfo.year.heaven }}</div>
                    </div>
                    <div class="row text-center">
                      <div class="col saju-cell">{{ sajuInfo.hour.earth }}</div>
                      <div class="col saju-cell">{{ sajuInfo.day.earth }}</div>
                      <div class="col saju-cell">{{ sajuInfo.month.earth }}</div>
                      <div class="col saju-cell">{{ sajuInfo.year.earth }}</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="elements p-3 border rounded mb-3">
                  <h6 class="mb-3 text-center">오행 분석</h6>
                  <div class="elements-chart">
                    <div class="element-bar mb-2">
                      <div class="d-flex justify-content-between">
                        <span>금(金)</span>
                        <span>{{ elements.metal }}%</span>
                      </div>
                      <div class="progress">
                        <div class="progress-bar bg-secondary" :style="`width: ${elements.metal}%`"></div>
                      </div>
                    </div>
                    <div class="element-bar mb-2">
                      <div class="d-flex justify-content-between">
                        <span>목(木)</span>
                        <span>{{ elements.wood }}%</span>
                      </div>
                      <div class="progress">
                        <div class="progress-bar bg-success" :style="`width: ${elements.wood}%`"></div>
                      </div>
                    </div>
                    <div class="element-bar mb-2">
                      <div class="d-flex justify-content-between">
                        <span>수(水)</span>
                        <span>{{ elements.water }}%</span>
                      </div>
                      <div class="progress">
                        <div class="progress-bar bg-info" :style="`width: ${elements.water}%`"></div>
                      </div>
                    </div>
                    <div class="element-bar mb-2">
                      <div class="d-flex justify-content-between">
                        <span>화(火)</span>
                        <span>{{ elements.fire }}%</span>
                      </div>
                      <div class="progress">
                        <div class="progress-bar bg-danger" :style="`width: ${elements.fire}%`"></div>
                      </div>
                    </div>
                    <div class="element-bar mb-2">
                      <div class="d-flex justify-content-between">
                        <span>토(土)</span>
                        <span>{{ elements.earth }}%</span>
                      </div>
                      <div class="progress">
                        <div class="progress-bar bg-warning" :style="`width: ${elements.earth}%`"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-6 mb-4">
        <div class="card card-names h-100">
      <div class="card-header">
            <h5 class="mb-0"><i class="bi bi-cursor-text me-2"></i>최근 작명 결과</h5>
          </div>
          <div class="card-body">
            <div v-if="recentNames.length === 0" class="text-center py-4">
              <p>최근 작명 결과가 없습니다.</p>
              <router-link to="/naming" class="btn btn-primary">AI 작명 서비스 이용하기</router-link>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="name in recentNames" :key="name.id" class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ name.type === 'baby' ? '아이 이름' : '상호명' }}</h6>
                    <small>{{ formatDate(name.date) }}</small>
                  </div>
                  <p class="mb-1">{{ name.description }}</p>
                  <div class="name-results">
                    <span v-for="(result, index) in name.results" :key="index" class="badge bg-light text-dark me-2 p-2">
                      {{ result }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 mb-4">
        <div class="card card-recommendation h-100">
          <div class="card-header">
            <h5 class="mb-0"><i class="bi bi-magic me-2"></i>맞춤 운세 추천</h5>
      </div>
      <div class="card-body">
            <div class="recommended-fortune p-3 border rounded mb-3">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h6>{{ recommendedFortune.title }}</h6>
                  <p class="text-muted mb-0">{{ recommendedFortune.description }}</p>
                </div>
                <span class="badge bg-primary">적합도 {{ recommendedFortune.matching }}%</span>
              </div>
              <p class="mb-3">{{ recommendedFortune.summary }}</p>
              <div class="text-end">
                <router-link :to="recommendedFortune.link" class="btn btn-primary">자세히 보기</router-link>
              </div>
            </div>
            
            <div class="quick-links">
              <h6 class="mb-3">빠른 운세 메뉴</h6>
              <div class="row g-2">
                <div class="col-6">
                  <router-link to="/fortune/love" class="quick-link-item p-3 rounded d-block text-decoration-none love-link">
                    <i class="bi bi-heart-fill me-2"></i>연애운
                  </router-link>
                </div>
                <div class="col-6">
                  <router-link to="/fortune/money" class="quick-link-item p-3 rounded d-block text-decoration-none money-link">
                    <i class="bi bi-coin me-2"></i>금전운
                  </router-link>
                </div>
                <div class="col-6">
                  <router-link to="/fortune/business" class="quick-link-item p-3 rounded d-block text-decoration-none business-link">
                    <i class="bi bi-briefcase-fill me-2"></i>사업운
                  </router-link>
                </div>
                <div class="col-6">
                  <router-link to="/fortune/health" class="quick-link-item p-3 rounded d-block text-decoration-none health-link">
                    <i class="bi bi-heart-pulse-fill me-2"></i>건강운
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 사주 정보 수정 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showModal }" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-person-bounding-box me-2"></i>사주 정보 {{ userBirthInfo.birthdate ? '수정' : '입력' }}
            </h5>
            <button type="button" class="btn-close" @click="hideModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveBirthInfo">
              <div class="mb-3">
                <label for="birthdate" class="form-label">생년월일</label>
                <input 
                  type="date" 
                  id="birthdate" 
                  v-model="editingBirthInfo.birthdate" 
                  class="form-control" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="birthtime" class="form-label">태어난 시간</label>
                <input 
                  type="time" 
                  id="birthtime" 
                  v-model="editingBirthInfo.birthtime" 
                  class="form-control"
                >
                <div class="form-text">정확한 시간을 모르시면 비워두셔도 됩니다.</div>
              </div>
              <div class="mb-3">
                <label class="form-label">성별</label>
                <div class="d-flex">
                  <div class="form-check me-4">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      name="gender" 
                      id="male" 
                      value="male" 
                      v-model="editingBirthInfo.gender"
                      required
                    >
                    <label class="form-check-label" for="male">남성</label>
                  </div>
                  <div class="form-check">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      name="gender" 
                      id="female" 
                      value="female"
                      v-model="editingBirthInfo.gender"
                    >
                    <label class="form-check-label" for="female">여성</label>
                  </div>
                </div>
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-outline-secondary me-2" @click="hideModal">취소</button>
                <button type="submit" class="btn btn-primary">저장</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 모달 배경 오버레이 -->
    <div class="modal-backdrop fade show" v-if="showModal" @click="hideModal"></div>
  </div>
</template>

<script>
import { ref, onMounted, computed, reactive } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore();
    const router = useRouter();
    const currentUser = computed(() => store.getters.currentUser);
    const sessionStartTime = ref(currentUser.value?.created_at || new Date().toISOString());
    
    // 오늘의 운세 지수 (랜덤 생성)
    const todayLuckLevel = ref(Math.floor(Math.random() * 30) + 70); // 70-99 사이의 랜덤 값
    
    // 모달 상태 관리
    const showModal = ref(false);
    
    // 사용자 생년월일 정보
    const userBirthInfo = ref({
      birthdate: '',
      birthtime: '',
      gender: ''
    });
    
    // 수정 중인 사주 정보
    const editingBirthInfo = reactive({
      birthdate: '',
      birthtime: '',
      gender: ''
    });
    
    // 사주 정보
    const sajuInfo = ref({
      year: { heaven: '경', earth: '신' },
      month: { heaven: '신', earth: '유' },
      day: { heaven: '계', earth: '미' },
      hour: { heaven: '을', earth: '사' }
    });
    
    // 오행 정보
    const elements = ref({
      metal: 25,  // 금
      wood: 15,   // 목
      water: 30,  // 수
      fire: 20,   // 화
      earth: 10   // 토
    });
    
    // 최근 본 운세 목록
    const recentFortunes = ref([]);
    
    // 최근 선택 기록
    const recentChoices = ref([]);
    
    // 최근 작명 결과
    const recentNames = ref([]);
    
    // 맞춤 운세 추천
    const recommendedFortune = ref({
      title: '',
      description: '',
      summary: '',
      matching: 0,
      link: ''
    });

    // 날짜 포맷 함수
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return '';
      
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    // 생일 포맷 함수
    const formatBirthdate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return '';
      
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };
    
    // 사주 정보 입력 모달 표시 함수
    const showBirthInfoModal = () => {
      // 현재 값을 수정 폼에 설정
      editingBirthInfo.birthdate = userBirthInfo.value.birthdate;
      editingBirthInfo.birthtime = userBirthInfo.value.birthtime;
      editingBirthInfo.gender = userBirthInfo.value.gender;
      
      // 모달 표시
      showModal.value = true;
      
      // 모달 표시 시 body에 클래스 추가
      document.body.classList.add('modal-open');
    };
    
    // 모달 숨김 함수
    const hideModal = () => {
      showModal.value = false;
      document.body.classList.remove('modal-open');
    };
    
    // 사주 정보 저장 함수
    const saveBirthInfo = () => {
      // 실제 서비스에서는 API 호출을 통해 서버에 데이터 저장
      userBirthInfo.value = {
        birthdate: editingBirthInfo.birthdate,
        birthtime: editingBirthInfo.birthtime,
        gender: editingBirthInfo.gender
      };
      
      // 세션 스토리지에 저장
      sessionStorage.setItem('userBirthInfo', JSON.stringify(userBirthInfo.value));
      
      // Vuex 스토어에 사용자 프로필 정보 업데이트
      store.dispatch('updateUserProfile', {
        birthdate: editingBirthInfo.birthdate,
        birthtime: editingBirthInfo.birthtime,
        gender: editingBirthInfo.gender
      });
      
      // 사주 정보 변경에 따른 사주팔자 및 오행 정보 업데이트
      updateSajuInfo();
      
      // 모달 닫기
      hideModal();
      
      // 성공 메시지 표시 (실제 서비스에서 토스트 알림 등으로 구현)
      console.log('사주 정보가 저장되었습니다.');
    };
    
    // 사주 정보 업데이트 함수
    const updateSajuInfo = () => {
      // 실제 서비스에서는 API 호출을 통해 사주팔자 계산
      // 여기서는 간단한 시뮬레이션만 수행
      
      // 예시: 생년월일에 따라 간단한 패턴으로 사주 정보 변경
      if (userBirthInfo.value.birthdate) {
        const birthYear = new Date(userBirthInfo.value.birthdate).getFullYear();
        const birthMonth = new Date(userBirthInfo.value.birthdate).getMonth() + 1;
        
        // 간지 배열
        const heavenlyStems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'];
        const earthlyBranches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해'];
        
        // 간단한 계산 (실제 사주 계산과는 다름)
        const yearHeaven = heavenlyStems[birthYear % 10];
        const yearEarth = earthlyBranches[birthYear % 12];
        const monthHeaven = heavenlyStems[(birthYear * 2 + birthMonth) % 10];
        const monthEarth = earthlyBranches[birthMonth - 1];
        const dayHeaven = heavenlyStems[(birthYear + birthMonth + 1) % 10];
        const dayEarth = earthlyBranches[(birthYear + birthMonth) % 12];
        
        // 사주 정보 업데이트
        sajuInfo.value = {
          year: { heaven: yearHeaven, earth: yearEarth },
          month: { heaven: monthHeaven, earth: monthEarth },
          day: { heaven: dayHeaven, earth: dayEarth },
          hour: { heaven: '을', earth: '사' } // 시간은 간략히 처리
        };
        
        // 오행 정보 업데이트 - 간단한 랜덤 값
        elements.value = {
          metal: Math.floor(Math.random() * 40) + 10,
          wood: Math.floor(Math.random() * 40) + 10,
          water: Math.floor(Math.random() * 40) + 10,
          fire: Math.floor(Math.random() * 40) + 10,
          earth: Math.floor(Math.random() * 40) + 10
        };
        
        // 오행 총합이 100%가 되도록 보정
        const total = elements.value.metal + elements.value.wood + elements.value.water + 
                     elements.value.fire + elements.value.earth;
        
        if (total > 0) {
          const factor = 100 / total;
          elements.value.metal = Math.round(elements.value.metal * factor);
          elements.value.wood = Math.round(elements.value.wood * factor);
          elements.value.water = Math.round(elements.value.water * factor);
          elements.value.fire = Math.round(elements.value.fire * factor);
          elements.value.earth = Math.round(elements.value.earth * factor);
        }
      }
    };
    
    // 데이터 로드 함수들
    const loadUserData = () => {
      // 실제 구현에서는 API 호출이나 로컬 스토리지에서 데이터 로드
      
      // 1. Vuex 스토어에서 사용자 프로필 정보 확인
      const userProfile = store.getters.userProfile;
      
      // 2. 사용자 프로필에 사주 정보가 있으면 사용
      if (userProfile && userProfile.birthdate) {
        userBirthInfo.value = {
          birthdate: userProfile.birthdate,
          birthtime: userProfile.birthtime,
          gender: userProfile.gender
        };
        
        // 세션 스토리지에 저장 (일관성 유지)
        sessionStorage.setItem('userBirthInfo', JSON.stringify(userBirthInfo.value));
      } 
      // 3. 없으면 세션 스토리지 확인
      else {
        const savedBirthInfo = sessionStorage.getItem('userBirthInfo');
        if (savedBirthInfo) {
          userBirthInfo.value = JSON.parse(savedBirthInfo);
          
          // Vuex 스토어에도 업데이트
          store.dispatch('updateUserProfile', userBirthInfo.value);
        } else {
          // 테스트 데이터 로드
          userBirthInfo.value = {
            birthdate: '1990-05-15',
            birthtime: '08:30',
            gender: 'female'
          };
          
          // 세션 스토리지와 Vuex 스토어에 저장
          sessionStorage.setItem('userBirthInfo', JSON.stringify(userBirthInfo.value));
          store.dispatch('updateUserProfile', userBirthInfo.value);
        }
      }
      
      // 사주 정보가 있으면 사주팔자 업데이트
      if (userBirthInfo.value.birthdate) {
        updateSajuInfo();
      }
      
      loadRecentFortunes();
      loadRecentChoices();
      loadRecentNames();
      loadRecommendedFortune();
    };
    
    const loadRecentFortunes = () => {
        // 테스트 데이터
      recentFortunes.value = [
          {
            id: 1,
          type: '오늘의 운세',
          date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2시간 전
          summary: '오늘은 전반적으로 좋은 기운이 흐르는 날입니다. 특히 목(木)의 기운이 강해 창의적인 일이나 새로운 시작에 좋은 날입니다.',
          luckScore: 82,
          link: '/daily-fortune'
          },
          {
            id: 2,
          type: '연애운',
          date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2일 전
          summary: '솔로라면 새로운 만남의 기회가 있을 수 있으며, 연인 관계에서는 서로의 이해와 배려가 필요한 시기입니다.',
          luckScore: 75,
          link: '/fortune/love'
          },
          {
            id: 3,
          type: '금전운',
          date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5일 전
          summary: '재물을 모으는 능력이 뛰어난 때입니다. 새로운 수입원이 생길 가능성이 높으며, 투자에서도 좋은 결과를 얻을 수 있습니다.',
          luckScore: 88,
          link: '/fortune/money'
        }
      ];
    };
    
    const loadRecentChoices = () => {
        // 테스트 데이터
      recentChoices.value = [
          {
            id: 1,
          category: '음식 선택',
          date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1일 전
          question: '오늘 저녁 식사로 무엇을 먹을까요?',
          options: ['한식', '중식', '일식', '양식'],
          selectedOption: '한식'
          },
          {
            id: 2,
          category: '여행 계획',
          date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 7일 전
          question: '다음 휴가 때 어디로 여행을 갈까요?',
          options: ['제주도', '부산', '강원도', '해외'],
          selectedOption: '제주도'
        }
      ];
    };
    
    const loadRecentNames = () => {
      // 테스트 데이터
      recentNames.value = [
          {
          id: 1,
          type: 'baby',
          date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3일 전
          description: '여자아이 이름 추천 결과',
          results: ['서윤', '지원', '하은', '서연', '민서']
          }
        ];
    };
    
    const loadRecommendedFortune = () => {
      // 테스트 데이터
      recommendedFortune.value = {
        title: '사업운 분석',
        description: '당신의 사주와 가장 잘 맞는 운세입니다',
        summary: '목(木)과 화(火)의 기운이 강해 창의적인 아이디어와 추진력이 뛰어납니다. 이러한 강점을 활용하여 새로운 트렌드를 선도하고 혁신적인 비즈니스 모델을 구축하는 데 집중하세요.',
        matching: 95,
        link: '/fortune/business'
      };
    };
    
    // 컴포넌트 마운트 시 데이터 로드
    onMounted(() => {
      // 로그인 상태 확인
      console.log('대시보드 로드: 로그인 상태:', store.getters.isLoggedIn);
      console.log('대시보드 로드: 사용자 정보:', store.getters.currentUser);
      
      // 1. Vuex 스토어에서 사용자 프로필 정보 가져오기
      const userProfile = store.getters.userProfile;
      console.log('대시보드 로드: 사용자 프로필:', userProfile);
      
      // 2. 사용자 프로필에 사주 정보가 있으면 사용
      if (userProfile && userProfile.birthdate) {
        console.log('대시보드 로드: 프로필에서 사주 정보 로드');
        userBirthInfo.value = {
          birthdate: userProfile.birthdate,
          birthtime: userProfile.birthtime,
          gender: userProfile.gender
        };
        
        // 세션 스토리지에도 저장 (일관성 유지)
        sessionStorage.setItem('userBirthInfo', JSON.stringify(userBirthInfo.value));
      } 
      // 3. 없으면 세션 스토리지 확인
      else {
        const savedBirthInfo = sessionStorage.getItem('userBirthInfo');
        console.log('대시보드 로드: 세션 스토리지 사주 정보:', savedBirthInfo);
        
        if (savedBirthInfo) {
          console.log('대시보드 로드: 세션에서 사주 정보 로드');
          userBirthInfo.value = JSON.parse(savedBirthInfo);
          
          // Vuex 스토어에도 업데이트
          store.dispatch('updateUserProfile', userBirthInfo.value);
        }
      }
      
      // 생년월일 정보가 있으면 사주팔자 및 운세 정보 로드
      if (userBirthInfo.value.birthdate) {
        console.log('대시보드 로드: 사주 정보 기반 운세 업데이트');
        updateSajuInfo();
      }
      
      loadUserData();
    });

    return {
      currentUser,
      sessionStartTime,
      todayLuckLevel,
      userBirthInfo,
      sajuInfo,
      elements,
      recentFortunes,
      recentChoices,
      recentNames,
      recommendedFortune,
      formatDate,
      formatBirthdate,
      showBirthInfoModal,
      showModal,
      hideModal,
      editingBirthInfo,
      saveBirthInfo
    };
  }
}
</script>

<style scoped>
.dashboard {
  padding: 1.5rem 0;
}

.welcome-banner {
  background: linear-gradient(135deg, #9b59b6, #3498db);
  padding: 2rem;
  border-radius: 15px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.welcome-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.fortune-pill {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  display: inline-block;
  font-weight: 600;
  font-size: 1.1rem;
}

.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  background-color: #fff;
}

.card-fortune .card-header {
  border-left: 5px solid #9b59b6;
}

.card-choice .card-header {
  border-left: 5px solid #3498db;
}

.card-profile .card-header {
  border-left: 5px solid #2ecc71;
}

.card-names .card-header {
  border-left: 5px solid #e67e22;
}

.card-recommendation .card-header {
  border-left: 5px solid #f1c40f;
}

.saju-cell {
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  background-color: #f8f9fa;
}

.quick-link-item {
  background-color: #f8f9fa;
  font-weight: 600;
  transition: all 0.3s ease;
}

.quick-link-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.love-link {
  color: #e74c3c;
}

.money-link {
  color: #f1c40f;
}

.business-link {
  color: #2ecc71;
}

.health-link {
  color: #3498db;
}

.love-link:hover {
  background-color: rgba(231, 76, 60, 0.1);
}

.money-link:hover {
  background-color: rgba(241, 196, 15, 0.1);
}

.business-link:hover {
  background-color: rgba(46, 204, 113, 0.1);
}

.health-link:hover {
  background-color: rgba(52, 152, 219, 0.1);
}

.name-results {
  margin-top: 0.75rem;
}

.badge {
  font-size: 0.9rem;
  font-weight: 500;
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
}

.modal-body {
  padding: 1.5rem;
}

.modal-title {
  font-weight: 600;
  color: #2c3e50;
}

/* body 스타일 */
:global(body.modal-open) {
  overflow: hidden;
}
</style>
