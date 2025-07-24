<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Breadcrumb -->
      <nav aria-label="Breadcrumb" class="mb-8">
        <ol class="flex items-center space-x-2 text-sm">
          <li>
            <NuxtLink to="/feedback" class="text-blue-600 hover:text-blue-800">
              Feedback
            </NuxtLink>
          </li>
          <li>
            <svg class="flex-shrink-0 h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </li>
          <li class="text-gray-500 truncate">{{ feedbackData?.title }}</li>
        </ol>
      </nav>

      <!-- Feedback Content -->
      <div v-if="feedbackData" class="bg-white shadow rounded-lg mb-8">
        <div class="p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-3">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getStatusBadgeClass(feedbackData.status)"
                >
                  {{ feedbackData.status.replace('_', ' ').toUpperCase() }}
                </span>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getTypeBadgeClass(feedbackData.type)"
                >
                  {{ feedbackData.type.toUpperCase() }}
                </span>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getPriorityBadgeClass(feedbackData.priority)"
                >
                  {{ feedbackData.priority.toUpperCase() }}
                </span>
              </div>
              
              <h1 class="text-3xl font-bold text-gray-900 mb-4">
                {{ feedbackData.title }}
              </h1>
            </div>
            
            <div class="ml-4 flex flex-col items-end space-y-2">
              <button
                @click="voteFeedback"
                class="flex items-center space-x-1 text-gray-500 hover:text-blue-600 transition-colors"
              >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                </svg>
                <span class="font-semibold">{{ feedbackData.votes }}</span>
              </button>
              <span class="text-sm text-gray-500">votes</span>
            </div>
          </div>
          
          <div class="prose max-w-none mb-6">
            <p class="text-gray-700 whitespace-pre-wrap">{{ feedbackData.description }}</p>
          </div>
          
          <div class="flex items-center justify-between pt-4 border-t border-gray-200">
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>By {{ feedbackData.user }}</span>
              <span>{{ formatDate(feedbackData.created_at) }}</span>
              <span v-if="feedbackData.updated_at !== feedbackData.created_at">
                Updated {{ formatDate(feedbackData.updated_at) }}
              </span>
            </div>
            
            <!-- Admin Controls -->
            <div v-if="authStore.isAdmin" class="flex items-center space-x-4">
              <select
                v-model="adminControls.status"
                @change="updateStatus"
                class="text-sm border border-gray-300 rounded-md px-2 py-1"
              >
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
              
              <select
                v-model="adminControls.priority"
                @change="updatePriority"
                class="text-sm border border-gray-300 rounded-md px-2 py-1"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="bg-white shadow rounded-lg">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-gray-900">
              Comments ({{ commentsData?.length || 0 }})
            </h2>
            <button
              v-if="authStore.isAuthenticated"
              @click="showCommentForm = true"
              class="btn btn-primary"
            >
              Add Comment
            </button>
          </div>

          <!-- Comment Form -->
          <div v-if="showCommentForm" class="mb-8 p-4 bg-gray-50 rounded-lg">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Add a Comment</h3>
            <form @submit.prevent="submitComment">
              <div class="mb-4">
                <textarea
                  v-model="newComment.content"
                  rows="4"
                  required
                  class="input"
                  placeholder="Share your thoughts..."
                ></textarea>
              </div>
              <div class="flex items-center space-x-4">
                <button type="submit" :disabled="submittingComment" class="btn btn-primary">
                  <span v-if="submittingComment">Posting...</span>
                  <span v-else>Post Comment</span>
                </button>
                <button
                  type="button"
                  @click="showCommentForm = false"
                  class="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>

          <!-- Loading Comments -->
          <div v-if="pendingComments" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-2 text-gray-600">Loading comments...</p>
          </div>

          <!-- Comments List -->
          <div v-else-if="commentsData && commentsData.length > 0" class="space-y-6">
            <div
              v-for="comment in commentsData"
              :key="comment.id"
              class="border-l-4 pl-4"
              :class="comment.is_admin_response ? 'border-blue-400' : 'border-gray-200'"
            >
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center space-x-2">
                    <span class="font-medium text-gray-900">{{ comment.user }}</span>
                    <span v-if="comment.is_admin_response" class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      Admin
                    </span>
                    <span class="text-sm text-gray-500">
                      {{ formatDate(comment.created_at) }}
                    </span>
                  </div>
                  
                  <button
                    v-if="canDeleteComment(comment)"
                    @click="deleteComment(comment.id)"
                    class="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                </div>
                <p class="text-gray-700 whitespace-pre-wrap">{{ comment.content }}</p>
              </div>
            </div>
          </div>

          <!-- No Comments -->
          <div v-else class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">No comments yet</h3>
            <p class="mt-2 text-gray-500">
              Be the first to comment on this feedback!
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const api = useApi()
const authStore = useAuthStore()

const feedbackId = route.params.id

// Get feedback data
const { data: feedbackData, refresh: refreshFeedback } = await useLazyAsyncData(
  `feedback-${feedbackId}`,
  () => api(`/feedback/${feedbackId}`)
)

// Get comments data
const { data: commentsData, pending: pendingComments, refresh: refreshComments } = await useLazyAsyncData(
  `feedback-comments-${feedbackId}`,
  () => api(`/feedback/${feedbackId}/comments`),
  {
    default: () => []
  }
)

// Admin controls
const adminControls = reactive({
  status: feedbackData.value?.status || '',
  priority: feedbackData.value?.priority || ''
})

// Comment form
const showCommentForm = ref(false)
const submittingComment = ref(false)
const newComment = reactive({
  content: ''
})

// Update admin controls when data loads
watch(feedbackData, (newData) => {
  if (newData) {
    adminControls.status = newData.status
    adminControls.priority = newData.priority
  }
}, { immediate: true })

const voteFeedback = async () => {
  try {
    await api(`/feedback/${feedbackId}/vote`, { method: 'POST' })
    await refreshFeedback()
  } catch (error) {
    // Handle vote error silently
  }
}

const updateStatus = async () => {
  try {
    await api(`/feedback/${feedbackId}`, {
      method: 'PUT',
      body: { status: adminControls.status }
    })
    await refreshFeedback()
  } catch (error) {
    // Handle status update error silently
  }
}

const updatePriority = async () => {
  try {
    await api(`/feedback/${feedbackId}`, {
      method: 'PUT',
      body: { priority: adminControls.priority }
    })
    await refreshFeedback()
  } catch (error) {
    // Handle priority update error silently
  }
}

const submitComment = async () => {
  if (!newComment.content.trim()) return
  
  submittingComment.value = true
  
  try {
    await api(`/feedback/${feedbackId}/comments`, {
      method: 'POST',
      body: newComment
    })
    
    // Reset form and refresh comments
    newComment.content = ''
    showCommentForm.value = false
    await refreshComments()
  } catch (error) {
    // Handle comment submission error silently
  } finally {
    submittingComment.value = false
  }
}

const canDeleteComment = (comment: Record<string, unknown>) => {
  return authStore.isAdmin || comment.user_id === authStore.user?.id
}

const deleteComment = async (commentId: number) => {
  if (!confirm('Are you sure you want to delete this comment?')) return
  
  try {
    await api(`/feedback/${feedbackId}/comments/${commentId}`, {
      method: 'DELETE'
    })
    await refreshComments()
  } catch (error) {
    // Handle comment deletion error silently
  }
}

// Badge styling helpers (same as feedback index)
const getStatusBadgeClass = (status: string) => {
  const classes = {
    'open': 'bg-green-100 text-green-800',
    'in_progress': 'bg-yellow-100 text-yellow-800',
    'resolved': 'bg-blue-100 text-blue-800',
    'closed': 'bg-gray-100 text-gray-800'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

const getTypeBadgeClass = (type: string) => {
  const classes = {
    'bug': 'bg-red-100 text-red-800',
    'feature': 'bg-purple-100 text-purple-800',
    'improvement': 'bg-blue-100 text-blue-800',
    'general': 'bg-gray-100 text-gray-800'
  }
  return classes[type as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

const getPriorityBadgeClass = (priority: string) => {
  const classes = {
    'low': 'bg-green-100 text-green-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'high': 'bg-orange-100 text-orange-800',
    'urgent': 'bg-red-100 text-red-800'
  }
  return classes[priority as keyof typeof classes] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

useHead({
  title: () => feedbackData.value ? `${feedbackData.value.title} - Feedback` : 'Feedback - Feedback Hub',
  meta: [
    { name: 'description', content: () => feedbackData.value?.description.substring(0, 160) || 'Feedback details' }
  ]
})
</script>