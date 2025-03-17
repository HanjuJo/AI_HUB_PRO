<template>
  <div class="home">
    <!-- 메인 배너 섹션 -->
    <section class="hero-section py-5 text-center text-white">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-10">
            <h1 class="display-4 fw-bold mb-4">선택의 신</h1>
            <p class="lead mb-4">
              사주팔자 기반 AI가 당신의 모든 선택을 도와드립니다
            </p>
            <div class="hero-buttons">
              <router-link to="/choice-helper" class="btn btn-primary btn-lg me-3">
                <i class="bi bi-magic me-2"></i>선택 도우미
              </router-link>
              <router-link to="/daily-fortune" class="btn btn-outline-light btn-lg">
                <i class="bi bi-stars me-2"></i>오늘의 운세
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 주요 기능 섹션 -->
    <section class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">선택의 순간, AI가 함께합니다</h2>
        
        <div class="row g-4">
          <!-- 오늘의 선택 -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-3">
                  <i class="bi bi-calendar-check fs-1 text-primary"></i>
                </div>
                <h4 class="card-title">오늘의 선택</h4>
                <p class="card-text">
                  당신의 사주팔자와 오늘의 운세를 분석하여 하루의 중요한 선택들을 도와드립니다.
                </p>
                <router-link to="/daily-choice" class="btn btn-sm btn-outline-primary mt-3">
                  알아보기
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- 선택 도우미 -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-3">
                  <i class="bi bi-shuffle fs-1 text-primary"></i>
                </div>
                <h4 class="card-title">선택 도우미</h4>
                <p class="card-text">
                  A와 B 중 고민될 때, 당신의 사주와 운세에 기반한 AI가 최적의 선택을 추천합니다.
                </p>
                <router-link to="/choice-helper" class="btn btn-sm btn-outline-primary mt-3">
                  선택하기
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- AI 작명 -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-3">
                  <i class="bi bi-cursor-text fs-1 text-primary"></i>
                </div>
                <h4 class="card-title">AI 작명</h4>
                <p class="card-text">
                  아이 이름부터 상호명까지, 사주와 음양오행을 고려한 행운의 이름을 추천해드립니다.
                </p>
                <router-link to="/naming" class="btn btn-sm btn-outline-primary mt-3">
                  이름 짓기
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 인기 서비스 섹션 -->
    <section class="popular-services py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">인기 서비스</h2>
        
        <div class="row g-4">
          <!-- 연애운 -->
          <div class="col-lg-3 col-md-6">
            <div class="card border-0 fortune-card h-100">
              <div class="card-body text-center">
                <div class="fortune-icon mb-3">
                  <i class="bi bi-heart-fill text-danger"></i>
                </div>
                <h5>연애운</h5>
                <p class="small text-muted">나의 오늘 연애운은?</p>
                <router-link to="/fortune/love" class="stretched-link"></router-link>
              </div>
            </div>
          </div>
          
          <!-- 금전운 -->
          <div class="col-lg-3 col-md-6">
            <div class="card border-0 fortune-card h-100">
              <div class="card-body text-center">
                <div class="fortune-icon mb-3">
                  <i class="bi bi-coin text-warning"></i>
                </div>
                <h5>금전운</h5>
                <p class="small text-muted">오늘의 재물을 부르는 행동은?</p>
                <router-link to="/fortune/money" class="stretched-link"></router-link>
              </div>
            </div>
          </div>
          
          <!-- 사업운 -->
          <div class="col-lg-3 col-md-6">
            <div class="card border-0 fortune-card h-100">
              <div class="card-body text-center">
                <div class="fortune-icon mb-3">
                  <i class="bi bi-briefcase-fill text-success"></i>
                </div>
                <h5>사업운</h5>
                <p class="small text-muted">비즈니스 결정에 도움이 필요하세요?</p>
                <router-link to="/fortune/business" class="stretched-link"></router-link>
              </div>
            </div>
          </div>
          
          <!-- 건강운 -->
          <div class="col-lg-3 col-md-6">
            <div class="card border-0 fortune-card h-100">
              <div class="card-body text-center">
                <div class="fortune-icon mb-3">
                  <i class="bi bi-activity text-info"></i>
                </div>
                <h5>건강운</h5>
                <p class="small text-muted">오늘 나의 건강 상태와 주의점</p>
                <router-link to="/fortune/health" class="stretched-link"></router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 리뷰 섹션 -->
    <section class="testimonials py-5">
      <div class="container">
        <h2 class="text-center mb-5">사용자 후기</h2>
        
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div id="testimonialCarousel" class="carousel slide" data-bs-ride="carousel">
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <div class="testimonial-item text-center p-4">
                    <p class="testimonial-text mb-3">
                      "매일 아침 어떤 옷을 입을지 고민했는데, 선택의 신 덕분에 항상 최고의 선택을 하고 있어요. 정말 신기하게도 추천해준 대로 했더니 하루가 정말 달라졌습니다!"
                    </p>
                    <h5 class="mb-1">김미영님</h5>
                    <p class="small text-muted">30대 / 회사원</p>
                  </div>
                </div>
                <div class="carousel-item">
                  <div class="testimonial-item text-center p-4">
                    <p class="testimonial-text mb-3">
                      "창업을 준비하면서 사업명을 정하기 위해 AI 작명 서비스를 이용했어요. 추천받은 이름으로 시작한 후 매출이 2배 이상 올랐습니다. 과학적으로 설명하기 어렵지만 효과는 확실해요!"
                    </p>
                    <h5 class="mb-1">박준호님</h5>
                    <p class="small text-muted">40대 / 자영업</p>
                  </div>
                </div>
                <div class="carousel-item">
                  <div class="testimonial-item text-center p-4">
                    <p class="testimonial-text mb-3">
                      "친구들과 여행지를 고르는 데 의견이 분분했어요. 선택 도우미로 결정했더니 모두가 만족스러운 여행을 다녀올 수 있었습니다. 이제 무슨 일이든 선택의 신과 함께해요!"
                    </p>
                    <h5 class="mb-1">이지은님</h5>
                    <p class="small text-muted">20대 / 대학생</p>
                  </div>
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 가입 유도 섹션 -->
    <section class="cta-section py-5 text-center text-white">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <h2 class="mb-4">지금 바로 나만의 운세를 확인해보세요</h2>
            <p class="mb-4">로그인 후 더 정확한 사주 기반 선택을 도와드립니다.</p>
            <button @click="showLoginModal" class="btn btn-light btn-lg px-4">
              로그인하기
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { inject } from 'vue'

export default {
  name: 'HomePage',
  setup() {
    const router = useRouter()
    const showLoginModal = inject('showLoginModal')
    
    return {
      showLoginModal
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  padding: 100px 0;
  border-radius: 0 0 30px 30px;
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: rgba(108, 92, 231, 0.1);
}

.fortune-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.fortune-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.fortune-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(108, 92, 231, 0.1);
  font-size: 24px;
}

.testimonial-item {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

.testimonial-text {
  font-size: 1.1rem;
  font-style: italic;
  color: #555;
}

.cta-section {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  border-radius: 30px 30px 0 0;
}

.carousel-control-prev,
.carousel-control-next {
  width: 40px;
  height: 40px;
  background-color: #6c5ce7;
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  opacity: 1;
}

.carousel-control-prev {
  left: -50px;
}

.carousel-control-next {
  right: -50px;
}
</style>
