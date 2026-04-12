import { useEffect, useState } from 'react';
import { listSessions, SOPSession } from './api';

export function SessionReplay() {
  const [sessions, setSessions] = useState<SOPSession[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listSessions()
      .then(setSessions)
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error) return <div className="sop-error">Error: {error}</div>;
  if (sessions === null) return <div className="sop-loading">Loading…</div>;
  if (sessions.length === 0) return <div className="sop-empty">No SOP sessions yet.</div>;

  return (
    <div className="sop-session-replay">
      <h3>SOP Session Replay</h3>
      <ul className="sop-session-list">
        {sessions.map((s) => {
          const after = (s.outcome.grade_after as string) ?? '?';
          return (
            <li key={s.session_id} className="sop-session-item">
              <div className="sop-session-header">
                <span className="sop-session-id">{s.session_id}</span>
                <span className="sop-session-bucket">{s.triage.bucket}</span>
                <span className="sop-session-grade">
                  {s.overall_grade_before} → {after}
                </span>
              </div>
              <div className="sop-session-fix">{s.fix.name}</div>
              <div className="sop-session-evidence">
                {s.triage.evidence.map((e, i) => (
                  <div key={i}>• {e}</div>
                ))}
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
