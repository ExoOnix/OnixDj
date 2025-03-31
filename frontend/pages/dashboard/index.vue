<script setup>
import Navbar from "@/components/page-specific/navbar/Navbar.vue";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

definePageMeta({
  middleware: "sidebase-auth",
  auth: true,
});

const { getSession } = useAuth()

import {Configuration, TodoApi } from '@/lib/ApiClient'
const apiConfig = new Configuration({
  basePath: useRuntimeConfig().public.SiteHost,
  accessToken: async () => {
    const values = await getSession()
    return values['access_token'];
  }
})
const client = new TodoApi(apiConfig);

const { data, status, error, refresh, clear } = useAsyncData(
    'todo',
    async () => {
        const response = await client.todoList()
        console.log(response)
        return response
    }
)

refresh()
</script>



<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />
        <div v-for="todo in data">
            {{ todo.title }}
        </div>
        <div class="flex justify-center items-center flex-grow">
            <div class="w-4/5 mx-auto">
                <Table class="w-full">
                    <TableCaption>A list of your recent invoices.</TableCaption>
                    <TableHeader>
                        <TableRow>
                            <TableHead class="w-[100px]">Invoice</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Method</TableHead>
                            <TableHead class="text-right">Amount</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        <TableRow>
                            <TableCell class="font-medium">INV001</TableCell>
                            <TableCell>Paid</TableCell>
                            <TableCell>Credit Card</TableCell>
                            <TableCell class="text-right">$250.00</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        </div>
    </div>
</template>
