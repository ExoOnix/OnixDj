<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { defineComponent } from 'vue'

defineComponent({})
</script>


<template>
    <nav class="w-full p-4 bg-white shadow-md flex justify-between items-center">
        <div class="text-2xl font-bold">
            <NuxtLink to="/">Onix Boilerplate</NuxtLink>
        </div>
        <ul class="flex space-x-4">
            <Button asChild>
                <NuxtLink to="/login">Login</NuxtLink>
            </Button>
        </ul>
    </nav>
</template>


<style scoped>
/* Optional: Add custom styles here */
</style>
