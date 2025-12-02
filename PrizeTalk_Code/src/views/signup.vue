<template>
  <section
    class="signup-shell min-h-screen flex flex-col items-center justify-center px-4 md:px-[5%] py-6
           bg-[var(--color-background)] text-[var(--color-text)]"
  >

    <div class="text-center heading-section signup-heading">
      <Title level="h1" class="text-[var(--color-heading)]">Sign-up for PrizeTalk</Title>
      <Paragraph align="center" class="text-[var(--color-text-muted)]">
        Already have an account?
        <RouterLink to="/login" class="text-[var(--color-button-bg)] hover:underline font-semibold">Sign-in</RouterLink>
      </Paragraph>
    </div>

    <div
  class="signup-card w-full max-w-md space-y-6 rounded-2xl p-8
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
          full
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
        <RouterLink to="/" class="text-[var(--color-button-bg)] hover:underline font-semibold">Terms</RouterLink> and
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
/* Color Palette Variables */
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

/* Background & Shell */
.signup-shell {
  background: linear-gradient(135deg, #faf8f5 0%, #f0e9dd 100%) !important;
  animation: fadeIn 0.5s ease;
  backdrop-filter: none;
}

@media (prefers-color-scheme: dark) {
  .signup-shell {
    background: linear-gradient(135deg, #0a0f1e 0%, #1e293b 100%) !important;
  }
}

/* Heading Section */
.signup-heading {
  margin-bottom: 2.5rem;
  animation: slideDown 0.6s ease;
}

.signup-heading :deep(h1) {
  color: #5e0b15 !important;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

@media (prefers-color-scheme: dark) {
  .signup-heading :deep(h1) {
    color: #f1f5f9 !important;
  }
}

.signup-heading :deep(p) {
  color: #8c7a6b !important;
  font-size: 1rem;
}

@media (prefers-color-scheme: dark) {
  .signup-heading :deep(p) {
    color: #94a3b8 !important;
  }
}

.signup-heading :deep(a) {
  color: #90323d !important;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .signup-heading :deep(a) {
    color: #60a5fa !important;
  }
}

.signup-heading :deep(a:hover) {
  color: #bc8034 !important;
  text-decoration: underline;
}

@media (prefers-color-scheme: dark) {
  .signup-heading :deep(a:hover) {
    color: #3b82f6 !important;
  }
}

/* Card */
.signup-card {
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
  .signup-card {
    background: #1e293b !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
    border: 1px solid #334155 !important;
  }
}

.signup-card:hover {
  box-shadow: 0 8px 32px rgba(94, 11, 21, 0.12) !important;
}

@media (prefers-color-scheme: dark) {
  .signup-card:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
  }
}

/* Social Buttons */
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

/* Separator */
.signup-separator > div {
  background: #d9cab3 !important;
}

@media (prefers-color-scheme: dark) {
  .signup-separator > div {
    background: #334155 !important;
  }
}

.signup-separator-text {
  color: #8c7a6b !important;
  font-weight: 600;
}

@media (prefers-color-scheme: dark) {
  .signup-separator-text {
    color: #94a3b8 !important;
  }
}

/* Form Fields */
.signup-label {
  color: #3a2f28 !important;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  .signup-label {
    color: #e2e8f0 !important;
  }
}

.signup-input {
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
  .signup-input {
    background: rgba(59, 130, 246, 0.1) !important;
    color: #e2e8f0 !important;
  }
}

.signup-input::placeholder {
  color: #8c7a6b;
  opacity: 0.6;
}

@media (prefers-color-scheme: dark) {
  .signup-input::placeholder {
    color: #94a3b8;
    opacity: 0.6;
  }
}

.signup-input:focus {
  outline: none;
  border-color: #bc8034 !important;
  background: white !important;
  box-shadow: 0 0 0 4px rgba(188, 128, 52, 0.1) !important;
}

@media (prefers-color-scheme: dark) {
  .signup-input:focus {
    border-color: #3b82f6 !important;
    background: #0f172a !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
  }
}

.signup-input:invalid:not(:placeholder-shown) {
  border-color: #90323d !important;
}

@media (prefers-color-scheme: dark) {
  .signup-input:invalid:not(:placeholder-shown) {
    border-color: #ef4444 !important;
  }
}

/* Select Dropdown */
select.signup-input {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%238c7a6b' d='M8 11L3 6h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  padding-right: 2.5rem;
  cursor: pointer;
  background-color: rgba(217, 202, 179, 0.15) !important;
}

@media (prefers-color-scheme: dark) {
  select.signup-input {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='%2394a3b8' d='M8 11L3 6h10z'/%3E%3C/svg%3E");
    background-color: rgba(59, 130, 246, 0.1) !important;
  }
}

select.signup-input:focus {
  background-color: white !important;
}

@media (prefers-color-scheme: dark) {
  select.signup-input:focus {
    background-color: #0f172a !important;
  }
}

/* Submit Button */
.signup-submit {
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
  .signup-submit {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  }
}

.signup-submit:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(94, 11, 21, 0.3) !important;
  filter: none !important;
}

@media (prefers-color-scheme: dark) {
  .signup-submit:hover:not(:disabled) {
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
  }
}

.signup-submit:active:not(:disabled) {
  transform: translateY(0) !important;
}

.signup-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Error & Success Messages */
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

p.text-emerald-400 {
  color: #10b981 !important;
  font-weight: 600;
  padding-top: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  p.text-emerald-400 {
    color: #34d399 !important;
  }
}

/* Terms */
.signup-terms {
  color: #8c7a6b !important;
  line-height: 1.6;
}

@media (prefers-color-scheme: dark) {
  .signup-terms {
    color: #94a3b8 !important;
  }
}

.signup-terms :deep(a) {
  color: #90323d !important;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .signup-terms :deep(a) {
    color: #60a5fa !important;
  }
}

.signup-terms :deep(a:hover) {
  color: #bc8034 !important;
  text-decoration: underline;
}

@media (prefers-color-scheme: dark) {
  .signup-terms :deep(a:hover) {
    color: #3b82f6 !important;
  }
}

/* Animations */
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

/* Responsive */
@media (max-width: 640px) {
  .signup-card {
    padding: 2rem 1.5rem !important;
  }

  .signup-heading :deep(h1) {
    font-size: 2rem;
  }

  .signup-heading {
    margin-bottom: 2rem;
  }
}
</style>