<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Forum Header -->
      <div v-if="forumData" class="mb-8">
        <nav aria-label="Breadcrumb" class="mb-4">
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
            <li class="text-gray-500">{{ forumData.name }}</li>
          </ol>
        </nav>
        
        <div class="bg-white shadow rounded-lg p-6">
          <h1 class="text-3xl font-bold text-gray-900">{{ forumData.name }}</h1>
          <p class="mt-2 text-gray-600">{{ forumData.description }}</p>
          <div class="mt-4 flex items-center justify-between">
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>{{ forumData.posts_count }} posts</span>
              <span>Created by {{ forumData.creator }}</span>
            </div>
            <button
              v-if="authStore.isAuthenticated"
              @click="showNewPostForm = true"
              class="btn btn-primary"
            >
              New Post
            </button>
          </div>
        </div>
      </div>

      <!-- New Post Form -->
      <div v-if="showNewPostForm" class="mb-8 bg-white shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Create New Post</h2>
        <form @submit.prevent="createPost">
          <div class="space-y-4">
            <div>
              <label for="title" class="block text-sm font-medium text-gray-700">
                Title
              </label>
              <input
                id="title"
                v-model="newPost.title"
                type="text"
                required
                class="mt-1 input"
                placeholder="Enter post title"
              >
            </div>
            <div>
              <label for="content" class="block text-sm font-medium text-gray-700">
                Content
              </label>
              <textarea
                id="content"
                v-model="newPost.content"
                rows="6"
                required
                class="mt-1 input"
                placeholder="Write your post content here..."
              ></textarea>
            </div>
          </div>
          <div class="mt-4 flex items-center space-x-4">
            <button type="submit" :disabled="submittingPost" class="btn btn-primary">
              <span v-if="submittingPost">Publishing...</span>
              <span v-else>Publish Post</span>
            </button>
            <button
              type="button"
              @click="showNewPostForm = false"
              class="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <!-- Loading State -->
      <div v-if="pendingPosts" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading posts...</p>
      </div>

      <!-- Posts List -->
      <div v-else-if="postsData && postsData.length > 0" class="space-y-6">
        <div
          v-for="post in postsData"
          :key="post.id"
          class="bg-white shadow rounded-lg hover:shadow-md transition-shadow"
        >
          <div class="p-6">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-2">
                  <span
                    v-if="post.is_pinned"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                  >
                    Pinned
                  </span>
                  <span
                    v-if="post.is_locked"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
                  >
                    Locked
                  </span>
                </div>
                <NuxtLink
                  :to="`/forums/${route.params.slug}/posts/${post.id}`"
                  class="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors"
                >
                  {{ post.title }}
                </NuxtLink>
                <p class="mt-2 text-gray-600 line-clamp-3">
                  {{ post.content }}
                </p>
                <div class="mt-4 flex items-center space-x-4 text-sm text-gray-500">
                  <span>By {{ post.author }}</span>
                  <span>{{ post.replies_count }} replies</span>
                  <span>{{ post.views }} views</span>
                  <span>{{ formatDate(post.created_at) }}</span>
                </div>
              </div>
              <div class="ml-4">
                <NuxtLink
                  :to="`/forums/${route.params.slug}/posts/${post.id}`"
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 transition-colors"
                >
                  View Post
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">No posts yet</h3>
        <p class="mt-2 text-gray-500">
          Be the first to start a discussion in this forum!
        </p>
        <button
          v-if="authStore.isAuthenticated"
          @click="showNewPostForm = true"
          class="mt-4 btn btn-primary"
        >
          Create First Post
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const api = useApi()
const authStore = useAuthStore()

// Get forum data
const { data: forumData } = await useLazyAsyncData(`forum-${route.params.slug}`, () =>
  api(`/forums/slug/${route.params.slug}`)
)

// Get posts data
const { data: postsData, pending: pendingPosts, refresh: refreshPosts } = await useLazyAsyncData(
  `forum-posts-${forumData.value?.id}`,
  () => api(`/posts/forum/${forumData.value?.id}`),
  {
    default: () => []
  }
)

// New post form
const showNewPostForm = ref(false)
const submittingPost = ref(false)
const newPost = reactive({
  title: '',
  content: ''
})

const createPost = async () => {
  if (!forumData.value) return
  
  submittingPost.value = true
  
  try {
    await api(`/posts/forum/${forumData.value.id}`, {
      method: 'POST',
      body: newPost
    })
    
    // Reset form and refresh posts
    newPost.title = ''
    newPost.content = ''
    showNewPostForm.value = false
    await refreshPosts()
  } catch (error) {
    // Silently handle post creation errors - user will see form still submitted and can retry
  } finally {
    submittingPost.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

useHead({
  title: () => forumData.value ? `${forumData.value.name} - Forums` : 'Forum - Feedback Hub',
  meta: [
    { name: 'description', content: () => forumData.value?.description || 'Forum discussion' }
  ]
})
</script>