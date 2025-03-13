<template>
  <div class="profile-page">
    <h2 class="mb-4">내 프로필</h2>
    
    <div class="row">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">프로필 정보</h5>
          </div>
          <div class="card-body">
            <div v-if="message" class="alert" :class="messageType" role="alert">
              {{ message }}
            </div>
            
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label for="username" class="form-label">사용자 이름</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="profile.username"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="email" class="form-label">이메일</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="profile.email"
                  required
                  disabled
                />
                <div class="form-text">이메일은 변경할 수 없습니다.</div>
              </div>
              
              <div class="mb-3">
                <label for="bio" class="form-label">자기소개</label>
                <textarea
                  class="form-control"
                  id="bio"
                  v-model="profile.bio"
                  rows="3"
                ></textarea>
              </div>
              
              <button type="submit" class="btn btn-primary" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                프로필 업데이트
              </button>
            </form>
          </div>
        </div>
        
        <div class="card mt-4">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">비밀번호 변경</h5>
          </div>
          <div class="card-body">
            <div v-if="passwordMessage" class="alert" :class="passwordMessageType" role="alert">
              {{ passwordMessage }}
            </div>
            
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label for="currentPassword" class="form-label">현재 비밀번호</label>
                <input
                  type="password"
                  class="form-control"
                  id="currentPassword"
                  v-model="passwordData.currentPassword"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="newPassword" class="form-label">새 비밀번호</label>
                <input
                  type="password"
                  class="form-control"
                  id="newPassword"
                  v-model="passwordData.newPassword"
                  required
                />
                <div class="form-text">비밀번호는 최소 8자 이상이어야 합니다.</div>
              </div>
              
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">비밀번호 확인</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="passwordData.confirmPassword"
                  required
                />
              </div>
              
              <button type="submit" class="btn btn-primary" :disabled="isPasswordLoading || !isPasswordValid">
                <span v-if="isPasswordLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                비밀번호 변경
              </button>
            </form>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">계정 정보</h5>
          </div>
          <div class="card-body">
            <p><strong>가입일:</strong> {{ formatDate(profile.created_at) }}</p>
            <p><strong>마지막 로그인:</strong> {{ formatDate(profile.last_login) }}</p>
            <p><strong>계정 상태:</strong> <span class="badge bg-success">활성</span></p>
            
            <hr>
            
            <h6>통계</h6>
            <p><strong>저장된 도구 조합:</strong> {{ stats.toolCombinations }}</p>
            <p><strong>분석한 유튜브 영상:</strong> {{ stats.analyzedVideos }}</p>
            <p><strong>생성한 콘텐츠:</strong> {{ stats.createdContents }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Profile',
  setup() {
    const profile = ref({
      username: '',
      email: '',
      bio: '',
      created_at: '',
      last_login: ''
    })
    
    const passwordData = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
    
    const stats = ref({
      toolCombinations: 0,
      analyzedVideos: 0,
      createdContents: 0
    })
    
    const isLoading = ref(false)
    const isPasswordLoading = ref(false)
    const message = ref('')
    const messageType = ref('alert-info')
    const passwordMessage = ref('')
    const passwordMessageType = ref('alert-info')
    
    const isPasswordValid = computed(() => {
      return (
        passwordData.value.newPassword.length >= 8 &&
        passwordData.value.newPassword === passwordData.value.confirmPassword
      )
    })
    
    const formatDate = (dateString) => {
      if (!dateString) return '정보 없음'
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const loadProfile = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return
        
        const response = await axios.get('/api/v1/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        profile.value = {
          ...response.data,
          bio: response.data.bio || ''
        }
        
        // 통계 데이터 로드 (실제 구현에서는 API에서 가져옵니다)
        stats.value = {
          toolCombinations: 2,
          analyzedVideos: 5,
          createdContents: 10
        }
      } catch (err) {
        console.error('프로필 로드 오류:', err)
        message.value = '프로필 정보를 불러오는 중 오류가 발생했습니다.'
        messageType.value = 'alert-danger'
      }
    }
    
    const updateProfile = async () => {
      try {
        isLoading.value = true
        message.value = ''
        
        const token = localStorage.getItem('token')
        if (!token) return
        
        const response = await axios.put('/api/v1/users/me', {
          username: profile.value.username,
          bio: profile.value.bio
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        // 로컬 스토리지의 사용자 정보 업데이트
        const userData = JSON.parse(localStorage.getItem('user') || '{}')
        userData.username = profile.value.username
        localStorage.setItem('user', JSON.stringify(userData))
        
        message.value = '프로필이 성공적으로 업데이트되었습니다.'
        messageType.value = 'alert-success'
      } catch (err) {
        console.error('프로필 업데이트 오류:', err)
        message.value = '프로필 업데이트 중 오류가 발생했습니다.'
        messageType.value = 'alert-danger'
      } finally {
        isLoading.value = false
      }
    }
    
    const changePassword = async () => {
      if (!isPasswordValid.value) {
        passwordMessage.value = '비밀번호가 일치하지 않거나 8자 미만입니다.'
        passwordMessageType.value = 'alert-danger'
        return
      }
      
      try {
        isPasswordLoading.value = true
        passwordMessage.value = ''
        
        const token = localStorage.getItem('token')
        if (!token) return
        
        await axios.put('/api/v1/users/me', {
          password: passwordData.value.newPassword
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        passwordData.value = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        
        passwordMessage.value = '비밀번호가 성공적으로 변경되었습니다.'
        passwordMessageType.value = 'alert-success'
      } catch (err) {
        console.error('비밀번호 변경 오류:', err)
        passwordMessage.value = '비밀번호 변경 중 오류가 발생했습니다.'
        passwordMessageType.value = 'alert-danger'
      } finally {
        isPasswordLoading.value = false
      }
    }
    
    onMounted(() => {
      loadProfile()
    })
    
    return {
      profile,
      passwordData,
      stats,
      isLoading,
      isPasswordLoading,
      message,
      messageType,
      passwordMessage,
      passwordMessageType,
      isPasswordValid,
      formatDate,
      updateProfile,
      changePassword
    }
  }
}
</script>

<style scoped>
.profile-page {
  margin-top: 1rem;
}
</style>
