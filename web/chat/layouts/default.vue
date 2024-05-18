<template>
    <sideBar>
        <NuxtPage ></NuxtPage>
    </sideBar>
    <Loader :loading="defaultStorePinia.loading" />
    <NotificationList />
    
</template>
<script setup>
import {defaultStore} from '@/stores/default'
import Loader from '@/components/Loader.vue'
import NotificationList from '@/components/notification/List.vue'
const defaultStorePinia = defaultStore()

</script>