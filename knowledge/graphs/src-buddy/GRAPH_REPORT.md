# Graph Report - /Users/jay/Developer/claude-code-agent/src/buddy  (2026-04-09)

## Corpus Check
- 6 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 30 nodes · 39 edges · 8 communities detected
- Extraction: 62% EXTRACTED · 38% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `rollFrom()` - 6 edges
2. `roll()` - 5 edges
3. `rollWithSeed()` - 4 edges
4. `spriteColWidth()` - 3 edges
5. `mulberry32()` - 3 edges
6. `hashString()` - 3 edges
7. `pick()` - 3 edges
8. `rollStats()` - 3 edges
9. `getCompanion()` - 3 edges
10. `wrap()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `rollFrom()` --calls--> `rollRarity()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/buddy/companion.ts → /Users/jay/Developer/claude-code-agent/src/buddy/companion.ts  _Bridges community 2 → community 5_
- `roll()` --calls--> `rollFrom()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/buddy/companion.ts → /Users/jay/Developer/claude-code-agent/src/buddy/companion.ts  _Bridges community 5 → community 3_
- `getCompanion()` --calls--> `roll()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/buddy/companion.ts → /Users/jay/Developer/claude-code-agent/src/buddy/companion.ts  _Bridges community 3 → community 2_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.53
Nodes (5): companionReservedColumns(), CompanionSprite(), SpeechBubble(), spriteColWidth(), wrap()

### Community 1 - "Community 1"
Cohesion: 0.4
Nodes (0): 

### Community 2 - "Community 2"
Cohesion: 0.67
Nodes (3): companionUserId(), getCompanion(), rollRarity()

### Community 3 - "Community 3"
Cohesion: 0.67
Nodes (4): hashString(), mulberry32(), roll(), rollWithSeed()

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (3): pick(), rollFrom(), rollStats()

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 7`** (1 nodes): `types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `rollFrom()` connect `Community 5` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `roll()` connect `Community 3` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `rollWithSeed()` connect `Community 3` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `rollFrom()` (e.g. with `rollRarity()` and `pick()`) actually correct?**
  _`rollFrom()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `roll()` (e.g. with `rollFrom()` and `mulberry32()`) actually correct?**
  _`roll()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `rollWithSeed()` (e.g. with `rollFrom()` and `mulberry32()`) actually correct?**
  _`rollWithSeed()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `spriteColWidth()` (e.g. with `companionReservedColumns()` and `CompanionSprite()`) actually correct?**
  _`spriteColWidth()` has 2 INFERRED edges - model-reasoned connections that need verification._