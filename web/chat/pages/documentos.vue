<template>
    <main class="">
        <CardsDocuments></CardsDocuments>
        <SlideOversWithFooter  v-if="modaImportarArquivo" title="Importar Arquivo" @close="changeModaImportarArquivo(false)" >
            <template #content>
                <FormFormsImportarArquivo :clear-form="clearForm" :submit-form="submitForm" @close="changeModaImportarArquivo(false)" />
            </template>
            <template #footer>
                <div class="space-x-2">
                    <buttonsDefault @action="clearForm = !clearForm" label="Limpar" custom="white !text-black border hover:bg-gray-100" />
                    <buttonsDefault @action="submitForm = !submitForm" label="Enviar" custom="bg-green-500 hover:bg-green-600" />
                </div>
            </template>
        </SlideOversWithFooter>
        <div class="floating-button left-[50%] md:left-[60%]">
            <buttonsIcon label="Adicionar" @action="changeModaImportarArquivo(true)">
                <template #icon>
                    <PlusCircleIcon class="w-5 h-5"></PlusCircleIcon>
                </template>
            </buttonsIcon>
        </div>

    </main>

</template>

<script setup lang="ts">
import { EnvelopeIcon,PlusCircleIcon,TrashIcon } from '@heroicons/vue/20/solid'
import buttonsDefault from '@/components/buttons/default.vue'
import SlideOversWithFooter from '@/components/slideOvers/withFooter.vue'
const modaImportarArquivo = ref(false)
const changeModaImportarArquivo = (value: boolean) => modaImportarArquivo.value = value
const submitForm = ref(false)
const clearForm = ref(false)
</script>
<style scoped>
.floating-button {
    position: fixed;
    bottom: 20px;

    transform: translateX(-50%);
    z-index: 1000;
}

</style>