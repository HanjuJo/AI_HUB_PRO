<template>
  <div class="choice-helper">
    <div class="container py-5">
      <h1 class="text-center mb-5">선택 도우미</h1>
      
      <div class="row justify-content-center mb-5">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <div class="choice-helper-icon mb-3">
                  <i class="bi bi-shuffle"></i>
                </div>
                <h4>결정하기 어려운 선택이 있나요?</h4>
                <p class="text-muted">당신의 사주팔자와 오늘의 운세를 기반으로 최적의 선택을 도와드립니다</p>
              </div>
              
              <div v-if="!userData.birthdate" class="user-info-form">
                <h5 class="mb-4">사주 정보 입력</h5>
                <div class="mb-3">
                  <label class="form-label">생년월일</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    v-model="userData.birthdate"
                  >
                </div>
                <div class="mb-3">
                  <label class="form-label">태어난 시간</label>
                  <select class="form-select" v-model="userData.birthtime">
                    <option value="">모르겠음</option>
                    <option value="자시">자시 (23:00~01:00)</option>
                    <option value="축시">축시 (01:00~03:00)</option>
                    <option value="인시">인시 (03:00~05:00)</option>
                    <option value="묘시">묘시 (05:00~07:00)</option>
                    <option value="진시">진시 (07:00~09:00)</option>
                    <option value="사시">사시 (09:00~11:00)</option>
                    <option value="오시">오시 (11:00~13:00)</option>
                    <option value="미시">미시 (13:00~15:00)</option>
                    <option value="신시">신시 (15:00~17:00)</option>
                    <option value="유시">유시 (17:00~19:00)</option>
                    <option value="술시">술시 (19:00~21:00)</option>
                    <option value="해시">해시 (21:00~23:00)</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label">성별</label>
                  <div>
                    <div class="form-check form-check-inline">
                      <input class="form-check-input" type="radio" id="male" value="남성" v-model="userData.gender">
                      <label class="form-check-label" for="male">남성</label>
                    </div>
                    <div class="form-check form-check-inline">
                      <input class="form-check-input" type="radio" id="female" value="여성" v-model="userData.gender">
                      <label class="form-check-label" for="female">여성</label>
                    </div>
                  </div>
                </div>
                <div class="d-grid">
                  <button class="btn btn-primary btn-lg" @click="saveUserInfo">정보 저장</button>
                </div>
              </div>
              
              <div v-else class="choice-form">
                <div v-if="!choiceResult">
                  <div class="mb-4">
                    <div class="d-flex align-items-center mb-3">
                      <div class="user-sajuinfo me-3">
                        <i class="bi bi-person-circle"></i>
                      </div>
                      <div>
                        <h6 class="mb-1">{{ formatBirthdate(userData.birthdate) }} {{ userData.birthtime || '시간미상' }}</h6>
                        <div class="saju-elements">
                          <span class="element" v-for="(element, index) in sajuElements" :key="index" :class="elementClass(element)">
                            {{ element }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h5 class="mb-3">어떤 선택을 도와드릴까요?</h5>
                  <div class="mb-3">
                    <select class="form-select mb-3" v-model="choiceType">
                      <option value="">선택 종류</option>
                      <option value="food">오늘 뭐 먹을까?</option>
                      <option value="travel">여행지 선택</option>
                      <option value="purchase">구매 결정</option>
                      <option value="career">진로/이직 결정</option>
                      <option value="investment">투자 결정</option>
                      <option value="etc">기타</option>
                    </select>
                  </div>
                  
                  <div v-if="choiceType">
                    <div class="mb-3">
                      <label class="form-label">선택지 입력</label>
                      <div class="input-group mb-3" v-for="(option, index) in choiceOptions" :key="index">
                        <span class="input-group-text">{{ index + 1 }}</span>
                        <input type="text" class="form-control" v-model="choiceOptions[index]" :placeholder="`선택지 ${index + 1}`">
                        <button 
                          class="btn btn-outline-danger" 
                          type="button"
                          @click="removeOption(index)"
                          v-if="choiceOptions.length > 2"
                        >
                          <i class="bi bi-x"></i>
                        </button>
                      </div>
                      <div v-if="choiceOptions.length < 5" class="d-grid">
                        <button class="btn btn-outline-primary" @click="addOption">
                          <i class="bi bi-plus"></i> 선택지 추가
                        </button>
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label">중요도</label>
                      <select class="form-select" v-model="importance">
                        <option value="low">낮음 (일상적인 선택)</option>
                        <option value="medium">중간 (단기적으로 중요한 선택)</option>
                        <option value="high">높음 (인생의 중요한 결정)</option>
                      </select>
                    </div>
                    
                    <div class="d-grid">
                      <button class="btn btn-primary btn-lg" @click="getChoiceResult" :disabled="isLoading">
                        <span v-if="isLoading">
                          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                          분석 중...
                        </span>
                        <span v-else>선택 추천받기</span>
                      </button>
                    </div>
                  </div>
                </div>
                
                <div v-else class="choice-result text-center">
                  <div class="result-icon mb-4">
                    <i class="bi bi-check-circle-fill"></i>
                  </div>
                  <h4 class="mb-3">당신에게 추천하는 선택은...</h4>
                  <div class="recommended-choice mb-4">
                    <h2>{{ choiceResult.recommendation }}</h2>
                  </div>
                  
                  <div class="card mb-4">
                    <div class="card-body">
                      <h5 class="card-title">오늘의 운세와 사주 분석</h5>
                      <p class="card-text">{{ choiceResult.analysis }}</p>
                    </div>
                  </div>
                  
                  <div class="elemental-chart mb-4">
                    <h5 class="mb-3">사주 오행 분석</h5>
                    <div class="elements-container">
                      <div v-for="(value, element) in choiceResult.elements" :key="element" class="element-item">
                        <div class="element-circle" :class="`element-${element}`">
                          {{ element }}
                        </div>
                        <div class="element-value">{{ value }}%</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="luck-factors mb-4">
                    <h5 class="mb-3">오늘 행운 요소</h5>
                    <div class="row">
                      <div class="col-md-4 mb-3">
                        <div class="luck-item">
                          <div class="luck-icon">
                            <i class="bi bi-palette"></i>
                          </div>
                          <div class="luck-label">행운의 색</div>
                          <div class="luck-value">{{ choiceResult.luckyColor }}</div>
                        </div>
                      </div>
                      <div class="col-md-4 mb-3">
                        <div class="luck-item">
                          <div class="luck-icon">
                            <i class="bi bi-geo-alt"></i>
                          </div>
                          <div class="luck-label">행운의 방향</div>
                          <div class="luck-value">{{ choiceResult.luckyDirection }}</div>
                        </div>
                      </div>
                      <div class="col-md-4 mb-3">
                        <div class="luck-item">
                          <div class="luck-icon">
                            <i class="bi bi-clock"></i>
                          </div>
                          <div class="luck-label">행운의 시간</div>
                          <div class="luck-value">{{ choiceResult.luckyTime }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                    <button class="btn btn-primary" @click="resetForm">다른 선택하기</button>
                    <button class="btn btn-outline-primary" @click="shareResult">
                      <i class="bi bi-share"></i> 공유하기
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row justify-content-center mt-5">
        <div class="col-lg-8">
          <div class="card shadow-sm p-4">
            <h4 class="mb-3">자주 묻는 질문</h4>
            <div class="accordion" id="accordionFAQ">
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne">
                    사주 정보는 어떻게 활용되나요?
                  </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFAQ">
                  <div class="accordion-body">
                    입력하신 생년월일과 시간을 바탕으로 사주팔자를 분석하고, 오늘의 운세와 결합하여 당신에게 가장 적합한 선택을 추천해드립니다. 사주 속 오행의 균형과 현재의 운세 흐름을 고려한 과학적인 분석 방법을 사용합니다.
                  </div>
                </div>
              </div>
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo">
                    선택의 중요도는 어떤 영향을 미치나요?
                  </button>
                </h2>
                <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionFAQ">
                  <div class="accordion-body">
                    중요도에 따라 분석의 깊이가 달라집니다. 일상적인 선택은 오늘의 운세에 더 비중을 두고, 중요한 인생 결정일수록 장기적인 사주 흐름과 대운을 더 깊이 분석합니다. 이를 통해 상황에 맞는 최적의 추천을 제공합니다.
                  </div>
                </div>
              </div>
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree">
                    선택 추천은 얼마나 정확한가요?
                  </button>
                </h2>
                <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionFAQ">
                  <div class="accordion-body">
                    선택의 신은 전통적인 사주명리학과 현대 AI 기술을 결합하여 약 85%의 정확도를 자랑합니다. 그러나 모든 선택은 궁극적으로 당신의 판단에 달려 있음을 기억해주세요. 저희 서비스는 결정을 내리는 과정에서 도움을 주는 도구로 활용하시길 권장합니다.
                  </div>
                </div>
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
  name: 'ChoiceHelper',
  data() {
    return {
      userData: {
        birthdate: '',
        birthtime: '',
        gender: ''
      },
      choiceType: '',
      choiceOptions: ['', ''],
      importance: 'medium',
      isLoading: false,
      choiceResult: null,
      sajuElements: ['목', '화', '토', '금', '수', '화', '토', '금']
    }
  },
  methods: {
    saveUserInfo() {
      if (!this.userData.birthdate) {
        alert('생년월일을 입력해주세요.');
        return;
      }
      if (!this.userData.gender) {
        alert('성별을 선택해주세요.');
        return;
      }
      
      // 실제로는 사주 정보를 분석하는 API 호출
      this.analyzeSaju();
      
      // 로컬 스토리지에 사용자 정보 저장
      localStorage.setItem('userSajuData', JSON.stringify(this.userData));
    },
    
    analyzeSaju() {
      // 실제로는 사주 분석 API 호출
      // 여기서는 간단한 예시 데이터로 대체
      this.sajuElements = ['목', '화', '토', '금', '수', '화', '토', '금'];
    },
    
    addOption() {
      if (this.choiceOptions.length < 5) {
        this.choiceOptions.push('');
      }
    },
    
    removeOption(index) {
      if (this.choiceOptions.length > 2) {
        this.choiceOptions.splice(index, 1);
      }
    },
    
    async getChoiceResult() {
      // 선택지 유효성 검사
      for (let i = 0; i < this.choiceOptions.length; i++) {
        if (!this.choiceOptions[i].trim()) {
          alert(`선택지 ${i+1}를 입력해주세요.`);
          return;
        }
      }
      
      this.isLoading = true;
      
      try {
        // 실제로는 API 호출
        // const response = await axios.post('/api/v1/choice-helper', {
        //   saju: {
        //     birthdate: this.userData.birthdate,
        //     birthtime: this.userData.birthtime,
        //     gender: this.userData.gender
        //   },
        //   choiceType: this.choiceType,
        //   options: this.choiceOptions,
        //   importance: this.importance
        // });
        // this.choiceResult = response.data;
        
        // 더미 데이터
        await new Promise(resolve => setTimeout(resolve, 2000)); // 분석 시간 시뮬레이션
        
        // 랜덤하게 선택지 중 하나 선택
        const randomIndex = Math.floor(Math.random() * this.choiceOptions.length);
        const selectedOption = this.choiceOptions[randomIndex];
        
        this.choiceResult = {
          recommendation: selectedOption,
          analysis: `오늘은 ${this.getSajuDayType()}일로, ${this.getChoiceTypeDescription()}에 적합한 날입니다. 당신의 사주에 ${this.getElementBalance()} 있어 '${selectedOption}'이(가) 당신에게 더 유리한 선택입니다. 특히 오늘은 ${this.getLuckyActivity()}에 행운이 함께합니다.`,
          elements: {
            '목': Math.floor(Math.random() * 30) + 10,
            '화': Math.floor(Math.random() * 30) + 10,
            '토': Math.floor(Math.random() * 30) + 10,
            '금': Math.floor(Math.random() * 30) + 10,
            '수': Math.floor(Math.random() * 30) + 10
          },
          luckyColor: this.getLuckyColor(),
          luckyDirection: this.getLuckyDirection(),
          luckyTime: this.getLuckyTime()
        };
      } catch (error) {
        console.error('선택 분석 중 오류가 발생했습니다:', error);
        alert('분석 중 오류가 발생했습니다. 다시 시도해주세요.');
      } finally {
        this.isLoading = false;
      }
    },
    
    resetForm() {
      this.choiceType = '';
      this.choiceOptions = ['', ''];
      this.importance = 'medium';
      this.choiceResult = null;
    },
    
    shareResult() {
      // 공유 기능 구현
      alert('공유 기능은 준비 중입니다.');
    },
    
    formatBirthdate(date) {
      if (!date) return '';
      const d = new Date(date);
      return `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일`;
    },
    
    elementClass(element) {
      const classes = {
        '목': 'element-wood',
        '화': 'element-fire',
        '토': 'element-earth',
        '금': 'element-metal',
        '수': 'element-water'
      };
      return classes[element] || '';
    },
    
    // 더미 데이터 생성 도우미 함수들
    getSajuDayType() {
      const types = ['양금', '음목', '양수', '음화', '양토', '음금', '양목', '음수', '양화', '음토'];
      return types[Math.floor(Math.random() * types.length)];
    },
    
    getChoiceTypeDescription() {
      const descriptions = {
        'food': '음식 선택과 식사',
        'travel': '여행과 외출',
        'purchase': '물건 구매와 소비',
        'career': '진로와 직업 결정',
        'investment': '투자와 재테크',
        'etc': '중요한 결정'
      };
      return descriptions[this.choiceType] || '일상적인 선택';
    },
    
    getElementBalance() {
      const elements = [
        '목(나무)이 부족하여',
        '화(불)의 기운이 강하여',
        '토(흙)의 기운이 균형있게 조화를 이루고',
        '금(쇠)의 기운이 약하여',
        '수(물)가 풍부하여'
      ];
      return elements[Math.floor(Math.random() * elements.length)];
    },
    
    getLuckyActivity() {
      const activities = [
        '창의적인 활동',
        '사람들과의 만남',
        '독서와 학습',
        '운동과 야외 활동',
        '재정 관리와 계획 세우기',
        '명상과 휴식'
      ];
      return activities[Math.floor(Math.random() * activities.length)];
    },
    
    getLuckyColor() {
      const colors = ['빨강', '파랑', '노랑', '초록', '보라', '하얀', '검정'];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    
    getLuckyDirection() {
      const directions = ['동', '서', '남', '북', '북동', '북서', '남동', '남서'];
      return directions[Math.floor(Math.random() * directions.length)];
    },
    
    getLuckyTime() {
      const times = ['오전 9시~11시', '오후 1시~3시', '오후 5시~7시', '오후 9시~11시'];
      return times[Math.floor(Math.random() * times.length)];
    }
  },
  mounted() {
    // 로컬 스토리지에서 사용자 정보 불러오기
    const savedUserData = localStorage.getItem('userSajuData');
    if (savedUserData) {
      this.userData = JSON.parse(savedUserData);
      this.analyzeSaju();
    }
  }
}
</script>

<style scoped>
.choice-helper {
  background-color: #f8f9fe;
  min-height: 100vh;
}

.choice-helper-icon {
  width: 80px;
  height: 80px;
  background-color: rgba(108, 92, 231, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 32px;
  color: #6c5ce7;
}

.user-sajuinfo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f1f3f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #495057;
}

.saju-elements {
  display: flex;
  gap: 5px;
}

.element {
  display: inline-block;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.element-wood {
  background-color: #2ecc71;
}

.element-fire {
  background-color: #e74c3c;
}

.element-earth {
  background-color: #f39c12;
}

.element-metal {
  background-color: #95a5a6;
}

.element-water {
  background-color: #3498db;
}

.result-icon {
  font-size: 64px;
  color: #6c5ce7;
}

.recommended-choice {
  border: 2px solid #6c5ce7;
  padding: 20px;
  border-radius: 15px;
  background-color: rgba(108, 92, 231, 0.05);
}

.elements-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.element-item {
  text-align: center;
}

.element-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  color: white;
  font-weight: bold;
}

.element-목, .element-wood {
  background-color: #2ecc71;
}

.element-화, .element-fire {
  background-color: #e74c3c;
}

.element-토, .element-earth {
  background-color: #f39c12;
}

.element-금, .element-metal {
  background-color: #95a5a6;
}

.element-수, .element-water {
  background-color: #3498db;
}

.luck-item {
  text-align: center;
  padding: 15px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.luck-icon {
  font-size: 24px;
  color: #6c5ce7;
  margin-bottom: 10px;
}

.luck-label {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 5px;
}

.luck-value {
  font-weight: bold;
}
</style> 