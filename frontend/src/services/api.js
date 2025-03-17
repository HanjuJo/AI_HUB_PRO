import axios from 'axios';

// API 기본 설정
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

// 요청 인터셉터 설정
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 설정
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        // 인증 오류 처리
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

/**
 * 유튜브 API 서비스
 */
export const youtubeApi = {
  /**
   * 유튜브 채널 분석
   * @param {string} channelUrl - 분석할 채널 URL
   * @returns {Promise} 분석 결과 데이터
   */
  analyzeChannel(channelUrl) {
    return apiClient.post('/youtube/analyze', { channel_url: channelUrl });
  },

  /**
   * 인기 유튜브 키워드 조회
   * @param {number} skip - 건너뛸 항목 수
   * @param {number} limit - 가져올 항목 수
   * @returns {Promise} 인기 키워드 목록
   */
  getTrendingKeywords(skip = 0, limit = 20) {
    return apiClient.get(`/youtube/trending?skip=${skip}&limit=${limit}`);
  },

  /**
   * 채널 추천 조회
   * @param {string} channelId - 채널 ID
   * @param {number} maxResults - 최대 결과 수
   * @returns {Promise} 추천 채널 목록
   */
  getChannelRecommendations(channelId, maxResults = 10) {
    return apiClient.get(`/youtube/recommendations?channel_id=${channelId}&max_results=${maxResults}`);
  }
};

/**
 * AI 도구 API 서비스
 */
export const aiToolsApi = {
  /**
   * AI 도구 목록 조회
   * @param {number} skip - 건너뛸 항목 수
   * @param {number} limit - 가져올 항목 수
   * @returns {Promise} AI 도구 목록
   */
  getTools(skip = 0, limit = 100) {
    return apiClient.get(`/ai-tools?skip=${skip}&limit=${limit}`);
  },

  /**
   * AI 도구 상세 조회
   * @param {number} id - 도구 ID
   * @returns {Promise} AI 도구 상세 정보
   */
  getTool(id) {
    return apiClient.get(`/ai-tools/${id}`);
  },

  /**
   * AI 도구 생성
   * @param {Object} toolData - 도구 생성 데이터
   * @returns {Promise} 생성된 도구 정보
   */
  createTool(toolData) {
    return apiClient.post('/ai-tools', toolData);
  },

  /**
   * AI 도구 수정
   * @param {number} id - 도구 ID
   * @param {Object} toolData - 수정할 도구 데이터
   * @returns {Promise} 수정된 도구 정보
   */
  updateTool(id, toolData) {
    return apiClient.put(`/ai-tools/${id}`, toolData);
  },

  /**
   * AI 도구 삭제
   * @param {number} id - 삭제할 도구 ID
   * @returns {Promise} 삭제 결과
   */
  deleteTool(id) {
    return apiClient.delete(`/ai-tools/${id}`);
  },

  /**
   * 카테고리 목록 조회
   * @param {number} skip - 건너뛸 항목 수
   * @param {number} limit - 가져올 항목 수
   * @returns {Promise} 카테고리 목록
   */
  getCategories(skip = 0, limit = 100) {
    return apiClient.get(`/ai-tools/categories?skip=${skip}&limit=${limit}`);
  }
};

/**
 * 도구 조합 API 서비스
 */
export const toolCombinationsApi = {
  /**
   * 도구 조합 목록 조회
   * @param {number} skip - 건너뛸 항목 수
   * @param {number} limit - 가져올 항목 수
   * @returns {Promise} 도구 조합 목록
   */
  getCombinations(skip = 0, limit = 100) {
    return apiClient.get(`/tool-combinations?skip=${skip}&limit=${limit}`);
  },

  /**
   * 도구 조합 상세 조회
   * @param {number} id - 도구 조합 ID
   * @returns {Promise} 도구 조합 상세 정보
   */
  getCombination(id) {
    return apiClient.get(`/tool-combinations/${id}`);
  },

  /**
   * 도구 조합 생성
   * @param {Object} combinationData - 도구 조합 생성 데이터
   * @returns {Promise} 생성된 도구 조합 정보
   */
  createCombination(combinationData) {
    return apiClient.post('/tool-combinations', combinationData);
  },

  /**
   * 도구 조합 수정
   * @param {number} id - 도구 조합 ID
   * @param {Object} combinationData - 수정할 도구 조합 데이터
   * @returns {Promise} 수정된 도구 조합 정보
   */
  updateCombination(id, combinationData) {
    return apiClient.put(`/tool-combinations/${id}`, combinationData);
  },

  /**
   * 도구 조합 삭제
   * @param {number} id - 삭제할 도구 조합 ID
   * @returns {Promise} 삭제 결과
   */
  deleteCombination(id) {
    return apiClient.delete(`/tool-combinations/${id}`);
  }
};

export default {
  youtubeApi,
  aiToolsApi,
  toolCombinationsApi
}; 