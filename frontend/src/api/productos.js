import http from './http'

export const productosApi = {
  listar: () => http.get('/productos'),
  obtener: (id) => http.get(`/productos/${id}`),
  crear: (data) => http.post('/productos', data),
  actualizar: (id, data) => http.put(`/productos/${id}`, data),
  eliminar: (id) => http.delete(`/productos/${id}`),
}
