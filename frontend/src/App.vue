<template>
  <div id="app">
    <router-view />
    <ToastContainer />
    <LoadingOverlay />
  </div>
</template>

<script setup lang="ts">
import ToastContainer from '@/components/common/ToastContainer.vue'
import LoadingOverlay from '@/components/common/LoadingOverlay.vue'

// This is the root component
</script>

<style>
#app {
  font-family: 'Poppins', 'Nunito', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
