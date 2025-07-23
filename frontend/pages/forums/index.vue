<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Community Forums</h1>
        <p class="mt-2 text-gray-600">
          Join discussions and connect with the community
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="pending" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading forums...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              Error loading forums
            </h3>
            <div class="mt-2 text-sm text-red-700">
              {{ error }}
            </div>
          </div>
        </div>
      </div>

      <!-- Forums List -->
      <div v-else-if="data && data.length > 0" class="space-y-6">
        <div
          v-for="forum in data"
          :key="forum.id"
          class="bg-white shadow rounded-lg hover:shadow-md transition-shadow"
        >
          <div class="p-6">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <NuxtLink
                  :to="`/forums/${forum.slug}`"
                  class="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors"
                >
                  {{ forum.name }}
                </NuxtLink>
                <p class="mt-2 text-gray-600">
                  {{ forum.description }}
                </p>
                <div class="mt-4 flex items-center space-x-4 text-sm text-gray-500">
                  <span>{{ forum.posts_count }} posts</span>
                  <span>Created by {{ forum.creator }}</span>
                  <span>{{ formatDate(forum.created_at) }}</span>
                </div>
              </div>
              <div class="ml-4">
                <NuxtLink
                  :to="`/forums/${forum.slug}`"
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 transition-colors"
                >
                  View Forum
                  <svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
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
        <h3 class="mt-4 text-lg font-medium text-gray-900">No forums available</h3>
        <p class="mt-2 text-gray-500">
          There are no public forums to display at the moment.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

useHead({
  title: 'Forums - Feedback Hub',
  meta: [
    { name: 'description', content: 'Browse community forums and join discussions' }
  ]
})
</script>