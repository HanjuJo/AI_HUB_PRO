import { createStore } from 'vuex';

const store = createStore({
  state: {
    user: {
      username: '게스트 사용자',
      role: 'guest',
      isGuest: true,
      created_at: null,
      profile: {
        birthdate: '',
        birthtime: '',
        gender: ''
      },
      preferences: {
        contentType: 'youtube',
        aiTools: ['ChatGPT', 'Midjourney']
      }
    },
    token: null,
    isMenuOpen: false,
    dashboardData: {
      toolCombinations: [],
      recentActivities: [],
      recommendedTools: []
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = {
        ...state.user,
        ...user
      };
      
      if (user && user.token) {
        state.token = user.token;
        localStorage.setItem('token', user.token);
      }
      
      sessionStorage.setItem('userInfo', JSON.stringify(state.user));
    },
    clearUser(state) {
      state.user = {
        username: '게스트 사용자',
        role: 'guest',
        isGuest: true,
        created_at: null,
        profile: {
          birthdate: '',
          birthtime: '',
          gender: ''
        },
        preferences: {
          contentType: 'youtube',
          aiTools: ['ChatGPT', 'Midjourney']
        }
      };
      state.token = null;
      state.dashboardData = {
        toolCombinations: [],
        recentActivities: [],
        recommendedTools: []
      };
      localStorage.removeItem('token');
      sessionStorage.removeItem('userInfo');
      sessionStorage.removeItem('userBirthInfo');
    },
    setMenuState(state, isOpen) {
      state.isMenuOpen = isOpen;
    },
    setDashboardData(state, data) {
      state.dashboardData = data;
    },
    updateUserProfile(state, profileData) {
      state.user.profile = {
        ...state.user.profile,
        ...profileData
      };
      
      sessionStorage.setItem('userInfo', JSON.stringify(state.user));
    }
  },
  actions: {
    login({ commit }, { user }) {
      console.log('로그인 액션 실행:', user);
      
      // 사용자 이름이 없으면 기본값 설정
      if (!user.username || user.username.trim() === '') {
        user.username = '게스트 사용자';
      }
      
      // 사용자 정보 저장
      commit('setUser', user);
      
      // 세션 저장 확인 로그
      console.log('로그인 후 세션 정보:', sessionStorage.getItem('userInfo'));
      console.log('사주 정보:', sessionStorage.getItem('userBirthInfo'));
      
      return true;
    },
    logout({ commit }) {
      console.log('로그아웃 액션 실행');
      commit('clearUser');
    },
    setMenuState({ commit }, isOpen) {
      commit('setMenuState', isOpen);
    },
    updateDashboardData({ commit }, data) {
      commit('setDashboardData', data);
    },
    updateUserProfile({ commit }, profileData) {
      commit('updateUserProfile', profileData);
    },
    initUserSession({ commit }) {
      const userInfo = sessionStorage.getItem('userInfo');
      if (userInfo) {
        commit('setUser', JSON.parse(userInfo));
        return true;
      }
      return false;
    }
  },
  getters: {
    currentUser: state => state.user,
    isAuthenticated: state => !!state.user && state.user.role !== 'guest',
    isLoggedIn: state => !!state.user && !!state.user.username && state.user.username !== '게스트 사용자',
    isMenuOpen: state => state.isMenuOpen,
    dashboardData: state => state.dashboardData,
    token: state => state.token,
    userProfile: state => state.user.profile
  }
});

export default store;
