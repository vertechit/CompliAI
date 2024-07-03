
export default defineEventHandler(async (e) => {

    try {
        const { baseURL}  = useRuntimeConfig().public        
        const token = getRequestHeader(e, 'Authorization');
        const { titulo, description, url} = await readBody(e)
        await $fetch(`/createDocumentUrl`, {
            baseURL: baseURL,
            headers: {
                'Authorization': token+''
             },
            method: 'POST',
            body: {
                titulo,
                description,
                url
            },
            timeout: 10000,
        });

    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })