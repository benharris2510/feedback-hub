<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-100">Community Forums</h1>
        <p class="text-gray-400 mt-1">
          Join discussions and connect with the community
        </p>
        <div class="flex items-center gap-4 mt-3 text-sm text-gray-500">
          <span class="flex items-center gap-1">
            <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
            {{ data?.length || 0 }} active forums
          </span>
          <span class="flex items-center gap-1">
            <div class="w-2 h-2 rounded-full bg-primary-400"></div>
            24 online users
          </span>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <button class="btn btn-ghost btn-sm">
          <MagnifyingGlassIcon class="w-4 h-4" />
          Search
        </button>
        <button class="btn btn-ghost btn-sm">
          <FunnelIcon class="w-4 h-4" />
          Filter
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-12">
      <div class="loading-spinner w-8 h-8 mb-4"></div>
      <p class="text-gray-400">Loading forums...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card border-red-500/20 bg-red-500/5">
      <div class="flex items-start gap-3">
        <ExclamationTriangleIcon class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
        <div>
          <h3 class="text-sm font-medium text-red-300">
            Error loading forums
          </h3>
          <p class="mt-1 text-sm text-red-400">
            {{ error }}
          </p>
          <button class="mt-3 btn btn-sm btn-ghost text-red-300 hover:text-red-200">
            Try again
          </button>
        </div>
      </div>
    </div>

    <!-- Forums List -->
    <div v-else-if="data && data.length > 0" class="space-y-4 stagger-children">
      <div
        v-for="forum in data"
        :key="forum.id"
        class="card card-hover card-interactive group"
      >
        <div class="flex items-start justify-between">
          <!-- Forum Icon and Content -->
          <div class="flex gap-4 flex-1 min-w-0">
            <!-- Forum Icon -->
            <div class="flex-shrink-0">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary-500/20 to-secondary-500/20 border border-primary-500/20 flex items-center justify-center">
                <ChatBubbleLeftRightIcon class="w-6 h-6 text-primary-400" />
              </div>
            </div>
            
            <!-- Forum Details -->
            <div class="flex-1 min-w-0">
              <NuxtLink :to="`/forums/${forum.slug}`" class="block">
                <h3 class="text-lg font-semibold text-gray-100 group-hover:text-primary-300 transition-colors line-clamp-1">
                  {{ forum.name }}
                </h3>
                <p class="mt-1 text-gray-400 text-sm line-clamp-2">
                  {{ forum.description }}
                </p>
              </NuxtLink>
              
              <!-- Forum Stats -->
              <div class="flex items-center gap-4 mt-3 text-xs text-gray-500">
                <span class="flex items-center gap-1">
                  <DocumentTextIcon class="w-3 h-3" />
                  {{ forum.posts_count }} posts
                </span>
                <span class="flex items-center gap-1">
                  <UserIcon class="w-3 h-3" />
                  {{ forum.creator }}
                </span>
                <span class="flex items-center gap-1">
                  <ClockIcon class="w-3 h-3" />
                  {{ formatDate(forum.created_at) }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Action Button -->
          <div class="flex-shrink-0 ml-6">
            <NuxtLink
              :to="`/forums/${forum.slug}`"
              class="btn btn-ghost btn-sm opacity-0 group-hover:opacity-100 transition-opacity"
            >
              View Forum
              <ArrowTopRightOnSquareIcon class="w-3 h-3" />
            </NuxtLink>
          </div>
        </div>
        
        <!-- Latest Activity (if available) -->
        <div v-if="forum.latest_post" class="mt-4 pt-4 border-t border-gray-800/50">
          <div class="flex items-center gap-2 text-xs text-gray-500">
            <span>Latest:</span>
            <NuxtLink 
              :to="`/forums/${forum.slug}/posts/${forum.latest_post.id}`"
              class="text-gray-400 hover:text-primary-400 transition-colors line-clamp-1 flex-1"
            >
              {{ forum.latest_post.title }}
            </NuxtLink>
            <span>by {{ forum.latest_post.user }}</span>
            <span>{{ formatRelativeTime(forum.latest_post.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="flex flex-col items-center justify-center py-16">
      <div class="relative">
        <div class="w-16 h-16 rounded-2xl bg-gray-800/50 flex items-center justify-center mb-4">
          <ChatBubbleLeftRightIcon class="w-8 h-8 text-gray-500" />
        </div>
        <div class="absolute -top-1 -right-1 w-4 h-4 bg-primary-500 rounded-full"></div>
      </div>
      
      <h3 class="text-lg font-semibold text-gray-200 mb-2">No forums available</h3>
      <p class="text-gray-400 text-center mb-6 max-w-md">
        There are no public forums to display at the moment. Check back later for community discussions!
      </p>
      
      <div class="flex items-center gap-3">
        <button class="btn btn-ghost">
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
  ExclamationTriangleIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  UserIcon,
  ClockIcon,
  ArrowTopRightOnSquareIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const api = useApi()

const { data, pending, error } = await useLazyAsyncData('forums', () => 
  api('/forums')
)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatRelativeTime = (dateString: string) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  
  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
  
  return formatDate(dateString)
}

useHead({
  title: 'Forums - FeedbackHub',
  meta: [
    { name: 'description', content: 'Browse community forums and join discussions' }
  ]
})
</script>