<template>
  <div class="fortune-love-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center py-5">
              <h1 class="fortune-title mb-4">연애운 분석</h1>
              <p class="fortune-subtitle">
                사주팔자를 기반으로 당신의 연애운을 살펴보고 최적의 파트너를 찾아보세요
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
                    <label class="form-label">현재 연애 상태</label>
                    <div class="d-flex">
                      <div class="form-check me-4">
                        <input 
                          class="form-check-input" 
                          type="radio" 
                          name="status" 
                          id="single" 
                          value="single" 
                          v-model="userInfo.status"
                          required
                        >
                        <label class="form-check-label" for="single">싱글</label>
                      </div>
                      <div class="form-check">
                        <input 
                          class="form-check-input" 
                          type="radio" 
                          name="status" 
                          id="relationship" 
                          value="relationship"
                          v-model="userInfo.status"
                        >
                        <label class="form-check-label" for="relationship">연애중</label>
                      </div>
                      <div class="form-check ms-4">
                        <input 
                          class="form-check-input" 
                          type="radio" 
                          name="status" 
                          id="complicated" 
                          value="complicated"
                          v-model="userInfo.status"
                        >
                        <label class="form-check-label" for="complicated">복잡한 관계</label>
                      </div>
                    </div>
                  </div>
                  <div class="d-grid">
                    <button type="submit" class="btn btn-love-gradient">
                      <i class="bi bi-heart-fill me-2"></i>연애운 분석하기
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
                
                <div class="mb-4">
                  <div class="fortune-result">
                    <div class="row">
                      <div class="col-md-4 mb-4 mb-md-0">
                        <div class="saju-info p-3 rounded-3">
                          <h4 class="text-center mb-3">{{ userInfo.gender === 'male' ? '남성' : '여성' }}의 사주</h4>
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
                          <h3 class="mb-3">연애운 분석</h3>
                          <div class="love-stats d-flex mb-4">
                            <div class="love-stat-item text-center me-4">
                              <div class="love-stat-circle">
                                <div class="love-stat-value">{{ loveStats.attraction }}%</div>
                              </div>
                              <div class="love-stat-label">매력도</div>
                            </div>
                            <div class="love-stat-item text-center me-4">
                              <div class="love-stat-circle">
                                <div class="love-stat-value">{{ loveStats.commitment }}%</div>
                              </div>
                              <div class="love-stat-label">애정 지속력</div>
                            </div>
                            <div class="love-stat-item text-center">
                              <div class="love-stat-circle">
                                <div class="love-stat-value">{{ loveStats.luck }}%</div>
                              </div>
                              <div class="love-stat-label">현재 운세</div>
                            </div>
                          </div>
                          
                          <div class="love-analysis mb-4">
                            <h4 class="mb-3">{{ getMonthPeriod() }} 연애운</h4>
                            <p>{{ loveFortuneText }}</p>
                          </div>
                          
                          <div class="partner-recommendation mb-4">
                            <h4 class="mb-3">이상적인 파트너 유형</h4>
                            <div class="row">
                              <div class="col-md-6 mb-3">
                                <div class="partner-type">
                                  <div class="partner-type-header d-flex align-items-center mb-2">
                                    <div class="partner-icon me-2"><i class="bi bi-check-circle-fill text-success"></i></div>
                                    <h5 class="mb-0">{{ partnerTypes.best.name }}</h5>
                                  </div>
                                  <p>{{ partnerTypes.best.description }}</p>
                                </div>
                              </div>
                              <div class="col-md-6 mb-3">
                                <div class="partner-type">
                                  <div class="partner-type-header d-flex align-items-center mb-2">
                                    <div class="partner-icon me-2"><i class="bi bi-star-fill text-warning"></i></div>
                                    <h5 class="mb-0">{{ partnerTypes.good.name }}</h5>
                                  </div>
                                  <p>{{ partnerTypes.good.description }}</p>
                                </div>
                              </div>
                              <div class="col-md-6 mb-3">
                                <div class="partner-type">
                                  <div class="partner-type-header d-flex align-items-center mb-2">
                                    <div class="partner-icon me-2"><i class="bi bi-exclamation-circle-fill text-danger"></i></div>
                                    <h5 class="mb-0">{{ partnerTypes.avoid.name }}</h5>
                                  </div>
                                  <p>{{ partnerTypes.avoid.description }}</p>
                                </div>
                              </div>
                              <div class="col-md-6 mb-3">
                                <div class="partner-type">
                                  <div class="partner-type-header d-flex align-items-center mb-2">
                                    <div class="partner-icon me-2"><i class="bi bi-calendar-check text-primary"></i></div>
                                    <h5 class="mb-0">좋은 만남의 시기</h5>
                                  </div>
                                  <p>{{ bestTimingText }}</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="love-advice card mb-4">
                  <div class="card-body">
                    <h4 class="mb-3"><i class="bi bi-chat-quote me-2 text-danger"></i>연애 조언</h4>
                    <div class="love-advice-content">
                      <p class="mb-1">{{ loveAdvice }}</p>
                      <p v-if="userInfo.status === 'relationship'" class="mt-3 mb-0">
                        <strong>현재 연인과의 궁합:</strong> {{ relationshipAdvice }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">궁합 확인하기</h3>
              <p class="mb-4">
                당신과 상대방의 사주를 비교하여 연애 궁합을 확인해보세요.
                사주팔자 정보를 입력하면 상세한 궁합 분석 결과를 제공해 드립니다.
              </p>
              <div class="text-center">
                <button class="btn btn-outline-danger px-4">
                  <i class="bi bi-heart me-2"></i>궁합 확인하러 가기
                </button>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">이번 달 운세 달력</h3>
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                회원 가입 후 이용하실 수 있는 서비스입니다. 매일의 연애운을 확인해보세요.
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
  name: 'FortuneLove',
  data() {
    return {
      userInfo: {
        birthdate: '',
        birthtime: '',
        gender: '',
        status: 'single'
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
        wood: 15,   // 목
        water: 20,  // 수
        fire: 5,    // 화
        earth: 30   // 토
      },
      loveStats: {
        attraction: 78,
        commitment: 65,
        luck: 82
      },
      loveFortuneText: '이번 달은 연애운이 매우 좋은 시기입니다. 당신의 매력이 빛을 발하며 새로운 인연을 만날 확률이 높아집니다. 특히 음식과 관련된 장소나 문화 활동 중에 의미 있는 만남이 있을 수 있으니 적극적으로 참여해 보세요. 기존 연인이 있다면 소통이 원활해지고 서로에 대한 이해가 깊어지는 시간이 될 것입니다.',
      partnerTypes: {
        best: {
          name: '화(火) 기운이 강한 사람',
          description: '열정적이고 활동적인 성격의 사람과 궁합이 좋습니다. 당신의 안정적인 기질과 균형을 이루어 서로 보완적인 관계를 형성할 수 있습니다.'
        },
        good: {
          name: '토(土) 기운이 적절한 사람',
          description: '믿음직하고 책임감 있는 성격의 사람과도 좋은 관계를 유지할 수 있습니다. 서로의 가치관이 비슷해 장기적인 관계로 발전하기 좋습니다.'
        },
        avoid: {
          name: '금(金) 기운이 과도한 사람',
          description: '지나치게 현실적이고 냉철한 성격의 사람과는 갈등이 생길 수 있습니다. 당신의 감성적인 면과 충돌할 가능성이 높습니다.'
        }
      },
      bestTimingText: '5월과 9월 사이에 새로운 만남이 이루어질 가능성이 높습니다. 특히 화요일과 토요일에 이루어진 만남은 좋은 결과로 이어질 수 있습니다.',
      loveAdvice: '당신은 상대방의 세심한 배려와 감정 표현에 큰 가치를 둡니다. 하지만 때로는 너무 이상적인 관계를 추구하여 현실과의 괴리감을 느낄 수 있습니다. 상대방의 있는 그대로를 받아들이고, 소소한 행복을 함께 나누는 것이 중요합니다. 또한, 자신의 감정을 솔직하게 표현하되 상대방의 의견도 존중하는 균형 잡힌 소통이 필요합니다.',
      relationshipAdvice: '현재 연인과는 대체로 조화로운 관계를 유지하고 있으나, 서로의 독립성을 존중하는 것이 중요합니다. 함께하는 시간만큼 각자의 시간도 충분히 가지는 것이 관계를 더욱 건강하게 만들 것입니다.'
    }
  },
  methods: {
    submitUserInfo() {
      // 실제 구현에서는 API를 호출하여 사주팔자 분석 데이터를 받아옵니다
      // 현재는 예시 데이터를 표시합니다
      this.userInfoSubmitted = true;
      this.analyzeLoveFortuneBasedOnStatus();
    },
    resetForm() {
      this.userInfoSubmitted = false;
      this.userInfo = {
        birthdate: '',
        birthtime: '',
        gender: '',
        status: 'single'
      };
    },
    getMonthPeriod() {
      const now = new Date();
      const monthNames = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
      const currentMonth = monthNames[now.getMonth()];
      const nextMonth = monthNames[(now.getMonth() + 1) % 12];
      return `${currentMonth}~${nextMonth}`;
    },
    analyzeLoveFortuneBasedOnStatus() {
      // 연애 상태에 따라 다른 운세 텍스트를 표시
      if (this.userInfo.status === 'single') {
        this.loveFortuneText = '이번 달은 새로운 인연을 만날 수 있는 좋은 시기입니다. 특히 친구 모임이나 취미 활동을 통해 마음이 맞는 사람을 만날 확률이 높습니다. 평소보다 외향적이고 적극적인 자세로 사람들과 교류해보세요. 당신의 매력이 자연스럽게 빛을 발할 것입니다.';
        this.loveAdvice = '새로운 만남을 위해 자신을 가꾸는 시간을 가지세요. 하지만 상대방을 지나치게 이상화하는 경향에 주의하고, 있는 그대로의 모습을 받아들이는 열린 마음이 필요합니다. 첫인상으로 판단하기보다는 충분한 시간을 두고 상대를 알아가세요.';
      } else if (this.userInfo.status === 'relationship') {
        this.loveFortuneText = '현재 연인과의 관계가 더욱 깊어지는 시기입니다. 서로에 대한 이해가 깊어지고 믿음이 강해질 수 있습니다. 작은 불화가 있더라도 대화를 통해 더 단단한 관계로 발전할 수 있으니, 솔직한 소통을 유지하세요.';
        this.loveAdvice = '현재 연인과의 관계에서 때로는 타협이 필요합니다. 자신의 주장만 고집하기보다는 상대방의 관점도 이해하려는 노력이 필요합니다. 또한 일상에서 감사함을 자주 표현하면 관계가 더욱 풍요로워집니다.';
      } else {
        this.loveFortuneText = '현재 복잡한 관계 속에서 명확한 방향을 찾아야 하는 시기입니다. 자신의 진정한 감정에 집중하고, 미래를 위한 결정을 내리는 것이 중요합니다. 중요한 결정을 내리기 전에 충분한 시간을 두고 생각해보세요.';
        this.loveAdvice = '현재의 복잡한 상황에서 자신의 마음을 솔직하게 들여다보세요. 감정에 휘둘리기보다는 이성적인 판단을 통해 장기적으로 자신에게 정말 중요한 것이 무엇인지 깊이 생각해볼 시간이 필요합니다.';
      }
    }
  }
}
</script>

<style scoped>
.fortune-love-page {
  padding: 2rem 0;
}

.fortune-title {
  font-weight: 700;
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fortune-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.btn-love-gradient {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
  border: none;
  transition: all 0.3s;
}

.btn-love-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.2);
}

.saju-info {
  background-color: #f8f9fa;
  border-left: 4px solid #ff6b6b;
}

.saju-cell {
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  background-color: white;
}

.love-stat-item {
  flex: 1;
}

.love-stat-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.love-stat-value {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
}

.love-stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.partner-type {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.5rem;
  height: 100%;
}

.partner-icon {
  font-size: 1.2rem;
}

.love-advice {
  border-left: 4px solid #ff6b6b;
}
</style> 