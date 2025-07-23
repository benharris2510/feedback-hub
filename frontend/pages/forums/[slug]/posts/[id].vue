<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Breadcrumb -->
      <nav aria-label="Breadcrumb" class="mb-8">
        <ol class="flex items-center space-x-2 text-sm">
          <li>
            <NuxtLink to="/forums" class="text-blue-600 hover:text-blue-800">
              Forums
            </NuxtLink>
          </li>
          <li>
            <svg class="flex-shrink-0 h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </li>
          <li>
            <NuxtLink :to="`/forums/${route.params.slug}`" class="text-blue-600 hover:text-blue-800">
              {{ postData?.forum }}
            </NuxtLink>
          </li>
          <li>
            <svg class="flex-shrink-0 h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </li>
          <li class="text-gray-500 truncate">{{ postData?.title }}</li>
        </ol>
      </nav>

      <!-- Post Content -->
      <div v-if="postData" class="bg-white shadow rounded-lg mb-8">
        <div class="p-6">
          <div class="flex items-center space-x-2 mb-4">
            <span
              v-if="postData.is_pinned"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
            >
              Pinned
            </span>
            <span
              v-if="postData.is_locked"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
            >
              Locked
            </span>
          </div>
          
          <h1 class="text-3xl font-bold text-gray-900 mb-4">
            {{ postData.title }}
          </h1>
          
          <div class="prose max-w-none mb-6">
            <p class="text-gray-700 whitespace-pre-wrap">{{ postData.content }}</p>
          </div>
          
          <div class="flex items-center justify-between pt-4 border-t border-gray-200">
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>By {{ postData.author }}</span>
              <span>{{ postData.views }} views</span>
              <span>{{ formatDate(postData.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Replies Section -->
      <div class="bg-white shadow rounded-lg">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-gray-900">
              Replies ({{ repliesData?.length || 0 }})
            </h2>
            <button
              v-if="authStore.isAuthenticated && postData && !postData.is_locked"
              @click="showReplyForm = true"
              class="btn btn-primary"
            >
              Reply
            </button>
          </div>

          <!-- Reply Form -->
          <div v-if="showReplyForm" class="mb-8 p-4 bg-gray-50 rounded-lg">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Write a Reply</h3>
            <form @submit.prevent="submitReply">
              <div class="mb-4">
                <label for="reply-content" class="block text-sm font-medium text-gray-700 mb-2">
                  Your Reply
                </label>
                <textarea
                  id="reply-content"
                  v-model="newReply.content"
                  rows="4"
                  required
                  class="input"
                  placeholder="Write your reply here..."
                ></textarea>
              </div>
              <div class="flex items-center space-x-4">
                <button type="submit" :disabled="submittingReply" class="btn btn-primary">
                  <span v-if="submittingReply">Posting...</span>
                  <span v-else>Post Reply</span>
                </button>
                <button
                  type="button"
                  @click="showReplyForm = false"
                  class="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>

          <!-- Post Locked Message -->
          <div v-if="postData?.is_locked && !authStore.isAdmin" class="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
            <div class="flex">
              <svg class="h-5 w-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <div class="ml-3">
                <p class="text-sm text-yellow-800">
                  This post is locked. New replies are not allowed.
                </p>
              </div>
            </div>
          </div>

          <!-- Loading Replies -->
          <div v-if="pendingReplies" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-2 text-gray-600">Loading replies...</p>
          </div>

          <!-- Replies List -->
          <div v-else-if="repliesData && repliesData.length > 0" class="space-y-6">
            <div
              v-for="reply in repliesData"
              :key="reply.id"
              class="border-l-4 border-blue-200 pl-4"
            >
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center space-x-2">
                    <span class="font-medium text-gray-900">{{ reply.author }}</span>
                    <span class="text-sm text-gray-500">
                      {{ formatDate(reply.created_at) }}
                    </span>
                  </div>
                </div>
                <p class="text-gray-700 whitespace-pre-wrap">{{ reply.content }}</p>
              </div>
            </div>
          </div>

          <!-- No Replies -->
          <div v-else class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">No replies yet</h3>
            <p class="mt-2 text-gray-500">
              Be the first to reply to this post!
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

const postId = route.params.id

// Get post data
const { data: postData } = await useLazyAsyncData(`post-${postId}`, () =>
  api(`/posts/${postId}`)
)

// Get replies data
const { data: repliesData, pending: pendingReplies, refresh: refreshReplies } = await useLazyAsyncData(
  `post-replies-${postId}`,
  () => api(`/posts/${postId}/replies`),
  {
    default: () => []
  }
)

// Reply form
const showReplyForm = ref(false)
const submittingReply = ref(false)
const newReply = reactive({
  content: ''
})

const submitReply = async () => {
  if (!postData.value) return
  
  submittingReply.value = true
  
  try {
    await api(`/posts/${postData.value.id}/replies`, {
      method: 'POST',
      body: newReply
    })
    
    // Reset form and refresh replies
    newReply.content = ''
    showReplyForm.value = false
    await refreshReplies()
  } catch (error) {
    console.error('Failed to post reply:', error)
  } finally {
    submittingReply.value = false
  }
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
  title: () => postData.value ? `${postData.value.title} - Forums` : 'Post - Feedback Hub',
  meta: [
    { name: 'description', content: () => postData.value?.content.substring(0, 160) || 'Forum post discussion' }
  ]
})
</script>