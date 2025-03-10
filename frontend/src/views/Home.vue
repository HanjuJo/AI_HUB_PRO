<template>
  <div class="home">
    <div class="jumbotron bg-light p-5 rounded mb-4">
      <h1 class="display-4">AI 콘텐츠 제작 지원 플랫폼</h1>
      <p class="lead">
        최신 AI 도구를 활용하여 콘텐츠 제작 효율을 높이고, 유튜브 데이터 분석을 통해 
        성공적인 콘텐츠 전략을 수립하세요.
      </p>
      <hr class="my-4">
      <p>
        회원가입하고 맞춤형 AI 도구 추천과 개인화된 대시보드를 이용해보세요.
      </p>
      <router-link to="/register" class="btn btn-primary btn-lg">시작하기</router-link>
    </div>

    <div class="row mb-5">
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">AI 도구 추천</h5>
            <p class="card-text">
              콘텐츠 유형에 맞는 최적의 AI 도구 조합을 추천받고 효율적으로 콘텐츠를 제작하세요.
            </p>
            <router-link to="/ai-tools" class="btn btn-outline-primary">AI 도구 보기</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">유튜브 데이터 분석</h5>
            <p class="card-text">
              인기 검색어와 트렌드를 분석하여 효과적인 콘텐츠 전략을 수립하세요.
            </p>
            <router-link to="/youtube-data" class="btn btn-outline-primary">데이터 분석하기</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">개인화된 대시보드</h5>
            <p class="card-text">
              나만의 AI 도구 조합을 저장하고 관리할 수 있는 개인화된 대시보드를 이용하세요.
            </p>
            <router-link to="/dashboard" class="btn btn-outline-primary">대시보드 보기</router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <h3>최신 AI 도구</h3>
        <ul class="list-group mb-4">
          <li class="list-group-item" v-for="tool in latestTools" :key="tool.id">
            <h5>{{ tool.name }}</h5>
            <p class="mb-1">{{ tool.description }}</p>
            <a :href="tool.url" target="_blank" class="btn btn-sm btn-primary">공식 사이트</a>
          </li>
        </ul>
      </div>
      <div class="col-md-6">
        <h3>인기 검색어</h3>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center" 
              v-for="keyword in trendingKeywords" :key="keyword.id">
            {{ keyword.keyword }}
            <span class="badge bg-primary rounded-pill">{{ keyword.search_volume }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Home',
  setup() {
    const latestTools = ref([
      { 
        id: 1, 
        name: 'ChatGPT', 
        description: '자연어 처리 AI 모델로 텍스트 생성 및 대화가 가능합니다.',
        url: 'https://chat.openai.com'
      },
      { 
        id: 2, 
        name: 'Midjourney', 
        description: '텍스트 프롬프트를 기반으로 고품질 이미지를 생성합니다.',
        url: 'https://www.midjourney.com'
      },
      { 
        id: 3, 
        name: 'Descript', 
        description: 'AI를 활용한 오디오 및 비디오 편집 도구입니다.',
        url: 'https://www.descript.com'
      }
    ])

    const trendingKeywords = ref([
      { id: 1, keyword: 'AI 콘텐츠 제작', search_volume: 15000 },
      { id: 2, keyword: '쇼츠 편집 방법', search_volume: 12500 },
      { id: 3, keyword: '유튜브 수익화', search_volume: 10000 },
      { id: 4, keyword: '미드저니 프롬프트', search_volume: 8500 },
      { id: 5, keyword: '챗GPT 활용법', search_volume: 7800 }
    ])

    onMounted(async () => {
      try {
        // 실제 구현에서는 API에서 데이터를 가져옵니다
        // const toolsResponse = await axios.get('/api/v1/ai-tools?limit=3')
        // latestTools.value = toolsResponse.data
        
        // const keywordsResponse = await axios.get('/api/v1/youtube/trending?limit=5')
        // trendingKeywords.value = keywordsResponse.data
      } catch (error) {
        console.error('데이터를 가져오는 중 오류가 발생했습니다:', error)
      }
    })

    return {
      latestTools,
      trendingKeywords
    }
  }
}
</script>
