<template>
  <nav>
    <router-link v-if="!isLoggedIn" to="/">Home</router-link>
    <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
    <router-link v-if="!isLoggedIn" to="/signup">Signup</router-link>
    <router-link v-if="isLoggedIn" to="/awards">Awards</router-link>
    <router-link v-if="isLoggedIn" to="/community">Community</router-link>
    <button v-if="isLoggedIn" @click="signOut" class="sign-out-btn">Sign Out</button>
  </nav>
  <router-view />
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)

onMounted(() => {
  checkLoginStatus()
})

watch(() => router.currentRoute.value, () => {
  checkLoginStatus()
})

const checkLoginStatus = () => {
  isLoggedIn.value = localStorage.getItem('loggedIn') === 'true'
}

const signOut = () => {
  localStorage.removeItem('loggedIn')
  isLoggedIn.value = false
  router.push('/')
}
</script>

<style>
nav {
  background: var(--color-background-soft);
  padding: 1rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  border-bottom: 1px solid var(--color-border);
}

nav a, nav button {
  text-decoration: none;
  color: var(--color-button-bg);
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
  border: none;
  background: none;
  cursor: pointer;
}

nav a:hover, nav button:hover {
  background: var(--color-background-mute);
  text-decoration: underline;
}

h1 {
  color: var(--color-heading);
  text-align: center;
}
</style>
