export const moneda = (valor) =>
  `Q${Number(valor).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`

export const esCorreo = (valor) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(valor)
