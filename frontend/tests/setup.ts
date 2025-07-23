import { vi } from 'vitest'

// Mock Nuxt composables for testing
global.navigateTo = vi.fn()
global.useRoute = vi.fn(() => ({
  path: '/',
  params: {},
  query: {}
}))
global.useRouter = vi.fn(() => ({
  push: vi.fn(),
  replace: vi.fn()
}))
global.useRuntimeConfig = vi.fn(() => ({
  public: {
    apiUrl: 'http://localhost:5000/api'
  }
}))
global.useNuxtApp = vi.fn(() => ({
  $fetch: vi.fn()
}))
global.useHead = vi.fn()
global.useLazyAsyncData = vi.fn()