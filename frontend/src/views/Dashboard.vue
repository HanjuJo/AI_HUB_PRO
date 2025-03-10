<template>
  <div class="dashboard">
    <h2 class="mb-4">내 대시보드</h2>
    
    <div class="row">
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">내 AI 도구 조합</h5>
            <p class="card-text">저장된 AI 도구 조합: {{ toolCombinations.length }}개</p>
            <router-link to="/tool-combinations" class="btn btn-primary">도구 조합 관리</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">최근 활동</h5>
            <p class="card-text">최근 7일간 활동: {{ recentActivities.length }}건</p>
            <button class="btn btn-primary" @click="loadActivities">활동 새로고침</button>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">추천 AI 도구</h5>
            <p class="card-text">맞춤형 추천 도구: {{ recommendedTools.length }}개</p>
            <button class="btn btn-primary" @click="loadRecommendations">추천 새로고침</button>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">내 AI 도구 조합</h5>
          </div>
          <div class="card-body">
            <div v-if="toolCombinations.length === 0" class="text-center py-4">
              <p>저장된 AI 도구 조합이 없습니다.</p>
              <router-link to="/tool-combinations" class="btn btn-primary">새 도구 조합 만들기</router-link>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="combo in toolCombinations" :key="combo.id" class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ combo.name }}</h5>
                    <small>{{ formatDate(combo.created_at) }}</small>
                  </div>
                  <p class="mb-1">{{ combo.description }}</p>
                  <div>
                    <span v-for="tool in combo.tools" :key="tool.id" class="badge bg-primary me-1">
                      {{ tool.name }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">최근 활동</h5>
          </div>
          <div class="card-body">
            <div v-if="recentActivities.length === 0" class="text-center py-4">
              <p>최근 활동이 없습니다.</p>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="activity in recentActivities" :key="activity.id" class="list-group-item">
                  <div class="d-flex w-100 justify-content-between">
                    <p class="mb-1">{{ activity.description }}</p>
                    <small>{{ formatDate(activity.timestamp) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">추천 AI 도구</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div v-for="tool in recommendedTools" :key="tool.id" class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">{{ tool.name }}</h5>
                <p class="card-text">{{ tool.description }}</p>
                <div class="mb-2">
                  <span v-for="category in tool.categories" :key="category.id" class="badge bg-secondary me-1">
                    {{ category.name }}
                  </span>
                </div>
                <a :href="tool.url" target="_blank" class="btn btn-sm btn-outline-primary">공식 사이트</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Dashboard',
  setup() {
    const toolCombinations = ref([])
    const recentActivities = ref([])
    const recommendedTools = ref([])

    // 날짜 포맷 함수
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // 도구 조합 로드
    const loadToolCombinations = async () => {
      try {
        // 실제 구현에서는 API에서 데이터를 가져옵니다
        // const response = await axios.get('/api/v1/tool-combinations/me')
        // toolCombinations.value = response.data
        
        // 테스트 데이터
        toolCombinations.value = [
          {
            id: 1,
            name: '유튜브 쇼츠 제작 세트',
            description: '유튜브 쇼츠 제작을 위한 최적의 AI 도구 조합입니다.',
            created_at: '2025-03-01T12:00:00Z',
            tools: [
              { id: 1, name: 'ChatGPT' },
              { id: 2, name: 'Midjourney' },
              { id: 3, name: 'Descript' }
            ]
          },
          {
            id: 2,
            name: '블로그 콘텐츠 제작 세트',
            description: 'SEO에 최적화된 블로그 콘텐츠 제작을 위한 AI 도구 조합입니다.',
            created_at: '2025-02-15T09:30:00Z',
            tools: [
              { id: 1, name: 'ChatGPT' },
              { id: 4, name: 'Grammarly' },
              { id: 5, name: 'Canva' }
            ]
          }
        ]
      } catch (error) {
        console.error('도구 조합을 가져오는 중 오류가 발생했습니다:', error)
      }
    }

    // 최근 활동 로드
    const loadActivities = async () => {
      try {
        // 실제 구현에서는 API에서 데이터를 가져옵니다
        // const response = await axios.get('/api/v1/users/me/activities')
        // recentActivities.value = response.data
        
        // 테스트 데이터
        recentActivities.value = [
          {
            id: 1,
            description: '새 도구 조합 "유튜브 쇼츠 제작 세트"를 생성했습니다.',
            timestamp: '2025-03-01T12:00:00Z'
          },
          {
            id: 2,
            description: 'AI 도구 "Descript"를 즐겨찾기에 추가했습니다.',
            timestamp: '2025-02-28T15:45:00Z'
          },
          {
            id: 3,
            description: '유튜브 데이터 분석을 실행했습니다.',
            timestamp: '2025-02-25T10:20:00Z'
          }
        ]
      } catch (error) {
        console.error('최근 활동을 가져오는 중 오류가 발생했습니다:', error)
      }
    }

    // 추천 AI 도구 로드
    const loadRecommendations = async () => {
      try {
        // 실제 구현에서는 API에서 데이터를 가져옵니다
        // const response = await axios.get('/api/v1/ai-tools/recommendations')
        // recommendedTools.value = response.data
        
        // 테스트 데이터
        recommendedTools.value = [
          {
            id: 1,
            name: 'ChatGPT',
            description: '자연어 처리 AI 모델로 텍스트 생성 및 대화가 가능합니다.',
            url: 'https://chat.openai.com',
            categories: [
              { id: 1, name: '텍스트 생성' },
              { id: 2, name: '콘텐츠 기획' }
            ]
          },
          {
            id: 2,
            name: 'Midjourney',
            description: '텍스트 프롬프트를 기반으로 고품질 이미지를 생성합니다.',
            url: 'https://www.midjourney.com',
            categories: [
              { id: 3, name: '이미지 생성' }
            ]
          },
          {
            id: 3,
            name: 'Descript',
            description: 'AI를 활용한 오디오 및 비디오 편집 도구입니다.',
            url: 'https://www.descript.com',
            categories: [
              { id: 4, name: '오디오 편집' },
              { id: 5, name: '비디오 편집' }
            ]
          }
        ]
      } catch (error) {
        console.error('추천 AI 도구를 가져오는 중 오류가 발생했습니다:', error)
      }
    }

    onMounted(() => {
      loadToolCombinations()
      loadActivities()
      loadRecommendations()
    })

    return {
      toolCombinations,
      recentActivities,
      recommendedTools,
      formatDate,
      loadActivities,
      loadRecommendations
    }
  }
}
</script>
