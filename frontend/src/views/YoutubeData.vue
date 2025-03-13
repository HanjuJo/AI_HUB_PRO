<template>
  <div class="youtube-data">
    <h2 class="mb-4">유튜브 데이터 분석</h2>
    
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">유튜브 채널 분석</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="analyzeChannel">
              <div class="mb-3">
                <label for="channelUrl" class="form-label">유튜브 채널 URL</label>
                <input
                  type="text"
                  class="form-control"
                  id="channelUrl"
                  v-model="channelUrl"
                  placeholder="https://www.youtube.com/c/채널이름"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary" :disabled="isChannelLoading">
                <span v-if="isChannelLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                채널 분석하기
              </button>
            </form>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">유튜브 동영상 분석</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="analyzeVideo">
              <div class="mb-3">
                <label for="videoUrl" class="form-label">유튜브 동영상 URL</label>
                <input
                  type="text"
                  class="form-control"
                  id="videoUrl"
                  v-model="videoUrl"
                  placeholder="https://www.youtube.com/watch?v=동영상ID"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary" :disabled="isVideoLoading">
                <span v-if="isVideoLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                동영상 분석하기
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 채널 분석 결과 -->
    <div v-if="channelData" class="card mb-4">
      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">채널 분석 결과: {{ channelData.title }}</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-4">
            <img :src="channelData.thumbnail" alt="Channel Thumbnail" class="img-fluid rounded mb-3">
            <div class="mb-3">
              <h6>채널 통계</h6>
              <p><strong>구독자:</strong> {{ formatNumber(channelData.subscribers) }}</p>
              <p><strong>동영상 수:</strong> {{ formatNumber(channelData.videoCount) }}</p>
              <p><strong>총 조회수:</strong> {{ formatNumber(channelData.viewCount) }}</p>
              <p><strong>개설일:</strong> {{ formatDate(channelData.createdAt) }}</p>
            </div>
          </div>
          <div class="col-md-8">
            <h6>채널 소개</h6>
            <p>{{ channelData.description }}</p>
            
            <h6 class="mt-4">인기 동영상</h6>
            <div class="row">
              <div v-for="video in channelData.popularVideos" :key="video.id" class="col-md-6 mb-3">
                <div class="card h-100">
                  <img :src="video.thumbnail" class="card-img-top" :alt="video.title">
                  <div class="card-body">
                    <h6 class="card-title">{{ video.title }}</h6>
                    <p class="card-text small">
                      <strong>조회수:</strong> {{ formatNumber(video.viewCount) }} | 
                      <strong>기간:</strong> {{ video.duration }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 동영상 분석 결과 -->
    <div v-if="videoData" class="card mb-4">
      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">동영상 분석 결과: {{ videoData.title }}</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-4">
            <img :src="videoData.thumbnail" alt="Video Thumbnail" class="img-fluid rounded mb-3">
            <div class="mb-3">
              <h6>동영상 통계</h6>
              <p><strong>조회수:</strong> {{ formatNumber(videoData.viewCount) }}</p>
              <p><strong>좋아요:</strong> {{ formatNumber(videoData.likeCount) }}</p>
              <p><strong>댓글 수:</strong> {{ formatNumber(videoData.commentCount) }}</p>
              <p><strong>기간:</strong> {{ videoData.duration }}</p>
              <p><strong>업로드일:</strong> {{ formatDate(videoData.publishedAt) }}</p>
            </div>
          </div>
          <div class="col-md-8">
            <h6>동영상 설명</h6>
            <p>{{ videoData.description }}</p>
            
            <h6 class="mt-4">동영상 태그</h6>
            <div class="mb-3">
              <span v-for="tag in videoData.tags" :key="tag" class="badge bg-secondary me-1 mb-1">
                {{ tag }}
              </span>
            </div>
            
            <h6 class="mt-4">인기 댓글</h6>
            <div class="list-group">
              <div v-for="comment in videoData.topComments" :key="comment.id" class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mb-1">{{ comment.author }}</h6>
                  <small>{{ formatDate(comment.publishedAt) }}</small>
                </div>
                <p class="mb-1">{{ comment.text }}</p>
                <small><strong>좋아요:</strong> {{ formatNumber(comment.likeCount) }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 추천 전략 -->
    <div v-if="videoData || channelData" class="card">
      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">AI 추천 전략</h5>
      </div>
      <div class="card-body">
        <div class="alert alert-info">
          <p class="mb-0">이 분석 결과를 기반으로 다음과 같은 전략을 추천합니다:</p>
        </div>
        <ul class="list-group">
          <li v-for="(strategy, index) in recommendations" :key="index" class="list-group-item">
            <h6>{{ strategy.title }}</h6>
            <p>{{ strategy.description }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'YoutubeData',
  setup() {
    const channelUrl = ref('')
    const videoUrl = ref('')
    const isChannelLoading = ref(false)
    const isVideoLoading = ref(false)
    const channelData = ref(null)
    const videoData = ref(null)
    const recommendations = ref([])
    
    const formatNumber = (num) => {
      if (!num) return '0'
      return new Intl.NumberFormat('ko-KR').format(num)
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
    
    const analyzeChannel = async () => {
      try {
        isChannelLoading.value = true
        channelData.value = null
        recommendations.value = []
        
        // 실제 구현에서는 API를 호출합니다
        // const response = await axios.post('/api/v1/youtube/analyze-channel', {
        //   url: channelUrl.value
        // })
        // channelData.value = response.data
        
        // 테스트 데이터
        setTimeout(() => {
          channelData.value = {
            id: 'UC1zFJrfEKvCixhsjNSb1toQ',
            title: '예시 채널',
            description: '이 채널은 인공지능, 프로그래밍, 데이터 분석에 관한 콘텐츠를 제공합니다. 최신 AI 동향과 프로그래밍 팁을 공유합니다.',
            thumbnail: 'https://via.placeholder.com/150',
            subscribers: 125000,
            videoCount: 87,
            viewCount: 3500000,
            createdAt: '2020-03-15T00:00:00Z',
            popularVideos: [
              {
                id: 'video1',
                title: '초보자를 위한 파이썬 기초',
                thumbnail: 'https://via.placeholder.com/300x180',
                viewCount: 250000,
                duration: '15:24'
              },
              {
                id: 'video2',
                title: '머신러닝 입문하기',
                thumbnail: 'https://via.placeholder.com/300x180',
                viewCount: 180000,
                duration: '22:15'
              },
              {
                id: 'video3',
                title: '데이터 분석을 위한 판다스 활용법',
                thumbnail: 'https://via.placeholder.com/300x180',
                viewCount: 120000,
                duration: '18:42'
              },
              {
                id: 'video4',
                title: '웹 개발을 위한 JavaScript 필수 기술',
                thumbnail: 'https://via.placeholder.com/300x180',
                viewCount: 95000,
                duration: '25:10'
              }
            ]
          }
          
          generateRecommendations()
        }, 1500)
      } catch (err) {
        console.error('채널 분석 오류:', err)
      } finally {
        isChannelLoading.value = false
      }
    }
    
    const analyzeVideo = async () => {
      try {
        isVideoLoading.value = true
        videoData.value = null
        recommendations.value = []
        
        // 실제 구현에서는 API를 호출합니다
        // const response = await axios.post('/api/v1/youtube/analyze-video', {
        //   url: videoUrl.value
        // })
        // videoData.value = response.data
        
        // 테스트 데이터
        setTimeout(() => {
          videoData.value = {
            id: 'dQw4w9WgXcQ',
            title: '머신러닝 입문 가이드: 초보자를 위한 완벽 튜토리얼',
            description: '이 동영상은 머신러닝의 기본 개념과 실제 활용 예제를 상세히 설명합니다. 초보자도 쉽게 따라할 수 있도록 자세히 설명합니다.',
            thumbnail: 'https://via.placeholder.com/640x360',
            viewCount: 180000,
            likeCount: 15000,
            commentCount: 1200,
            duration: '32:15',
            publishedAt: '2023-05-20T00:00:00Z',
            tags: ['AI', '머신러닝', '파이썬', '데이터사이언스', '튜토리얼'],
            topComments: [
              {
                id: 'comment1',
                author: '데이터러버',
                text: '정말 유용한 동영상입니다! 머신러닝을 처음 접하는 사람에게 완벽한 가이드예요.',
                publishedAt: '2023-05-21T00:00:00Z',
                likeCount: 350
              },
              {
                id: 'comment2',
                author: 'AI연구자',
                text: '설명이 너무 자세해서 좋습니다. 다음 동영상은 딥러닝에 대해 다루어주세요!',
                publishedAt: '2023-05-22T00:00:00Z',
                likeCount: 215
              },
              {
                id: 'comment3',
                author: '코딩마스터',
                text: '예제 코드가 정말 이해하기 쉽게 잘 설명해주셨어요. 다음 시리즈도 기대하겠습니다!',
                publishedAt: '2023-05-23T00:00:00Z',
                likeCount: 180
              }
            ]
          }
          
          generateRecommendations()
        }, 1500)
      } catch (err) {
        console.error('동영상 분석 오류:', err)
      } finally {
        isVideoLoading.value = false
      }
    }
    
    const generateRecommendations = () => {
      // 실제 구현에서는 AI 모델을 통해 추천을 생성합니다
      recommendations.value = [
        {
          title: '콘텐츠 전략',
          description: '인기 동영상의 패턴을 분석한 결과, 보다 길고 자세한 튜토리얼 형태의 콘텐츠가 높은 참여율을 보입니다. 15-30분 길이의 심층적인 튜토리얼을 제작하는 것을 추천합니다.'
        },
        {
          title: '태그 전략',
          description: '현재 사용 중인 태그에 더해 "AI 튜토리얼", "코딩 강좌", "실시간 코딩" 과 같은 검색량이 많은 키워드를 추가하는 것이 좋습니다.'
        },
        {
          title: '썸네일 최적화',
          description: '인기 동영상의 썸네일은 선명한 텍스트와 시각적으로 눈에 띄는 요소를 포함하고 있습니다. 썸네일에 숙련된 사람의 얼굴과 분명한 텍스트를 포함하는 것이 클릭율을 높일 수 있습니다.'
        },
        {
          title: '스케줄 최적화',
          description: '조회수 데이터를 분석한 결과, 화요일과 목요일에 업로드한 동영상의 성과가 가장 좋았습니다. 오후 4시에서 7시 사이에 게시하는 것이 최적의 노출을 얻을 수 있습니다.'
        }
      ]
    }
    
    return {
      channelUrl,
      videoUrl,
      isChannelLoading,
      isVideoLoading,
      channelData,
      videoData,
      recommendations,
      formatNumber,
      formatDate,
      analyzeChannel,
      analyzeVideo
    }
  }
}
</script>

<style scoped>
.youtube-data {
  margin-top: 1rem;
}
</style>
