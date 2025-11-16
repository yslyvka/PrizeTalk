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
h1 {
  color: teal;
  text-align: center;
}
</style>
