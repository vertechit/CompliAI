<template>
    <div class="container-main">
        <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
            <div class="flex justify-center sm:mx-auto sm:w-full sm:max-w-sm space-x-3">
                <img class="h-14 w-auto" src="~/assets/img/logo.png" alt="Compliance Soluções" />
                 <!-- <Icon name="ri:robot-2-line" class="h-14 w-14 text-sky-500" color=""> </Icon> -->
                <!-- <Icon name="ri:robot-3-line" class="h-14 w-14 text-sky-500" color=""> </Icon> -->
                <!-- <Icon name="ri:robot-line" class="h-14 w-14 text-sky-500" color=""> </Icon>  -->
                <!-- <Icon name="fluent:bot-24-regular" class="h-14 w-14 text-sky-500" color=""> </Icon> -->
            </div>

            <div class="mt-5 sm:mx-auto sm:w-full sm:max-w-sm">
                <form class="space-y-3" action="#" method="POST">
                    <div>
                        <div class="flex items-center w-full relative border-[1.5px] border-gray-300 rounded-lg px-2 focus:shadow">
                        <IconsMail  />
                        <input id="email" name="email"  autocomplete="off" type="email" placeholder="Email" 
                        class="block w-full py-1.5 text-gray-900 shadow-sm 
                                ring-inset ring-gray-300 placeholder:text-gray-400 
                                focus:ring-0  sm:text-sm sm:leading-6 focus:outline-none
                                p-2  border-transparent  rounded-lg focus:border-transparent
                                " />
                        </div>
                    </div>
                    <div>
                        <div class="flex focus:bg-gray-800 items-center w-full relative border-[1.5px] border-gray-300 rounded-lg px-2 focus:shadow">
                            <IconsKey  />
                            <input id="password" name="password"     autocomplete="off" type="password" placeholder="Senha" 
                                class="block w-full py-1.5 text-gray-900 shadow-sm 
                                ring-inset ring-gray-300 placeholder:text-gray-400 
                                focus:ring-0  sm:text-sm sm:leading-6 focus:outline-none
                                p-2  border-transparent  rounded-lg focus:border-transparent
                                " />
                        </div>
                    </div>
                    <div class="mt-2">
                        <button type="submit" class="flex 
                        w-full justify-center rounded-lg bg-blue-600 
                        p-3  text-sm font-semibold leading-6
                        text-white shadow-sm hover:bg-blue-700 focus-visible:outline 
                        focus-visible:outline-2 focus-visible:outline-offset-2 
                        focus-visible:outline-blue-700">Entrar</button>
                    </div>
                   
                  
                </form>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
definePageMeta({
    layout: false
})
</script>
<style scoped>
.container-main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

input{
    padding: 8px;
}
</style>