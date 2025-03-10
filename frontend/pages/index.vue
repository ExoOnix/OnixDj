<script setup lang="ts">
import Navbar from '@/components/modules/navbar/Navbar.vue'
import { Button } from '@/components/ui/button'

const route = useRoute()


// const { token, setToken } = useAccessToken();

// import {Configuration, DjRestAuthApi } from '@/lib/ApiClient'
//  const apiConfig = new Configuration({
//   accessToken: () => {return token.value}
// })
// const client = new DjRestAuthApi(apiConfig);

</script>

<template>
  <div>
    <Navbar />

    <div class="py-12 text-center inter-montserrat svelte-ejp5be" style="margin-top: 100px; margin-bottom: 200px;">
      <div class="container mx-auto px-4" style="max-width: 70vw; width: 100%;">
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight lg:text-7xl">Accelerate Development by
          Using a Boilerplate</h1>
        <p class="mt-4 text-base">Streamline your development process with integrated authentication, powered by Vue and
          Django.</p>
        <Button variant="outline" class="mt-3" asChild><NuxtLink to="/register">Get Started</NuxtLink></Button>
      </div>
    </div>


  </div>
</template>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

  .montserrat-300 {
    font-family: "Montserrat", serif;
    font-optical-sizing: auto;
    font-weight: 300;
    font-style: normal;
  }

</style>