<template>
  <div class="app-container">
    <Navbar />
    <main class="main-content">
      <div class="container py-4">
        <router-view />
      </div>
    </main>
    <footer class="footer py-3 bg-light">
      <div class="container text-center">
        <span class="text-muted">© 2025 AI HUB. All rights reserved.</span>
      </div>
    </footer>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import Navbar from './components/Navbar.vue'

export default defineComponent({
  name: 'App',
  components: {
    Navbar
  }
})
</script>

<style>
/* 기본 스타일 초기화 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f8f9fa;
  color: #343a40;
  line-height: 1.6;
}

/* 레이아웃 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px 0;
}

/* 푸터 */
.footer {
  margin-top: auto;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

/* 드롭다운 메뉴 */
.dropdown-item {
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  transform: translateX(5px);
  background-color: #e9ecef;
}

.dropdown-item.text-danger:hover {
  background-color: #dc3545;
  color: white;
}

.dropdown-divider {
  border-top: 1px solid #e9ecef;
  margin: 0.5rem 0;
}

/* 유틸리티 클래스 */
.text-muted {
  color: #6c757d !important;
}

.bg-light {
  background-color: #f8f9fa !important;
}
</style>
