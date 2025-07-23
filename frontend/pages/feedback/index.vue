<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">User Feedback</h1>
            <p class="mt-2 text-gray-600">
              Browse feedback from the community and share your ideas
            </p>
          </div>
          <NuxtLink 
            to="/feedback/new"
            class="btn btn-primary"
          >
            Submit Feedback
          </NuxtLink>
        </div>
      </div>

      <!-- Search and Filters -->
      <div class="mb-8 bg-white rounded-lg shadow p-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label for="search" class="block text-sm font-medium text-gray-700 mb-2">
              Search
            </label>
            <input
              id="search"
              v-model="searchQuery"
              type="text"
              placeholder="Search feedback..."
              class="input"
              @input="debouncedSearch"
            >
          </div>
          <div>
            <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select id="status" v-model="filters.status" class="input" @change="applyFilters">
              <option value="">All Statuses</option>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <div>
            <label for="type" class="block text-sm font-medium text-gray-700 mb-2">
              Type
            </label>
            <select id="type" v-model="filters.type" class="input" @change="applyFilters">
              <option value="">All Types</option>
              <option value="bug">Bug Report</option>
              <option value="feature">Feature Request</option>
              <option value="improvement">Improvement</option>
              <option value="general">General</option>
            </select>
          </div>
          <div>
            <label for="priority" class="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <select id="priority" v-model="filters.priority" class="input" @change="applyFilters">
              <option value="">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="pending" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading feedback...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              Error loading feedback
            </h3>
            <div class="mt-2 text-sm text-red-700">
              {{ error }}
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback List -->
      <div v-else-if="data && data.length > 0" class="space-y-6">
        <div
          v-for="feedback in data"
          :key="feedback.id"
          class="bg-white shadow rounded-lg hover:shadow-md transition-shadow"
        >
          <div class="p-6">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-2">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getStatusBadgeClass(feedback.status)"
                  >
                    {{ feedback.status.replace('_', ' ').toUpperCase() }}
                  </span>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getTypeBadgeClass(feedback.type)"
                  >
                    {{ feedback.type.toUpperCase() }}
                  </span>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getPriorityBadgeClass(feedback.priority)"
                  >
                    {{ feedback.priority.toUpperCase() }}
                  </span>
                </div>
                
                <NuxtLink
                  :to="`/feedback/${feedback.id}`"
                  class="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors"
                >
                  {{ feedback.title }}
                </NuxtLink>
                
                <p class="mt-2 text-gray-600 line-clamp-2">
                  {{ feedback.description }}
                </p>
                
                <div class="mt-4 flex items-center space-x-4 text-sm text-gray-500">
                  <span>{{ feedback.votes }} votes</span>
                  <span>{{ feedback.comments_count }} comments</span>
                  <span>By {{ feedback.user }}</span>
                  <span>{{ formatDate(feedback.created_at) }}</span>
                </div>
              </div>
              
              <div class="ml-4 flex flex-col items-end space-y-2">
                <button
                  @click="voteFeedback(feedback.id)"
                  class="flex items-center space-x-1 text-gray-500 hover:text-blue-600 transition-colors"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                  <span>{{ feedback.votes }}</span>
                </button>
                
                <NuxtLink
                  :to="`/feedback/${feedback.id}`"
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 transition-colors"
                >
                  View Details
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
        <h3 class="mt-4 text-lg font-medium text-gray-900">No feedback found</h3>
        <p class="mt-2 text-gray-500">
          Be the first to share your feedback!
        </p>
        <NuxtLink
          to="/feedback/new"
          class="mt-4 btn btn-primary"
        >
          Submit Feedback
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()

// Search and filters
const searchQuery = ref('')
const filters = reactive({
  status: '',
  type: '',
  priority: ''
})

// Build query parameters
const queryParams = computed(() => {
  const params: Record<string, string> = {}
  if (searchQuery.value) params.search = searchQuery.value
  if (filters.status) params.status = filters.status
  if (filters.type) params.type = filters.type
  if (filters.priority) params.priority = filters.priority
  return params
})

// Fetch data with reactivity
const { data, pending, error, refresh } = await useLazyAsyncData(
  'feedback',
  () => api('/feedback', { query: queryParams.value }),
  {
    default: () => [],
    watch: [queryParams]
  }
)

// Debounced search
const debouncedSearch = useDebounceFn(() => {
  refresh()
}, 300)

const applyFilters = () => {
  refresh()
}

const voteFeedback = async (id: number) => {
  try {
    await api(`/feedback/${id}/vote`, { method: 'POST' })
    await refresh()
  } catch (error) {
    console.error('Failed to vote:', error)
  }
}

// Badge styling helpers
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
    month: 'short',
    day: 'numeric'
  })
}

useHead({
  title: 'Feedback - Feedback Hub',
  meta: [
    { name: 'description', content: 'Browse community feedback and suggestions' }
  ]
})
</script>