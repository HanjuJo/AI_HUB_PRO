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
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'YoutubeAnalysis',
  setup() {
    const channelUrl = ref('')
    const isAnalyzing = ref(false)
    const error = ref(null)
    const channelData = ref(null)
    const topVideos = ref([])
    const popularTags = ref([])
    const viewsChart = ref(null)
    const uploadPatternChart = ref(null)
    const videoCharts = ref({})

    const analyzeChannel = async () => {
      if (!channelUrl.value) {
        error.value = '유튜브 채널 URL을 입력해주세요.'
        return
      }
      
      isAnalyzing.value = true
      error.value = null
      channelData.value = null
      topVideos.value = []
      
      try {
        const response = await axios.post('/youtube/analyze', {
          channel_url: channelUrl.value
        })
        
        if (response.data && response.data.channel) {
          // 채널 데이터 설정
          channelData.value = response.data.channel
          
          // 비디오 데이터 설정
          topVideos.value = response.data.videos || []
          
          // 분석 데이터 설정
          if (response.data.analysis) {
            if (response.data.analysis.popularTags) {
              popularTags.value = response.data.analysis.popularTags
            }
            
            if (response.data.analysis.mostViewed) {
              // 가장 많이 본 비디오를 topVideos로 설정
              topVideos.value = response.data.analysis.mostViewed
            }
          }
          
          // 차트 초기화
          await nextTick()
          initializeCharts()
        } else {
          error.value = '채널 데이터를 가져오는데 실패했습니다.'
        }
      } catch (err) {
        console.error('채널 분석 오류:', err)
        error.value = err.response?.data?.detail || '채널 분석 중 오류가 발생했습니다.'
      } finally {
        isAnalyzing.value = false
      }
    }

    const initializeCharts = () => {
      renderViewsChart()
      renderUploadPatternChart()
    }

    const renderViewsChart = () => {
      const ctx = document.getElementById('viewsChart')
      if (!ctx || !topVideos.value || topVideos.value.length === 0) return

      if (videoCharts.value?.viewsChart) {
        videoCharts.value.viewsChart.destroy()
      }

      const chartData = {
        labels: topVideos.value.slice(0, 5).map(video => truncateTitle(video.title)),
          datasets: [{
          label: '조회수',
          data: topVideos.value.slice(0, 5).map(video => video.viewCount),
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      }

      videoCharts.value.viewsChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: '인기 영상 조회수'
            },
            tooltip: {
              callbacks: {
                title: (items) => {
                  const index = items[0].dataIndex
                  return topVideos.value[index].title
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    const renderUploadPatternChart = () => {
      // ... 기존 차트 렌더링 코드 유지 ...
    }

    const truncateTitle = (title, maxLength = 20) => {
      if (!title) return ''
      return title.length > maxLength ? title.substring(0, maxLength) + '...' : title
    }

    const formatNumber = (num) => {
      if (num === undefined || num === null) return '0'
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    return {
      channelUrl,
      isAnalyzing,
      error,
      channelData,
      topVideos,
      popularTags,
      analyzeChannel,
      formatNumber,
      formatDate,
      truncateTitle
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
