<template>
  <div class="tool-combinations">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>내 AI 도구 조합</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <i class="bi bi-plus-circle"></i> 새 도구 조합 만들기
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
      <p class="mt-2">도구 조합을 불러오는 중입니다...</p>
    </div>

    <div v-else-if="combinations.length === 0" class="text-center py-5">
      <p class="mb-3">저장된 AI 도구 조합이 없습니다.</p>
      <button class="btn btn-primary" @click="showCreateModal = true">
        첫 번째 도구 조합 만들기
      </button>
    </div>

    <div v-else class="row">
      <div v-for="combo in combinations" :key="combo.id" class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">{{ combo.name }}</h5>
            <div class="dropdown">
              <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="dropdown">
                <i class="bi bi-three-dots-vertical"></i>
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><button class="dropdown-item" @click="editCombination(combo)">편집</button></li>
                <li><button class="dropdown-item" @click="duplicateCombination(combo)">복제</button></li>
                <li><hr class="dropdown-divider"></li>
                <li><button class="dropdown-item text-danger" @click="confirmDelete(combo)">삭제</button></li>
              </ul>
            </div>
          </div>
          <div class="card-body">
            <p class="card-text">{{ combo.description }}</p>
            <h6 class="mt-3 mb-2">포함된 AI 도구:</h6>
            <div class="mb-3">
              <span v-for="tool in combo.tools" :key="tool.id" class="badge bg-primary me-1 mb-1">
                {{ tool.name }}
              </span>
              <span v-if="combo.tools.length === 0" class="text-muted">
                포함된 도구가 없습니다.
              </span>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <div class="d-flex justify-content-between">
              <small class="text-muted">생성일: {{ formatDate(combo.created_at) }}</small>
              <button class="btn btn-sm btn-outline-primary" @click="editCombination(combo)">
                도구 관리
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 새 도구 조합 생성 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showCreateModal }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editMode ? '도구 조합 편집' : '새 도구 조합 만들기' }}</h5>
            <button type="button" class="btn-close" @click="closeCreateModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveCombination">
              <div class="mb-3">
                <label for="combinationName" class="form-label">도구 조합 이름</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="combinationName"
                  v-model="formData.name" 
                  required
                  placeholder="도구 조합 이름을 입력하세요"
                >
              </div>
              <div class="mb-3">
                <label for="combinationDesc" class="form-label">설명</label>
                <textarea 
                  class="form-control" 
                  id="combinationDesc"
                  v-model="formData.description" 
                  rows="3"
                  placeholder="도구 조합에 대한 설명을 입력하세요"
                ></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">AI 도구 선택</label>
                <div class="card">
                  <div class="card-body p-2">
                    <div class="mb-2">
                      <input 
                        type="text" 
                        class="form-control form-control-sm" 
                        placeholder="도구 검색..." 
                        v-model="toolSearchQuery"
                      >
                    </div>
                    <div class="tool-selection-list">
                      <div 
                        v-for="tool in filteredTools" 
                        :key="tool.id" 
                        class="form-check"
                      >
                        <input 
                          class="form-check-input" 
                          type="checkbox" 
                          :id="'tool-' + tool.id"
                          :value="tool.id"
                          v-model="formData.selectedTools"
                        >
                        <label class="form-check-label" :for="'tool-' + tool.id">
                          {{ tool.name }}
                          <small class="text-muted d-block">{{ tool.description }}</small>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeCreateModal">취소</button>
            <button type="button" class="btn btn-primary" @click="saveCombination">
              {{ editMode ? '저장' : '생성' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ 'show': showCreateModal }" v-if="showCreateModal"></div>

    <!-- 삭제 확인 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showDeleteModal }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">도구 조합 삭제</h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            <p>정말 <strong>{{ combinationToDelete?.name }}</strong> 도구 조합을 삭제하시겠습니까?</p>
            <p class="text-danger">이 작업은 되돌릴 수 없습니다.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">취소</button>
            <button type="button" class="btn btn-danger" @click="deleteCombination">삭제</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ 'show': showDeleteModal }" v-if="showDeleteModal"></div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ToolCombinations',
  setup() {
    const combinations = ref([])
    const availableTools = ref([])
    const isLoading = ref(true)
    const showCreateModal = ref(false)
    const showDeleteModal = ref(false)
    const editMode = ref(false)
    const combinationToDelete = ref(null)
    const toolSearchQuery = ref('')
    
    const formData = ref({
      id: null,
      name: '',
      description: '',
      selectedTools: []
    })

    // 필터링된 도구 목록
    const filteredTools = computed(() => {
      if (!toolSearchQuery.value) {
        return availableTools.value
      }
      
      const query = toolSearchQuery.value.toLowerCase()
      return availableTools.value.filter(tool => 
        tool.name.toLowerCase().includes(query) || 
        tool.description.toLowerCase().includes(query)
      )
    })

    // 날짜 포맷 함수
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // 도구 조합 목록 로드
    const loadCombinations = async () => {
      try {
        isLoading.value = true
        // 실제 구현에서는 API에서 데이터를 가져옵니다
        // const response = await axios.get('/api/v1/tool-combinations/me')
        // combinations.value = response.data
        
        // 테스트 데이터
        combinations.value = [
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
      } finally {
        isLoading.value = false
      }
    }

    // 사용 가능한 AI 도구 목록 로드
    const loadTools = async () => {
      try {
        // 실제 구현에서는 API에서 데이터를 가져옵니다
        // const response = await axios.get('/api/v1/ai-tools/')
        // availableTools.value = response.data
        
        // 테스트 데이터
        availableTools.value = [
          {
            id: 1,
            name: 'ChatGPT',
            description: '자연어 처리 AI 모델로 텍스트 생성 및 대화가 가능합니다.'
          },
          {
            id: 2,
            name: 'Midjourney',
            description: '텍스트 프롬프트를 기반으로 고품질 이미지를 생성합니다.'
          },
          {
            id: 3,
            name: 'Descript',
            description: 'AI를 활용한 오디오 및 비디오 편집 도구입니다.'
          },
          {
            id: 4,
            name: 'Grammarly',
            description: 'AI 기반 문법 및 맞춤법 검사 도구입니다.'
          },
          {
            id: 5,
            name: 'Canva',
            description: 'AI 기능이 포함된 그래픽 디자인 플랫폼입니다.'
          },
          {
            id: 6,
            name: 'Runway',
            description: 'AI 기반 비디오 편집 및 생성 도구입니다.'
          }
        ]
      } catch (error) {
        console.error('AI 도구를 가져오는 중 오류가 발생했습니다:', error)
      }
    }

    // 모달 닫기
    const closeCreateModal = () => {
      showCreateModal.value = false
      editMode.value = false
      formData.value = {
        id: null,
        name: '',
        description: '',
        selectedTools: []
      }
      toolSearchQuery.value = ''
    }

    // 도구 조합 편집 모달 열기
    const editCombination = (combo) => {
      editMode.value = true
      formData.value = {
        id: combo.id,
        name: combo.name,
        description: combo.description,
        selectedTools: combo.tools.map(tool => tool.id)
      }
      showCreateModal.value = true
    }

    // 도구 조합 복제
    const duplicateCombination = (combo) => {
      editMode.value = false
      formData.value = {
        id: null,
        name: `${combo.name} (복사본)`,
        description: combo.description,
        selectedTools: combo.tools.map(tool => tool.id)
      }
      showCreateModal.value = true
    }

    // 도구 조합 저장 (생성 또는 업데이트)
    const saveCombination = async () => {
      try {
        if (!formData.value.name) {
          alert('도구 조합 이름을 입력해주세요.')
          return
        }

        if (editMode.value) {
          // 기존 도구 조합 업데이트
          // 실제 구현에서는 API 호출
          // await axios.put(`/api/v1/tool-combinations/${formData.value.id}`, {
          //   name: formData.value.name,
          //   description: formData.value.description,
          //   tools: formData.value.selectedTools
          // })
          
          // 테스트 데이터 업데이트
          const index = combinations.value.findIndex(c => c.id === formData.value.id)
          if (index !== -1) {
            const selectedTools = formData.value.selectedTools.map(toolId => {
              const tool = availableTools.value.find(t => t.id === toolId)
              return { id: tool.id, name: tool.name }
            })
            
            combinations.value[index] = {
              ...combinations.value[index],
              name: formData.value.name,
              description: formData.value.description,
              tools: selectedTools
            }
          }
        } else {
          // 새 도구 조합 생성
          // 실제 구현에서는 API 호출
          // const response = await axios.post('/api/v1/tool-combinations/', {
          //   name: formData.value.name,
          //   description: formData.value.description,
          //   tools: formData.value.selectedTools
          // })
          
          // 테스트 데이터 업데이트
          const newId = Math.max(...combinations.value.map(c => c.id), 0) + 1
          const selectedTools = formData.value.selectedTools.map(toolId => {
            const tool = availableTools.value.find(t => t.id === toolId)
            return { id: tool.id, name: tool.name }
          })
          
          combinations.value.push({
            id: newId,
            name: formData.value.name,
            description: formData.value.description,
            created_at: new Date().toISOString(),
            tools: selectedTools
          })
        }
        
        closeCreateModal()
      } catch (error) {
        console.error('도구 조합 저장 중 오류가 발생했습니다:', error)
      }
    }

    // 삭제 확인 모달 열기
    const confirmDelete = (combo) => {
      combinationToDelete.value = combo
      showDeleteModal.value = true
    }

    // 도구 조합 삭제
    const deleteCombination = async () => {
      try {
        if (!combinationToDelete.value) return
        
        // 실제 구현에서는 API 호출
        // await axios.delete(`/api/v1/tool-combinations/${combinationToDelete.value.id}`)
        
        // 테스트 데이터 업데이트
        combinations.value = combinations.value.filter(c => c.id !== combinationToDelete.value.id)
        
        showDeleteModal.value = false
        combinationToDelete.value = null
      } catch (error) {
        console.error('도구 조합 삭제 중 오류가 발생했습니다:', error)
      }
    }

    onMounted(() => {
      loadCombinations()
      loadTools()
    })

    return {
      combinations,
      availableTools,
      isLoading,
      showCreateModal,
      showDeleteModal,
      editMode,
      combinationToDelete,
      formData,
      toolSearchQuery,
      filteredTools,
      formatDate,
      closeCreateModal,
      editCombination,
      duplicateCombination,
      saveCombination,
      confirmDelete,
      deleteCombination
    }
  }
}
</script>

<style scoped>
.tool-selection-list {
  max-height: 200px;
  overflow-y: auto;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: #000;
}

.modal-backdrop.fade {
  opacity: 0;
}

.modal-backdrop.show {
  opacity: 0.5;
}

.modal.fade {
  z-index: 1050;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal.show {
  display: block;
}
</style>
