
import { authStore } from '@/stores/auth'

export default defineNuxtRouteMiddleware((to, from) => {
  const auth = authStore()
    if (!auth.isAuthtenticate) {
      return navigateTo('/login')
    }
  })