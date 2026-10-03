import http from './http'

export const pedidosApi = {
  listar: () => http.get('/pedidos'),
  obtener: (id) => http.get(`/pedidos/${id}`),
  crear: (data) => http.post('/pedidos', data),
  actualizar: (id, data) => http.put(`/pedidos/${id}`, data),
  eliminar: (id) => http.delete(`/pedidos/${id}`),
}
