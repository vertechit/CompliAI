

export default defineEventHandler(async (e) => {

    try {
       
       const { baseURL}  = useRuntimeConfig().public
       const { id } = e.context.params || {}
       const data = await $fetch(`/deleteDocument/${id}`, {
          baseURL: baseURL,
          method: 'DELETE',
          timeout: 10000,
       });
       return data || []
 
    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })