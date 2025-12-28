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
    path: "/admin",
    component: () => import("@/views/AdminPage.vue"),
    name: "admin-home",
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/issue",
    component: () => import("@/views/AdminIssuePage.vue"),
    name: "admin-issue",
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/revoke",
    component: () => import("@/views/AdminRevokePage.vue"),
    name: "admin-revoke",
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/sign",
    component: () => import("@/views/AdminSignPage.vue"),
    name: "admin-sign",
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/students",
    component: () => import("@/views/StudentsPage.vue"),
    name: "students",
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/issuer-registrations",
    component: () => import("@/views/AdminIssuerPage.vue"),
    name: "admin-issuer-registrations",
    meta: { requiresAuth: true },
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

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (!authStore.isReady) {
    await authStore.init()
  }

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      next("/login")
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router