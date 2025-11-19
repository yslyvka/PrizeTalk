<template>
  <section class="signup-shell min-h-screen flex flex-col items-center justify-center px-4 py-10 md:px-[5%] bg-[var(--color-background)] text-[var(--color-text)]">
    <div class="text-center space-y-3">
      <Title :level="1" :class="'text-3xl md:text-4xl text-[var(--color-heading)]'">Create your Award-Pulse account</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Already have an account?
        <RouterLink to="/login" class="text-[var(--color-button-bg)] font-semibold hover:underline">Sign in</RouterLink>
      </Paragraph>
    </div>

    <div class="signup-card mt-10 w-full max-w-3xl overflow-hidden rounded-3xl border border-[var(--color-border)] bg-[var(--color-background-soft)]/80 shadow-xl backdrop-blur-sm">
      <div class="border-b border-[var(--color-border)] px-8 py-6">
        <Paragraph align="center" class="text-sm text-[var(--color-text-muted)]">
          Continue with one of your existing accounts
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
          <span>or sign up with email</span>
          <div class="h-px flex-1 bg-[var(--color-border)]" />
        </div>

        <form class="mt-6 space-y-6" @submit.prevent="handleSubmit">
          <div v-if="errorMessage" class="rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {{ errorMessage }}
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-[var(--color-heading)]" for="first-name">First name</label>
              <div class="relative">
                <input
                  id="first-name"
                  v-model="firstName"
                  type="text"
                  placeholder="Jane"
                  required
                  class="signup-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
                />
              </div>
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-[var(--color-heading)]" for="last-name">Last name</label>
              <div class="relative">
                <input
                  id="last-name"
                  v-model="lastName"
                  type="text"
                  placeholder="Doe"
                  required
                  class="signup-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
                />
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <label class="block text-sm font-semibold text-[var(--color-heading)]" for="email">Email address</label>
            <div class="relative">
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="you@example.com"
                required
                class="signup-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
              />
            </div>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-[var(--color-heading)]" for="password">Password</label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Create a secure password"
                  required
                  class="signup-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
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
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-[var(--color-heading)]" for="confirm-password">Confirm password</label>
              <div class="relative">
                <input
                  id="confirm-password"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="Repeat your password"
                  required
                  class="signup-input w-full rounded-full border border-[var(--color-border)] bg-[var(--color-background-mute)] px-4 py-3 text-sm transition focus:border-[var(--color-button-bg)] focus:outline-none focus:ring-2 focus:ring-[var(--color-button-bg)]/30"
                />
                <button
                  type="button"
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] hover:text-[var(--color-button-bg)]"
                  @click="toggleConfirmPasswordVisibility"
                >
                  <EyeSlashIcon v-if="showConfirmPassword" class="h-5 w-5" />
                  <EyeIcon v-else class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>

          <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-background-mute)]/60 px-5 py-4 text-sm text-[var(--color-text-muted)]">
            Passwords must be at least 8 characters and include a mix of letters and numbers.
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
              Creating your account...
            </span>
            <span v-else>Create account</span>
          </Button>
        </form>
      </div>

      <div class="border-t border-[var(--color-border)] bg-[var(--color-background-soft)] px-8 py-5 text-center">
        <Paragraph align="center" class="text-xs text-[var(--color-text-muted)]">
          By signing up, you agree to our
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
