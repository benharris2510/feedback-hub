<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-100">Feedback</h1>
        <p class="text-gray-400 mt-1">
          Browse community feedback and share your ideas
        </p>
        <div class="flex items-center gap-4 mt-3 text-sm text-gray-500">
          <span class="flex items-center gap-1">
            <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
            {{ data?.length || 0 }} total feedback
          </span>
          <span class="flex items-center gap-1">
            <div class="w-2 h-2 rounded-full bg-primary-400"></div>
            12 this week
          </span>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <button class="btn btn-ghost btn-sm">
          <FunnelIcon class="w-4 h-4" />
          Filter
        </button>
        <NuxtLink to="/feedback/new" class="btn btn-primary">
          <PlusIcon class="w-4 h-4" />
          Submit Feedback
        </NuxtLink>
      </div>
    </div>

    <!-- Modern Search and Filters -->
    <div class="card">
      <div class="flex flex-col lg:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1">
          <div class="relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search feedback..."
              class="input pl-10"
              @input="debouncedSearch"
            >
          </div>
        </div>
        
        <!-- Filters -->
        <div class="flex gap-3">
          <select v-model="filters.status" class="input min-w-[140px]" @change="applyFilters">
            <option value="">All Statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
          
          <select v-model="filters.type" class="input min-w-[140px]" @change="applyFilters">
            <option value="">All Types</option>
            <option value="bug">Bug Report</option>
            <option value="feature">Feature Request</option>
            <option value="improvement">Improvement</option>
            <option value="general">General</option>
          </select>
          
          <select v-model="filters.priority" class="input min-w-[140px]" @change="applyFilters">
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
    <div v-if="pending" class="flex flex-col items-center justify-center py-12">
      <div class="loading-spinner w-8 h-8 mb-4"></div>
      <p class="text-gray-400">Loading feedback...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card border-red-500/20 bg-red-500/5">
      <div class="flex items-start gap-3">
        <ExclamationTriangleIcon class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
        <div>
          <h3 class="text-sm font-medium text-red-300">
            Error loading feedback
          </h3>
          <p class="mt-1 text-sm text-red-400">
            {{ error }}
          </p>
          <button 
            @click="refresh()" 
            class="mt-3 btn btn-sm btn-ghost text-red-300 hover:text-red-200"
          >
            Try again
          </button>
        </div>
      </div>
    </div>

    <!-- Feedback List -->
    <div v-else-if="data && data.length > 0" class="space-y-4 stagger-children">
      <div
        v-for="feedback in data"
        :key="feedback.id"
        class="card card-hover card-interactive group"
      >
        <div class="flex items-start justify-between">
          <!-- Main Content -->
          <div class="flex-1 min-w-0">
            <!-- Badges -->
            <div class="flex items-center gap-2 mb-3">
              <span :class="getStatusBadgeClass(feedback.status)" class="badge">
                {{ feedback.status.replace('_', ' ') }}
              </span>
              <span :class="getTypeBadgeClass(feedback.type)" class="badge">
                {{ feedback.type }}
              </span>
              <span :class="getPriorityBadgeClass(feedback.priority)" class="badge">
                {{ feedback.priority }}
              </span>
            </div>
            
            <!-- Title and Description -->
            <NuxtLink :to="`/feedback/${feedback.id}`" class="block">
              <h3 class="text-lg font-semibold text-gray-100 group-hover:text-primary-300 transition-colors line-clamp-2">
                {{ feedback.title }}
              </h3>
              <p class="mt-2 text-gray-400 line-clamp-2 text-sm">
                {{ feedback.description }}
              </p>
            </NuxtLink>
            
            <!-- Meta Information -->
            <div class="flex items-center gap-4 mt-4 text-xs text-gray-500">
              <span class="flex items-center gap-1">
                <UserIcon class="w-3 h-3" />
                {{ feedback.user }}
              </span>
              <span class="flex items-center gap-1">
                <ClockIcon class="w-3 h-3" />
                {{ formatDate(feedback.created_at) }}
              </span>
              <span class="flex items-center gap-1">
                <ChatBubbleLeftIcon class="w-3 h-3" />
                {{ feedback.comments_count }} comments
              </span>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="flex flex-col items-end gap-3 ml-6">
            <!-- Vote Button -->
            <button
              @click.stop="voteFeedback(feedback.id)"
              class="flex flex-col items-center gap-1 p-2 rounded-lg text-gray-400 hover:text-primary-400 hover:bg-primary-500/10 transition-all duration-200 group"
              :class="{ 'text-primary-400 bg-primary-500/10': feedback.voted }"
            >
              <ChevronUpIcon class="w-5 h-5 group-hover:scale-110 transition-transform" />
              <span class="text-xs font-medium">{{ feedback.votes }}</span>
            </button>
            
            <!-- View Button -->
            <NuxtLink
              :to="`/feedback/${feedback.id}`"
              class="btn btn-ghost btn-sm opacity-0 group-hover:opacity-100 transition-opacity"
            >
              View
              <ArrowTopRightOnSquareIcon class="w-3 h-3" />
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="flex flex-col items-center justify-center py-16">
      <div class="relative">
        <div class="w-16 h-16 rounded-2xl bg-gray-800/50 flex items-center justify-center mb-4">
          <ChatBubbleBottomCenterTextIcon class="w-8 h-8 text-gray-500" />
        </div>
        <div class="absolute -top-1 -right-1 w-4 h-4 bg-primary-500 rounded-full"></div>
      </div>
      
      <h3 class="text-lg font-semibold text-gray-200 mb-2">No feedback found</h3>
      <p class="text-gray-400 text-center mb-6 max-w-md">
        Be the first to share your feedback and help shape the future of this platform!
      </p>
      
      <div class="flex items-center gap-3">
        <NuxtLink to="/feedback/new" class="btn btn-primary">
          <PlusIcon class="w-4 h-4" />
          Submit Feedback
        </NuxtLink>
        <button @click="refresh()" class="btn btn-ghost">
          <ArrowPathIcon class="w-4 h-4" />
          Refresh
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  MagnifyingGlassIcon,
  FunnelIcon,
  PlusIcon,
  ExclamationTriangleIcon,
  UserIcon,
  ClockIcon,
  ChatBubbleLeftIcon,
  ChevronUpIcon,
  ArrowTopRightOnSquareIcon,
  ChatBubbleBottomCenterTextIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

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
    // Silently handle voting errors - user feedback will come from UI state
  }
}

// Modern badge styling helpers
const getStatusBadgeClass = (status: string) => {
  const classes = {
    'open': 'badge-success',
    'in_progress': 'badge-warning',
    'resolved': 'badge-info',
    'closed': 'badge-secondary'
  }
  return classes[status as keyof typeof classes] || 'badge-secondary'
}

const getTypeBadgeClass = (type: string) => {
  const classes = {
    'bug': 'badge-danger',
    'feature': 'badge-primary',
    'improvement': 'badge-info',
    'general': 'badge-secondary'
  }
  return classes[type as keyof typeof classes] || 'badge-secondary'
}

const getPriorityBadgeClass = (priority: string) => {
  const classes = {
    'low': 'badge-success',
    'medium': 'badge-warning',
    'high': 'badge-warning',
    'urgent': 'badge-danger'
  }
  return classes[priority as keyof typeof classes] || 'badge-secondary'
}

const formatDate = (dateString: string) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  
  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
  
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

useHead({
  title: 'Feedback - FeedbackHub',
  meta: [
    { name: 'description', content: 'Browse community feedback and suggestions' }
  ]
})
</script>