# Graph Report - /Users/jay/Developer/claude-code-agent/src/memdir  (2026-04-09)

## Corpus Check
- 8 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 49 nodes · 68 edges · 10 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `loadMemoryPrompt()` - 5 edges
2. `getTeamMemPath()` - 5 edges
3. `validateTeamMemKey()` - 5 edges
4. `buildMemoryLines()` - 4 edges
5. `buildMemoryPrompt()` - 4 edges
6. `isRealPathWithinTeamDir()` - 4 edges
7. `validateTeamMemWritePath()` - 4 edges
8. `logMemoryDirCounts()` - 3 edges
9. `buildAssistantDailyLogPrompt()` - 3 edges
10. `buildSearchingPastContextSection()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `isTeamMemPath()` --calls--> `getTeamMemPath()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/memdir/teamMemPaths.ts → /Users/jay/Developer/claude-code-agent/src/memdir/teamMemPaths.ts  _Bridges community 2 → community 4_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.21
Nodes (4): getAutoMemPathOverride(), getAutoMemPathSetting(), hasAutoMemPathOverride(), validateMemoryPath()

### Community 1 - "Community 1"
Cohesion: 0.47
Nodes (8): buildAssistantDailyLogPrompt(), buildMemoryLines(), buildMemoryPrompt(), buildSearchingPastContextSection(), ensureMemoryDirExists(), loadMemoryPrompt(), logMemoryDirCounts(), truncateEntrypointContent()

### Community 2 - "Community 2"
Cohesion: 0.53
Nodes (6): getTeamMemPath(), isRealPathWithinTeamDir(), realpathDeepestExisting(), sanitizePathKey(), validateTeamMemKey(), validateTeamMemWritePath()

### Community 3 - "Community 3"
Cohesion: 0.7
Nodes (4): memoryAge(), memoryAgeDays(), memoryFreshnessNote(), memoryFreshnessText()

### Community 4 - "Community 4"
Cohesion: 0.6
Nodes (3): isTeamMemFile(), isTeamMemoryEnabled(), isTeamMemPath()

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (2): findRelevantMemories(), selectRelevantMemories()

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): PathTraversalError

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 7`** (2 nodes): `memoryTypes.ts`, `parseMemoryType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (2 nodes): `PathTraversalError`, `.constructor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (2 nodes): `teamMemPrompts.ts`, `buildCombinedMemoryPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PathTraversalError` connect `Community 8` to `Community 4`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `validateTeamMemKey()` connect `Community 2` to `Community 4`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `loadMemoryPrompt()` (e.g. with `logMemoryDirCounts()` and `buildAssistantDailyLogPrompt()`) actually correct?**
  _`loadMemoryPrompt()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `getTeamMemPath()` (e.g. with `isRealPathWithinTeamDir()` and `isTeamMemPath()`) actually correct?**
  _`getTeamMemPath()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `validateTeamMemKey()` (e.g. with `sanitizePathKey()` and `getTeamMemPath()`) actually correct?**
  _`validateTeamMemKey()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `buildMemoryLines()` (e.g. with `buildSearchingPastContextSection()` and `buildMemoryPrompt()`) actually correct?**
  _`buildMemoryLines()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `buildMemoryPrompt()` (e.g. with `buildMemoryLines()` and `truncateEntrypointContent()`) actually correct?**
  _`buildMemoryPrompt()` has 3 INFERRED edges - model-reasoned connections that need verification._