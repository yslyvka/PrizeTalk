<template>
  <section class="login-shell min-h-screen flex flex-col items-center justify-center px-4 md:px-[5%] py-6 bg-[var(--color-background)] text-[var(--color-text)]">
    <div class="text-center heading-section login-heading">
      <Title :level="1" class="text-[var(--color-heading)]">Sign-in to Award-Pulse</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Don't have an account?
        <RouterLink to="/signup" class="text-[var(--color-button-bg)] hover:underline font-semibold">Sign-up</RouterLink>
      </Paragraph>
    </div>

    <div class="login-card w-full max-w-xl space-y-8 rounded-2xl p-8 bg-[var(--color-background-soft)] border border-[var(--color-border)] shadow-lg">
      <div class="social-row flex flex-col items-center gap-3 sm:flex-row">
        <form class="w-full relative" action="/api/auth/signin/google" method="GET">
          <button type="submit"
            class="social-button w-full border border-[var(--color-border)] bg-[var(--color-background-soft)] text-[var(--color-text)] hover:border-[var(--color-border-hover)] rounded-[var(--button-radius)] py-2">
            <span class="inline-flex items-center justify-center gap-1 min-w-0 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="24" height="24" class="relative -left-2"></svg>
              <span>Sign-in with Google</span>
            </span>
          </button>
        </form>

        <form class="w-full relative" action="/api/auth/signin/apple" method="GET">
          <button type="submit"
            class="social-button w-full border border-[var(--color-border)] bg-[var(--color-background-soft)] text-[var(--color-text)] hover:border-[var(--color-border-hover)] rounded-[var(--button-radius)] py-2">
            <span class="inline-flex items-center justify-center gap-1 min-w-0 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" class="relative -left-2"></svg>
              <span>Sign-in with Apple</span>
            </span>
          </button>
        </form>
      </div>

      <div class="login-separator flex items-center justify-center gap-2">
        <div class="flex-grow h-px bg-[var(--color-border)]"></div>
        <span class="login-separator-text px-3 text-sm text-[var(--color-text-muted)]">or</span>
        <div class="flex-grow h-px bg-[var(--color-border)]"></div>
      </div>

      <form class="form-fields space-y-5" @submit.prevent="handleSubmit">
        <div v-if="errorMessage" class="rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
          {{ errorMessage }}
        </div>

        <div class="relative">
          <label for="email" class="login-label block text-sm text-[var(--color-text)]">Email</label>
          <svg class="login-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="example.user@gmail.com"
            required
            class="login-input w-full pl-10 pr-4 py-2 rounded-full bg-[var(--color-background-mute)] text-[var(--color-text)] border border-[var(--color-border)] focus:border-[var(--color-border-hover)] focus:outline-none"
          />
        </div>

        <div class="relative">
          <label for="password" class="login-label block text-sm text-[var(--color-text)]">Password</label>
          <svg class="login-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            id="password"
            placeholder="••••••••••••"
            required
            class="login-input w-full pl-10 pr-10 py-2 rounded-full bg-[var(--color-background-mute)] text-[var(--color-text)] border border-[var(--color-border)] focus:border-[var(--color-border-hover)] focus:outline-none"
          />
          <button type="button" @click="togglePasswordVisibility"
            class="password-toggle absolute right-3 top-8 h-5 w-5 text-[var(--color-text-muted)] hover:text-[var(--color-button-bg)]">
            <EyeSlashIcon v-if="showPassword" class="h-5 w-5" />
            <EyeIcon v-else class="h-5 w-5" />
          </button>

          <div class="flex items-center justify-between mt-1 text-sm">
            <label class="remember-label text-[var(--color-text-muted)] inline-flex items-center gap-2">
              <input v-model="rememberMe" type="checkbox" class="rounded border-[var(--color-border)] text-[var(--color-button-bg)] focus:ring-[var(--color-button-bg)]" />
              Remember me
            </label>
            <RouterLink to="/ForgotPassword" class="text-[var(--color-button-bg)] hover:underline font-semibold">Forgot your password?</RouterLink>
          </div>
        </div>

        <Button
          variant="primary"
          block
          type="submit"
          :disabled="isLoading"
          class="login-submit !rounded-full bg-[var(--color-button-bg)] text-[var(--color-button-text)] hover:bg-[var(--color-button-hover-bg)] py-3 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="inline-flex items-center gap-2 text-white">
            <svg class="h-5 w-5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-30" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-70" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Signing you in...
          </span>
          <span v-else>Log In</span>
        </Button>
      </form>

      <Paragraph align="center" class="text-xs text-[var(--color-text-muted)]">
        By signing in, you agree to our
        <RouterLink to="/Terms" class="text-[var(--color-button-bg)] hover:underline font-semibold">Terms</RouterLink>
        and
        <RouterLink to="/PrivacyPolicy" class="text-[var(--color-button-bg)] hover:underline font-semibold">Privacy Policy</RouterLink>
      </Paragraph>
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
