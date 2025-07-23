<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <NuxtLink to="/" class="text-xl font-bold text-blue-600">
                Feedback Hub
              </NuxtLink>
            </div>
            
            <!-- Navigation Links -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink
                to="/forums"
                class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm transition-colors"
                :class="{ 'border-blue-500 text-gray-900': $route.path.startsWith('/forums') }"
              >
                Forums
              </NuxtLink>
              <NuxtLink
                to="/feedback"
                class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm transition-colors"
                :class="{ 'border-blue-500 text-gray-900': $route.path.startsWith('/feedback') }"
              >
                Feedback
              </NuxtLink>
            </div>
          </div>
          
          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <template v-if="authStore.isAuthenticated && authStore.user">
              <NuxtLink
                to="/dashboard"
                class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Dashboard
              </NuxtLink>
              <div class="relative" ref="userMenuRef">
                <button
                  @click="showUserMenu = !showUserMenu"
                  class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <div class="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
                    <span class="text-white font-medium">
                      {{ authStore.user.username.charAt(0).toUpperCase() }}
                    </span>
                  </div>
                </button>
                
                <!-- User Dropdown -->
                <div
                  v-show="showUserMenu"
                  class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
                >
                  <div class="py-1">
                    <div class="px-4 py-2 text-sm text-gray-700 border-b border-gray-100">
                      {{ authStore.user.username }}
                    </div>
                    <NuxtLink
                      to="/dashboard"
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      @click="showUserMenu = false"
                    >
                      Dashboard
                    </NuxtLink>
                    <button
                      @click="logout"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              </div>
            </template>
            
            <template v-else>
              <NuxtLink
                to="/login"
                class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Sign in
              </NuxtLink>
              <NuxtLink
                to="/register"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Sign up
              </NuxtLink>
            </template>
          </div>
          
          <!-- Mobile menu button -->
          <div class="sm:hidden flex items-center">
            <button
              @click="showMobileMenu = !showMobileMenu"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile menu -->
      <div v-show="showMobileMenu" class="sm:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <NuxtLink
            to="/forums"
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="$route.path.startsWith('/forums') 
              ? 'bg-blue-50 border-blue-500 text-blue-700' 
              : 'border-transparent text-gray-600 hover:text-gray-800 hover:bg-gray-50 hover:border-gray-300'"
            @click="showMobileMenu = false"
          >
            Forums
          </NuxtLink>
          <NuxtLink
            to="/feedback"
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="$route.path.startsWith('/feedback') 
              ? 'bg-blue-50 border-blue-500 text-blue-700' 
              : 'border-transparent text-gray-600 hover:text-gray-800 hover:bg-gray-50 hover:border-gray-300'"
            @click="showMobileMenu = false"
          >
            Feedback
          </NuxtLink>
        </div>
        
        <div v-if="authStore.isAuthenticated" class="pt-4 pb-3 border-t border-gray-200">
          <div class="flex items-center px-4">
            <div class="flex-shrink-0">
              <div class="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center">
                <span class="text-white font-medium">
                  {{ authStore.user?.username.charAt(0).toUpperCase() }}
                </span>
              </div>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ authStore.user?.username }}</div>
              <div class="text-sm font-medium text-gray-500">{{ authStore.user?.email }}</div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <NuxtLink
              to="/dashboard"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              @click="showMobileMenu = false"
            >
              Dashboard
            </NuxtLink>
            <button
              @click="logout"
              class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            >
              Sign out
            </button>
          </div>
        </div>
        
        <div v-else class="pt-4 pb-3 border-t border-gray-200">
          <div class="space-y-1">
            <NuxtLink
              to="/login"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              @click="showMobileMenu = false"
            >
              Sign in
            </NuxtLink>
            <NuxtLink
              to="/register"
              class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              @click="showMobileMenu = false"
            >
              Sign up
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>
    
    <!-- Main Content -->
    <main>
      <slot />
    </main>
    
    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <p class="text-gray-500 text-sm">
            © 2025 Feedback Hub. Built with Vue 3, Nuxt 3, and Python Flask.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const route = useRoute()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const userMenuRef = ref(null)

// Close user menu when clicking outside
onClickOutside(userMenuRef, () => {
  showUserMenu.value = false
})

const logout = () => {
  showUserMenu.value = false
  showMobileMenu.value = false
  authStore.logout()
}

// Close mobile menu on route change
watch(() => route.path, () => {
  showMobileMenu.value = false
})
</script>