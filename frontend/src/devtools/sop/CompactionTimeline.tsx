import { useEffect, useState } from 'react';
import { fetchTimeline, Timeline } from './api';

interface Props {
  traceId: string;
}

export function CompactionTimeline({ traceId }: Props) {
  const [data, setData] = useState<Timeline | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTimeline(traceId).then(setData).catch((e: Error) => setError(e.message));
  }, [traceId]);

  if (error) return <div className="sop-error">Error: {error}</div>;
  if (data === null) return <div className="sop-loading">Loading…</div>;
  if (data.turns.length === 0) return <div className="sop-empty">No timeline data.</div>;

  const maxTotal = Math.max(
    ...data.turns.map((t) => Object.values(t.layers).reduce((a, b) => a + b, 0)),
  );

  return (
    <div className="sop-compaction-timeline">
      <h3>Compaction &amp; Scratchpad — {traceId}</h3>
      <div className="sop-timeline-stack">
        {data.turns.map((t) => {
          const total = Object.values(t.layers).reduce((a, b) => a + b, 0);
          const height = maxTotal > 0 ? (total / maxTotal) * 100 : 0;
          return (
            <div key={t.turn} className="sop-timeline-bar" style={{ height: `${height}%` }}>
              <span>Turn {t.turn}</span>
              <small>{total} tokens</small>
            </div>
          );
        })}
      </div>
      <div className="sop-timeline-events">
        <strong>Events</strong>
        <ul>
          {data.events.map((e, i) => (
            <li key={i}>
              t{e.turn}: <strong>{e.kind}</strong> — {e.detail}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
