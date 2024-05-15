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
                            class="relative inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-br-lg border border-transparent py-4 text-sm font-semibold text-red-500">
                            <TrashIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
                            Excluir
                        </button>
                    </div>
                </div>
            </div>
        </li>
    </ul>

</template>

<script setup lang="ts">
import { Documents } from '@/models/Documents/List'
import { EnvelopeIcon, PlusCircleIcon, TrashIcon } from '@heroicons/vue/20/solid'

defineProps({
    listDocuments: Array<Documents>
})

const listDocuments = ref<Documents[]>([])
const getList = async () => {
    try {
        const response = await $fetch('/api/documents/list') as Documents[]
        listDocuments.value = response
    } catch (error) {
        console.error(error)
    }
}
onMounted(async () => {
    await getList()
})
</script>

<style scoped></style>