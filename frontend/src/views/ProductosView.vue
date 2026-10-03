<template>
  <section>
    <h2>Productos</h2>
    <AlertMessage :message="error" />

    <form class="card form-grid" novalidate @submit.prevent="guardar">
      <BaseInput v-model="form.nombre" label="Nombre" :error="errores.nombre" />
      <BaseInput v-model="form.descripcion" label="Descripción" :error="errores.descripcion" />
      <BaseInput
        v-model="form.precio"
        label="Precio (Q)"
        type="number"
        min="0"
        step="0.01"
        :error="errores.precio"
      />
      <BaseInput
        v-model="form.stock"
        label="Stock"
        type="number"
        min="0"
        step="1"
        :error="errores.stock"
      />
      <label class="field field--check">
        <input v-model="form.activo" type="checkbox" />
        <span>Producto activo</span>
      </label>
      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ editando ? 'Actualizar' : 'Crear' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="limpiar">Cancelar</BaseButton>
      </div>
    </form>

    <p v-if="cargando" class="status">Cargando productos…</p>
    <DataTable :rows="productos" :columns="columns">
      <template #actions="{ row }">
        <BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'
import { moneda } from '../utils/format'

const productos = ref([])
const error = ref('')
const cargando = ref(false)
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'precio', label: 'Precio', format: (v) => moneda(v) },
  { key: 'stock', label: 'Stock' },
  { key: 'activo', label: 'Activo', format: (v) => (v ? 'Sí' : 'No') },
]

const vacio = () => ({ nombre: '', descripcion: '', precio: 0, stock: 0, activo: true })
const vacioErrores = () => ({ nombre: '', descripcion: '', precio: '', stock: '' })
const form = reactive(vacio())
const errores = reactive(vacioErrores())

function validar() {
  Object.assign(errores, vacioErrores())
  if (!String(form.nombre).trim()) errores.nombre = 'El nombre es obligatorio.'
  else if (form.nombre.length > 120) errores.nombre = 'Máximo 120 caracteres.'
  if (form.descripcion && form.descripcion.length > 300) errores.descripcion = 'Máximo 300 caracteres.'
  const precio = Number(form.precio)
  if (form.precio === '' || Number.isNaN(precio) || precio < 0) errores.precio = 'Ingrese un precio mayor o igual a 0.'
  const stock = Number(form.stock)
  if (form.stock === '' || !Number.isInteger(stock) || stock < 0) errores.stock = 'Ingrese un entero mayor o igual a 0.'
  return !Object.values(errores).some(Boolean)
}

function limpiar() {
  Object.assign(form, vacio())
  Object.assign(errores, vacioErrores())
  editando.value = false
  idEditando.value = null
}

async function cargar() {
  cargando.value = true
  try {
    productos.value = (await productosApi.listar()).data
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
    const payload = { ...form, precio: Number(form.precio), stock: Number(form.stock) }
    if (editando.value) await productosApi.actualizar(idEditando.value, payload)
    else await productosApi.crear(payload)
    limpiar()
    await cargar()
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

function editar(producto) {
  Object.assign(form, { ...vacio(), ...producto, descripcion: producto.descripcion ?? '' })
  editando.value = true
  idEditando.value = producto.id
}

async function eliminar(producto) {
  if (!window.confirm(`¿Eliminar ${producto.nombre}?`)) return
  error.value = ''
  try {
    await productosApi.eliminar(producto.id)
    await cargar()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargar)
</script>
