import { describe, it, expect, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { VoiceButton } from '../VoiceButton'

describe('VoiceButton', () => {
  const w = window as unknown as {
    SpeechRecognition?: unknown
    webkitSpeechRecognition?: unknown
  }
  const origSR = w.SpeechRecognition
  const origWSR = w.webkitSpeechRecognition

  afterEach(() => {
    w.SpeechRecognition = origSR
    w.webkitSpeechRecognition = origWSR
  })

  it('returns null when SpeechRecognition is unavailable', () => {
    delete w.SpeechRecognition
    delete w.webkitSpeechRecognition
    const { container } = render(<VoiceButton onTranscript={() => {}} />)
    expect(container.firstChild).toBeNull()
  })

  it('renders button when available', () => {
    w.SpeechRecognition = class {}
    render(<VoiceButton onTranscript={() => {}} />)
    expect(screen.getByRole('button', { name: /voice/i })).toBeInTheDocument()
  })
})
