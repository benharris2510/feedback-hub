<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="p-6">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center space-x-3 mb-8">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h1 class="text-xl font-bold gradient-text">Feedback Hub</h1>
        </NuxtLink>
        
        <!-- Navigation -->
        <nav class="space-y-2">
          <NuxtLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v3H8V5z"/>
            </svg>
            Dashboard
          </NuxtLink>
          
          <NuxtLink to="/forums" class="nav-link" :class="{ active: $route.path.startsWith('/forums') }">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a2 2 0 01-2-2v-1M15 8V6a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2h2m8-8V6a2 2 0 00-2-2H9a2 2 0 00-2 2v2m8 4V8a2 2 0 00-2-2H9a2 2 0 00-2 2v8a2 2 0 002 2h6l4 4v-4z"/>
            </svg>
            Forums
          </NuxtLink>
          
          <NuxtLink to="/feedback" class="nav-link" :class="{ active: $route.path.startsWith('/feedback') }">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
            </svg>
            Feedback
          </NuxtLink>
        </nav>
        
        <!-- Divider -->
        <div class="my-8 h-px bg-gradient-to-r from-transparent via-slate-700 to-transparent"></div>
        
        <!-- User Section -->
        <div v-if="authStore.isAuthenticated" class="space-y-2">
          <div class="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Account
          </div>
          <NuxtLink to="/dashboard" class="nav-link">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            Profile
          </NuxtLink>
          <button @click="authStore.logout" class="nav-link w-full text-left">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            Sign Out
          </button>
        </div>
        
        <div v-else class="space-y-3">
          <NuxtLink to="/login" class="btn btn-ghost w-full justify-start">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
            </svg>
            Sign In
          </NuxtLink>
          <NuxtLink to="/register" class="btn btn-primary w-full justify-start">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
            Get Started
          </NuxtLink>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64">
      <!-- Top Header -->
      <header class="h-16 glass border-b border-slate-800/50 flex items-center justify-between px-6 sticky top-0 z-40">
        <div class="flex items-center space-x-4">
          <h2 class="text-lg font-semibold text-slate-100">
            {{ getPageTitle() }}
          </h2>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Quick Actions -->
          <div class="flex items-center space-x-2">
            <NuxtLink 
              v-if="$route.path.startsWith('/feedback')" 
              to="/feedback/new" 
              class="btn btn-primary btn-sm"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              Submit Feedback
            </NuxtLink>
          </div>
          
          <!-- User Avatar -->
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-3">
            <div class="flex items-center space-x-2">
              <div class="status-dot status-online"></div>
              <span class="text-sm text-slate-400">{{ authStore.user?.email }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="p-6">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const route = useRoute()

function getPageTitle() {
  const path = route.path
  if (path === '/') return 'Dashboard'
  if (path.startsWith('/forums')) return 'Forums'
  if (path.startsWith('/feedback')) return 'Feedback'
  if (path === '/login') return 'Sign In'
  if (path === '/register') return 'Sign Up'
  return 'Feedback Hub'
}
</script>