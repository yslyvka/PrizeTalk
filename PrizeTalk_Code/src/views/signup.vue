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
          <svg class="signup-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="firstName"
            type="text"
            placeholder="John"
            required
            class="signup-input w-full pl-10 pr-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Last Name</label>
          <svg class="signup-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="lastName"
            type="text"
            placeholder="Doe"
            required
            class="signup-input w-full pl-10 pr-4 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Email</label>
          <svg class="signup-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="email"
            type="email"
            placeholder="example.user@gmail.com"
            required
            class="signup-input w-full pl-10 pr-4 py-2 rounded-full
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
            <option value="staff_admin">Staff Admin</option>
          </select>
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Password</label>
          <svg class="signup-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••••••"
            required
            class="signup-input w-full pl-10 pr-10 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="password-toggle absolute right-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"
            :class="{ 'is-active': showPassword }"
          ></button>
        </div>

        <div class="relative">
          <label class="signup-label block text-sm text-[var(--color-text)]">Confirm Password</label>
          <svg class="signup-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="••••••••••••"
            required
            class="signup-input w-full pl-10 pr-10 py-2 rounded-full
                   bg-[var(--color-background-mute)]
                   border border-[var(--color-border)]
                   text-[var(--color-text)]
                   focus:border-[var(--color-border-hover)]"
          />
          <button
            type="button"
            @click="toggleConfirmPasswordVisibility"
            class="password-toggle absolute right-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"
            :class="{ 'is-active': showConfirmPassword }"
          ></button>
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
const role = ref('')
const isSubmitting = ref(false)
const submitError = ref('')
const submitSuccess = ref('')
const router = useRouter()

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const handleSubmit = () => {
  submitError.value = ''
  submitSuccess.value = ''

  if (password.value !== confirmPassword.value) {
    submitError.value = 'Passwords do not match.'
    return
  }

  isSubmitting.value = true

  axios
    .post(`${API_BASE_URL}/api/auth/signup/staff-admin/`, {
      firstName: firstName.value,
      lastName: lastName.value,
      email: email.value,
      password: password.value,
    })
    .then(() => {
      submitSuccess.value = 'Staff admin account created successfully.'

      try {
        const payload = {
          email: email.value,
          role: 'staff_admin',
          firstName: firstName.value,
          lastName: lastName.value,
        }
        window.localStorage.setItem('ap_staff_auth', JSON.stringify(payload))
        window.dispatchEvent(
          new CustomEvent('staff-auth-changed', {
            detail: { isLoggedIn: true, user: payload },
          }),
        )
      } catch (e) {
        console.error('Failed to persist staff auth state', e)
      }

      router.push({ name: 'admin-dashboard' })
    })
    .catch((error) => {
      console.error(error)
      if (error.response?.data?.errors) {
        const errs = error.response.data.errors
        submitError.value = Object.values(errs).join(' ')
      } else {
        submitError.value = 'Failed to create account. Please try again.'
      }
    })
    .finally(() => {
      isSubmitting.value = false
    })
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}
</script>

<style scoped>
.signup-card {
  max-width: 28rem !important;
}

.signup-input {
  max-width: 100%;
}

.password-toggle {
  background: none;
  border: none;
  cursor: pointer;
}

.password-toggle::before {
  content: '';
  display: inline-block;
  width: 20px;
  height: 20px;
  mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><path d="M2.25 12s3.75-6 9.75-6 9.75 6 9.75 6-3.75 6-9.75 6-9.75-6-9.75-6Z"/><path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/></svg>') no-repeat center;
  background-color: currentColor;
}

.password-toggle.is-active::before {
  mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><path d="M3.98 8.223A10.477 10.477 0 0 0 2.25 12c0 1.003.138 1.972.396 2.887M6.228 6.228C7.79 4.82 9.795 3.75 12 3.75c6 0 9.75 6 9.75 6a10.516 10.516 0 0 1-1.459 1.905M9.53 9.53a3 3 0 0 0 4.943 3.355M9.53 9.53 12 12m0 0 2.47 2.47M12 12l-3.75 3.75M12 12l3.75-3.75M4.5 19.5 19.5 4.5"/></svg>') no-repeat center;
}

.password-toggle:focus {
  outline: none;
}

.password-toggle:focus-visible {
  outline: 2px solid var(--color-button-bg);
  outline-offset: 2px;
}

.password-toggle {
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: var(--color-button-bg);
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
</style>
