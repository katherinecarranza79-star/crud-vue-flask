import { describe, expect, it } from 'vitest'
import { esCorreo, moneda } from '../utils/format'

describe('format', () => {
  it('valida correos', () => {
    expect(esCorreo('ana@example.com')).toBe(true)
    expect(esCorreo('ana@')).toBe(false)
  })
  it('formatea moneda en quetzales', () => {
    expect(moneda(1500)).toBe('Q1,500.00')
  })
})
