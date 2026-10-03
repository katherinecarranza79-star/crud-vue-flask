import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import DataTable from '../components/DataTable.vue'

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'activo', label: 'Activo', format: (v) => (v ? 'Sí' : 'No') },
]

describe('DataTable', () => {
  it('muestra mensaje cuando no hay filas', () => {
    const wrapper = mount(DataTable, { props: { rows: [], columns } })
    expect(wrapper.text()).toContain('No hay registros.')
  })

  it('renderiza filas y aplica format', () => {
    const wrapper = mount(DataTable, {
      props: { rows: [{ id: 1, activo: true }], columns },
      slots: { actions: '<button>Editar</button>' },
    })
    expect(wrapper.text()).toContain('Sí')
    expect(wrapper.find('button').text()).toBe('Editar')
  })
})
