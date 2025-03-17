<template>
  <div class="fortune-business-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center py-5">
              <h1 class="fortune-title mb-4">사업운 분석</h1>
              <p class="fortune-subtitle">
                사주팔자를 기반으로 당신의 사업 운세를 분석하고 최적의 비즈니스 전략을 알아보세요
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
                    <label class="form-label">현재 사업 상태</label>
                    <select class="form-select" v-model="userInfo.businessStatus" required>
                      <option value="" disabled selected>선택해주세요</option>
                      <option value="planning">창업 준비 중</option>
                      <option value="early">초기 사업 단계</option>
                      <option value="growing">성장 단계</option>
                      <option value="mature">안정화 단계</option>
                      <option value="considering">사업 전환 고려 중</option>
                    </select>
                  </div>
                  <div class="d-grid">
                    <button type="submit" class="btn btn-business-gradient">
                      <i class="bi bi-briefcase me-2"></i>사업운 분석하기
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
                      <h3 class="mb-3">사업운 분석</h3>
                      <div class="business-stats d-flex mb-4">
                        <div class="business-stat-item text-center me-3">
                          <div class="business-stat-circle">
                            <div class="business-stat-value">{{ businessStats.leadership }}%</div>
                          </div>
                          <div class="business-stat-label">리더십</div>
                        </div>
                        <div class="business-stat-item text-center me-3">
                          <div class="business-stat-circle">
                            <div class="business-stat-value">{{ businessStats.strategy }}%</div>
                          </div>
                          <div class="business-stat-label">전략안목</div>
                        </div>
                        <div class="business-stat-item text-center me-3">
                          <div class="business-stat-circle">
                            <div class="business-stat-value">{{ businessStats.networking }}%</div>
                          </div>
                          <div class="business-stat-label">인맥활용</div>
                        </div>
                        <div class="business-stat-item text-center">
                          <div class="business-stat-circle">
                            <div class="business-stat-value">{{ businessStats.luck }}%</div>
                          </div>
                          <div class="business-stat-label">현재 운세</div>
                        </div>
                      </div>
                      
                      <div class="business-analysis mb-4">
                        <h4 class="mb-3">{{ getMonthPeriod() }} 사업운</h4>
                        <p>{{ businessFortuneText }}</p>
                      </div>
                      
                      <div class="business-recommendation mb-4">
                        <h4 class="mb-3">비즈니스 추천</h4>
                        <div class="row">
                          <div class="col-md-6 mb-3">
                            <div class="business-type">
                              <div class="business-type-header d-flex align-items-center mb-2">
                                <div class="business-icon me-2"><i class="bi bi-check-circle-fill text-success"></i></div>
                                <h5 class="mb-0">{{ businessTypes.best.name }}</h5>
                              </div>
                              <p>{{ businessTypes.best.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="business-type">
                              <div class="business-type-header d-flex align-items-center mb-2">
                                <div class="business-icon me-2"><i class="bi bi-star-fill text-warning"></i></div>
                                <h5 class="mb-0">{{ businessTypes.good.name }}</h5>
                              </div>
                              <p>{{ businessTypes.good.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="business-type">
                              <div class="business-type-header d-flex align-items-center mb-2">
                                <div class="business-icon me-2"><i class="bi bi-exclamation-circle-fill text-danger"></i></div>
                                <h5 class="mb-0">{{ businessTypes.avoid.name }}</h5>
                              </div>
                              <p>{{ businessTypes.avoid.description }}</p>
                            </div>
                          </div>
                          <div class="col-md-6 mb-3">
                            <div class="business-type">
                              <div class="business-type-header d-flex align-items-center mb-2">
                                <div class="business-icon me-2"><i class="bi bi-calendar-check text-primary"></i></div>
                                <h5 class="mb-0">좋은 사업 시기</h5>
                              </div>
                              <p>{{ bestTimingText }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="business-advice card mb-4">
                  <div class="card-body">
                    <h4 class="mb-3"><i class="bi bi-chat-quote me-2 text-primary"></i>사업 조언</h4>
                    <div class="business-advice-content">
                      <p>{{ businessAdvice }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">사업 성공 키워드</h3>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="success-factor">
                    <h5><i class="bi bi-check2-circle text-success me-2"></i>당신의 강점</h5>
                    <ul class="list-unstyled ps-4">
                      <li v-for="(item, index) in successFactors.strengths" :key="`strength-${index}`" class="mb-2">
                        {{ item }}
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="success-factor">
                    <h5><i class="bi bi-shield-fill-check text-primary me-2"></i>필요한 보완점</h5>
                    <ul class="list-unstyled ps-4">
                      <li v-for="(item, index) in successFactors.improvements" :key="`improvement-${index}`" class="mb-2">
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
              <h3 class="mb-3">파트너 궁합 분석</h3>
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                회원 가입 후 이용하실 수 있는 서비스입니다. 비즈니스 파트너와의 궁합을 확인해보세요.
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
  name: 'FortuneBusiness',
  data() {
    return {
      userInfo: {
        birthdate: '',
        birthtime: '',
        gender: '',
        businessStatus: ''
      },
      userInfoSubmitted: false,
      sajuInfo: {
        year: { heaven: '경', earth: '신' },
        month: { heaven: '신', earth: '유' },
        day: { heaven: '계', earth: '미' },
        hour: { heaven: '을', earth: '사' }
      },
      elementsAnalysis: {
        metal: 25,  // 금
        wood: 30,   // 목
        water: 15,  // 수
        fire: 20,   // 화
        earth: 10   // 토
      },
      businessStats: {
        leadership: 78,
        strategy: 65,
        networking: 82,
        luck: 70
      },
      businessFortuneText: '이번 달은 사업 운이 상승하는 시기입니다. 특히 목(木)의 기운이 강해 새로운 아이디어와 창의력이 넘치고 이를 실행에 옮길 수 있는 좋은 때입니다. 다양한 사람들과의 네트워킹을 통해 새로운 기회를 얻을 수 있습니다. 다만, 너무 많은 일을 동시에 벌이지 않도록 주의하세요. 집중력을 유지하고 한 가지씩 실행에 옮기는 전략이 효과적일 것입니다.',
      businessTypes: {
        best: {
          name: '콘텐츠 및 교육 사업',
          description: '당신의 사주에 목(木)의 기운이 강하므로, 창의적인 콘텐츠 제작이나 지식 전달과 관련된 사업이 유리합니다. 온라인 교육, 코칭, 디지털 콘텐츠 비즈니스 등을 고려해보세요.'
        },
        good: {
          name: '서비스 및 컨설팅 업종',
          description: '인적 네트워크를 활용할 수 있는 서비스업이 적합합니다. 특히 트렌드를 예측하고 새로운 서비스 모델을 제시하는 컨설팅 분야에서 좋은 성과를 거둘 수 있습니다.'
        },
        avoid: {
          name: '제조업 및 중공업',
          description: '현재 당신의 사주에는 토(土)의 기운이 약해 장기적인 투자와 안정성이 필요한 제조업이나 중공업은 어려움을 겪을 수 있습니다. 또한 금속을 다루는 산업도 피하는 것이 좋습니다.'
        }
      },
      bestTimingText: '8월부터 11월 사이가 사업을 확장하거나 새로운 프로젝트를 시작하기 좋은 시기입니다. 특히 화요일과 목요일이 중요한 결정을 내리기에 유리한 날입니다.',
      businessAdvice: '당신의 사주에는 목(木)과 화(火)의 기운이 강하여 창의적인 아이디어와 추진력이 뛰어납니다. 이러한 강점을 활용하여 새로운 트렌드를 선도하고 혁신적인 비즈니스 모델을 구축하는 데 집중하세요. 다만, 토(土)의 기운이 부족하여 안정성과 체계적인 관리 측면에서는 보완이 필요합니다. 전문적인 관리자를 영입하거나 시스템을 구축하여 이러한 약점을 보완하면 더욱 성공적인 사업을 운영할 수 있을 것입니다.',
      successFactors: {
        strengths: [
          '창의적인 아이디어 발상 능력',
          '빠른 결단력과 추진력',
          '인맥 형성 및 네트워킹 능력',
          '트렌드를 빠르게 파악하는 안목',
          '설득력 있는 커뮤니케이션 스킬'
        ],
        improvements: [
          '장기적인 계획 수립 및 실행',
          '재무 관리 및 비용 통제',
          '체계적인 조직 관리',
          '인내심을 갖고 기다리는 능력',
          '디테일에 대한 집중력'
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
        businessStatus: ''
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
.fortune-business-page {
  padding: 2rem 0;
}

.fortune-title {
  font-weight: 700;
  background: linear-gradient(135deg, #4e54c8, #8f94fb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fortune-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.btn-business-gradient {
  background: linear-gradient(135deg, #4e54c8, #8f94fb);
  color: white;
  border: none;
  transition: all 0.3s;
}

.btn-business-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(78, 84, 200, 0.2);
}

.saju-info {
  background-color: #f8f9fa;
  border-left: 4px solid #4e54c8;
}

.saju-cell {
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  background-color: white;
}

.business-stat-item {
  flex: 1;
}

.business-stat-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4e54c8, #8f94fb);
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.business-stat-value {
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
}

.business-stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.business-type {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.5rem;
  height: 100%;
}

.business-icon {
  font-size: 1.2rem;
}

.business-advice {
  border-left: 4px solid #4e54c8;
}

.success-factor {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  height: 100%;
}

.success-factor li {
  position: relative;
  padding-left: 1.5rem;
}

.success-factor li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #4e54c8;
}
</style> 