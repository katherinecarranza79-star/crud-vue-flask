<template>
  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!rows.length">
          <td :colspan="columns.length + 1" class="empty">No hay registros.</td>
        </tr>
        <tr v-for="row in rows" :key="row.id">
          <td v-for="column in columns" :key="column.key">
            {{ column.format ? column.format(row[column.key], row) : row[column.key] }}
          </td>
          <td class="actions">
            <slot name="actions" :row="row" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  rows: { type: Array, default: () => [] },
  columns: { type: Array, required: true },
})
</script>
