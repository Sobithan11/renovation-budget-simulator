<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/dashboard">Dashboard</RouterLink>
      <RouterLink to="/projects">Projects</RouterLink>
      <RouterLink to="/scenarios">Scenarios</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f5f5f5;
}

nav {
  display: flex;
  gap: 24px;
  padding: 20px 40px;
  background: #222;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: 600;
}

nav a.router-link-active {
  text-decoration: underline;
}
</style>