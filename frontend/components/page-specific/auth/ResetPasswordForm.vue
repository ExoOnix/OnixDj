<script setup>
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const newPassword1 = ref("");
const newPassword2 = ref("");
const successMessage = ref("");
const errorMessage = ref("");

const route = useRoute();

import { Configuration, DjRestAuthApi } from "@/lib/ApiClient";
const apiConfig = new Configuration({
  basePath: useRuntimeConfig().public.SiteHost,
});
const client = new DjRestAuthApi(apiConfig);

const { data, status, error, refresh } = useAsyncData(
  "reset_password",
  async () => {
    successMessage.value = "";
    errorMessage.value = "";
    if (!newPassword1.value || !newPassword2.value) return null;
    try {
      const response = await client.djRestAuthPasswordResetConfirmCreate({
        passwordResetConfirm: {
          newPassword1: newPassword1.value,
          newPassword2: newPassword2.value,
          uid: route.params.uid,
          token: route.params.token,
        },
      });
      return response;
    } catch (err) {
      errorMessage.value = "There was an error resetting your password.";
      return null;
    }
  },
  { immediate: false },
);

const handleChangePassword = async () => {
  await refresh();
  if (data.value) {
    successMessage.value = "Password reset successfully";
    await navigateTo("/login");
  }
};
</script>

<template>
  <form
    :class="cn('flex flex-col gap-6')"
    @submit.prevent="handleChangePassword"
  >
    <div class="flex flex-col items-center gap-2 text-center">
      <h1 class="text-2xl font-bold">Reset password</h1>
      <p class="text-sm text-muted-foreground">Set your new password</p>
    </div>
    <div class="grid gap-6">
      <div class="grid gap-2">
        <div class="flex items-center">
          <Label for="password">Password 1</Label>
        </div>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          v-model="newPassword1"
          required
        />
      </div>
      <div class="grid gap-2">
        <div class="flex items-center">
          <Label for="password">Password 2</Label>
        </div>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          v-model="newPassword2"
          required
        />
      </div>
      <Button type="submit" class="w-full" :disabled="status == 'pending'">
        <span v-if="status == 'pending'">Reseting password...</span>
        <span v-else>Reset Password</span>
      </Button>
    </div>
    <p v-if="successMessage" class="text-green-500 text-sm text-center">
      {{ successMessage }}
    </p>
    <p v-if="errorMessage" class="text-red-500 text-sm text-center">
      {{ errorMessage }}
    </p>
  </form>
</template>
