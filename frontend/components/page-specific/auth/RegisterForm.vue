<script setup>
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Configuration, DjRestAuthApi } from "@/lib/ApiClient";

const { signIn } = useAuth();

const email = ref("");
const password1 = ref("");
const password2 = ref("");

// Api client
const apiConfig = new Configuration({
  basePath: useRuntimeConfig().public.SiteHost,
});
const client = new DjRestAuthApi(apiConfig);

const successMessage = ref("");
const errorMessage = ref("");

const { data, status, error, refresh } = useAsyncData(
  "register",
  async () => {
    successMessage.value = "";
    errorMessage.value = "";
    if (!email.value || !password1.value || !password2.value) return null;
    try {
      return await client.djRestAuthRegistrationCreate({
        customRegister: {
          email: email.value,
          password1: password1.value,
          password2: password2.value,
        },
      });
    } catch (err) {
      const errResponse = await err.response.json();
      let allErrors = [];
      for (let key in errResponse) {
        if (Array.isArray(errResponse[key])) {
          allErrors = [...allErrors, ...errResponse[key]]; // Add each array of error messages
        }
      }

      // Join them into one string to print
      errorMessage.value = allErrors.join(" ");
      console.log(errorMessage);
    }
  },
  { immediate: false },
);

const handleRegister = async () => {
  await refresh();
  if (data.value) {
    successMessage.value = "Verification e-mail sent";
    console.log("Register successful:", data.value.detail);
  }
};

const handleResend = async () => {
  try {
    const response = await client.djRestAuthRegistrationResendEmailCreate({
      resendEmailVerification: {
        email: email.value,
      },
    });
    successMessage.value = "Registration email resent";
    errorMessage.value = "";
  } catch (err) {
    successMessage.value = "";
    errorMessage.value =
      "Can not resend email, have you entered a valid email?";
  }
};

const handleGithub = async () => {
  const res = await signIn("github");

  if (res?.error) {
    errorMessage.value = true;
  } else {
    await navigateTo("/");
  }
};
</script>

<template>
  <form :class="cn('flex flex-col gap-6')" @submit.prevent="handleRegister">
    <div class="flex flex-col items-center gap-2 text-center">
      <h1 class="text-2xl font-bold">Create a new account</h1>
      <p class="text-balance text-sm text-muted-foreground">
        Enter your email and password to sign up
      </p>
    </div>
    <div class="grid gap-6">
      <div class="grid gap-2">
        <Label for="email"
          >Email.
          <span class="underline cursor-pointer" @click="handleResend"
            >To Resend Email</span
          ></Label
        >
        <Input
          id="email"
          type="email"
          placeholder="m@example.com"
          v-model="email"
          required
        />
      </div>
      <div class="grid gap-2">
        <Label for="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          v-model="password1"
          required
        />
      </div>
      <div class="grid gap-2">
        <Label for="confirmPassword">Confirm Password</Label>
        <Input
          id="confirmPassword"
          type="password"
          placeholder="••••••••"
          v-model="password2"
          required
        />
      </div>
      <Button type="submit" class="w-full" :disabled="status == 'pending'">
        <span v-if="status == 'pending'">Signing in...</span>
        <span v-else>Sign Up</span>
      </Button>
    </div>
    <p v-if="successMessage" class="text-green-500 text-sm text-center">
      {{ successMessage }}. If you have not recieved an email,
      <span class="underline cursor-pointer" @click="handleResend"
        >click here.</span
      >
    </p>
    <p v-if="errorMessage" class="text-red-500 text-sm text-center">
      {{ errorMessage }}
    </p>
  </form>
  <div>
    <div
      style="margin-top: 15px"
      class="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border"
    >
      <span class="relative z-10 bg-background px-2 text-muted-foreground">
        Or continue with
      </span>
    </div>
    <Button
      style="margin-top: 15px"
      variant="outline"
      class="w-full"
      @click="handleGithub"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path
          d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
          fill="currentColor"
        />
      </svg>
      Sign up with GitHub
    </Button>
    <div style="margin-top: 15px" class="text-center text-sm">
      Already have an account?
      <NuxtLink to="/login" class="underline underline-offset-4">
        Login
      </NuxtLink>
    </div>
  </div>
</template>
