<template>
  <div class="min-h-screen flex bg-gray-950">
    <!-- Mobile overlay -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 z-40 lg:hidden"
      @click="sidebarOpen = false"
    >
      <div class="absolute inset-0 bg-gray-950/80 backdrop-blur-sm"></div>
    </div>

    <!-- Sidebar -->
    <aside 
      class="sidebar transform"
      :class="{ '-translate-x-full lg:translate-x-0': !sidebarOpen }"
    >
      <div class="flex flex-col h-full">
        <!-- Logo Section -->
        <div class="p-6 border-b border-gray-800/50">
          <NuxtLink to="/" class="flex items-center gap-3 group">
            <div class="relative">
              <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/25 group-hover:shadow-primary-500/40 transition-all duration-200">
                <ChatBubbleBottomCenterTextIcon class="w-5 h-5 text-white" />
              </div>
              <div class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full border-2 border-gray-950"></div>
            </div>
            <div>
              <h1 class="text-lg font-bold gradient-text">FeedbackHub</h1>
              <p class="text-xs text-gray-500">v2.0</p>
            </div>
          </NuxtLink>
        </div>
        
        <!-- Navigation -->
        <nav class="flex-1 p-4 space-y-1">
          <div class="mb-6">
            <div class="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Main
            </div>
            <div class="space-y-1">
              <NuxtLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">
                <HomeIcon class="w-5 h-5" />
                Dashboard
              </NuxtLink>
              
              <NuxtLink to="/forums" class="nav-link" :class="{ active: $route.path.startsWith('/forums') }">
                <ChatBubbleLeftRightIcon class="w-5 h-5" />
                Forums
                <span class="ml-auto badge badge-secondary">12</span>
              </NuxtLink>
              
              <NuxtLink to="/feedback" class="nav-link" :class="{ active: $route.path.startsWith('/feedback') }">
                <ClipboardDocumentListIcon class="w-5 h-5" />
                Feedback
                <span class="ml-auto badge badge-primary">24</span>
              </NuxtLink>
            </div>
          </div>
          
          <!-- User Section -->
          <div v-if="authStore?.isAuthenticated">
            <div class="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Account
            </div>
            <div class="space-y-1">
              <NuxtLink to="/dashboard" class="nav-link">
                <UserIcon class="w-5 h-5" />
                Profile
              </NuxtLink>
              <NuxtLink to="/settings" class="nav-link">
                <Cog6ToothIcon class="w-5 h-5" />
                Settings
              </NuxtLink>
              <button @click="authStore?.logout" class="nav-link w-full text-left">
                <ArrowRightOnRectangleIcon class="w-5 h-5" />
                Sign Out
              </button>
            </div>
          </div>
        </nav>
        
        <!-- Auth Section for non-authenticated users -->
        <div v-if="!authStore?.isAuthenticated" class="p-4 border-t border-gray-800/50">
          <div class="space-y-2">
            <NuxtLink to="/login" class="btn btn-ghost w-full justify-start">
              <ArrowRightOnRectangleIcon class="w-5 h-5" />
              Sign In
            </NuxtLink>
            <NuxtLink to="/register" class="btn btn-primary w-full justify-start">
              <UserPlusIcon class="w-5 h-5" />
              Get Started
            </NuxtLink>
          </div>
        </div>

        <!-- User Profile (for authenticated users) -->
        <div v-if="authStore?.isAuthenticated" class="p-4 border-t border-gray-800/50">
          <div class="flex items-center gap-3 p-3 rounded-xl bg-gray-800/30 border border-gray-700/50">
            <div class="relative">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-sm font-semibold text-white">
                {{ authStore.user?.email?.charAt(0).toUpperCase() }}
              </div>
              <div class="status-dot status-online absolute -bottom-0.5 -right-0.5"></div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-200 truncate">
                {{ authStore.user?.username || authStore.user?.email }}
              </p>
              <p class="text-xs text-gray-400 truncate">{{ authStore.user?.email }}</p>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 lg:ml-64 flex flex-col min-h-screen">
      <!-- Top Header -->
      <header class="glass border-b border-gray-800/50 sticky top-0 z-30">
        <div class="flex items-center justify-between h-16 px-4 lg:px-6">
          <!-- Mobile menu button -->
          <button
            @click="sidebarOpen = !sidebarOpen"
            class="lg:hidden p-2 text-gray-400 hover:text-gray-100 hover:bg-gray-800/50 rounded-lg transition-colors"
          >
            <Bars3Icon v-if="!sidebarOpen" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>

          <!-- Page title -->
          <div class="flex items-center gap-4">
            <div>
              <h2 class="text-lg font-semibold text-gray-100">
                {{ pageTitle }}
              </h2>
              <p v-if="pageDescription" class="text-sm text-gray-400">
                {{ pageDescription }}
              </p>
            </div>
          </div>
          
          <!-- Header actions -->
          <div class="flex items-center gap-3">
            <!-- Quick Actions -->
            <NuxtLink 
              v-if="$route.path.startsWith('/feedback')" 
              to="/feedback/new" 
              class="btn btn-primary btn-sm"
            >
              <PlusIcon class="w-4 h-4" />
              <span class="hidden sm:inline">Submit Feedback</span>
            </NuxtLink>

            <!-- Notifications -->
            <button class="relative p-2 text-gray-400 hover:text-gray-100 hover:bg-gray-800/50 rounded-lg transition-colors">
              <BellIcon class="w-5 h-5" />
              <span class="absolute top-1 right-1 w-2 h-2 bg-primary-500 rounded-full"></span>
            </button>

            <!-- Search -->
            <button class="hidden sm:flex p-2 text-gray-400 hover:text-gray-100 hover:bg-gray-800/50 rounded-lg transition-colors">
              <MagnifyingGlassIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-4 lg:p-6">
        <div class="fade-in">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  ClipboardDocumentListIcon,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  ChatBubbleBottomCenterTextIcon,
  Bars3Icon,
  XMarkIcon,
  PlusIcon,
  BellIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const route = useRoute()

// Reactive state for mobile sidebar
const sidebarOpen = ref(false)

// Page metadata
const pageTitle = computed(() => {
  const path = route.path
  if (path === '/') return 'Dashboard'
  if (path.startsWith('/forums')) return 'Forums'
  if (path.startsWith('/feedback')) return 'Feedback'
  if (path === '/login') return 'Sign In'
  if (path === '/register') return 'Sign Up'
  return 'FeedbackHub'
})

const pageDescription = computed(() => {
  const path = route.path
  if (path === '/') return 'Overview of your feedback and forum activity'
  if (path.startsWith('/forums')) return 'Community discussions and support'
  if (path.startsWith('/feedback')) return 'Submit and browse user feedback'
  return null
})

// Close sidebar when route changes (mobile)
watch(() => route.path, () => {
  sidebarOpen.value = false
})

// Close sidebar on escape key
onMounted(() => {
  const handleEscape = (e: Event) => {
    const keyboardEvent = e as KeyboardEvent
    if (keyboardEvent.key === 'Escape') {
      sidebarOpen.value = false
    }
  }
  document.addEventListener('keydown', handleEscape)
  
  onUnmounted(() => {
    document.removeEventListener('keydown', handleEscape)
  })
})
</script>