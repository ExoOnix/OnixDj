<script setup>
import { Button } from '@/components/ui/button'
// Dropdown
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

// Icons
import { User } from 'lucide-vue-next';


const { status, getSession, signOut } = useAuth()
const loggedIn = computed(() => status.value === "authenticated")


const handleLogout = async () => {
    const values = await getSession()
    console.log(values['refresh_token'])
    const response = await fetch('/api/dj-rest-auth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({refresh: values['refresh_token']}),
    });
    // console.log(response)
    signOut({ callbackUrl: '/' })

}
</script>


<template>
    <nav class="w-full p-4 bg-white shadow-md flex justify-between items-center">
        <div class="text-2xl font-bold">
            <NuxtLink to="/">Onix Boilerplate</NuxtLink>
        </div>
        <ul class="flex space-x-4">
            <Button v-if="!loggedIn" as-child>
                <NuxtLink to="/login">Login</NuxtLink>
            </Button>
            <DropdownMenu v-else>
                <DropdownMenuTrigger as-child>
                    <Button variant="outline" size="icon">
                        <User />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                    <DropdownMenuLabel>My Account</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem @click="handleLogout">
                        Logout
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </ul>
    </nav>
</template>