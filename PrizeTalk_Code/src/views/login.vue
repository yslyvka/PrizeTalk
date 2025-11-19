<template>
  <section class="login-shell min-h-screen flex flex-col items-center justify-center px-4 py-10 md:px-[5%] bg-[var(--color-background)] text-[var(--color-text)]">
    <div class="text-center space-y-3">
      <Title :level="1" :class="'text-3xl md:text-4xl text-[var(--color-heading)]'">Welcome back to Award-Pulse</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Don't have an account?
        <RouterLink to="/signup" class="text-[var(--color-button-bg)] font-semibold hover:underline">Create one</RouterLink>
      </Paragraph>
    </div>

    <div class="login-card mt-10 w-full max-w-xl rounded-3xl border border-[var(--color-border)] bg-[var(--color-background-soft)]/80 shadow-xl backdrop-blur-sm">
      <div class="border-b border-[var(--color-border)] px-8 py-6">
        <Paragraph align="center" class="text-sm text-[var(--color-text-muted)]">
          Sign in with one of your social accounts
        </Paragraph>
        <div class="mt-4 grid gap-3 sm:grid-cols-2">
          <button
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-full border border-[var(--color-border)] bg-white px-5 py-2 text-sm font-semibold text-[var(--color-text)] shadow-sm hover:border-[var(--color-border-hover)] hover:bg-white/80"
          >
            <span class="inline-flex items-center gap-2">
              <span class="h-5 w-5 rounded-full bg-gradient-to-tr from-blue-500 via-red-500 to-yellow-400" />
              Google
            </span>
          </button>
          <button
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-full border border-[var(--color-border)] bg-white px-5 py-2 text-sm font-semibold text-[var(--color-text)] shadow-sm hover:border-[var(--color-border-hover)] hover:bg-white/80"
          >
            <span class="inline-flex items-center gap-2">
              <span class="h-5 w-5 rounded-full bg-black" />
              Apple
            </span>
          </button>
        </div>
      </div>

      <div class="px-8 py-6">
        <div class="flex items-center gap-4 text-sm text-[var(--color-text-muted)]">
          <div class="h-px flex-1 bg-[var(--color-border)]" />
          <span>or continue with email</span>
          <div class="h-px flex-1 bg-[var(--color-border)]" />
        </div>

        <form class="mt-6 space-y-6" @submit.prevent="handleSubmit">
          <div v-if="errorMessage" class="rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {{ errorMessage }}
          </div>

          <div class="space-y-2">
            <label for="email" class="block text-sm font-semibold text-[var(--color-heading)]">Email address</label>
            <div class="relative">
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="you@example.com"
                required
                class="login-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
              />
            </div>
          </div>

          <div class="space-y-2">
            <label for="password" class="block text-sm font-semibold text-[var(--color-heading)]">Password</label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter your password"
                required
                class="login-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
              />
              <button
                type="button"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] hover:text-[var(--color-button-bg)]"
                @click="togglePasswordVisibility"
              >
                <EyeSlashIcon v-if="showPassword" class="h-5 w-5" />
                <EyeIcon v-else class="h-5 w-5" />
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm">
            <label class="inline-flex items-center gap-2 text-[var(--color-text-muted)]">
              <input v-model="rememberMe" type="checkbox" class="h-4 w-4 rounded border-[var(--color-border)] text-[var(--color-button-bg)] focus:ring-[var(--color-button-bg)]" />
              Remember me
            </label>
            <RouterLink to="/ForgotPassword" class="font-semibold text-[var(--color-button-bg)] hover:underline">
              Forgot password?
            </RouterLink>
          </div>

          <Button
            variant="primary"
            block
            type="submit"
            :disabled="isLoading"
            class="!rounded-full bg-[var(--color-button-bg)] py-3 text-base font-semibold shadow-lg shadow-[var(--color-button-bg)]/30 transition hover:translate-y-0.5 hover:bg-[var(--color-button-hover-bg)] disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="inline-flex items-center gap-2">
              <svg class="h-5 w-5 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-30" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-70" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Signing you in...
            </span>
            <span v-else>Sign in</span>
          </Button>
        </form>
      </div>

      <div class="rounded-b-3xl border-t border-[var(--color-border)] bg-[var(--color-background-soft)] px-8 py-5 text-center">
        <Paragraph align="center" class="text-xs text-[var(--color-text-muted)]">
          By signing in, you agree to our
          <RouterLink to="/Terms" class="font-semibold text-[var(--color-button-bg)] hover:underline">Terms</RouterLink>
          and
          <RouterLink to="/PrivacyPolicy" class="font-semibold text-[var(--color-button-bg)] hover:underline">Privacy Policy</RouterLink>
        </Paragraph>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Title from '../components/BasicComponents/Title.vue'
import Paragraph from '../components/BasicComponents/Paragraph.vue'
import Button from '../components/BasicComponents/Button.vue'
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await axios.post('/api/login', {
      email: email.value,
      password: password.value
    })
    if (response.data.success) {
      localStorage.setItem('loggedIn', 'true')
      router.push('/awards')
    } else {
      errorMessage.value = 'Invalid credentials'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>
