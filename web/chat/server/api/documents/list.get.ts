

export default defineEventHandler(async (e) => {

    try {
       const token = getRequestHeader(e, 'Authorization');
       const { baseURL}  = useRuntimeConfig().public
       const data = await $fetch(`/listDocument?folder_id=1`, {
          baseURL: baseURL,
          method: 'GET',
          headers: {
            'Authorization': token+''
          },
          timeout: 10000,
         
       });
       return data || []
 
    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })