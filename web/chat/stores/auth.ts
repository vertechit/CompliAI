import { defineStore } from 'pinia'
import  { defaultStore } from './default'
export const authStore = defineStore('authStore', {
    state: () => ({
      token: useCookie('token'),
      login: useCookie('login')
    }),
    actions: {
      async authenticate(email: string, senha: string) {
        try {
          defaultStore().setLoading(true)
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

          const loginCookie = useCookie('login', {
            maxAge: 60*24*28,
            sameSite: true,
            secure: true,
          })
          loginCookie.value = email

          this.token = result.access_token
          this.login = email

        } catch (error) {
          this.logout()
        }finally{
          defaultStore().setLoading(false)
        }
  
      },
      async register(email: string, senha: string) {
        
        let result = await $fetch('/api/register',{
            method:'POST',
            body:{
              username: email,
              password: senha
            }
          })

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