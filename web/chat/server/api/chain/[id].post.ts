

export default defineEventHandler(async (e) => {

   try {
      const { baseURL}  = useRuntimeConfig().public
      const { id } = e.context.params || {}
      const { SystemMessage, HumamMessage} = await readBody(e)
      const token = getRequestHeader(e, 'Authorization');
      const data = await $fetch(`/graph/${id}`, {
         baseURL: baseURL,
         method: 'POST',
         timeout: 1000000,
         headers: {
            'Authorization': token+''
         },
         body: { 
            SystemMessage,
            HumamMessage
         },
        
      });
      return data || []

   } catch (error:any) {
      console.log(error)
      throw error
   }

})