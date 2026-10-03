<template>
  <section>
    <h2>Resumen de ventas</h2>
    <AlertMessage :message="error" />
    <p v-if="cargando" class="status">Cargando resumen…</p>

    <div class="summary">
      <RouterLink to="/clientes" class="summary__item">
        <strong>{{ clientes.length }}</strong>
        <span>Clientes</span>
      </RouterLink>
      <RouterLink to="/productos" class="summary__item">
        <strong>{{ productos.length }}</strong>
        <span>Productos</span>
      </RouterLink>
      <RouterLink to="/pedidos" class="summary__item">
        <strong>{{ pedidos.length }}</strong>
        <span>Pedidos</span>
      </RouterLink>
      <div class="summary__item summary__item--money">
        <strong>{{ moneda(ventas) }}</strong>
        <span>Vendido (sin cancelados)</span>
      </div>
    </div>

    <h3>Últimos pedidos</h3>
    <DataTable :rows="recientes" :columns="columns" />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import { pedidosApi } from '../api/pedidos'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import DataTable from '../components/DataTable.vue'
import { moneda } from '../utils/format'

const clientes = ref([])
const productos = ref([])
const pedidos = ref([])
const error = ref('')
const cargando = ref(false)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'cliente', label: 'Cliente' },
  { key: 'producto', label: 'Producto' },
  { key: 'total', label: 'Total', format: (v) => moneda(v) },
  { key: 'estado', label: 'Estado' },
]

const recientes = computed(() => pedidos.value.slice(0, 5))
const ventas = computed(() =>
  pedidos.value.filter((p) => p.estado !== 'cancelado').reduce((s, p) => s + p.total, 0),
)

onMounted(async () => {
  cargando.value = true
  try {
    const [c, p, pe] = await Promise.all([
      clientesApi.listar(),
      productosApi.listar(),
      pedidosApi.listar(),
    ])
    clientes.value = c.data
    productos.value = p.data
    pedidos.value = pe.data
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
})
</script>
