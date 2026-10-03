import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    const data = error.response?.data
    let message = data?.error || 'No fue posible comunicarse con el servidor'
    if (Array.isArray(data?.details)) message += `: ${data.details.join(', ')}`
    return Promise.reject(new Error(message))
  },
)

export default http
