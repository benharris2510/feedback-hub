<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h1 class="text-2xl font-bold text-gray-900 mb-4">
            Welcome to your Dashboard
          </h1>
          
          <div v-if="authStore.user" class="space-y-4">
            <p class="text-gray-600">
              Hello, <strong>{{ authStore.user.username }}</strong>!
            </p>
            <p class="text-sm text-gray-500">
              Email: {{ authStore.user.email }}
            </p>
            <p v-if="authStore.isAdmin" class="text-sm text-green-600 font-medium">
              You have admin privileges
            </p>
            
            <div class="pt-4">
              <button
                @click="authStore.logout()"
                class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
          
          <div class="mt-8">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Quick Actions</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <NuxtLink
                to="/forums"
                class="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <h3 class="font-medium text-gray-900">Browse Forums</h3>
                <p class="text-sm text-gray-500 mt-1">
                  View and participate in community discussions
                </p>
              </NuxtLink>
              
              <NuxtLink
                to="/feedback"
                class="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <h3 class="font-medium text-gray-900">View Feedback</h3>
                <p class="text-sm text-gray-500 mt-1">
                  See what users are saying about the platform
                </p>
              </NuxtLink>
              
              <NuxtLink
                to="/feedback/new"
                class="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <h3 class="font-medium text-gray-900">Submit Feedback</h3>
                <p class="text-sm text-gray-500 mt-1">
                  Share your ideas and suggestions
                </p>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

const authStore = useAuthStore()
</script>