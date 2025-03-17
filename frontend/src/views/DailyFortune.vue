<template>
  <div class="daily-fortune-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center py-5">
              <h1 class="fortune-title mb-4">오늘의 운세</h1>
              <p class="fortune-subtitle">
                사주팔자를 기반으로 오늘 하루의 운세와 조언을 알아보세요
              </p>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <div v-if="!userInfoSubmitted">
                <h3 class="mb-4">사주 정보 입력</h3>
                <form @submit.prevent="submitUserInfo">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="birthdate" class="form-label">생년월일</label>
                      <input 
                        type="date" 
                        id="birthdate" 
                        v-model="userInfo.birthdate" 
                        class="form-control" 
                        required
                      >
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="birthtime" class="form-label">태어난 시간</label>
                      <input 
                        type="time" 
                        id="birthtime" 
                        v-model="userInfo.birthtime" 
                        class="form-control"
                      >
                      <div class="form-text text-muted">정확한 시간을 모르시면 비워두셔도 됩니다.</div>
                    </div>
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
                          v-model="userInfo.gender"
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
                          v-model="userInfo.gender"
                        >
                        <label class="form-check-label" for="female">여성</label>
                      </div>
                    </div>
                  </div>
                  <div class="d-grid">
                    <button type="submit" class="btn btn-fortune-gradient">
                      <i class="bi bi-calendar-check me-2"></i>오늘의 운세 보기
                    </button>
                  </div>
                </form>
              </div>
              
              <div v-else>
                <div class="text-end mb-4">
                  <button @click="resetForm" class="btn btn-sm btn-outline-secondary">
                    <i class="bi bi-arrow-repeat me-1"></i>다시 입력하기
                  </button>
                </div>
                
                <div class="fortune-result mb-4">
                  <div class="fortune-date text-center mb-4">
                    <h3>{{ todayDate }} ({{ todayLunarDate }})</h3>
                    <p class="text-muted">{{ getZodiacInfo() }}</p>
                  </div>
                  
                  <div class="row mb-4">
                    <div class="col-md-4 mb-3 mb-md-0">
                      <div class="fortune-card">
                        <div class="fortune-card-header">
                          <h4><i class="bi bi-star-fill text-warning me-2"></i>오늘의 개운지수</h4>
                        </div>
                        <div class="fortune-card-body">
                          <div class="fortune-score-circle mb-3">
                            <div class="fortune-score-value">{{ todayLuck.overall }}%</div>
                          </div>
                          <div class="fortune-keywords">
                            <p><strong>행운의 색:</strong> {{ todayLuck.color }}</p>
                            <p><strong>행운의 방향:</strong> {{ todayLuck.direction }}</p>
                            <p><strong>행운의 시간:</strong> {{ todayLuck.time }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-8">
                      <div class="fortune-card h-100">
                        <div class="fortune-card-header">
                          <h4><i class="bi bi-chat-quote-fill text-primary me-2"></i>오늘의 운세</h4>
                        </div>
                        <div class="fortune-card-body">
                          <p>{{ todayFortuneText }}</p>
                          <div class="tips mt-3">
                            <p><strong>조언:</strong> {{ todayAdvice }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="row">
                    <div class="col-md-3 mb-3 mb-md-0">
                      <div class="fortune-mini-card">
                        <div class="fortune-mini-header">
                          <h5><i class="bi bi-heart-fill text-danger me-2"></i>애정운</h5>
                        </div>
                        <div class="fortune-mini-body">
                          <div class="fortune-mini-score">{{ todayLuck.love }}%</div>
                          <p>{{ loveFortuneText }}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-3 mb-3 mb-md-0">
                      <div class="fortune-mini-card">
                        <div class="fortune-mini-header">
                          <h5><i class="bi bi-coin text-warning me-2"></i>금전운</h5>
                        </div>
                        <div class="fortune-mini-body">
                          <div class="fortune-mini-score">{{ todayLuck.money }}%</div>
                          <p>{{ moneyFortuneText }}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-3 mb-3 mb-md-0">
                      <div class="fortune-mini-card">
                        <div class="fortune-mini-header">
                          <h5><i class="bi bi-briefcase-fill text-info me-2"></i>사업운</h5>
                        </div>
                        <div class="fortune-mini-body">
                          <div class="fortune-mini-score">{{ todayLuck.business }}%</div>
                          <p>{{ businessFortuneText }}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-3">
                      <div class="fortune-mini-card">
                        <div class="fortune-mini-header">
                          <h5><i class="bi bi-heart-pulse-fill text-success me-2"></i>건강운</h5>
                        </div>
                        <div class="fortune-mini-body">
                          <div class="fortune-mini-score">{{ todayLuck.health }}%</div>
                          <p>{{ healthFortuneText }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="card shadow-sm mb-4">
                  <div class="card-body">
                    <h4 class="mb-3">오늘 하면 좋은 일 / 피해야 할 일</h4>
                    <div class="row">
                      <div class="col-md-6 mb-3 mb-md-0">
                        <div class="daily-dos">
                          <h5 class="text-success"><i class="bi bi-check-circle me-2"></i>하면 좋은 일</h5>
                          <ul class="list-unstyled ps-4">
                            <li v-for="(item, index) in todayDos" :key="`do-${index}`" class="mb-2">
                              {{ item }}
                            </li>
                          </ul>
                        </div>
                      </div>
                      <div class="col-md-6">
                        <div class="daily-donts">
                          <h5 class="text-danger"><i class="bi bi-x-circle me-2"></i>피해야 할 일</h5>
                          <ul class="list-unstyled ps-4">
                            <li v-for="(item, index) in todayDonts" :key="`dont-${index}`" class="mb-2">
                              {{ item }}
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">주간/월간 운세</h3>
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                회원 가입 후 이용하실 수 있는 서비스입니다. 더 자세한 주간/월간 운세를 확인해보세요.
              </div>
              <div class="text-center">
                <button class="btn btn-primary">
                  <i class="bi bi-person-plus me-2"></i>회원가입하고 더 많은 운세 보기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DailyFortune',
  data() {
    return {
      userInfo: {
        birthdate: '',
        birthtime: '',
        gender: ''
      },
      userInfoSubmitted: false,
      todayDate: '2023년 8월 15일',
      todayLunarDate: '음력 7월 1일',
      todayLuck: {
        overall: 78,
        love: 65,
        money: 82,
        business: 75,
        health: 80,
        color: '청색, 남색',
        direction: '북동쪽',
        time: '오전 10시 - 12시'
      },
      todayFortuneText: '오늘은 전반적으로 좋은 기운이 흐르는 날입니다. 특히 목(木)의 기운이 강하게 나타나므로 창의적인 일이나 새로운 시작에 좋은 날입니다. 주변 사람들과의 소통이 원활하며, 예상치 못한 좋은 소식을 들을 수 있습니다. 다만, 너무 많은 일을 한꺼번에 시작하려 하면 어려움을 겪을 수 있으니 우선순위를 정하고 차근차근 진행하는 것이 좋겠습니다.',
      todayAdvice: '오늘은 자신의 의견을 분명히 표현하되, 상대방의 말에도 귀 기울이는 균형있는 태도가 필요합니다. 또한 갑작스러운 제안이나 결정은 신중하게 생각해보고 결정하세요.',
      loveFortuneText: '연인 관계에서 소소한 갈등이 있을 수 있으나 대화로 해결 가능합니다. 솔로라면 새로운 만남의 기회가 있을 수 있습니다.',
      moneyFortuneText: '예상치 못한 수입이나 재정적 기회가 올 수 있는 날입니다. 계획했던 투자가 있다면 좋은 결과를 얻을 수 있습니다.',
      businessFortuneText: '업무 관련 새로운, 창의적인 아이디어가 떠오르는 날입니다. 동료나 상사의 협조를 얻기 좋은 날이니 적극적으로 의견을 나누세요.',
      healthFortuneText: '전반적인 건강 상태는 양호하나, 소화계통에 약간의 불편함이 있을 수 있습니다. 규칙적인 식사와 충분한 수분 섭취가 중요합니다.',
      todayDos: [
        '중요한 결정이나 계약 체결하기',
        '새로운 프로젝트 시작하기',
        '친구나 동료와 만남 갖기',
        '운동이나 야외 활동하기',
        '푸른색 계열의 옷 입기'
      ],
      todayDonts: [
        '과도한 지출이나 충동구매',
        '중요한 갈등 상황에서 감정적으로 대응하기',
        '지나친 음주나 늦은 취침',
        '너무 많은 약속 잡기',
        '남쪽 방향으로의 장거리 이동'
      ]
    }
  },
  methods: {
    submitUserInfo() {
      // 실제 구현에서는 API를 호출하여 사주팔자 분석 데이터를 받아옵니다
      // 현재는 예시 데이터를 표시합니다
      this.userInfoSubmitted = true;
    },
    resetForm() {
      this.userInfoSubmitted = false;
      this.userInfo = {
        birthdate: '',
        birthtime: '',
        gender: ''
      };
    },
    getZodiacInfo() {
      // 실제 구현에서는 사용자의 생년월일로 계산
      return '계묘년 청묘월 병신일';
    }
  }
}
</script>

<style scoped>
.daily-fortune-page {
  padding: 2rem 0;
}

.fortune-title {
  font-weight: 700;
  background: linear-gradient(135deg, #9b59b6, #3498db);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fortune-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.btn-fortune-gradient {
  background: linear-gradient(135deg, #9b59b6, #3498db);
  color: white;
  border: none;
  transition: all 0.3s;
}

.btn-fortune-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(155, 89, 182, 0.2);
}

.fortune-date h3 {
  color: #333;
  font-weight: 600;
}

.fortune-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  height: 100%;
}

.fortune-card-header {
  background: linear-gradient(135deg, #9b59b6, #3498db);
  color: white;
  padding: 1rem;
}

.fortune-card-header h4 {
  margin: 0;
  font-weight: 600;
}

.fortune-card-body {
  padding: 1.5rem;
}

.fortune-score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #9b59b6, #3498db);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fortune-score-value {
  color: white;
  font-size: 2rem;
  font-weight: 700;
}

.fortune-keywords p {
  margin-bottom: 0.5rem;
}

.fortune-mini-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  height: 100%;
}

.fortune-mini-header {
  background-color: #e9ecef;
  padding: 0.75rem;
  text-align: center;
}

.fortune-mini-header h5 {
  margin: 0;
  font-weight: 600;
}

.fortune-mini-body {
  padding: 1rem;
}

.fortune-mini-score {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 0.5rem;
}

.daily-dos li, .daily-donts li {
  position: relative;
  padding-left: 1.5rem;
}

.daily-dos li::before,
.daily-donts li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.daily-dos li::before {
  background-color: #28a745;
}

.daily-donts li::before {
  background-color: #dc3545;
}
</style> 