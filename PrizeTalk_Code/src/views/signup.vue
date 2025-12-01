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
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="24" height="24" class="relative -left-2"></svg>
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
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="relative -left-2"></svg>
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

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">First Name</label>
          <input
            v-model="firstName"
            type="text"
            placeholder="John"
            required
            class="signup-input w-full px-4 py-2 rounded-full
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
            class="signup-input w-full px-4 py-2 rounded-full
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
            class="signup-input w-full px-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Role</label>
          <select
            v-model="role"
            required
            class="signup-input w-full px-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          >
            <option value="" disabled>Select a role</option>
            <option
              v-for="option in roleOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••••••"
            required
            class="signup-input w-full px-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Confirm Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="••••••••••••"
            required
            class="signup-input w-full px-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <Button
          variant="primary"
          block
          type="submit"
          :disabled="isSubmitting"
          class="signup-submit !rounded-full
                 bg-[var(--color-button-bg)]
                 text-[var(--color-button-text)]
                 hover:bg-[var(--color-button-hover-bg)]"
        >
          <span v-if="isSubmitting">Creating your account...</span>
          <span v-else>Sign-up</span>
        </Button>

        <p v-if="submitError" class="text-sm text-red-500 text-center">
          {{ submitError }}
        </p>
        <p v-if="submitSuccess" class="text-sm text-emerald-400 text-center">
          {{ submitSuccess }}
        </p>

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
import { useRouter } from 'vue-router'
import axios from 'axios'
import Title from '../components/BasicComponents/Title.vue'
import Paragraph from '../components/BasicComponents/Paragraph.vue'
import Button from '../components/BasicComponents/Button.vue'

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const roleOptions = [
  { value: 'staff_admin', label: 'Staff Admin' },
  { value: 'admin', label: 'Administrator' },
  { value: 'moderator', label: 'Moderator' },
  { value: 'data_curator', label: 'Data Curator' },
  { value: 'user', label: 'Member' },
]
const defaultRole = roleOptions[0]?.value || 'staff_admin'
const role = ref(defaultRole)
const isSubmitting = ref(false)
const submitError = ref('')
const submitSuccess = ref('')
const router = useRouter()

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const handleSubmit = () => {
  submitError.value = ''
  submitSuccess.value = ''

  if (password.value !== confirmPassword.value) {
    submitError.value = 'Passwords do not match.'
    return
  }

  isSubmitting.value = true

  axios
    .post(`${API_BASE_URL}/api/auth/signup/`, {
      firstName: firstName.value,
      lastName: lastName.value,
      email: email.value,
      password: password.value,
      role: role.value,
    })
    .then(({ data }) => {
      submitError.value = ''
      submitSuccess.value = data?.message || 'Account created successfully.'

      try {
        const payload = {
          email: email.value,
          role: data?.user?.role || role.value,
          firstName: firstName.value,
          lastName: lastName.value,
        }
        window.localStorage.setItem('ap_staff_auth', JSON.stringify(payload))
        window.localStorage.setItem('loggedIn', 'true')
        window.dispatchEvent(
          new CustomEvent('staff-auth-changed', {
            detail: { isLoggedIn: true, user: payload },
          }),
        )
        window.dispatchEvent(new Event('auth-state-changed'))
      } catch (e) {
        console.error('Failed to persist staff auth state', e)
      }

      router.push('/awards')
    })
    .catch((error) => {
      console.error(error)
      submitSuccess.value = ''
      if (error.response?.data?.errors) {
        const errs = error.response.data.errors
        submitError.value = Object.values(errs).join(' ')
      } else if (error.response?.data?.message) {
        submitError.value = error.response.data.message
      } else {
        submitError.value = 'Failed to create account. Please try again.'
      }
    })
    .finally(() => {
      isSubmitting.value = false
    })
}
</script>

<style scoped>
.signup-card {
  max-width: 28rem !important;
}

.signup-input {
  max-width: 100%;
}

.signup-separator {
  display: flex;
}

.signup-separator-text {
  text-transform: lowercase;
}

.signup-shell {
  background: var(--color-background);
}

/* Override to fix field overflow */
.signup-input {
  width: 100% !important;
  box-sizing: border-box !important;
}
</style>
