<script setup>
import Navbar from "~/components/page-specific/navbar/Navbar.vue";
import ResetPasswordForm from "~/components/page-specific/auth/ResetPasswordForm.vue";

definePageMeta({
  middleware: "sidebase-auth",
  auth: { unauthenticatedOnly: true, navigateAuthenticatedTo: "/" },
});
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />

    <!-- Main Content -->
    <div class="flex-1 grid lg:grid-cols-2">
      <div class="flex flex-col gap-4 p-6 md:p-10 h-full">
        <div class="flex flex-1 items-center justify-center">
          <div class="w-full max-w-xs">
            <ResetPasswordForm />
          </div>
        </div>
      </div>
      <div class="relative hidden bg-muted lg:block">
        <img
          src="https://www.shadcn-vue.com/placeholder.svg"
          alt="Image"
          class="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
        />
      </div>
    </div>
  </div>
</template>
