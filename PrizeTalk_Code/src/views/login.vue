<template>
  <section class="login-shell min-h-screen flex flex-col items-center justify-center px-4 md:px-[5%] py-6 bg-[var(--color-background)] text-[var(--color-text)]">
    <div class="text-center heading-section login-heading">
      <Title level="h1" class="text-[var(--color-heading)]">Sign-in to PrizeTalk</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Don't have an account?
        <RouterLink to="/signup" class="text-[var(--color-button-bg)] hover:underline font-semibold">Sign-up</RouterLink>
      </Paragraph>
    </div>

    <div class="login-card w-full max-w-xl space-y-8 rounded-2xl p-8 bg-[var(--color-background-soft)] border border-[var(--color-border)]">
      <div class="social-row flex flex-col items-center gap-3 sm:flex-row">
        <!-- Google -->
        <form class="w-full relative" action="/api/auth/signin/google" method="GET">
          <button type="submit" class="social-button w-full">Sign-in with Google</button>
        </form>

        <!-- Apple -->
        <form class="w-full relative" action="/api/auth/signin/apple" method="GET">
          <button type="submit" class="social-button w-full">Sign-in with Apple</button>
        </form>
      </div>

      <div class="login-separator flex items-center justify-center gap-2">
        <div class="flex-grow h-px bg-[var(--color-border)]"></div>
        <span class="login-separator-text px-3 text-sm text-[var(--color-text-muted)]">or</span>
        <div class="flex-grow h-px bg-[var(--color-border)]"></div>
      </div>

      <!-- Email login -->
      <form class="form-fields space-y-5" @submit.prevent="handleSubmit">
        <div class="relative">
          <label for="email" class="login-label block text-sm text-[var(--color-text)]">Email</label>
          <input v-model="email" type="email" id="email" placeholder="example.user@gmail.com" required class="login-input" />
        </div>

        <div class="relative">
          <label for="password" class="login-label block text-sm text-[var(--color-text)]">Password</label>
          <input v-model="password" type="password" id="password" placeholder="••••••••" required class="login-input" />
          <div class="flex items-center justify-between mt-1">
            <label class="remember-label text-sm text-[var(--color-text-muted)]">
              <input v-model="rememberMe" type="checkbox" /> Remember me
            </label>
            <RouterLink to="/" class="text-[var(--color-button-bg)] hover:underline font-semibold">Forgot your password?</RouterLink>
          </div>
        </div>

        <Button variant="primary" block type="submit" :disabled="isSubmitting" class="login-submit">
          <span v-if="isSubmitting">Signing you in...</span>
          <span v-else>Log In</span>
        </Button>

        <p v-if="loginError" class="text-sm text-red-500 text-center">{{ loginError }}</p>
      </form>

      <Paragraph align="center" class="text-xs text-[var(--color-text-muted)]">
        By signing in, you agree to our
        <RouterLink to="/" class="text-[var(--color-button-bg)] hover:underline font-semibold">Terms</RouterLink>
        and
        <RouterLink to="/" class="text-[var(--color-button-bg)] hover:underline font-semibold">Privacy Policy</RouterLink>
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

    const payload = {
      userId: data.account.id,
      username: data.account.username,
      email: data.account.email,
      role: data.account.role || 'user',
      kind: data.kind
    }

    // Save to localStorage
    localStorage.setItem('loggedInUser', JSON.stringify(payload))
    localStorage.setItem('loggedIn', 'true')
    localStorage.setItem('userRole', payload.role)

    console.log(localStorage.getItem('loggedInUser'))


    window.dispatchEvent(new Event('auth-state-changed'))

    await router.push('/awards')

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
:root {
  --night-bordeaux: #5e0b15;
  --burnt-rose: #90323d;
  --pale-oak: #d9cab3;
  --bronze: #bc8034;
  --dusty-taupe: #8c7a6b;
}

@media (prefers-color-scheme: dark) {
  :root {
    --midnight-blue: #0f172a;
    --deep-blue: #1e293b;
    --ocean-blue: #3b82f6;
    --sky-blue: #60a5fa;
    --slate: #475569;
  }
}


.login-shell {
  background: linear-gradient(135deg, #faf8f5 0%, #f0e9dd 100%) !important;
  animation: fadeIn 0.5s ease;
  backdrop-filter: none;
}

@media (prefers-color-scheme: dark) {
  .login-shell {
    background: linear-gradient(135deg, #0a0f1e 0%, #1e293b 100%) !important;
  }
}

.login-heading {
  margin-bottom: 2.5rem;
  animation: slideDown 0.6s ease;
}

.login-heading :deep(h1) {
  color: #5e0b15 !important;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

@media (prefers-color-scheme: dark) {
  .login-heading :deep(h1) {
    color: #f1f5f9 !important;
  }
}

.login-heading :deep(p) {
  color: #8c7a6b !important;
  font-size: 1rem;
}

@media (prefers-color-scheme: dark) {
  .login-heading :deep(p) {
    color: #94a3b8 !important;
  }
}

.login-heading :deep(a) {
  color: #90323d !important;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .login-heading :deep(a) {
    color: #60a5fa !important;
  }
}

.login-heading :deep(a:hover) {
  color: #bc8034 !important;
  text-decoration: underline;
}

@media (prefers-color-scheme: dark) {
  .login-heading :deep(a:hover) {
    color: #3b82f6 !important;
  }
}

/* Card */
.login-card {
  max-width: 480px !important;
  margin-left: auto;
  margin-right: auto;
  background: white !important;
  border-radius: 16px !important;
  padding: 2.5rem !important;
  box-shadow: 0 4px 24px rgba(94, 11, 21, 0.08) !important;
  border: 1px solid rgba(217, 202, 179, 0.3) !important;
  transition: box-shadow 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .login-card {
    background: #1e293b !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
    border: 1px solid #334155 !important;
  }
}

.login-card:hover {
  box-shadow: 0 8px 32px rgba(94, 11, 21, 0.12) !important;
}

@media (prefers-color-scheme: dark) {
  .login-card:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
  }
}

.social-row {
  gap: 1rem;
}

.social-button {
  padding: 0.875rem 1rem !important;
  background: white !important;
  border: 2px solid #d9cab3 !important;
  border-radius: 12px !important;
  font-size: 0.95rem;
  font-weight: 600;
  color: #3a2f28 !important;
  transition: all 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .social-button {
    background: #0f172a !important;
    border: 2px solid #334155 !important;
    color: #e2e8f0 !important;
  }
}

.social-button:hover {
  border-color: #bc8034 !important;
  background: rgba(188, 128, 52, 0.05) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(188, 128, 52, 0.15);
}

@media (prefers-color-scheme: dark) {
  .social-button:hover {
    border-color: #3b82f6 !important;
    background: rgba(59, 130, 246, 0.1) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
  }
}

.social-button span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-separator > div {
  background: #d9cab3 !important;
}

@media (prefers-color-scheme: dark) {
  .login-separator > div {
    background: #334155 !important;
  }
}

.login-separator-text {
  color: #8c7a6b !important;
  font-weight: 600;
}

@media (prefers-color-scheme: dark) {
  .login-separator-text {
    color: #94a3b8 !important;
  }
}

.login-label {
  color: #3a2f28 !important;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  .login-label {
    color: #e2e8f0 !important;
  }
}

.login-input {
  padding: 0.875rem 1rem !important;
  background: rgba(217, 202, 179, 0.15) !important;
  border: 2px solid transparent !important;
  border-radius: 12px !important;
  font-size: 0.95rem;
  color: #3a2f28 !important;
  transition: all 0.3s ease;
  width: 100% !important;
  min-height: 3rem;
  box-sizing: border-box !important;
}

@media (prefers-color-scheme: dark) {
  .login-input {
    background: rgba(59, 130, 246, 0.1) !important;
    color: #e2e8f0 !important;
  }
}

.login-input::placeholder {
  color: #8c7a6b;
  opacity: 0.6;
}

@media (prefers-color-scheme: dark) {
  .login-input::placeholder {
    color: #94a3b8;
    opacity: 0.6;
  }
}

.login-input:focus {
  outline: none;
  border-color: #bc8034 !important;
  background: white !important;
  box-shadow: 0 0 0 4px rgba(188, 128, 52, 0.1) !important;
}

@media (prefers-color-scheme: dark) {
  .login-input:focus {
    border-color: #3b82f6 !important;
    background: #0f172a !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
  }
}

.login-input:invalid:not(:placeholder-shown) {
  border-color: #90323d !important;
}

@media (prefers-color-scheme: dark) {
  .login-input:invalid:not(:placeholder-shown) {
    border-color: #ef4444 !important;
  }
}

.remember-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #8c7a6b !important;
  font-size: 0.875rem;
}

@media (prefers-color-scheme: dark) {
  .remember-label {
    color: #94a3b8 !important;
  }
}

.remember-label input[type="checkbox"] {
  width: auto !important;
  min-height: auto !important;
  margin: 0;
  cursor: pointer;
  accent-color: #90323d;
}

@media (prefers-color-scheme: dark) {
  .remember-label input[type="checkbox"] {
    accent-color: #3b82f6;
  }
}

.login-input:focus ~ .flex a,
.flex a {
  color: #90323d !important;
  font-size: 0.875rem;
  transition: color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .login-input:focus ~ .flex a,
  .flex a {
    color: #60a5fa !important;
  }
}

.flex a:hover {
  color: #bc8034 !important;
}

@media (prefers-color-scheme: dark) {
  .flex a:hover {
    color: #3b82f6 !important;
  }
}

.login-submit {
  width: 100%;
  padding: 1rem !important;
  background: linear-gradient(135deg, #90323d 0%, #5e0b15 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  cursor: pointer;
  transition: all 0.3s ease !important;
  margin-top: 1rem;
  box-shadow: 0 4px 12px rgba(94, 11, 21, 0.2);
  filter: none !important;
}

@media (prefers-color-scheme: dark) {
  .login-submit {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  }
}

.login-submit:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(94, 11, 21, 0.3) !important;
  filter: none !important;
}

@media (prefers-color-scheme: dark) {
  .login-submit:hover:not(:disabled) {
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
  }
}

.login-submit:active:not(:disabled) {
  transform: translateY(0) !important;
}

.login-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


p.text-red-500 {
  color: #90323d !important;
  font-weight: 600;
  padding-top: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  p.text-red-500 {
    color: #ef4444 !important;
  }
}


.login-card :deep(p:last-child) {
  color: #8c7a6b !important;
  line-height: 1.6;
}

@media (prefers-color-scheme: dark) {
  .login-card :deep(p:last-child) {
    color: #94a3b8 !important;
  }
}

.login-card :deep(p:last-child a) {
  color: #90323d !important;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .login-card :deep(p:last-child a) {
    color: #60a5fa !important;
  }
}

.login-card :deep(p:last-child a:hover) {
  color: #bc8034 !important;
  text-decoration: underline;
}

@media (prefers-color-scheme: dark) {
  .login-card :deep(p:last-child a:hover) {
    color: #3b82f6 !important;
  }
}


@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .login-card {
    padding: 2rem 1.5rem !important;
  }

  .login-heading :deep(h1) {
    font-size: 2rem;
  }

  .login-heading {
    margin-bottom: 2rem;
  }
}
</style>
