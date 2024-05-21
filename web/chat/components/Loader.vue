<template>
    <div>
        <div v-if="loading" class="z-50 fixed inset-0 p-10 bg-white bg-opacity-50 flex justify-center items-center">
            <UtilsDots height="3em" width="3em" fill="#3b82f6"></UtilsDots>
        </div>
    </div>
</template>

<script setup>
    
    const props = defineProps({
        loading: {
            type: Boolean,
            default: false
        }
    })

</script>

<style scoped>

    .load_animation{
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        position: relative;
    }
    .load_percent {
        position: absolute;
        bottom: 40px;
        font-size: .65rem;
        font-weight: 700;
        color: #0480b9;
        margin-top: 1px;
        z-index: 200;
    }
    .load_animation_1, .load_animation_2, .load_animation_3 {
        position: relative;
        width: 5px;
        height: 5px;
        background: #0480b9;
        margin: 3px;
        border-radius: 5px;
    }

    .load_animation_1 {
        -webkit-animation: scale .8s ease infinite;
        animation: scale .8s ease infinite;
    }

    .load_animation_2 {
        -webkit-animation: scale .8s ease .2s infinite;
        animation: scale .8s ease .2s infinite;
    }
    .load_animation_3 {
        -webkit-animation: scale .8s ease .4s infinite;
        animation: scale .8s ease .4s infinite;
    }

    @keyframes scale {
        50% { height: 25px; }
        0%{ height:5px }
    }
</style>