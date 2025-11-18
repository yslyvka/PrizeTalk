<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/awards">Awards</router-link>
    <router-link to="/community">Community</router-link>
    <router-link to="/login">Login</router-link>
    <router-link to="/signup">Signup</router-link>
  </nav>
  <router-view />
</template>

<script setup>
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

nav a {
  text-decoration: none;
  color: var(--color-button-bg);
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
}

nav a:hover {
  background: var(--color-background-mute);
  text-decoration: underline;
}

h1 {
  color: var(--color-heading);
  text-align: center;
}
</style>
