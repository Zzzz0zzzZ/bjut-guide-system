import { createRouter, createWebHashHistory } from 'vue-router'
import HelpView from '@/views/help/HelpView.vue'
import HomeView from '@/views/home/HomeView.vue'
import UserView from '@/views/user/UserView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/help',
    name: 'help',
    component: HelpView
  },
  {
    path: '/user',
    name: 'user',
    component: UserView
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
