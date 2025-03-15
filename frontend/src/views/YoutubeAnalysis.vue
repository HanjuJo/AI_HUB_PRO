<template>
  <div class="youtube-analysis">
    <div class="analysis-header mb-4">
      <h1 class="display-5 mb-3">유튜브 채널 분석</h1>
      
      <!-- 채널 검색 섹션 -->
      <div class="search-section bg-light p-4 rounded">
        <div class="row">
          <div class="col-md-8 mx-auto">
            <div class="input-group mb-3">
              <input 
                type="text" 
                class="form-control form-control-lg"
                v-model="channelUrl"
                placeholder="유튜브 채널 URL을 입력하세요"
                @keyup.enter="analyzeChannel"
              >
              <button 
                class="btn btn-primary btn-lg"
                @click="analyzeChannel"
                :disabled="isAnalyzing"
              >
                <i class="bi" :class="isAnalyzing ? 'bi-hourglass-split' : 'bi-search'"></i>
                {{ isAnalyzing ? '분석 중...' : '분석하기' }}
              </button>
            </div>
            <div class="form-text text-center">
              예시: https://www.youtube.com/@example
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 분석 결과 섹션 -->
    <div v-if="channelData" class="analysis-results">
      <!-- 채널 개요 -->
      <div class="channel-overview card mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-2">
              <img 
                :src="channelData.thumbnail" 
                class="img-fluid rounded-circle"
                :alt="channelData.title"
              >
            </div>
            <div class="col-md-10">
              <h2 class="mb-2">{{ channelData.title }}</h2>
              <p class="text-muted mb-3">{{ channelData.description }}</p>
              <div class="stats d-flex gap-4">
                <div class="stat-item">
                  <div class="h4 mb-0">{{ formatNumber(channelData.subscriberCount) }}</div>
                  <div class="text-muted">구독자</div>
                </div>
                <div class="stat-item">
                  <div class="h4 mb-0">{{ formatNumber(channelData.videoCount) }}</div>
                  <div class="text-muted">총 영상</div>
                </div>
                <div class="stat-item">
                  <div class="h4 mb-0">{{ formatNumber(channelData.viewCount) }}</div>
                  <div class="text-muted">총 조회수</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 성장 분석 -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="card-title mb-0">구독자 성장 추이</h5>
            </div>
            <div class="card-body">
              <canvas ref="subscriberChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="card-title mb-0">조회수 추이</h5>
            </div>
            <div class="card-body">
              <canvas ref="viewsChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- 콘텐츠 분석 -->
      <div class="content-analysis card mb-4">
        <div class="card-header">
          <h5 class="card-title mb-0">콘텐츠 분석</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <!-- 인기 영상 TOP 5 -->
              <h6 class="mb-3">인기 영상 TOP 5</h6>
              <div class="list-group mb-4">
                <a 
                  v-for="video in topVideos" 
                  :key="video.id"
                  :href="'https://youtube.com/watch?v=' + video.id"
                  target="_blank"
                  class="list-group-item list-group-item-action"
                >
                  <div class="d-flex w-100 justify-content-between align-items-center">
                    <h6 class="mb-1">{{ video.title }}</h6>
                    <span class="badge bg-primary rounded-pill">
                      {{ formatNumber(video.views) }} 회
                    </span>
                  </div>
                  <p class="mb-1">{{ video.description }}</p>
                  <small class="text-muted">
                    <i class="bi bi-hand-thumbs-up me-1"></i>
                    {{ formatNumber(video.likes) }}
                    <i class="bi bi-chat-dots ms-3 me-1"></i>
                    {{ formatNumber(video.comments) }}
                  </small>
                </a>
              </div>
            </div>
            <div class="col-md-6">
              <!-- 주요 키워드 -->
              <h6 class="mb-3">주요 키워드</h6>
              <div class="keywords-cloud mb-4">
                <span 
                  v-for="keyword in keywords" 
                  :key="keyword.text"
                  class="badge"
                  :class="getKeywordClass(keyword.weight)"
                  :style="{ fontSize: getKeywordSize(keyword.weight) }"
                >
                  {{ keyword.text }}
                </span>
              </div>

              <!-- 업로드 패턴 -->
              <h6 class="mb-3">업로드 패턴</h6>
              <div class="upload-pattern">
                <canvas ref="uploadPatternChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 추천 -->
      <div class="ai-recommendations card">
        <div class="card-header">
          <h5 class="card-title mb-0">AI 추천 사항</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4" v-for="(rec, index) in recommendations" :key="index">
              <div class="recommendation-item">
                <div class="icon-wrapper mb-3">
                  <i :class="rec.icon"></i>
                </div>
                <h6>{{ rec.title }}</h6>
                <p class="text-muted">{{ rec.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isAnalyzing" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">채널 데이터를 분석하고 있습니다...</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'YoutubeAnalysis',
  setup() {
    const channelUrl = ref('')
    const channelData = ref(null)
    const isAnalyzing = ref(false)
    const error = ref(null)
    const subscriberChart = ref(null)
    const viewsChart = ref(null)
    const uploadPatternChart = ref(null)

    // 테스트 데이터
    const topVideos = ref([
      {
        id: 'abc123',
        title: '가장 인기있는 영상',
        description: '이 영상은 채널에서 가장 높은 조회수를 기록했습니다.',
        views: 1500000,
        likes: 50000,
        comments: 3000
      },
      // ... 더 많은 비디오 데이터
    ])

    const keywords = ref([
      { text: '프로그래밍', weight: 1.0 },
      { text: '인공지능', weight: 0.8 },
      { text: '데이터 분석', weight: 0.6 },
      // ... 더 많은 키워드
    ])

    const recommendations = ref([
      {
        icon: 'bi bi-graph-up',
        title: '조회수 개선',
        description: '썸네일 최적화와 SEO 개선을 통해 조회수를 높일 수 있습니다.'
      },
      {
        icon: 'bi bi-people',
        title: '시청자 참여',
        description: '댓글 응답률을 높여 시청자 참여도를 개선하세요.'
      },
      {
        icon: 'bi bi-calendar-check',
        title: '업로드 일정',
        description: '화요일과 목요일 저녁에 업로드하면 더 많은 시청자에게 도달할 수 있습니다.'
      }
    ])

    const analyzeChannel = async () => {
      if (!channelUrl.value) {
        error.value = '채널 URL을 입력해주세요.'
        return
      }

      isAnalyzing.value = true
      error.value = null

      try {
        // API 호출 및 데이터 처리
        // const response = await axios.post('/api/v1/youtube/analyze', {
        //   channelUrl: channelUrl.value
        // })
        
        // 테스트 데이터
        channelData.value = {
          thumbnail: 'https://example.com/channel-thumbnail.jpg',
          title: '테스트 채널',
          description: '프로그래밍과 인공지능에 대해 다루는 채널입니다.',
          subscriberCount: 100000,
          videoCount: 200,
          viewCount: 5000000
        }

        // 차트 초기화
        initializeCharts()
      } catch (err) {
        error.value = '채널 분석 중 오류가 발생했습니다. 다시 시도해주세요.'
        console.error('Channel analysis error:', err)
      } finally {
        isAnalyzing.value = false
      }
    }

    const initializeCharts = () => {
      // 구독자 성장 차트
      if (subscriberChart.value) {
        new Chart(subscriberChart.value, {
          type: 'line',
          data: {
            labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
            datasets: [{
              label: '구독자 수',
              data: [80000, 85000, 87000, 90000, 95000, 100000],
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            }]
          }
        })
      }

      // 조회수 차트
      if (viewsChart.value) {
        new Chart(viewsChart.value, {
          type: 'bar',
          data: {
            labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
            datasets: [{
              label: '월간 조회수',
              data: [800000, 850000, 900000, 950000, 1000000, 1100000],
              backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
          }
        })
      }

      // 업로드 패턴 차트
      if (uploadPatternChart.value) {
        new Chart(uploadPatternChart.value, {
          type: 'radar',
          data: {
            labels: ['월', '화', '수', '목', '금', '토', '일'],
            datasets: [{
              label: '업로드 빈도',
              data: [3, 5, 2, 4, 3, 1, 2],
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgb(255, 99, 132)'
            }]
          }
        })
      }
    }

    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }

    const getKeywordClass = (weight) => {
      if (weight >= 0.8) return 'bg-primary'
      if (weight >= 0.6) return 'bg-info'
      return 'bg-secondary'
    }

    const getKeywordSize = (weight) => {
      return (0.8 + weight) + 'rem'
    }

    onMounted(() => {
      // 차트 초기화
    })

    return {
      channelUrl,
      channelData,
      isAnalyzing,
      error,
      subscriberChart,
      viewsChart,
      uploadPatternChart,
      topVideos,
      keywords,
      recommendations,
      analyzeChannel,
      formatNumber,
      getKeywordClass,
      getKeywordSize
    }
  }
}
</script>

<style scoped>
.youtube-analysis {
  padding: 20px;
}

.channel-overview img {
  width: 120px;
  height: 120px;
  object-fit: cover;
}

.stats .stat-item {
  text-align: center;
  padding: 10px 20px;
  border-right: 1px solid #dee2e6;
}

.stats .stat-item:last-child {
  border-right: none;
}

.keywords-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.keywords-cloud .badge {
  padding: 8px 16px;
  margin: 4px;
}

.recommendation-item {
  text-align: center;
  padding: 20px;
}

.recommendation-item .icon-wrapper {
  width: 60px;
  height: 60px;
  margin: 0 auto;
  background-color: #f8f9fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.recommendation-item .icon-wrapper i {
  font-size: 24px;
  color: #0d6efd;
}

.list-group-item:hover {
  transform: translateX(5px);
  transition: transform 0.2s;
}
</style>
