
export default defineEventHandler(async (e) => {

    try {
        const { pergunta } = await readBody(e)
        const { baseURL}  = useRuntimeConfig().public        
        const token = getRequestHeader(e, 'Authorization');

        const retorno = await $fetch(`/createSession`, {
            baseURL: baseURL,
            headers: {
                'Authorization': token+''
             },
            method: 'POST',
            body: {
                "Pergunta": pergunta
            },
            timeout: 300000,
        });
        return retorno

    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })