import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8004';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 설정
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 설정
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  login: (credentials) => api.post('/auth/login/access-token', credentials, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: (token) => api.get('/users/me', {
    headers: { Authorization: `Bearer ${token}` }
  }),
};

export const content = {
  create: (data) => api.post('/content', data),
  getAll: () => api.get('/content'),
  getById: (id) => api.get(`/content/${id}`),
  update: (id, data) => api.put(`/content/${id}`, data),
  delete: (id) => api.delete(`/content/${id}`),
  analyze: (data) => api.post('/content/analyze', data),
};

export const aiTools = {
  getAll: () => api.get('/ai-tools'),
  getById: (id) => api.get(`/ai-tools/${id}`),
  getRecommendations: () => api.get('/ai-tools/recommendations'),
};

export const toolCombinations = {
  getAll: () => api.get('/tool-combinations'),
  getById: (id) => api.get(`/tool-combinations/${id}`),
  create: (data) => api.post('/tool-combinations', data),
};

export const youtubeData = {
  analyze: (data) => api.post('/youtube-data/analyze', data),
  getHistory: () => api.get('/youtube-data/history'),
};

export const user = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data) => api.put('/users/me', data),
};

export default api;
