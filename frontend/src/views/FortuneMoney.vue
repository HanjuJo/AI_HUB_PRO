<template>
  <div class="fortune-money-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center py-5">
              <h1 class="fortune-title mb-4">금전운 분석</h1>
              <p class="fortune-subtitle">
                사주팔자를 기반으로 당신의 재물운을 분석하고 최적의 재테크 전략을 알아보세요
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
                    <button type="submit" class="btn btn-money-gradient">
                      <i class="bi bi-cash-coin me-2"></i>금전운 분석하기
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
                      <h3 class="mb-3">금전운 분석</h3>
                      <div class="money-stats d-flex mb-4">
                        <div class="money-stat-item text-center me-3">
                          <div class="money-stat-circle">
                            <div class="money-stat-value">{{ moneyStats.income }}%</div>
                          </div>
                          <div class="money-stat-label">소득</div>
                        </div>
                        <div class="money-stat-item text-center me-3">
                          <div class="money-stat-circle">
                            <div class="money-stat-value">{{ moneyStats.saving }}%</div>
                          </div>
                          <div class="money-stat-label">저축</div>
                        </div>
                        <div class="money-stat-item text-center me-3">
                          <div class="money-stat-circle">
                            <div class="money-stat-value">{{ moneyStats.investment }}%</div>
                          </div>
                          <div class="money-stat-label">투자</div>
                        </div>
                        <div class="money-stat-item text-center">
                          <div class="money-stat-circle">
                            <div class="money-stat-value">{{ moneyStats.luck }}%</div>
                          </div>
                          <div class="money-stat-label">현재 운세</div>
                        </div>
                      </div>
                      
                      <div class="money-analysis mb-4">
                        <h4 class="mb-3">{{ getMonthPeriod() }} 금전운</h4>
                        <p>{{ moneyFortuneText }}</p>
                      </div>
                      
                      <div class="money-recommendation mb-4">
                        <h4 class="mb-3">투자 유형 추천</h4>
                        <div class="row">
                          <div class="col-md-6 mb-3">
                            <div class="investment-type">
                              <div class="investment-type-header d-flex align-items-center mb-2">
                                <div class="investment-icon me-2"><i class="bi bi-check-circle-fill text-success"></i></div>
                                <h5 class="mb-0">{{ investmentTypes.best.name }}</h5>
                              </div>
                              <p>{{ investmentTypes.best.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="investment-type">
                              <div class="investment-type-header d-flex align-items-center mb-2">
                                <div class="investment-icon me-2"><i class="bi bi-star-fill text-warning"></i></div>
                                <h5 class="mb-0">{{ investmentTypes.good.name }}</h5>
                              </div>
                              <p>{{ investmentTypes.good.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="investment-type">
                              <div class="investment-type-header d-flex align-items-center mb-2">
                                <div class="investment-icon me-2"><i class="bi bi-exclamation-circle-fill text-danger"></i></div>
                                <h5 class="mb-0">{{ investmentTypes.avoid.name }}</h5>
                              </div>
                              <p>{{ investmentTypes.avoid.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="investment-type">
                              <div class="investment-type-header d-flex align-items-center mb-2">
                                <div class="investment-icon me-2"><i class="bi bi-calendar-check text-primary"></i></div>
                                <h5 class="mb-0">좋은 투자 시기</h5>
                              </div>
                              <p>{{ bestTimingText }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="money-advice card mb-4">
                  <div class="card-body">
                    <h4 class="mb-3"><i class="bi bi-chat-quote me-2 text-primary"></i>재정 관리 조언</h4>
                    <div class="money-advice-content">
                      <p>{{ moneyAdvice }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">행운을 부르는 행동</h3>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="money-action-item">
                    <h5><i class="bi bi-check2-circle text-success me-2"></i>행운을 부르는 행동</h5>
                    <ul class="list-unstyled ps-4">
                      <li v-for="(item, index) in luckyActions.attract" :key="`attract-${index}`" class="mb-2">
                        {{ item }}
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="money-action-item">
                    <h5><i class="bi bi-x-circle text-danger me-2"></i>피해야 할 행동</h5>
                    <ul class="list-unstyled ps-4">
                      <li v-for="(item, index) in luckyActions.avoid" :key="`avoid-${index}`" class="mb-2">
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
              <h3 class="mb-3">월별 금전운 달력</h3>
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                회원 가입 후 이용하실 수 있는 서비스입니다. 월별 금전운과 투자 타이밍을 확인해보세요.
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
  name: 'FortuneMoney',
  data() {
    return {
      userInfo: {
        birthdate: '',
        birthtime: '',
        gender: ''
      },
      userInfoSubmitted: false,
      sajuInfo: {
        year: { heaven: '경', earth: '신' },
        month: { heaven: '신', earth: '유' },
        day: { heaven: '계', earth: '미' },
        hour: { heaven: '을', earth: '사' }
      },
      elementsAnalysis: {
        metal: 30,  // 금
        wood: 10,   // 목
        water: 15,  // 수
        fire: 25,   // 화
        earth: 20   // 토
      },
      moneyStats: {
        income: 75,
        saving: 68,
        investment: 82,
        luck: 77
      },
      moneyFortuneText: '이번 달은 금전적으로 안정적인 시기입니다. 특히 금(金)의 기운이 강해 재물을 모으고 관리하는 능력이 뛰어난 때입니다. 새로운 수입원이 생길 가능성이 높으며, 투자에서도 좋은 결과를 얻을 수 있습니다. 다만, 화(火)의 기운도 있어 충동적인 지출이나 과시적인 소비에 주의해야 합니다. 안정적이고 장기적인 관점에서 재정을 관리하는 것이 중요합니다.',
      investmentTypes: {
        best: {
          name: '안정적인 장기 투자',
          description: '당신의 사주에 금(金)의 기운이 강하므로, 안정적이고 견고한 투자가 유리합니다. 부동산, 국채, 우량주 등 장기적 관점의 투자를 고려해보세요.'
        },
        good: {
          name: '중간 위험의 분산 투자',
          description: '화(火)와 금(金)의 균형이 잡혀 있어 적절한 위험을 감수하는 투자도 좋은 결과를 가져올 수 있습니다. ETF나 인덱스 펀드처럼 분산된 포트폴리오가 적합합니다.'
        },
        avoid: {
          name: '고위험 단기 투자',
          description: '목(木)의 기운이 약해 급격한 변동성이 있는 투자는 불리합니다. 암호화폐, 선물 옵션, 고위험 주식 등의 단기 투자는 현재 피하는 것이 좋습니다.'
        }
      },
      bestTimingText: '9월부터 11월 사이에 투자를 시작하거나 재정 계획을 세우기 좋은 시기입니다. 특히 금요일과 수요일이 금융 관련 결정을 내리기에 유리한 날입니다.',
      moneyAdvice: '당신의 사주를 분석한 결과, 금(金)과 화(火)의 기운이 강하게 나타납니다. 이는 재물을 모으는 능력과 창의적인 수입원을 찾는 능력이 모두 뛰어나다는 것을 의미합니다. 하지만 목(木)의 기운이 약해 장기적인 성장과 안정성을 위한 계획이 필요합니다. 정기적인 저축 습관을 들이고, 수입의 30%는 반드시 장기 투자에 배정하세요. 또한 토(土)의 기운을 보완하기 위해 부동산이나 실물 자산에 일부 투자하는 것도 좋습니다. 올해는 특히 9월부터 금전운이 상승하니, 이 시기에 중요한 재정 결정을 내리는 것이 유리합니다.',
      luckyActions: {
        attract: [
          '동쪽에 재물을 상징하는 물건 배치하기',
          '금색 또는 노란색 지갑 사용하기',
          '정기적으로 기부 또는 봉사활동 참여하기',
          '화요일에 중요한 금융 결정하기',
          '금전 관련 서적 읽고 지식 쌓기'
        ],
        avoid: [
          '밤 늦게 돈 세거나 금전 거래하기',
          '침실에 지갑이나 현금 두기',
          '검은색 지갑 사용하기',
          '돈을 빌려주거나 보증인 서기',
          '충동적인 고액 구매 결정하기'
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
        gender: ''
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
.fortune-money-page {
  padding: 2rem 0;
}

.fortune-title {
  font-weight: 700;
  background: linear-gradient(135deg, #f1c40f, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fortune-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.btn-money-gradient {
  background: linear-gradient(135deg, #f1c40f, #e67e22);
  color: white;
  border: none;
  transition: all 0.3s;
}

.btn-money-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(241, 196, 15, 0.2);
}

.saju-info {
  background-color: #f8f9fa;
  border-left: 4px solid #f1c40f;
}

.saju-cell {
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  background-color: white;
}

.money-stat-item {
  flex: 1;
}

.money-stat-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f1c40f, #e67e22);
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.money-stat-value {
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
}

.money-stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.investment-type {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.5rem;
  height: 100%;
}

.investment-icon {
  font-size: 1.2rem;
}

.money-advice {
  border-left: 4px solid #f1c40f;
}

.money-action-item {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  height: 100%;
}

.money-action-item li {
  position: relative;
  padding-left: 1.5rem;
}

.money-action-item li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #f1c40f;
}
</style> 