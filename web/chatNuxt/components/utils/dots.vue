<template>
    <div class="typing">
        <span class="dot dot1">.</span>
        <span class="dot dot2">.</span>
        <span class="dot dot3">.</span>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
    .typing {
        display: inline-block;
        font-size: 24px;
        font-weight: bold;
    }

    @keyframes blink {
        0%, 20%, 100% {
            opacity: 1; 
        }
        50% {
            opacity: 0; 
        }
    }

    .dot {
        animation: blink 0.8s infinite; 
    }

    .dot1 {
        animation-delay: 0s;
    }

    .dot2 {
        animation-delay: 0.3s;
    }

    .dot3 {
        animation-delay: 0.6s;
    }
</style>