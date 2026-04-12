import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { SessionReplay } from './SessionReplay';

const mockSession = {
  session_id: '2026-04-12-level3-001',
  date: '2026-04-12',
  level: 3,
  overall_grade_before: 'C',
  triage: { bucket: 'context', evidence: ['e'], hypothesis: 'h' },
  fix: {
    ladder_id: 'context-01', name: 'Lower threshold',
    files_changed: ['backend/app/context/manager.py'],
    model_used_for_fix: 'sonnet', cost_bucket: 'trivial',
  },
  outcome: { grade_after: 'B', regressions: 'none', iterations: 1, success: true },
  trace_links: { before: 'a.json', after: 'b.json' },
  preflight: { evaluation_bias: 'pass', data_quality: 'pass', determinism: 'pass' },
};

beforeEach(() => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ sessions: [mockSession] }),
  }) as unknown as typeof fetch;
});

describe('SessionReplay', () => {
  it('renders session list from API', async () => {
    render(<SessionReplay />);
    await waitFor(() => {
      expect(screen.getByText('2026-04-12-level3-001')).toBeInTheDocument();
      expect(screen.getByText(/context/i)).toBeInTheDocument();
      expect(screen.getByText(/C.*→.*B/)).toBeInTheDocument();
    });
  });

  it('shows empty state when no sessions', async () => {
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ sessions: [] }),
    });
    render(<SessionReplay />);
    await waitFor(() => {
      expect(screen.getByText(/no sop sessions yet/i)).toBeInTheDocument();
    });
  });
});
