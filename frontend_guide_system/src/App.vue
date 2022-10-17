<template>
  <van-config-provider :theme-vars="themeVars">
    <router-view />
    <NavBar />
  </van-config-provider>
</template>


<script setup>
import NavBar from './components/NavBar.vue';

const themeVars = {
  navBarBackgroundColor: '#3d8af2',
  navBarTitleTextColor: '#ffffff',
  navBarTitleFontSize: '16px',
}
</script>
