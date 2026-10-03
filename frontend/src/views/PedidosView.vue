<template>
  <section>
    <h2>Pedidos</h2>
    <AlertMessage :message="error" />

    <form class="card form-grid" novalidate @submit.prevent="guardar">
      <BaseSelect
        v-model="form.cliente_id"
        label="Cliente"
        placeholder="Seleccione un cliente"
        :options="opcionesClientes"
        :error="errores.cliente_id"
      />
      <BaseSelect
        v-model="form.producto_id"
        label="Producto"
        placeholder="Seleccione un producto"
        :options="opcionesProductos"
        :error="errores.producto_id"
      />
      <BaseInput
        v-model="form.cantidad"
        label="Cantidad"
        type="number"
        min="1"
        step="1"
        :error="errores.cantidad"
      />
      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">Crear pedido</BaseButton>
      </div>
    </form>

    <p v-if="cargando" class="status">Cargando pedidos…</p>
    <DataTable :rows="pedidos" :columns="columns">
      <template #actions="{ row }">
        <select
          class="estado-select"
          :value="row.estado"
          :aria-label="`Estado del pedido ${row.id}`"
          @change="cambiarEstado(row, $event.target.value)"
        >
          <option v-for="estado in estados" :key="estado" :value="estado">{{ estado }}</option>
        </select>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import { pedidosApi } from '../api/pedidos'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import BaseSelect from '../components/BaseSelect.vue'
import DataTable from '../components/DataTable.vue'
import { moneda } from '../utils/format'

const estados = ['pendiente', 'pagado', 'enviado', 'cancelado']

const pedidos = ref([])
const clientes = ref([])
const productos = ref([])
const error = ref('')
const cargando = ref(false)
const guardando = ref(false)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'cliente', label: 'Cliente' },
  { key: 'producto', label: 'Producto' },
  { key: 'cantidad', label: 'Cantidad' },
  { key: 'total', label: 'Total', format: (v) => moneda(v) },
  { key: 'estado', label: 'Estado' },
]

const opcionesClientes = computed(() =>
  clientes.value.map((c) => ({ value: c.id, label: c.nombre })),
)
// Solo se ofrecen productos activos y con existencias.
const opcionesProductos = computed(() =>
  productos.value
    .filter((p) => p.activo && p.stock > 0)
    .map((p) => ({ value: p.id, label: `${p.nombre} — ${moneda(p.precio)} (stock ${p.stock})` })),
)

const vacio = () => ({ cliente_id: '', producto_id: '', cantidad: 1 })
const vacioErrores = () => ({ cliente_id: '', producto_id: '', cantidad: '' })
const form = reactive(vacio())
const errores = reactive(vacioErrores())

function validar() {
  Object.assign(errores, vacioErrores())
  if (!form.cliente_id) errores.cliente_id = 'Seleccione un cliente.'
  if (!form.producto_id) errores.producto_id = 'Seleccione un producto.'
  const cantidad = Number(form.cantidad)
  if (!Number.isInteger(cantidad) || cantidad <= 0) errores.cantidad = 'Ingrese un entero mayor que 0.'
  else {
    const producto = productos.value.find((p) => p.id === form.producto_id)
    if (producto && cantidad > producto.stock) errores.cantidad = `Solo hay ${producto.stock} en stock.`
  }
  return !Object.values(errores).some(Boolean)
}

async function cargar() {
  cargando.value = true
  try {
    const [p, c, pr] = await Promise.all([
      pedidosApi.listar(),
      clientesApi.listar(),
      productosApi.listar(),
    ])
    pedidos.value = p.data
    clientes.value = c.data
    productos.value = pr.data
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
}

async function guardar() {
  error.value = ''
  if (!validar()) return
  guardando.value = true
  try {
    await pedidosApi.crear({
      cliente_id: form.cliente_id,
      producto_id: form.producto_id,
      cantidad: Number(form.cantidad),
    })
    Object.assign(form, vacio())
    await cargar() // refresca también el stock de los productos
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

async function cambiarEstado(pedido, estado) {
  error.value = ''
  try {
    await pedidosApi.actualizar(pedido.id, { estado })
  } catch (err) {
    error.value = err.message
  }
  await cargar()
}

async function eliminar(pedido) {
  if (!window.confirm(`¿Eliminar el pedido #${pedido.id}?`)) return
  error.value = ''
  try {
    await pedidosApi.eliminar(pedido.id)
    await cargar()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargar)
</script>
