<template>
  <div class="naming-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-sm mb-4">
            <div class="card-body text-center py-5">
              <h1 class="naming-title mb-4">AI 작명 서비스</h1>
              <p class="naming-subtitle">
                사주팔자를 기반으로 아이나 상호에 최적화된 이름을 추천해드립니다
              </p>
            </div>
          </div>
          
          <div class="row mb-4">
            <div class="col-md-6 mb-3 mb-md-0">
              <div class="naming-type-card baby-card" @click="selectNamingType('baby')" :class="{ active: namingType === 'baby' }">
                <div class="naming-type-content text-center py-4">
                  <div class="naming-icon mb-3">
                    <i class="bi bi-emoji-smile display-1"></i>
                  </div>
                  <h3>아이 이름</h3>
                  <p>사주팔자에 맞는 아이 이름을 추천해드립니다</p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="naming-type-card business-card" @click="selectNamingType('business')" :class="{ active: namingType === 'business' }">
                <div class="naming-type-content text-center py-4">
                  <div class="naming-icon mb-3">
                    <i class="bi bi-building display-1"></i>
                  </div>
                  <h3>상호명</h3>
                  <p>당신의 사업 성공을 도울 상호명을 추천해드립니다</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4" v-if="namingType">
            <div class="card-body p-4">
              <div v-if="!userInfoSubmitted">
                <h3 class="mb-4">정보 입력</h3>
                <form @submit.prevent="submitUserInfo">
                  <!-- 아이 이름인 경우 앞의 3개 항목만 표시 -->
                  <div v-if="namingType === 'baby'">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="birthdate" class="form-label">아이 생년월일</label>
                        <input 
                          type="date" 
                          id="birthdate" 
                          v-model="babyInfo.birthdate" 
                          class="form-control" 
                          required
                        >
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="birthtime" class="form-label">태어난 시간</label>
                        <input 
                          type="time" 
                          id="birthtime" 
                          v-model="babyInfo.birthtime" 
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
                            v-model="babyInfo.gender"
                            required
                          >
                          <label class="form-check-label" for="male">남자아이</label>
                        </div>
                        <div class="form-check">
                          <input 
                            class="form-check-input" 
                            type="radio" 
                            name="gender" 
                            id="female" 
                            value="female"
                            v-model="babyInfo.gender"
                          >
                          <label class="form-check-label" for="female">여자아이</label>
                        </div>
                      </div>
                    </div>
                    <div class="mb-3">
                      <label for="lastName" class="form-label">성(姓)</label>
                      <input 
                        type="text" 
                        id="lastName" 
                        v-model="babyInfo.lastName" 
                        class="form-control" 
                        placeholder="성을 입력하세요 (예: 김, 이, 박)"
                        required
                      >
                    </div>
                    <div class="mb-3">
                      <label class="form-label">이름 글자수</label>
                      <div class="d-flex">
                        <div class="form-check me-4">
                          <input 
                            class="form-check-input" 
                            type="radio" 
                            name="nameLength" 
                            id="oneCharacter" 
                            value="1" 
                            v-model="babyInfo.nameLength"
                            required
                          >
                          <label class="form-check-label" for="oneCharacter">한 글자</label>
                        </div>
                        <div class="form-check">
                          <input 
                            class="form-check-input" 
                            type="radio" 
                            name="nameLength" 
                            id="twoCharacters" 
                            value="2"
                            v-model="babyInfo.nameLength"
                          >
                          <label class="form-check-label" for="twoCharacters">두 글자</label>
                        </div>
                      </div>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">원하는 이름의 특성 (복수 선택 가능)</label>
                      <div class="row">
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="strength" value="strength" v-model="babyInfo.traits">
                            <label class="form-check-label" for="strength">강인함</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="intelligence" value="intelligence" v-model="babyInfo.traits">
                            <label class="form-check-label" for="intelligence">지혜로움</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="kindness" value="kindness" v-model="babyInfo.traits">
                            <label class="form-check-label" for="kindness">친절함</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="prosperity" value="prosperity" v-model="babyInfo.traits">
                            <label class="form-check-label" for="prosperity">부귀</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="creativity" value="creativity" v-model="babyInfo.traits">
                            <label class="form-check-label" for="creativity">창의성</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="confidence" value="confidence" v-model="babyInfo.traits">
                            <label class="form-check-label" for="confidence">자신감</label>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 상호명인 경우 뒤의 3개 항목만 표시 -->
                  <div v-if="namingType === 'business'">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label for="ownerBirthdate" class="form-label">대표자 생년월일</label>
                        <input 
                          type="date" 
                          id="ownerBirthdate" 
                          v-model="businessInfo.ownerBirthdate" 
                          class="form-control" 
                          required
                        >
                      </div>
                      <div class="col-md-6 mb-3">
                        <label for="foundingDate" class="form-label">창업일(예상)</label>
                        <input 
                          type="date" 
                          id="foundingDate" 
                          v-model="businessInfo.foundingDate" 
                          class="form-control" 
                          required
                        >
                      </div>
                    </div>
                    <div class="mb-3">
                      <label for="businessType" class="form-label">업종</label>
                      <select 
                        id="businessType" 
                        v-model="businessInfo.businessType" 
                        class="form-select"
                        required
                      >
                        <option value="" disabled selected>업종을 선택하세요</option>
                        <option value="restaurant">음식점/카페</option>
                        <option value="retail">소매/판매</option>
                        <option value="service">서비스업</option>
                        <option value="tech">IT/기술</option>
                        <option value="education">교육</option>
                        <option value="manufacturing">제조/생산</option>
                        <option value="beauty">미용/뷰티</option>
                        <option value="health">건강/의료</option>
                        <option value="other">기타</option>
                      </select>
                    </div>
                    <div class="mb-3">
                      <label for="businessDetail" class="form-label">사업 내용 (상세)</label>
                      <textarea 
                        id="businessDetail" 
                        v-model="businessInfo.businessDetail" 
                        class="form-control" 
                        rows="3"
                        placeholder="사업의 특성, 판매 상품/서비스, 대상 고객층 등을 간략히 적어주세요"
                        required
                      ></textarea>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">원하는 상호명 특성 (복수 선택 가능)</label>
                      <div class="row">
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="memorability" value="memorability" v-model="businessInfo.traits">
                            <label class="form-check-label" for="memorability">기억하기 쉬움</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="modernity" value="modernity" v-model="businessInfo.traits">
                            <label class="form-check-label" for="modernity">현대적인</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="tradition" value="tradition" v-model="businessInfo.traits">
                            <label class="form-check-label" for="tradition">전통적인</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="luxury" value="luxury" v-model="businessInfo.traits">
                            <label class="form-check-label" for="luxury">고급스러움</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="friendly" value="friendly" v-model="businessInfo.traits">
                            <label class="form-check-label" for="friendly">친근한</label>
                          </div>
                        </div>
                        <div class="col-md-4 mb-2">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="professional" value="professional" v-model="businessInfo.traits">
                            <label class="form-check-label" for="professional">전문적인</label>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="d-grid">
                    <button type="submit" class="btn btn-naming-gradient">
                      <i class="bi bi-magic me-2"></i>이름 추천받기
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
                
                <div class="naming-result mb-4">
                  <div class="result-header text-center mb-4">
                    <h3 v-if="namingType === 'baby'">
                      <span class="text-primary">{{ babyInfo.lastName }}</span>님의 아이를 위한 이름 추천
                    </h3>
                    <h3 v-else>
                      <span class="text-primary">{{ getBusinessTypeText() }}</span> 사업을 위한 상호명 추천
                    </h3>
                    <div class="sajuInfo mt-3">
                      <p class="mb-0">{{ getSajuText() }}</p>
                      <p class="text-muted">{{ getElementsText() }}</p>
                    </div>
                  </div>
                  
                  <div class="row">
                    <div class="col-md-8 offset-md-2">
                      <div class="recommended-names mb-4">
                        <h4 class="text-center mb-3">추천 이름</h4>
                        <div class="row">
                          <div v-for="(name, index) in recommendedNames" :key="index" class="col-md-4 mb-4">
                            <div class="name-card" @click="selectName(index)" :class="{ active: selectedNameIndex === index }">
                              <div class="name-card-content text-center">
                                <h3 class="mb-3">{{ name.name }}</h3>
                                <p class="mb-2">{{ name.meaning }}</p>
                                <div class="name-score">
                                  <span class="score-label">적합도</span>
                                  <div class="progress">
                                    <div class="progress-bar" role="progressbar" :style="`width: ${name.score}%`" :aria-valuenow="name.score" aria-valuemin="0" aria-valuemax="100"></div>
                                  </div>
                                  <span class="score-value">{{ name.score }}%</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div class="name-analysis card mb-4" v-if="selectedNameIndex !== null">
                        <div class="card-body">
                          <h4 class="mb-3"><i class="bi bi-search me-2 text-primary"></i>선택한 이름 분석</h4>
                          <p><strong>이름:</strong> {{ recommendedNames[selectedNameIndex].name }}</p>
                          <p><strong>의미:</strong> {{ recommendedNames[selectedNameIndex].meaning }}</p>
                          <p><strong>발음:</strong> {{ recommendedNames[selectedNameIndex].pronunciation }}</p>
                          <p><strong>음양오행:</strong> {{ recommendedNames[selectedNameIndex].elements }}</p>
                          <p><strong>길흉 분석:</strong> {{ recommendedNames[selectedNameIndex].analysis }}</p>
                          <p><strong>총획:</strong> {{ recommendedNames[selectedNameIndex].strokes }}획</p>
                          <p><strong>이름이 가져다 줄 특성:</strong> {{ recommendedNames[selectedNameIndex].traits }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="text-center">
                  <button class="btn btn-lg btn-primary">
                    <i class="bi bi-download me-2"></i>이름 분석 결과 저장하기
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">작명 서비스 특징</h3>
              <div class="row">
                <div class="col-md-4 mb-3">
                  <div class="feature-item">
                    <div class="feature-icon mb-3">
                      <i class="bi bi-stars text-warning"></i>
                    </div>
                    <h5>사주팔자 기반 분석</h5>
                    <p>태어난 날짜와 시간의 사주팔자를 분석하여 가장 적합한 음양오행의 이름을 추천합니다.</p>
                  </div>
                </div>
                <div class="col-md-4 mb-3">
                  <div class="feature-item">
                    <div class="feature-icon mb-3">
                      <i class="bi bi-graph-up-arrow text-success"></i>
                    </div>
                    <h5>AI 기반 길흉 분석</h5>
                    <p>인공지능이 수천 개의 한자와 발음을 분석하여 길한 이름을 찾아 추천해드립니다.</p>
                  </div>
                </div>
                <div class="col-md-4 mb-3">
                  <div class="feature-item">
                    <div class="feature-icon mb-3">
                      <i class="bi bi-shield-check text-primary"></i>
                    </div>
                    <h5>한자 부수와 음운 조화</h5>
                    <p>한자의 부수와 발음의 조화를 고려하여 의미와 소리가 모두 아름다운 이름을 제안합니다.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card shadow-sm mb-4">
            <div class="card-body p-4">
              <h3 class="mb-3">고급 작명 서비스</h3>
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-2"></i>
                회원 가입 후 이용하실 수 있는 서비스입니다. 전문가의 1:1 상담과 함께 더 정교한 작명 서비스를 받아보세요.
              </div>
              <div class="text-center">
                <button class="btn btn-primary">
                  <i class="bi bi-person-plus me-2"></i>회원가입하고 프리미엄 작명 서비스 이용하기
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
  name: 'Naming',
  data() {
    return {
      namingType: null,
      userInfoSubmitted: false,
      selectedNameIndex: null,
      babyInfo: {
        birthdate: '',
        birthtime: '',
        gender: '',
        lastName: '',
        nameLength: '',
        traits: []
      },
      businessInfo: {
        ownerBirthdate: '',
        foundingDate: '',
        businessType: '',
        businessDetail: '',
        traits: []
      },
      recommendedNames: [
        {
          name: '준서',
          meaning: '진리를 따르는 맑은 물과 같은 사람',
          pronunciation: '준서 [Jun-seo]',
          elements: '수(水) + 금(金)',
          analysis: '매우 길한 이름으로, 학문과 지혜, 리더십에 좋은 영향을 줍니다.',
          strokes: 23,
          traits: '총명함, 정의감, 리더십, 성실함',
          score: 95
        },
        {
          name: '지호',
          meaning: '지혜롭고 큰 포부를 가진 호랑이 같은 사람',
          pronunciation: '지호 [Ji-ho]',
          elements: '토(土) + 화(火)',
          analysis: '길한 이름으로, 창의성과 도전 정신, 직관력에 좋은 영향을 줍니다.',
          strokes: 18,
          traits: '창의력, 추진력, 열정, 직관력',
          score: 88
        },
        {
          name: '서윤',
          meaning: '맑은 물처럼 은혜로운 사람',
          pronunciation: '서윤 [Seo-yun]',
          elements: '금(金) + 수(水)',
          analysis: '길한 이름으로, 예술적 감각과 소통 능력, 섬세함에 좋은 영향을 줍니다.',
          strokes: 21,
          traits: '섬세함, 언변, 예술성, 균형감',
          score: 92
        },
        {
          name: '도원미소',
          meaning: '사람들에게 기쁨과 웃음을 주는 카페',
          pronunciation: '도원미소 [Do-won-mi-so]',
          elements: '토(土) + 목(木) + 화(火)',
          analysis: '길한 상호명으로, 고객에게 편안함과 기쁨을 주는 사업에 좋은 영향을 줍니다.',
          strokes: 36,
          traits: '친근함, 따뜻함, 기억하기 쉬움',
          score: 89
        },
        {
          name: '청담명가',
          meaning: '맑고 정직한 명품 요리를 제공하는 집',
          pronunciation: '청담명가 [Cheong-dam-myeong-ga]',
          elements: '수(水) + 토(土) + 금(金)',
          analysis: '매우 길한 상호명으로, 고급스러움과 신뢰감을 주는 음식점에 좋은 영향을 줍니다.',
          strokes: 42,
          traits: '고급스러움, 전통성, 신뢰감',
          score: 94
        },
        {
          name: '미래기술',
          meaning: '미래를 선도하는 기술을 제공하는 기업',
          pronunciation: '미래기술 [Mi-rae-gi-sul]',
          elements: '화(火) + 목(木) + 금(金)',
          analysis: '길한 상호명으로, 혁신과 성장을 추구하는 기술 기업에 좋은 영향을 줍니다.',
          strokes: 31,
          traits: '혁신성, 미래지향적, 전문성',
          score: 87
        }
      ]
    }
  },
  methods: {
    selectNamingType(type) {
      this.namingType = type;
      this.userInfoSubmitted = false;
      this.selectedNameIndex = null;
    },
    submitUserInfo() {
      // 실제 구현에서는 API를 호출하여 이름 추천 데이터를 받아옵니다
      // 현재는 예시 데이터를 표시합니다
      this.userInfoSubmitted = true;
      
      // 아기 이름인 경우 앞의 3개 항목만 표시
      // 상호명인 경우 뒤의 3개 항목만 표시
      if (this.namingType === 'baby') {
        this.recommendedNames = this.recommendedNames.slice(0, 3);
      } else {
        this.recommendedNames = this.recommendedNames.slice(3, 6);
      }
    },
    resetForm() {
      this.userInfoSubmitted = false;
      this.selectedNameIndex = null;
      
      if (this.namingType === 'baby') {
        this.babyInfo = {
          birthdate: '',
          birthtime: '',
          gender: '',
          lastName: '',
          nameLength: '',
          traits: []
        };
      } else {
        this.businessInfo = {
          ownerBirthdate: '',
          foundingDate: '',
          businessType: '',
          businessDetail: '',
          traits: []
        };
      }
    },
    selectName(index) {
      this.selectedNameIndex = index;
    },
    getSajuText() {
      // 사주팔자 계산 로직
      return '계묘년 경진월 정유일 병자시';
    },
    getElementsText() {
      // 오행 분석 로직
      return '금(2) 목(1) 화(2) 토(1) 수(2)';
    },
    getBusinessTypeText() {
      const businessTypes = {
        'restaurant': '음식점/카페',
        'retail': '소매/판매',
        'service': '서비스업',
        'tech': 'IT/기술',
        'education': '교육',
        'manufacturing': '제조/생산',
        'beauty': '미용/뷰티',
        'health': '건강/의료',
        'other': '기타'
      };
      return businessTypes[this.businessInfo.businessType] || '신규';
    }
  }
}
</script>

<style scoped>
.naming-page {
  padding: 2rem 0;
}

.naming-title {
  font-weight: 700;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.naming-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.naming-type-card {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  cursor: pointer;
  height: 100%;
}

.naming-type-card:hover, .naming-type-card.active {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.baby-card {
  background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
}

.business-card {
  background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
}

.naming-type-content {
  color: #333;
  padding: 0 1rem;
}

.naming-icon {
  color: rgba(255, 255, 255, 0.8);
}

.btn-naming-gradient {
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  color: white;
  border: none;
  transition: all 0.3s;
}

.btn-naming-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 154, 158, 0.2);
}

.name-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  cursor: pointer;
  height: 100%;
}

.name-card:hover, .name-card.active {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #ff9a9e;
}

.name-card-content {
  padding: 1.5rem 1rem;
}

.name-card h3 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.name-score {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
}

.score-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.score-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.progress {
  flex: 1;
  margin: 0 0.5rem;
  height: 0.5rem;
}

.progress-bar {
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
}

.name-analysis {
  border-left: 4px solid #ff9a9e;
}

.feature-item {
  text-align: center;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #f8f9fa;
  height: 100%;
}

.feature-icon {
  font-size: 2rem;
}
</style> 