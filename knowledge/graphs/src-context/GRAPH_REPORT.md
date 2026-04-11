# Graph Report - /Users/jay/Developer/claude-code-agent/src/context  (2026-04-09)

## Corpus Check
- 9 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 45 nodes · 44 edges · 9 communities detected
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `useStats()` - 5 edges
2. `useVoiceStore()` - 4 edges
3. `createStatsStore()` - 2 edges
4. `StatsProvider()` - 2 edges
5. `useCounter()` - 2 edges
6. `useGauge()` - 2 edges
7. `useTimer()` - 2 edges
8. `useSet()` - 2 edges
9. `useVoiceState()` - 2 edges
10. `useSetVoiceState()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (7): createStatsStore(), StatsProvider(), useCounter(), useGauge(), useSet(), useStats(), useTimer()

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (0): 

### Community 2 - "Community 2"
Cohesion: 0.43
Nodes (4): useGetVoiceState(), useSetVoiceState(), useVoiceState(), useVoiceStore()

### Community 3 - "Community 3"
Cohesion: 0.33
Nodes (0): 

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (0): 

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (0): 

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 4 inferred relationships involving `useStats()` (e.g. with `useCounter()` and `useGauge()`) actually correct?**
  _`useStats()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `useVoiceStore()` (e.g. with `useVoiceState()` and `useSetVoiceState()`) actually correct?**
  _`useVoiceStore()` has 3 INFERRED edges - model-reasoned connections that need verification._