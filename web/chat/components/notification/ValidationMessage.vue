<template>
    <div>
        <span v-show="showMessage" class="text-red-500 text-sm p-1">{{message}}</span>
    </div>
</template>
<script setup>
    defineProps({
        message:String,
        showMessage:Boolean
    })
</script>