

export default defineEventHandler(async (e) => {

    try {
       
       const { baseURL}  = useRuntimeConfig().public
       const { id } = e.context.params || {}
       const token = getRequestHeader(e, 'Authorization');
       const data = await $fetch(`/deleteSession/${id}`, {
          baseURL: baseURL,
          headers: {
            'Authorization': token+''
         },
          method: 'DELETE',
          timeout: 10000,
       });
       return data || []
 
    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })