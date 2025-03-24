import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import OnboardingPage from '../components/OnboardingPage.vue'
import LessonsPage from '../components/LessonsPage.vue'
import ProfilePage from '../components/ProfilePage.vue'
import LessonDetail from '../components/LessonDetail.vue'
import IndividualPlanPage from '../components/IndividualPlanPage.vue'
import CoinShopPage from '../components/CoinShopPage.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage
    },
    {
        path: '/onboarding',
        name: 'Onboarding',
        component: OnboardingPage
    },
    {
        path: '/lessons',
        name: 'Lessons',
        component: LessonsPage
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfilePage
    },
    {
        path: '/lesson/:id',
        name: 'LessonDetail',
        component: LessonDetail,
        props: true
    },
    {
        path: '/individual-plan',
        name: 'IndividualPlan',
        component: IndividualPlanPage
    },
    {
        path: '/coin-shop',
        name: 'CoinShop',
        component: CoinShopPage
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router 