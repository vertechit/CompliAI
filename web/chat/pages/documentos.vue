<template>
    <main class="">
        <CardsDocuments :forceGetList="forceGetList"></CardsDocuments>
        <SlideOversWithFooter  v-if="modaImportarArquivo" title="Importar Arquivo" @close="changeModaImportarArquivo(false)" >
            <template #content>
                <FormFormsImportarArquivo :clear-form="clearForm" :submit-form="submitForm" :url-form="false" @close="forceGetList = !forceGetList ,changeModaImportarArquivo(false)"  />
            </template>
            <template #footer>
                <div class="space-x-2">
                    <buttonsDefault @action="clearForm = !clearForm" label="Limpar" custom="white !text-black border hover:bg-gray-100" />
                    <buttonsDefault @action="submitForm = !submitForm" label="Enviar" custom="bg-green-500 hover:bg-green-600" />
                </div>
            </template>
        </SlideOversWithFooter>

        <SlideOversWithFooter  v-if="modaImportarSite" title="Importar site" @close="changeModaImportarSite(false)" >
            <template #content>
                <FormFormsImportarArquivo :clear-form="clearForm" :submit-form="submitForm" :url-form="true" @close="forceGetList = !forceGetList ,changeModaImportarSite(false)"  />
            </template>
            <template #footer>
                <div class="space-x-2">
                    <buttonsDefault @action="clearForm = !clearForm" label="Limpar" custom="white !text-black border hover:bg-gray-100" />
                    <buttonsDefault @action="submitForm = !submitForm" label="Enviar" custom="bg-green-500 hover:bg-green-600" />
                </div>
            </template>
        </SlideOversWithFooter>

        <div class="group flex gap-x-3 floating-button left-[50%]">
            <div v-if="!defaultStorePinia.loading">
                <buttonsIcon label="Adicionar arquivo" @action="changeModaImportarArquivo(true)">
                    <template #icon>
                        <PlusCircleIcon class="w-5 h-5"></PlusCircleIcon>
                    </template>
                </buttonsIcon>
            </div>
            <div v-if="!defaultStorePinia.loading">
                <buttonsIcon label="Adicionar site" @action="changeModaImportarSite(true)">
                    <template #icon>
                        <PlusCircleIcon class="w-5 h-5"></PlusCircleIcon>
                    </template>
                </buttonsIcon>
            </div>
        </div>

    </main>
</template>

<script setup lang="ts">
  definePageMeta({
    middleware: 'auth'
  })
import { PlusCircleIcon } from '@heroicons/vue/20/solid'
import buttonsDefault from '@/components/buttons/default.vue'
import SlideOversWithFooter from '@/components/slideOvers/withFooter.vue'
import {defaultStore} from '@/stores/default'
const defaultStorePinia = defaultStore()
const modaImportarArquivo = ref(false)
const changeModaImportarArquivo = (value: boolean) => modaImportarArquivo.value = value

const modaImportarSite = ref(false)
const changeModaImportarSite = (value: boolean) => modaImportarSite.value = value

const submitForm = ref(false)
const clearForm = ref(false)
const forceGetList = ref(false)


</script>
<style scoped>
.floating-button {
    position: fixed;
    bottom: 20px;

    transform: translateX(-50%);
    z-index: 1000;
}

</style>