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
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="example.user@gmail.com"
            required
            class="login-input w-full px-4 py-2 rounded-full bg-[var(--color-background-mute)] text-[var(--color-text)] border border-[var(--color-border)] focus:border-[var(--color-border-hover)]"
          />
        </div>

        <div class="relative">
          <label for="password" class="login-label block text-sm text-[var(--color-text)]">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="••••••••••••"
            required
            class="login-input w-full px-4 py-2 rounded-full bg-[var(--color-background-mute)] text-[var(--color-text)] border border-[var(--color-border)] focus:border-[var(--color-border-hover)]"
          />

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
      await router.push('/awards')
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
        window.localStorage.setItem('loggedIn', 'true')
        window.dispatchEvent(
          new CustomEvent('org-auth-changed', {
            detail: { isLoggedIn: true, user: payload },
          }),
        )
        window.dispatchEvent(new Event('auth-state-changed'))
      } catch (e) {
        console.error('Failed to persist organization auth state', e)
      }
      await router.push('/awards')
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
        window.localStorage.setItem('loggedIn', 'true')
        window.dispatchEvent(
          new CustomEvent('business-auth-changed', {
            detail: { isLoggedIn: true, user: payload },
          }),
        )
        window.dispatchEvent(new Event('auth-state-changed'))
      } catch (e) {
        console.error('Failed to persist business auth state', e)
      }
      await router.push('/awards')
    }
  } catch (error: any) {
    console.error(error)
    const serverMessage = error.response?.data?.message
    if (serverMessage) {
      loginError.value = serverMessage
    } else if (error.response?.status === 401) {
      loginError.value = 'Invalid email or password.'
    } else {
      loginError.value = 'Login failed. Please try again.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.login-card {
  max-width: 28rem !important;
}

.login-input {
  max-width: 100%;
}

/* Override to fix field overflow */
.login-input {
  width: 100% !important;
  box-sizing: border-box !important;
}
</style>
