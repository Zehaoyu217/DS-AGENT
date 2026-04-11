# Graph Report - /Users/jay/Developer/claude-code-agent/src/skills  (2026-04-09)

## Corpus Check
- 20 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 91 nodes · 95 edges · 22 communities detected
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `loadSkillsFromCommandsDir()` - 6 edges
2. `getCommandName()` - 5 edges
3. `buildPrompt()` - 4 edges
4. `processContent()` - 3 edges
5. `buildInlineReference()` - 3 edges
6. `markdownTable()` - 3 edges
7. `getBundledSkillExtractDir()` - 3 edges
8. `extractBundledSkillFiles()` - 3 edges
9. `writeSkillFiles()` - 3 edges
10. `parseSkillFrontmatterFields()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `getCommandName()` --calls--> `isSkillFile()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/skills/loadSkillsDir.ts → /Users/jay/Developer/claude-code-agent/src/skills/loadSkillsDir.ts  _Bridges community 5 → community 6_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (0): 

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (5): extractBundledSkillFiles(), getBundledSkillExtractDir(), registerBundledSkill(), resolveSkillFilePath(), writeSkillFiles()

### Community 2 - "Community 2"
Cohesion: 0.31
Nodes (6): buildPrompt(), formatConnectorsInfo(), formatSetupNotes(), getConnectedClaudeAIConnectors(), sanitizeConnectorName(), taggedIdToUUID()

### Community 3 - "Community 3"
Cohesion: 0.48
Nodes (4): buildInlineReference(), buildPrompt(), getFilesForLanguage(), processContent()

### Community 4 - "Community 4"
Cohesion: 0.38
Nodes (3): generateActionsTable(), generateContextsTable(), markdownTable()

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (6): createSkillCommand(), isSkillFile(), loadSkillsFromCommandsDir(), parseHooksFromFrontmatter(), parseSkillFrontmatterFields(), transformSkillFiles()

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (4): buildNamespace(), getCommandName(), getRegularCommandName(), getSkillCommandName()

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (0): 

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 0.67
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 13`** (2 nodes): `claudeInChrome.ts`, `registerClaudeInChromeSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (2 nodes): `debug.ts`, `registerDebugSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `index.ts`, `initBundledSkills()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `remember.ts`, `registerRememberSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (2 nodes): `simplify.ts`, `registerSimplifySkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (2 nodes): `stuck.ts`, `registerStuckSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (2 nodes): `verify.ts`, `registerVerifySkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `claudeApiContent.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `verifyContent.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `loadSkillsFromCommandsDir()` connect `Community 5` to `Community 0`, `Community 6`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Why does `getCommandName()` connect `Community 6` to `Community 0`, `Community 5`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `loadSkillsFromCommandsDir()` (e.g. with `transformSkillFiles()` and `isSkillFile()`) actually correct?**
  _`loadSkillsFromCommandsDir()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `getCommandName()` (e.g. with `isSkillFile()` and `getSkillCommandName()`) actually correct?**
  _`getCommandName()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `buildPrompt()` (e.g. with `processContent()` and `getFilesForLanguage()`) actually correct?**
  _`buildPrompt()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `processContent()` (e.g. with `buildInlineReference()` and `buildPrompt()`) actually correct?**
  _`processContent()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `buildInlineReference()` (e.g. with `processContent()` and `buildPrompt()`) actually correct?**
  _`buildInlineReference()` has 2 INFERRED edges - model-reasoned connections that need verification._