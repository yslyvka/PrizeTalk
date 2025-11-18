<template>
  <section
    class="signup-shell min-h-screen flex flex-col items-center justify-center px-4 md:px-[5%] py-6
           bg-[var(--color-background)] text-[var(--color-text)]"
  >

    <div class="text-center heading-section signup-heading">
      <Title level="h1" class="text-[var(--color-heading)]">Sign-up for Award-Pulse</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Already have an account?
        <RouterLink to="/login" class="text-[var(--color-button-bg)] hover:underline font-semibold">Sign-in</RouterLink>
      </Paragraph>
    </div>

    <div
      class="signup-card w-full max-w-xl space-y-8 rounded-2xl p-8
             bg-[var(--color-background-soft)] border border-[var(--color-border)]"
    >

      <div class="social-row flex flex-col items-center gap-3 sm:flex-row">
        <form class="w-full relative" action="/api/auth/signin/google" method="GET">
          <button
            type="submit"
            class="social-button w-full rounded-[var(--button-radius)] py-2
                   border border-[var(--color-border)]
                   hover:border-[var(--color-border-hover)]
                   bg-[var(--color-background-soft)]
                   text-[var(--color-text)]"
          >
            <span class="inline-flex items-center justify-center gap-1 min-w-0 text-sm">
              <span>Sign-up with Google</span>
            </span>
          </button>
        </form>

        <form class="w-full relative" action="/api/auth/signin/apple" method="GET">
          <button
            type="submit"
            class="social-button w-full rounded-[var(--button-radius)] py-2
                   border border-[var(--color-border)]
                   hover:border-[var(--color-border-hover)]
                   bg-[var(--color-background-soft)]
                   text-[var(--color-text)]"
          >
            <span class="inline-flex items-center justify-center gap-1 min-w-0 text-sm">
              <span>Sign-up with Apple</span>
            </span>
          </button>
        </form>
      </div>

      <div class="signup-separator flex items-center justify-center gap-2">
        <div class="flex-grow h-px bg-[var(--color-border)]"></div>
        <span class="signup-separator-text px-3 text-sm text-[var(--color-text-muted)]">or</span>
        <div class="flex-grow h-px bg-[var(--color-border)]"></div>
      </div>

      <form class="form-fields space-y-5" @submit.prevent="handleSubmit">

        <div v-if="errorMessage" class="error-message bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span class="block sm:inline">{{ errorMessage }}</span>
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">First Name</label>
          <input
            v-model="firstName"
            type="text"
            placeholder="John"
            required
            class="signup-input w-full pl-4 pr-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Last Name</label>
          <input
            v-model="lastName"
            type="text"
            placeholder="Doe"
            required
            class="signup-input w-full pl-4 pr-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="example.user@gmail.com"
            required
            class="signup-input w-full pl-4 pr-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Password</label>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••••••"
            required
            class="signup-input w-full pl-4 pr-10 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
          <button type="button" @click="togglePasswordVisibility"
            class="absolute right-3 top-8 h-5 w-5 text-[var(--color-text-muted)]">
            <EyeSlashIcon v-if="showPassword" class="h-5 w-5" />
            <EyeIcon v-else class="h-5 w-5" />
          </button>
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Confirm Password</label>
          <input
            v-model="confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="••••••••••••"
            required
            class="signup-input w-full pl-4 pr-10 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
          <button type="button" @click="toggleConfirmPasswordVisibility"
            class="absolute right-3 top-8 h-5 w-5 text-[var(--color-text-muted)]">
            <EyeSlashIcon v-if="showConfirmPassword" class="h-5 w-5" />
            <EyeIcon v-else class="h-5 w-5" />
          </button>
        </div>

        <Button
          variant="primary"
          block
          type="submit"
          :disabled="isLoading"
          class="signup-submit !rounded-full
                 bg-[var(--color-button-bg)]
                 text-[var(--color-button-text)]
                 hover:bg-[var(--color-button-hover-bg)]
                 disabled:opacity-50">
          <span v-if="isLoading" class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Signing up...
          </span>
          <span v-else>Sign-up</span>
        </Button>

      </form>

      <Paragraph align="center" class="signup-terms text-xs text-center text-[var(--color-text-muted)]">
        By signing-up, you agree to our
        <RouterLink to="/Terms" class="text-[var(--color-button-bg)] hover:underline font-semibold">Terms</RouterLink> and
        <RouterLink to="/PrivacyPolicy" class="text-[var(--color-button-bg)] hover:underline font-semibold">Privacy Policy</RouterLink>
      </Paragraph>

    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await axios.post('/api/signup', {
      firstName: firstName.value,
      lastName: lastName.value,
      email: email.value,
      password: password.value
    })
    if (response.data.success) {
      // Signup successful, redirect to login
      router.push('/login')
    } else {
      errorMessage.value = response.data.message || 'Signup failed'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Signup failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}
</script>
