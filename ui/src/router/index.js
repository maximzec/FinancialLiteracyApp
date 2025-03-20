import { createRouter, createWebHistory } from 'vue-router'
import UserOnboarding from '../components/UserOnboarding.vue'
import HomePage from '../components/HomePage.vue'

const routes = [
    {
        path: '/',
        name: 'Onboarding',
        component: UserOnboarding
    },
    {
        path: '/home',
        name: 'Home',
        component: HomePage
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router 