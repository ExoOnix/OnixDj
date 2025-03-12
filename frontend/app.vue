<script setup>

const { setToken } = useAccessToken(); // Get token from useAccessToken()


fetch('/api/dj-rest-auth/token/refresh/', 
{
  credentials: 'include', 
  method: 'POST' 
}).then(response => {
    if (!response.ok) {
        setToken("")
    }
    return response.json(); // Parse the response as JSON
})
.then(data => {
    console.log(data.access); // Handle the data from the response
    setToken(data.access)
})
.catch(error => {
    console.error('Fetch error:', error);
    setToken("")
});

</script>

<template>
  <div>
    <NuxtPage />
    <NuxtRouteAnnouncer />
  </div>
</template>

<style>
@import "~/assets/css/main.css";
</style>

