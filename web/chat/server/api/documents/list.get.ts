

export default defineEventHandler(async (e) => {

    try {
       
       const { baseURL}  = useRuntimeConfig().public
       const data = await $fetch(`/listDocument`, {
          baseURL: baseURL,
          method: 'GET',
          timeout: 10000,
         
       });
       return data || []
 
    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })