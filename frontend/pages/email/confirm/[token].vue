<script setup>
import { Configuration, DjRestAuthApi } from '@/lib/ApiClient'

// Api client
const apiConfig = new Configuration({})
const client = new DjRestAuthApi(apiConfig)

const route = useRoute()

const verifyEmail = async () => {
  try {
    await client.djRestAuthRegistrationVerifyEmailCreate2({
      verifyEmail: {
        key: route.params.token
      }
    })
    await navigateTo('/login')
  } catch (error) {
    await navigateTo('/')
  }
}

// Call the verifyEmail function
verifyEmail()
</script>
