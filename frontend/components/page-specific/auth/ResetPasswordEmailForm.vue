<script setup>
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const email = ref("")
const successMessage = ref("")
const errorMessage = ref("")

import { Configuration, DjRestAuthApi } from '@/lib/ApiClient'
const apiConfig = new Configuration({})
const client = new DjRestAuthApi(apiConfig)

const { data, status, error, refresh } = useAsyncData('reset_password', async () => {
  successMessage.value = ""
  errorMessage.value = ""

  // Validate email input
  if (!email.value) {
    errorMessage.value = "Please enter your email."
    return null
  }

  try {
    const response = await client.djRestAuthPasswordResetCreate({
      passwordReset: {
        email: email.value
      }
    })
    return response
  } catch (err) {
    console.log(err)
    errorMessage.value = "There was an error resetting the password."
    return null
  }
}, { immediate: false })

const handleChangePassword = async () => {
  await refresh()
  if (data.value) {
    successMessage.value = "Password reset link has been sent to your email."
  }
}
</script>

<template>
  <form :class="cn('flex flex-col gap-6')" @submit.prevent="handleChangePassword">
    <div class="flex flex-col items-center gap-2 text-center">
      <h1 class="text-2xl font-bold">
        Reset Password
      </h1>
      <p class="text-sm text-muted-foreground">
        Enter your email to reset your password
      </p>
    </div>
    <div class="grid gap-6">
      <div class="grid gap-2">
        <div class="flex items-center">
          <Label for="email">Email</Label>
        </div>
        <Input id="email" type="email" placeholder="m@example.com" v-model="email" required />
      </div>
      <Button type="submit" class="w-full" :disabled="status == 'pending'">
        <span v-if="status == 'pending'">Sending password reset...</span>
        <span v-else>Send Reset Link</span>
      </Button>
    </div>
    <!-- Success Message -->
    <p v-if="successMessage" class="text-green-500 text-sm text-center">
      {{ successMessage }}
    </p>
    <!-- Error Message -->
    <p v-if="errorMessage" class="text-red-500 text-sm text-center">
      {{ errorMessage }}
    </p>
  </form>
</template>
