import {basename,extname} from 'path'
export default defineEventHandler(async (e) => {

    try {
        const formData = await readFormData(e)
        let file = formData.get('file') as File
        let name = file.name
        let filenameWithoutExtension = basename(name, extname(name));
        let newFormData = new FormData();
        newFormData.append('file', file);
        let description = formData.get('description') as string
        
        const { baseURL}  = useRuntimeConfig().public
        await $fetch(`/createDocument/?filename=${filenameWithoutExtension}&description=${description}`, {
            baseURL: baseURL,
            method: 'POST',
            body:newFormData,
            timeout: 10000,
        });

    } catch (error:any) {
       console.log(error)
       throw error
    }
 
 })