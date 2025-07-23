import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  username: string
  is_admin: boolean
  created_at: string
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false
  }),

  getters: {
    isAdmin: (state) => state.user?.is_admin || false
  },

  actions: {
    async login(email: string, password: string) {
      const { $fetch } = useNuxtApp()
      const config = useRuntimeConfig()
      
      try {
        const response = await $fetch(`${config.public.apiUrl}/auth/login`, {
          method: 'POST',
          body: { email, password }
        })
        
        this.setAuth(response)
        return { success: true }
      } catch (error: any) {
        return { success: false, error: error.data?.message || 'Login failed' }
      }
    },

    async register(email: string, username: string, password: string) {
      const { $fetch } = useNuxtApp()
      const config = useRuntimeConfig()
      
      try {
        const response = await $fetch(`${config.public.apiUrl}/auth/register`, {
          method: 'POST',
          body: { email, username, password }
        })
        
        this.setAuth(response)
        return { success: true }
      } catch (error: any) {
        return { success: false, error: error.data?.message || 'Registration failed' }
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) return false
      
      const { $fetch } = useNuxtApp()
      const config = useRuntimeConfig()
      
      try {
        const response = await $fetch(`${config.public.apiUrl}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.refreshToken}`
          }
        })
        
        this.accessToken = response.access_token
        this.saveTokens()
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    async fetchProfile() {
      const { $fetch } = useNuxtApp()
      const config = useRuntimeConfig()
      
      try {
        const user = await $fetch(`${config.public.apiUrl}/auth/profile`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        })
        
        this.user = user
        return true
      } catch (error) {
        return false
      }
    },

    setAuth(authData: any) {
      this.user = authData.user
      this.accessToken = authData.access_token
      this.refreshToken = authData.refresh_token
      this.isAuthenticated = true
      this.saveTokens()
    },

    saveTokens() {
      if (process.client) {
        if (this.accessToken) {
          localStorage.setItem('access_token', this.accessToken)
        }
        if (this.refreshToken) {
          localStorage.setItem('refresh_token', this.refreshToken)
        }
      }
    },

    loadTokens() {
      if (process.client) {
        this.accessToken = localStorage.getItem('access_token')
        this.refreshToken = localStorage.getItem('refresh_token')
        this.isAuthenticated = !!this.accessToken
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false
      
      if (process.client) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
      
      navigateTo('/')
    }
  }
})