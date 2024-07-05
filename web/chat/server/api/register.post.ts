

export default defineEventHandler(async (e) => {

   try {
      
      const { baseURL}  = useRuntimeConfig().public
      const { username, password} = await readBody(e)

      const data = await $fetch(`/createUsers`, {
         baseURL: baseURL,
         method: 'POST',
         timeout: 10000,
         body: {
            username,
            password
         },
        
      });
      return data || []

   } catch (error:any) {
      throw error
   }

})