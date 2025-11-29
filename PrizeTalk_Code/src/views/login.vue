<template>
  <section class="login-shell min-h-screen flex flex-col items-center justify-center px-4 md:px-[5%] py-6 bg-[var(--color-background)] text-[var(--color-text)]">
    <div class="text-center heading-section login-heading">
      <Title level="h1" class="text-[var(--color-heading)]">Sign-in to Award-Pulse</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Don't have an account?
        <RouterLink to="/signup" class="text-[var(--color-button-bg)] hover:underline font-semibold">Sign-up</RouterLink>
      </Paragraph>
    </div>

    <div class="login-card w-full max-w-xl space-y-8 rounded-2xl p-8 bg-[var(--color-background-soft)] border border-[var(--color-border)]">
      <div class="social-row flex flex-col items-center gap-3 sm:flex-row">
        <form class="w-full relative" action="/api/auth/signin/google" method="GET">
          <button
            type="submit"
            class="social-button w-full border border-[var(--color-border)] bg-[var(--color-background-soft)] text-[var(--color-text)] hover:border-[var(--color-border-hover)] rounded-[var(--button-radius)] py-2"
          >
            <span class="inline-flex items-center justify-center gap-1 min-w-0 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="24" height="24" class="relative -left-2"></svg>
              <span>Sign-in with Google</span>
            </span>
          </button>
        </form>

        <form class="w-full relative" action="/api/auth/signin/apple" method="GET">
          <button
            type="submit"
            class="social-button w-full border border-[var(--color-border)] bg-[var(--color-background-soft)] text-[var(--color-text)] hover:border-[var(--color-border-hover)] rounded-[var(--button-radius)] py-2"
          >
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
        <div class="relative">
          <label for="email" class="login-label block text-sm text-[var(--color-text)]">Email</label>
          <svg class="login-icon absolute left-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"></svg>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="example.user@gmail.com"
            required
            class="login-input w-full pl-10 pr-4 py-2 rounded-full bg-[var(--color-background-mute)] text-[var(--color-text)] border border-[var(--color-border)] focus:border-[var(--color-border-hover)]"
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
            class="login-input w-full pl-10 pr-10 py-2 rounded-full bg-[var(--color-background-mute)] text-[var(--color-text)] border border-[var(--color-border)] focus:border-[var(--color-border-hover)]"
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="password-toggle absolute right-3 top-8 h-5 w-5 text-[var(--color-text-muted)]"
            :class="{ 'is-active': showPassword }"
          ></button>

          <div class="flex items-center justify-between mt-1">
            <label class="remember-label text-sm text-[var(--color-text-muted)]">
              <input v-model="rememberMe" type="checkbox" /> Remember me
            </label>
            <RouterLink to="/ForgotPassword" class="text-[var(--color-button-bg)] hover:underline font-semibold">Forgot your password?</RouterLink>
          </div>
        </div>

        <Button
          variant="primary"
          block
          type="submit"
          :disabled="isSubmitting"
          class="login-submit !rounded-full bg-[var(--color-button-bg)] text-[var(--color-button-text)] hover:bg-[var(--color-button-hover-bg)]"
        >
          <span v-if="isSubmitting">Signing you in...</span>
          <span v-else>Log In</span>
        </Button>

        <p v-if="loginError" class="text-sm text-red-500 text-center">
          {{ loginError }}
        </p>
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
import { useRouter } from 'vue-router'
import axios from 'axios'
import Title from '../components/BasicComponents/Title.vue'
import Paragraph from '../components/BasicComponents/Paragraph.vue'
import Button from '../components/BasicComponents/Button.vue'

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isSubmitting = ref(false)
const loginError = ref('')

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const router = useRouter()

const showPassword = ref(false)

const handleSubmit = async () => {
  loginError.value = ''

  if (!email.value || !password.value) {
    loginError.value = 'Email and password are required.'
    return
  }

  isSubmitting.value = true
  try {
    const { data } = await axios.post(`${API_BASE_URL}/api/auth/login/`, {
      email: email.value,
      password: password.value,
    })

    if (data.kind === 'staff') {
      const payload = {
        email: data.account.email,
        role: data.staff?.role,
        firstName: data.account.firstName,
        lastName: data.account.lastName,
      }
      try {
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
    } else if (data.kind === 'organization') {
      const org = data.organization?.organization
      const payload = {
        organizationId: org?.id,
        organizationName: org?.name,
        userId: data.organization?.membershipId,
        email: data.account.email,
        role: data.organization?.role,
        firstName: data.account.firstName,
        lastName: data.account.lastName,
      }

      try {
        window.localStorage.setItem('ap_org_auth', JSON.stringify(payload))
        window.dispatchEvent(
          new CustomEvent('org-auth-changed', {
            detail: { isLoggedIn: true, user: payload },
          }),
        )
      } catch (e) {
        console.error('Failed to persist organization auth state', e)
      }
      router.push({ name: 'home' })
    } else if (data.kind === 'business') {
      const biz = data.business?.business
      const payload = {
        businessId: biz?.id,
        businessName: biz?.name,
        organization: data.business?.organization || null,
        userId: data.business?.membershipId,
        email: data.account.email,
        role: data.business?.role,
        firstName: data.account.firstName,
        lastName: data.account.lastName,
      }

      try {
        window.localStorage.setItem('ap_business_auth', JSON.stringify(payload))
        window.dispatchEvent(
          new CustomEvent('business-auth-changed', {
            detail: { isLoggedIn: true, user: payload },
          }),
        )
      } catch (e) {
        console.error('Failed to persist business auth state', e)
      }
      router.push({ name: 'demo' })
    }
  } catch (error: any) {
    console.error(error)
    if (error.response?.status === 401) {
      loginError.value = 'Invalid email or password.'
    } else {
      loginError.value = 'Login failed. Please try again.'
    }
  } finally {
    isSubmitting.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>

<style scoped>
.login-card {
  max-width: 28rem !important;
}

.login-input {
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
</style>
