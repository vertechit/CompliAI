

export default defineEventHandler(async (e) => {

   try {
      
      const { baseURL}  = useRuntimeConfig().public
      const { SystemMessage, HumamMessage} = await readBody(e)
      const data = await $fetch(`/chain`, {
         baseURL: baseURL,
         method: 'POST',
         timeout: 10000,
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