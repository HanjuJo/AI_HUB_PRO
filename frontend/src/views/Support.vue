<template>
  <div class="support">
    <div class="support-header mb-4">
      <h1 class="display-5 mb-3">고객 지원 센터</h1>
      <p class="lead text-muted">AI 도구 사용과 관련된 모든 문의사항을 해결해드립니다.</p>
    </div>

    <!-- FAQ 섹션 -->
    <div class="faq-section card mb-4">
      <div class="card-header bg-white">
        <h2 class="h5 mb-0">자주 묻는 질문</h2>
      </div>
      <div class="card-body">
        <div class="accordion" id="faqAccordion">
          <div class="accordion-item" v-for="(faq, index) in faqs" :key="index">
            <h3 class="accordion-header">
              <button 
                class="accordion-button" 
                :class="{ collapsed: !faq.isOpen }"
                type="button" 
                @click="toggleFaq(index)"
              >
                {{ faq.question }}
              </button>
            </h3>
            <div 
              class="accordion-collapse collapse" 
              :class="{ show: faq.isOpen }"
            >
              <div class="accordion-body">
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 문의하기 폼 -->
    <div class="inquiry-form card">
      <div class="card-header bg-white">
        <h2 class="h5 mb-0">문의하기</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitInquiry">
          <!-- 문의 유형 -->
          <div class="mb-3">
            <label class="form-label">문의 유형</label>
            <div class="btn-group w-100">
              <button
                v-for="type in inquiryTypes"
                :key="type.value"
                type="button"
                class="btn"
                :class="selectedType === type.value ? 'btn-primary' : 'btn-outline-primary'"
                @click="selectedType = type.value"
              >
                <i :class="type.icon"></i>
                {{ type.label }}
              </button>
            </div>
          </div>

          <!-- 제목 -->
          <div class="mb-3">
            <label for="inquiryTitle" class="form-label">제목</label>
            <input
              type="text"
              class="form-control"
              id="inquiryTitle"
              v-model="inquiryTitle"
              placeholder="문의 제목을 입력하세요"
              required
            >
          </div>

          <!-- 내용 -->
          <div class="mb-3">
            <label for="inquiryContent" class="form-label">내용</label>
            <textarea
              class="form-control"
              id="inquiryContent"
              v-model="inquiryContent"
              rows="5"
              placeholder="자세한 내용을 입력하세요"
              required
            ></textarea>
          </div>

          <!-- 첨부파일 -->
          <div class="mb-3">
            <label for="attachments" class="form-label">첨부파일 (선택사항)</label>
            <input
              type="file"
              class="form-control"
              id="attachments"
              multiple
              @change="handleFileUpload"
            >
            <div class="form-text">최대 5개 파일, 각 파일 10MB 이하</div>
          </div>

          <!-- 선택된 파일 목록 -->
          <div v-if="selectedFiles.length > 0" class="mb-3">
            <div class="selected-files">
              <div 
                v-for="(file, index) in selectedFiles" 
                :key="index"
                class="selected-file d-flex align-items-center p-2 border rounded mb-2"
              >
                <i class="bi bi-file-earmark me-2"></i>
                <span class="flex-grow-1">{{ file.name }}</span>
                <button 
                  type="button" 
                  class="btn btn-sm btn-outline-danger"
                  @click="removeFile(index)"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- 알림 설정 -->
          <div class="mb-4">
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="emailNotification"
                v-model="emailNotification"
              >
              <label class="form-check-label" for="emailNotification">
                답변 시 이메일로 알림 받기
              </label>
            </div>
          </div>

          <!-- 제출 버튼 -->
          <div class="d-grid">
            <button 
              type="submit" 
              class="btn btn-primary btn-lg"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting">
                <span class="spinner-border spinner-border-sm me-2"></span>
                제출 중...
              </span>
              <span v-else>
                <i class="bi bi-send me-2"></i>
                문의하기
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 성공 알림 모달 -->
    <div 
      class="modal fade" 
      :class="{ show: showSuccessModal }" 
      tabindex="-1"
      v-if="showSuccessModal"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">문의가 접수되었습니다</h5>
            <button 
              type="button" 
              class="btn-close"
              @click="showSuccessModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <div class="text-center mb-4">
              <i class="bi bi-check-circle text-success" style="font-size: 3rem;"></i>
              <p class="mt-3">문의하신 내용이 성공적으로 접수되었습니다.</p>
              <p class="text-muted">문의번호: {{ lastInquiryId }}</p>
            </div>
            <p>답변이 등록되면 알려드리겠습니다.</p>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-primary"
              @click="showSuccessModal = false"
            >
              확인
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Support',
  setup() {
    // FAQ 데이터
    const faqs = ref([
      {
        question: 'AI 도구 추천은 어떤 기준으로 이루어지나요?',
        answer: '사용자의 콘텐츠 유형, 목적, 예산 등을 고려하여 최적의 AI 도구를 추천해드립니다.',
        isOpen: false
      },
      {
        question: '유튜브 채널 분석은 어떤 데이터를 제공하나요?',
        answer: '구독자 성장률, 조회수 추이, 인기 영상 분석, 시청자 참여도 등 다양한 지표를 제공합니다.',
        isOpen: false
      },
      {
        question: '도구 조합 기능은 무엇인가요?',
        answer: '여러 AI 도구를 효과적으로 조합하여 콘텐츠 제작 워크플로우를 최적화할 수 있는 기능입니다.',
        isOpen: false
      },
      {
        question: '결제는 어떤 방식으로 이루어지나요?',
        answer: '신용카드, 계좌이체, 페이팔 등 다양한 결제 수단을 지원합니다.',
        isOpen: false
      }
    ])

    // 문의 유형
    const inquiryTypes = [
      { value: 'technical', label: '기술 문의', icon: 'bi bi-gear' },
      { value: 'billing', label: '결제 문의', icon: 'bi bi-credit-card' },
      { value: 'feature', label: '기능 제안', icon: 'bi bi-lightbulb' },
      { value: 'other', label: '기타', icon: 'bi bi-question-circle' }
    ]

    // 폼 데이터
    const selectedType = ref('')
    const inquiryTitle = ref('')
    const inquiryContent = ref('')
    const selectedFiles = ref([])
    const emailNotification = ref(true)
    const isSubmitting = ref(false)
    const showSuccessModal = ref(false)
    const lastInquiryId = ref('')

    // FAQ 토글
    const toggleFaq = (index) => {
      faqs.value[index].isOpen = !faqs.value[index].isOpen
    }

    // 파일 업로드 처리
    const handleFileUpload = (event) => {
      const files = Array.from(event.target.files)
      if (selectedFiles.value.length + files.length > 5) {
        alert('최대 5개의 파일만 첨부할 수 있습니다.')
        return
      }

      files.forEach(file => {
        if (file.size > 10 * 1024 * 1024) {
          alert('파일 크기는 10MB를 초과할 수 없습니다.')
          return
        }
        selectedFiles.value.push(file)
      })
    }

    // 파일 제거
    const removeFile = (index) => {
      selectedFiles.value.splice(index, 1)
    }

    // 문의 제출
    const submitInquiry = async () => {
      if (!selectedType.value) {
        alert('문의 유형을 선택해주세요.')
        return
      }

      isSubmitting.value = true

      try {
        // API 호출 및 파일 업로드 로직
        // const formData = new FormData()
        // formData.append('type', selectedType.value)
        // formData.append('title', inquiryTitle.value)
        // formData.append('content', inquiryContent.value)
        // selectedFiles.value.forEach(file => {
        //   formData.append('files', file)
        // })
        
        // const response = await axios.post('/api/v1/inquiries', formData)
        // lastInquiryId.value = response.data.inquiryId

        // 테스트용 지연
        await new Promise(resolve => setTimeout(resolve, 1500))
        lastInquiryId.value = 'INQ' + Date.now()

        showSuccessModal.value = true
        resetForm()
      } catch (error) {
        console.error('문의 제출 오류:', error)
        alert('문의 제출 중 오류가 발생했습니다. 다시 시도해주세요.')
      } finally {
        isSubmitting.value = false
      }
    }

    // 폼 초기화
    const resetForm = () => {
      selectedType.value = ''
      inquiryTitle.value = ''
      inquiryContent.value = ''
      selectedFiles.value = []
      emailNotification.value = true
    }

    return {
      faqs,
      inquiryTypes,
      selectedType,
      inquiryTitle,
      inquiryContent,
      selectedFiles,
      emailNotification,
      isSubmitting,
      showSuccessModal,
      lastInquiryId,
      toggleFaq,
      handleFileUpload,
      removeFile,
      submitInquiry
    }
  }
}
</script>

<style scoped>
.support {
  padding: 20px;
}

.support-header {
  text-align: center;
  background-color: #f8f9fa;
  padding: 3rem;
  border-radius: 10px;
}

.accordion-button:not(.collapsed) {
  background-color: #e7f1ff;
  color: #0d6efd;
}

.selected-file {
  background-color: #f8f9fa;
  transition: all 0.2s;
}

.selected-file:hover {
  background-color: #e9ecef;
}

.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}

/* 문의 유형 버튼 스타일 */
.btn-group .btn {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-group .btn i {
  margin-right: 8px;
}

/* 애니메이션 */
.accordion-collapse {
  transition: all 0.3s ease-in-out;
}

.selected-file {
  animation: slideIn 0.3s ease-in-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
