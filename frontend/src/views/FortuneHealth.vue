<template>
  <div class="fortune-health-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center py-5">
              <h1 class="fortune-title mb-4">건강운 분석</h1>
              <p class="fortune-subtitle">
                사주팔자를 기반으로 당신의 건강 상태와 주의점을 분석하고 건강관리 전략을 알아보세요
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
                  <div class="mb-3">
                    <label class="form-label">나이</label>
                    <input 
                      type="number"
                      class="form-control"
                      v-model="userInfo.age"
                      min="1"
                      max="120"
                      required
                    >
                  </div>
                  <div class="d-grid">
                    <button type="submit" class="btn btn-health-gradient">
                      <i class="bi bi-heart-pulse me-2"></i>건강운 분석하기
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
                
                <div class="row fortune-result mb-4">
                  <div class="col-md-4 mb-4 mb-md-0">
                    <div class="saju-info p-3 rounded-3">
                      <h4 class="text-center mb-3">사주팔자 분석</h4>
                      <div class="saju-chart">
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
                      
                      <div class="elements-chart mt-4">
                        <h5 class="text-center mb-3">오행 분석</h5>
                        <div class="element-bars">
                          <div class="element-bar mb-2">
                            <div class="d-flex justify-content-between mb-1">
                              <span>금(金)</span>
                              <span>{{ elementsAnalysis.metal }}%</span>
                            </div>
                            <div class="progress">
                              <div class="progress-bar bg-secondary" role="progressbar" 
                                   :style="`width: ${elementsAnalysis.metal}%`" 
                                   :aria-valuenow="elementsAnalysis.metal" 
                                   aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                          </div>
                          <div class="element-bar mb-2">
                            <div class="d-flex justify-content-between mb-1">
                              <span>목(木)</span>
                              <span>{{ elementsAnalysis.wood }}%</span>
                            </div>
                            <div class="progress">
                              <div class="progress-bar bg-success" role="progressbar" 
                                   :style="`width: ${elementsAnalysis.wood}%`" 
                                   :aria-valuenow="elementsAnalysis.wood" 
                                   aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                          </div>
                          <div class="element-bar mb-2">
                            <div class="d-flex justify-content-between mb-1">
                              <span>수(水)</span>
                              <span>{{ elementsAnalysis.water }}%</span>
                            </div>
                            <div class="progress">
                              <div class="progress-bar bg-info" role="progressbar" 
                                   :style="`width: ${elementsAnalysis.water}%`" 
                                   :aria-valuenow="elementsAnalysis.water" 
                                   aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                          </div>
                          <div class="element-bar mb-2">
                            <div class="d-flex justify-content-between mb-1">
                              <span>화(火)</span>
                              <span>{{ elementsAnalysis.fire }}%</span>
                            </div>
                            <div class="progress">
                              <div class="progress-bar bg-danger" role="progressbar" 
                                   :style="`width: ${elementsAnalysis.fire}%`" 
                                   :aria-valuenow="elementsAnalysis.fire" 
                                   aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                          </div>
                          <div class="element-bar mb-2">
                            <div class="d-flex justify-content-between mb-1">
                              <span>토(土)</span>
                              <span>{{ elementsAnalysis.earth }}%</span>
                            </div>
                            <div class="progress">
                              <div class="progress-bar bg-warning" role="progressbar" 
                                   :style="`width: ${elementsAnalysis.earth}%`" 
                                   :aria-valuenow="elementsAnalysis.earth" 
                                   aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="col-md-8">
                    <div class="fortune-details p-4 h-100">
                      <h3 class="mb-3">건강운 분석</h3>
                      <div class="health-stats d-flex mb-4">
                        <div class="health-stat-item text-center me-3">
                          <div class="health-stat-circle">
                            <div class="health-stat-value">{{ healthStats.strength }}%</div>
                          </div>
                          <div class="health-stat-label">체력</div>
                        </div>
                        <div class="health-stat-item text-center me-3">
                          <div class="health-stat-circle">
                            <div class="health-stat-value">{{ healthStats.immunity }}%</div>
                          </div>
                          <div class="health-stat-label">면역력</div>
                        </div>
                        <div class="health-stat-item text-center me-3">
                          <div class="health-stat-circle">
                            <div class="health-stat-value">{{ healthStats.mental }}%</div>
                          </div>
                          <div class="health-stat-label">정신력</div>
                        </div>
                        <div class="health-stat-item text-center">
                          <div class="health-stat-circle">
                            <div class="health-stat-value">{{ healthStats.currentHealth }}%</div>
                          </div>
                          <div class="health-stat-label">현재 건강</div>
                        </div>
                      </div>
                      
                      <div class="health-analysis mb-4">
                        <h4 class="mb-3">{{ getMonthPeriod() }} 건강운</h4>
                        <p>{{ healthFortuneText }}</p>
                      </div>
                      
                      <div class="health-concerns mb-4">
                        <h4 class="mb-3">주의해야 할 건강 부위</h4>
                        <div class="row">
                          <div class="col-md-6 mb-3">
                            <div class="health-concern">
                              <div class="health-concern-header d-flex align-items-center mb-2">
                                <div class="concern-icon me-2"><i class="bi bi-exclamation-triangle-fill text-warning"></i></div>
                                <h5 class="mb-0">{{ healthConcerns.primary.name }}</h5>
                              </div>
                              <p>{{ healthConcerns.primary.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="health-concern">
                              <div class="health-concern-header d-flex align-items-center mb-2">
                                <div class="concern-icon me-2"><i class="bi bi-info-circle-fill text-info"></i></div>
                                <h5 class="mb-0">{{ healthConcerns.secondary.name }}</h5>
                              </div>
                              <p>{{ healthConcerns.secondary.description }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="health-recommendation card mb-4">
                  <div class="card-body">
                    <h4 class="mb-3"><i class="bi bi-chat-quote me-2 text-success"></i>건강 관리 조언</h4>
                    <div class="health-recommendation-content">
                      <p>{{ healthAdvice }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">건강 관리 추천</h3>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="health-recommendation-item">
                    <h5><i class="bi bi-activity text-danger me-2"></i>추천 운동</h5>
                    <ul class="list-unstyled ps-4">
                      <li v-for="(item, index) in recommendations.exercise" :key="`exercise-${index}`" class="mb-2">
                        {{ item }}
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="health-recommendation-item">
                    <h5><i class="bi bi-cup-hot text-success me-2"></i>추천 음식</h5>
                    <ul class="list-unstyled ps-4">
                      <li v-for="(item, index) in recommendations.diet" :key="`diet-${index}`" class="mb-2">
                        {{ item }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">연령대별 건강 주의점</h3>
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                회원 가입 후 이용하실 수 있는 서비스입니다. 나이별 맞춤형 건강 관리 방법을 제공합니다.
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
  name: 'FortuneHealth',
  data() {
    return {
      userInfo: {
        birthdate: '',
        birthtime: '',
        gender: '',
        age: ''
      },
      userInfoSubmitted: false,
      sajuInfo: {
        year: { heaven: '경', earth: '신' },
        month: { heaven: '신', earth: '유' },
        day: { heaven: '계', earth: '미' },
        hour: { heaven: '을', earth: '사' }
      },
      elementsAnalysis: {
        metal: 20,  // 금
        wood: 15,   // 목
        water: 30,  // 수
        fire: 25,   // 화
        earth: 10   // 토
      },
      healthStats: {
        strength: 75,
        immunity: 82,
        mental: 68,
        currentHealth: 77
      },
      healthFortuneText: '이번 달은 수(水)의 기운이 강해 신장과 방광에 관련된 건강 문제에 주의가 필요합니다. 충분한 수분 섭취와 함께 과로와 과음을 피하는 것이 좋습니다. 정신적인 스트레스가 신체 건강에 영향을 미칠 수 있으니 규칙적인 생활과 휴식이 중요합니다. 특히 밤 시간대에 충분한 휴식을 취하고, 소변에 이상이 있는지 주의 깊게 살펴보세요.',
      healthConcerns: {
        primary: {
          name: '비뇨기계 및 신장',
          description: '사주에 수(水)의 기운이 강하여 신장, 방광, 비뇨기계 건강에 특별한 주의가 필요합니다. 충분한 수분 섭취를 유지하고, 너무 차가운 음식을 과도하게 섭취하지 마세요.'
        },
        secondary: {
          name: '호흡기 및 면역계',
          description: '금(金)과 화(火)의 균형이 중요한데, 현재 화(火)가 다소 강해 호흡기 계통과 면역력에 영향을 줄 수 있습니다. 적절한 환기와 면역력 강화에 신경쓰세요.'
        }
      },
      healthAdvice: '당신의 사주를 분석한 결과, 수(水)와 화(火)의 기운이 강하게 나타납니다. 수(水)는 신장과 방광에, 화(火)는 심장과 순환계에 관련이 있습니다. 이러한 오행 특성을 고려할 때, 수분 섭취는 충분히 하되 차가운 음료는 적당히 제한하고, 심장에 무리가 가지 않도록 적절한 운동을 꾸준히 하는 것이 좋습니다. 또한 스트레스 관리에 특히 신경 쓰고, 규칙적인 생활 리듬을 유지하세요. 토(土)의 기운이 부족하니 소화기능 강화를 위해 식사 시간을 규칙적으로 지키고 천천히 씹어 먹는 습관을 들이는 것이 좋습니다.',
      recommendations: {
        exercise: [
          '가벼운 수영 또는 물 속 운동',
          '요가와 스트레칭',
          '규칙적인 걷기 운동',
          '적절한 강도의 유산소 운동',
          '태극권과 같은 부드러운 운동'
        ],
        diet: [
          '신선한 채소와 과일',
          '적절한 단백질 (생선, 두부)',
          '견과류와 씨앗',
          '따뜻한 차와 약용 차',
          '소화가 잘 되는 통곡물'
        ]
      }
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
        gender: '',
        age: ''
      };
    },
    getMonthPeriod() {
      const now = new Date();
      const monthNames = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
      const currentMonth = monthNames[now.getMonth()];
      const nextMonth = monthNames[(now.getMonth() + 1) % 12];
      return `${currentMonth}~${nextMonth}`;
    }
  }
}
</script>

<style scoped>
.fortune-health-page {
  padding: 2rem 0;
}

.fortune-title {
  font-weight: 700;
  background: linear-gradient(135deg, #16a085, #3498db);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fortune-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.btn-health-gradient {
  background: linear-gradient(135deg, #16a085, #3498db);
  color: white;
  border: none;
  transition: all 0.3s;
}

.btn-health-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(22, 160, 133, 0.2);
}

.saju-info {
  background-color: #f8f9fa;
  border-left: 4px solid #16a085;
}

.saju-cell {
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  background-color: white;
}

.health-stat-item {
  flex: 1;
}

.health-stat-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #16a085, #3498db);
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.health-stat-value {
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
}

.health-stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.health-concern {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.5rem;
  height: 100%;
}

.concern-icon {
  font-size: 1.2rem;
}

.health-recommendation {
  border-left: 4px solid #16a085;
}

.health-recommendation-item {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  height: 100%;
}

.health-recommendation-item li {
  position: relative;
  padding-left: 1.5rem;
}

.health-recommendation-item li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #16a085;
}
</style> 