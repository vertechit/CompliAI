<template>
    <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5 mt-2 mr-4">
        <li v-for="document in listDocuments" :key="document.documento_id"
            class="col-span-1 divide-y divide-gray-200 rounded-lg bg-white shadow-md ">
            <div class="flex w-full items-center justify-between space-x-6 p-6">
                <div class="flex-1 truncate">
                    <div class="flex items-center space-x-3">
                        <h3 class="truncate text-sm font-medium text-gray-900" v-tooltip="document.titulo" >{{ document.titulo }}</h3>

                    </div>
                    <p class="mt-1 truncate text-sm text-gray-500" v-tooltip="document.descricao">{{ document.descricao }}</p>
                </div>
                <div class="flex items-center justify-center h-15 w-15 flex-shrink-0 rounded-full ">
                    <IconsPdf />
                </div>
            </div>
            <div>
                <div class="-mt-px flex divide-x divide-gray-200">
                    <div class="-ml-px flex w-0 flex-1">
                        <button
                            @click="isOpenModalDelete = true; currentElement = document.documento_id"
                            class="relative inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-br-lg border border-transparent py-4 text-sm font-semibold text-red-500">
                            <TrashIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
                            Excluir
                        </button>
                    </div>
                </div>
            </div>
        </li>
    </ul>
    <ModalConfirmDelete
    title="Atenção"
    text="Deseja realmente excluir o documento?"
    :isOpen="isOpenModalDelete"
    @confirm="deleteDocument(currentElement)"
    @close="close()"
    >

    </ModalConfirmDelete>

</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { type Documents } from '@/models/Documents/List'
import { TrashIcon } from '@heroicons/vue/20/solid'
import {defaultStore} from '@/stores/default'
const defaultStorePinia = defaultStore()
const props = defineProps({
    listDocuments: Array<Documents>,
    forceGetList: Boolean
})
const isOpenModalDelete = ref(false)
const listDocuments = ref<Documents[]>([])
const auth = authStore()
let currentElement = ref(0)
const getList = async () => {
    try {
        setLoading(true)
        const token = auth.token
        const response = await $fetch('/api/documents/list',{
            headers: {
                "Authorization" :"bearer "+token
            }
        }) as Documents[]
        listDocuments.value = response
    } catch (error) {
        clearError({ redirect: '/login?message=Token expirado' })
    }finally{
        setLoading(false)
    }
}
const close = async () => {
    isOpenModalDelete.value = false;
    currentElement.value = 0
}

const deleteDocument = async (documentId: number) => {
    try {
        setLoading(true)
        const token = auth.token
        try{
            await $fetch(`/api/documents/${documentId}`, {
            method: 'DELETE',
            headers: {
                "Authorization" :"bearer "+token
            }
            })
        }catch(error){
            clearError({ redirect: '/login?message=Token expirado' })
        }

        await getList()
    } catch (error) {
        console.error(error)
    }finally{
        setLoading(false)
        currentElement.value = 0
        isOpenModalDelete.value = false
    }
}
const setLoading = (loading:boolean) => {
    defaultStorePinia.setLoading(loading)
  }
onMounted(async () => {
    await getList()
})
watch(() => props.forceGetList, async() => {
    await getList()
})
</script>

<style scoped></style>