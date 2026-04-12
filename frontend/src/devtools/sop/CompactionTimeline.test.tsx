import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { CompactionTimeline } from './CompactionTimeline';

beforeEach(() => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      turns: [
        { turn: 0, layers: { system: 500, conversation: 100 } },
        { turn: 1, layers: { system: 500, conversation: 600 } },
      ],
      events: [
        { turn: 1, kind: 'scratchpad_write', detail: 'sql result' },
        { turn: 2, kind: 'compaction', detail: 'threshold hit' },
      ],
    }),
  }) as unknown as typeof fetch;
});

describe('CompactionTimeline', () => {
  it('renders turns and events', async () => {
    render(<CompactionTimeline traceId="eval-x" />);
    await waitFor(() => {
      expect(screen.getByText(/Turn 0/)).toBeInTheDocument();
      expect(screen.getByText(/Turn 1/)).toBeInTheDocument();
      expect(screen.getByText(/scratchpad_write/)).toBeInTheDocument();
      expect(screen.getByText(/compaction/)).toBeInTheDocument();
    });
  });
});
