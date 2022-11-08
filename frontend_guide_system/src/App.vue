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
  navBarTextColor: '#ffffff',
  navBarIconColor: '#ffffff',
  navBarTitleFontSize: '16px',
  treeSelectItemActiveColor: '#3d8af2',
  sidebarSelectedBorderColor: '#3d8af2',
  calendarSelectedDayBackgroundColor: '#3d8af2'
}
</script>
