export const useApi = () => {
  const authStore = useAuthStore()
  const config = useRuntimeConfig()
  
  const api = $fetch.create({
    baseURL: config.public.apiUrl,
    onRequest({ request, options }) {
      if (authStore.accessToken) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${authStore.accessToken}`
        }
      }
    },
    onResponseError({ request, response, options }) {
      if (response.status === 401 && authStore.isAuthenticated) {
        // Token expired, try to refresh
        authStore.refreshAccessToken().then((success) => {
          if (!success) {
            authStore.logout()
          }
        })
      }
    }
  })
  
  return api
}