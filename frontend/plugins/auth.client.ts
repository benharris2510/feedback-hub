export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  
  // Load tokens from localStorage
  authStore.loadTokens()
  
  // If we have tokens, try to fetch the user profile
  if (authStore.accessToken) {
    await authStore.fetchProfile()
  }
})