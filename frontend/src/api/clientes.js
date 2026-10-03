import http from './http'

export const clientesApi = {
  listar: () => http.get('/clientes'),
  obtener: (id) => http.get(`/clientes/${id}`),
  crear: (data) => http.post('/clientes', data),
  actualizar: (id, data) => http.put(`/clientes/${id}`, data),
  eliminar: (id) => http.delete(`/clientes/${id}`),
}
