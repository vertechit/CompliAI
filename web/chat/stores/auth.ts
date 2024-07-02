import { defineStore } from 'pinia'

export const authStore = defineStore('authStore', {
    state: () => ({
      token: useCookie('token')
    }),
    actions: {
      async authenticate(email: string, senha: string) {
        
        let result = await $fetch('/api/login',{
            method:'POST',
            body:{
              username: email,
              password: senha
            }
          }) as { access_token: string, token_type: string}

          const tokenCookie = useCookie('token', {
            maxAge: 60*24*28,
            sameSite: true,
            secure: true,
          })
          tokenCookie.value = result.access_token

      },
      async logout(){
        this.token = null
        const tokenCookie = useCookie('token')
        tokenCookie.value = null
      }

    },
    getters: {
      isAuthtenticate: (state) => (state.token ? true : false)
    }
  })