<template>
    <div class="container-main">
        <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
            <div v-if="successMessage"
                class="flex justify-center sm:mx-auto sm:w-full sm:max-w-sm space-x-3 items-center p-4 mb-4 text-sm text-green-800 border border-green-300 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800"
                role="alert">
                <svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor" viewBox="0 0 20 20">
                    <path
                        d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z" />
                </svg>
                <span class="sr-only">Info</span>
                <div>
                    <span class="font-medium">Sucesso!</span> {{ successMessage }}
                </div>
            </div>
            <div class="flex justify-center sm:mx-auto sm:w-full sm:max-w-sm space-x-3">
                <img class="h-14 w-auto" src="~/assets/img/logo.png" alt="Compliance Soluções" />
                <!-- <Icon name="ri:robot-2-line" class="h-14 w-14 text-sky-500" color=""> </Icon> -->
                <!-- <Icon name="ri:robot-3-line" class="h-14 w-14 text-sky-500" color=""> </Icon> -->
                <!-- <Icon name="ri:robot-line" class="h-14 w-14 text-sky-500" color=""> </Icon>  -->
                <!-- <Icon name="fluent:bot-24-regular" class="h-14 w-14 text-sky-500" color=""> </Icon> -->
            </div>

            <div class="mt-5 sm:mx-auto sm:w-full sm:max-w-sm">
                <div class="space-y-3">
                    <div>
                        <div
                            :class="{'border-red-500': (errorMessage && !email)}" 
                            class="flex items-center w-full relative border-[1.5px] border-gray-300 rounded-lg px-2 focus:shadow">
                            <IconsMail />
                            <input id="email" name="email" autocomplete="off" placeholder="Email" v-model.trim="email" class="block w-full py-1.5 text-gray-900 shadow-sm 
                                ring-inset ring-gray-300 placeholder:text-gray-400 
                                focus:ring-0  sm:text-sm sm:leading-6 focus:outline-none
                                p-2  border-transparent  rounded-lg focus:border-transparent
                                "
                            
                                />
                        </div>
                    </div>
                    <div>
                        <div
                            :class="{'border-red-500': (errorMessage && !password)}" 
                            class="flex focus:bg-gray-800 items-center w-full relative border-[1.5px] border-gray-300 rounded-lg px-2 focus:shadow">
                            <IconsKey />
                            <input id="password" name="password" autocomplete="off" type="password" placeholder="Senha"
                                v-model="password" class="block w-full py-1.5 text-gray-900 shadow-sm 
                                ring-inset ring-gray-300 placeholder:text-gray-400 
                                focus:ring-0  sm:text-sm sm:leading-6 focus:outline-none
                                p-2  border-transparent  rounded-lg focus:border-transparent
                                "
                                />
                        </div>
                    </div>
                    <div class="mt-2">
                        <ButtonsDefault 
                            type="submit"
                            @click="handleSubmit"
                            custom="flex w-full justify-center rounded-lg bg-blue-600 
                                p-3  text-sm font-semibold leading-6 text-white shadow-sm 
                                hover:bg-blue-700 focus-visible:outline 
                                focus-visible:outline-2 focus-visible:outline-offset-2 
                                focus-visible:outline-blue-700" 
                            label="Entrar" 
                        />
                     
                        <!-- <button type="submit" @click="handleSubmit" class="flex 
                        w-full justify-center rounded-lg bg-blue-600 
                        p-3  text-sm font-semibold leading-6
                        text-white shadow-sm hover:bg-blue-700 focus-visible:outline 
                        focus-visible:outline-2 focus-visible:outline-offset-2 
                        focus-visible:outline-blue-700">Entrar</button> -->
                    </div>

                    <div class="">
                        <ButtonsDefault 
                            type="submit"
                            @click="registrar"
                            custom="flex w-full justify-center rounded-lg bg-white
                            !py-1.5
                                 text-sm font-semibold leading-6 text-sm text-black font-semibold leading-6
                        text-blue-600 border border-blue-600 shadow-sm hover:shadow-md hover:border-blue-800 hover:text-blue-800" 
                            label="Registrar" 

                        />
                        <!-- <button type="submit" @click="registrar"
                            class="flex 
                        w-full justify-center rounded-lg bg-white 
                        p-1  text-sm font-semibold leading-6
                        text-blue-600 border border-blue-600 shadow-sm hover:shadow-md hover:border-blue-800 hover:text-blue-800">Registrar</button> -->
                    </div>

                    <div class="text-red-500">{{ errorMessage }}</div>

                </div>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { authStore } from '@/stores/auth';
import ButtonsDefault from '@/components/buttons/default.vue'
definePageMeta({
    layout: false,
});

let email = '';
let password = '';
const route = useRoute();
const errorMessage = ref(route.query.message);
const successMessage = ref(route.query.successMessage);
const auth = authStore()
await auth.logout()

const handleSubmit = async () => {
    try {
        if (!email || !password) {
            errorMessage.value = 'Preencha todos os campos.'
            return
        }
        await auth.authenticate(email, password)
        await navigateTo('/home')
    } catch (error) {
        errorMessage.value = 'Erro no login. Verifique suas credenciais.'
    }
};

const registrar = async () => {
    try {
        await navigateTo('/register')
    } catch (error) {
    }
};

</script>
<style scoped>
.container-main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

input {
    padding: 8px;
}
</style>