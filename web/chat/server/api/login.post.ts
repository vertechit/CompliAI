

export default defineEventHandler(async (e) => {

   try {
      
      const { baseURL}  = useRuntimeConfig().public
      const { username, password} = await readBody(e)

      const params = {
         username: username,
         password: password,
       };
      const urlSearchParams = new URLSearchParams(params);
      const encodedData = urlSearchParams.toString();

      const data = await $fetch(`/token`, {
         baseURL: baseURL,
         method: 'POST',
         timeout: 10000,
         headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
         body: encodedData,
        
      });
      return data || []

   } catch (error:any) {
      throw error
   }

})