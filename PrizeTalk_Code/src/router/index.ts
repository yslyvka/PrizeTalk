import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/home.vue'
import Awards from '../views/awards.vue'
import Community from '../views/community.vue'
import Login from '../views/login.vue'
import Signup from '../views/signup.vue'
import Groups from '../views/groupcommunity.vue'
import GroupDetail from '../views/GroupDetailPage.vue' 

const routes = [
  { path: '/', component: Home },
  { path: '/awards', component: Awards },
  { path: '/community', component: Community },
  { path: '/groups', component: Groups },
  { 
    path: '/groups/:id',
    name: 'GroupDetail',
    component: GroupDetail,
    props: true
  },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router