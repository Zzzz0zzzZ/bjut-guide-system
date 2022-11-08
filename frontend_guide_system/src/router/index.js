import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/home/HomeView.vue'
import UserView from '@/views/user/UserView.vue'
import GuideView from '@/views/home/GuideView.vue'
import TodoView from '@/views/todo/TodoView.vue'
import SrouteView from '@/views/home/SrouteView'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/todo',
    name: 'todo',
    component: TodoView
  },
  {
    path: '/user',
    name: 'user',
    component: UserView
  },
  {
    path: '/guide',
    name: 'guide',
    component: GuideView
  },
  {
    path: '/sroute',
    name: 'sroute',
    component: SrouteView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
