import { createRouter, createWebHistory } from 'vue-router'
import UserOnboarding from '../components/UserOnboarding.vue'
import HomePage from '../components/HomePage.vue'
import LessonsPage from '../components/LessonsPage.vue'
import ProfilePage from '../components/ProfilePage.vue'
import LessonDetail from '../components/LessonDetail.vue'
import LessonCompletedPage from '../components/LessonCompletedPage.vue'
import IndividualPlanPage from '../components/IndividualPlanPage.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage
    },
    {
        path: '/onboarding',
        name: 'Onboarding',
        component: UserOnboarding
    },
    {
        path: '/lessons',
        name: 'Lessons',
        component: LessonsPage
    },
    {
        path: '/lesson/:id',
        name: 'LessonDetail',
        component: LessonDetail,
        props: true
    },
    {
        path: '/lesson/:id/completed',
        name: 'LessonCompleted',
        component: LessonCompletedPage,
        props: true
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfilePage
    },
    {
        path: '/individual-plan',
        name: 'IndividualPlan',
        component: IndividualPlanPage
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router 