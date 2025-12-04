import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
import { useAuthStore } from "@/stores/authStore"


const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("@/views/Home.vue"),
    name: "home",
  },
  {
    path: "/login",
    component: () => import("@/views/LoginPage.vue"),
    name: "login",
  },
  {
    path: "/admin/issue",
    component: () => import("@/views/AdminIssuePage.vue"),
    name: "admin-issue",
    meta: { requiresAuth: true, requiresRole: "admin" },
  },
  {
    path: "/admin/revoke",
    component: () => import("@/views/AdminRevokePage.vue"),
    name: "admin-revoke",
    meta: { requiresAuth: true, requiresRole: "admin" },
  },
  {
    path: "/verify",
    component: () => import("@/views/VerifyPage.vue"),
    name: "verify",
  },
  {
    path: "/explorer",
    component: () => import("@/views/ExplorerPage.vue"),
    name: "explorer",
  },
  {
    path: "/certificate/:id",
    component: () => import("@/views/CertificateDetailPage.vue"),
    name: "certificate-detail",
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login")
  } else if (to.meta.requiresRole && authStore.userRole !== to.meta.requiresRole) {
    next("/")
  } else {
    next()
  }
})

export default router
