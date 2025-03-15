import { createStore } from 'vuex';

const store = createStore({
  state: {
    user: {
      username: '게스트 사용자',
      role: 'guest',
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
      state.user = user;
      if (user && user.token) {
        state.token = user.token;
        localStorage.setItem('token', user.token);
      }
    },
    clearUser(state) {
      state.user = {
        username: '게스트 사용자',
        role: 'guest',
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
      sessionStorage.removeItem('guestName');
    },
    setMenuState(state, isOpen) {
      state.isMenuOpen = isOpen;
    },
    setDashboardData(state, data) {
      state.dashboardData = data;
    }
  },
  actions: {
    login({ commit }, { user }) {
      commit('setUser', user);
    },
    logout({ commit }) {
      commit('clearUser');
      router.push('/');
    },
    setMenuState({ commit }, isOpen) {
      commit('setMenuState', isOpen);
    },
    updateDashboardData({ commit }, data) {
      commit('setDashboardData', data);
    }
  },
  getters: {
    currentUser: state => state.user,
    isAuthenticated: state => !!state.user && state.user.role !== 'guest',
    isMenuOpen: state => state.isMenuOpen,
    dashboardData: state => state.dashboardData,
    token: state => state.token
  }
});

export default store;
