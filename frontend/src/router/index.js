import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: () => import('../views/DashboardView.vue') },
    { path: '/clientes', component: () => import('../views/ClientesView.vue') },
    { path: '/productos', component: () => import('../views/ProductosView.vue') },
    { path: '/pedidos', component: () => import('../views/PedidosView.vue') },
    { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
  ],
})

export default router
