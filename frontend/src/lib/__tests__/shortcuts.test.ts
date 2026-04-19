import { describe, it, expect } from 'vitest'
import { CMD } from '../shortcuts'

describe('shortcuts CMD registry', () => {
  it('exposes CYCLE_MODEL id', () => {
    expect(CMD.CYCLE_MODEL).toBe('cycle-model')
  })

  it('exposes TOGGLE_EXTENDED id', () => {
    expect(CMD.TOGGLE_EXTENDED).toBe('toggle-extended')
  })
})
