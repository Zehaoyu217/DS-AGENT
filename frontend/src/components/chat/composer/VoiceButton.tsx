import { useEffect, useRef, useState } from 'react'
import { Mic, MicOff } from 'lucide-react'

interface VoiceButtonProps {
  onTranscript: (text: string) => void
}

interface SpeechRecognitionLike {
  continuous: boolean
  interimResults: boolean
  onresult: ((e: { results: { [index: number]: { [index: number]: { transcript: string } } } }) => void) | null
  onend: (() => void) | null
  onerror: (() => void) | null
  start: () => void
  stop: () => void
}

type SpeechRecognitionCtor = new () => SpeechRecognitionLike

function getRecognitionCtor(): SpeechRecognitionCtor | null {
  const w = window as unknown as {
    SpeechRecognition?: SpeechRecognitionCtor
    webkitSpeechRecognition?: SpeechRecognitionCtor
  }
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null
}

export function VoiceButton({ onTranscript }: VoiceButtonProps) {
  const [supported, setSupported] = useState(false)
  const [active, setActive] = useState(false)
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null)

  useEffect(() => {
    setSupported(getRecognitionCtor() !== null)
  }, [])

  const start = () => {
    const Ctor = getRecognitionCtor()
    if (!Ctor) return
    const r = new Ctor()
    r.continuous = false
    r.interimResults = false
    r.onresult = (e) => {
      const text = e.results?.[0]?.[0]?.transcript ?? ''
      if (text) onTranscript(text)
    }
    r.onend = () => setActive(false)
    r.onerror = () => setActive(false)
    try {
      r.start()
      setActive(true)
    } catch {
      setActive(false)
    }
    recognitionRef.current = r
  }

  const stop = () => {
    recognitionRef.current?.stop?.()
    setActive(false)
  }

  if (!supported) return null
  return (
    <button
      type="button"
      aria-label="Voice"
      data-active={active}
      onClick={() => (active ? stop() : start())}
      className="flex h-7 w-7 items-center justify-center rounded-md"
      style={{ color: active ? 'var(--acc)' : 'var(--fg-2)' }}
    >
      {active ? <MicOff size={14} /> : <Mic size={14} />}
    </button>
  )
}
