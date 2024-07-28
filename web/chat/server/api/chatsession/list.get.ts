import {useMyFetchServer} from '@/composables/useMyFetchServer'
export default defineEventHandler(async (e) => {
    try {
       const data = await useMyFetchServer(`/listSession`, {
          method: 'GET',
          timeout: 10000,
       },e);
       return data || []
 
    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })