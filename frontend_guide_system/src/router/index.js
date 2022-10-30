import { createRouter, createWebHistory } from 'vue-router'
import HelpView from '@/views/help/HelpView.vue'
import HomeView from '@/views/home/HomeView.vue'
import UserView from '@/views/user/UserView.vue'
import GuideView from '@/views/home/GuideView.vue'
import TodoView from '@/views/todo/TodoView.vue'

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
    path: '/help',
    name: 'help',
    component: HelpView
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
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
