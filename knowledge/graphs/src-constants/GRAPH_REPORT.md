# Graph Report - /Users/jay/Developer/claude-code-agent/src/constants  (2026-04-09)

## Corpus Check
- 22 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 75 nodes · 91 edges · 25 communities detected
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `getSystemPrompt()` - 15 edges
2. `prependBullets()` - 7 edges
3. `computeSimpleEnvInfo()` - 6 edges
4. `computeEnvInfo()` - 5 edges
5. `getClaudeAiBaseUrl()` - 4 edges
6. `getSimpleSystemSection()` - 4 edges
7. `getSessionSpecificGuidanceSection()` - 4 edges
8. `getMcpInstructionsSection()` - 3 edges
9. `getSimpleDoingTasksSection()` - 3 edges
10. `getUsingYourToolsSection()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `getSystemPrompt()` --calls--> `getMcpInstructionsSection()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts → /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts  _Bridges community 12 → community 0_
- `getSimpleSystemSection()` --calls--> `prependBullets()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts → /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts  _Bridges community 2 → community 11_
- `computeSimpleEnvInfo()` --calls--> `prependBullets()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts → /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts  _Bridges community 2 → community 1_
- `getSystemPrompt()` --calls--> `getSimpleSystemSection()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts → /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts  _Bridges community 11 → community 0_
- `getSystemPrompt()` --calls--> `getSimpleDoingTasksSection()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts → /Users/jay/Developer/claude-code-agent/src/constants/prompts.ts  _Bridges community 2 → community 0_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.26
Nodes (9): getActionsSection(), getFunctionResultClearingSection(), getLanguageSection(), getOutputEfficiencySection(), getProactiveSection(), getScratchpadInstructions(), getSimpleIntroSection(), getSystemPrompt() (+1 more)

### Community 1 - "Community 1"
Cohesion: 0.38
Nodes (7): computeEnvInfo(), computeSimpleEnvInfo(), enhanceSystemPromptWithEnvDetails(), getDiscoverSkillsGuidance(), getKnowledgeCutoff(), getShellInfoLine(), getUnameSR()

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (6): getAgentToolSection(), getSessionSpecificGuidanceSection(), getSimpleDoingTasksSection(), getSimpleToneAndStyleSection(), getUsingYourToolsSection(), prependBullets()

### Community 3 - "Community 3"
Cohesion: 0.5
Nodes (2): fileSuffixForOauthConfig(), getOauthConfigType()

### Community 4 - "Community 4"
Cohesion: 0.4
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 0.7
Nodes (4): getClaudeAiBaseUrl(), getRemoteSessionUrl(), isRemoteSessionLocal(), isRemoteSessionStaging()

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (2): getAttributionHeader(), isAttributionHeaderEnabled()

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (0): 

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (2): getHooksSection(), getSimpleSystemSection()

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (2): getMcpInstructions(), getMcpInstructionsSection()

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

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 10`** (2 nodes): `keys.ts`, `getGrowthBookClientKey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `getHooksSection()`, `getSimpleSystemSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `getMcpInstructions()`, `getMcpInstructionsSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `spinnerVerbs.ts`, `getSpinnerVerbs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `apiLimits.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `betas.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `cyberRiskInstruction.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `errorIds.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `github-app.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `messages.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `querySource.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `toolLimits.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `tools.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `turnCompletionVerbs.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `xml.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `getSystemPrompt()` connect `Community 0` to `Community 1`, `Community 2`, `Community 11`, `Community 12`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `prependBullets()` connect `Community 2` to `Community 0`, `Community 1`, `Community 11`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `computeSimpleEnvInfo()` connect `Community 1` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `getSystemPrompt()` (e.g. with `computeSimpleEnvInfo()` and `getSystemRemindersSection()`) actually correct?**
  _`getSystemPrompt()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `prependBullets()` (e.g. with `getSimpleSystemSection()` and `getSimpleDoingTasksSection()`) actually correct?**
  _`prependBullets()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `computeSimpleEnvInfo()` (e.g. with `getSystemPrompt()` and `getUnameSR()`) actually correct?**
  _`computeSimpleEnvInfo()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `computeEnvInfo()` (e.g. with `getUnameSR()` and `getKnowledgeCutoff()`) actually correct?**
  _`computeEnvInfo()` has 4 INFERRED edges - model-reasoned connections that need verification._