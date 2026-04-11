# Graph Report - /Users/jay/Developer/claude-code-agent/src/tools  (2026-04-09)

## Corpus Check
- 184 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 640 nodes · 854 edges · 94 communities detected
- Extraction: 64% EXTRACTED · 36% INFERRED · 0% AMBIGUOUS · INFERRED: 308 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `bashToolHasPermission()` - 12 edges
2. `getPrompt()` - 8 edges
3. `checkPathConstraintsForStatement()` - 8 edges
4. `handleSpawnSeparateWindow()` - 8 edges
5. `suggestionForExactCommand()` - 7 edges
6. `matchingRulesForInput()` - 7 edges
7. `bashToolCheckExactMatchPermission()` - 7 edges
8. `sedCommandIsAllowedByAllowlist()` - 7 edges
9. `handleSpawnSplitPane()` - 7 edges
10. `runAsyncAgentLifecycle()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `getPrompt()` --calls--> `shouldInjectAgentListInMessages()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/ToolSearchTool/prompt.ts → /Users/jay/Developer/claude-code-agent/src/tools/AgentTool/prompt.ts
- `getPrompt()` --calls--> `getSleepGuidance()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/ToolSearchTool/prompt.ts → /Users/jay/Developer/claude-code-agent/src/tools/PowerShellTool/prompt.ts
- `getPrompt()` --calls--> `getEditionSection()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/ToolSearchTool/prompt.ts → /Users/jay/Developer/claude-code-agent/src/tools/PowerShellTool/prompt.ts
- `renderToolResultMessage()` --calls--> `truncateCommand()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/WebSearchTool/UI.tsx → /Users/jay/Developer/claude-code-agent/src/tools/TaskStopTool/UI.tsx
- `checkPathConstraints()` --calls--> `validateOutputRedirections()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/PowerShellTool/pathValidation.ts → /Users/jay/Developer/claude-code-agent/src/tools/BashTool/pathValidation.ts

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (26): applyCurlyDoubleQuotes(), applyCurlySingleQuotes(), applyEditToFile(), areFileEditsEquivalent(), areFileEditsInputsEquivalent(), buildImageToolResult(), checkDomainBlocklist(), DomainBlockedError (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (27): dedup(), formatAgentLine(), formatCommandDescription(), formatCommandsWithinBudget(), generateModelSection(), generatePrompt(), getBackgroundUsageNote(), getCharBudget() (+19 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (19): countLines(), FileWriteToolCreatedMessage(), getAgentOutputTaskId(), getSearchOrReadInfo(), getSearchSummary(), getToolUseSummary(), hasProgressMessage(), MCPTextOutput() (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (16): bashCommandIsSafe_DEPRECATED(), bashCommandIsSafeAsync_DEPRECATED(), extractQuotedContent(), hasBackslashEscapedOperator(), hasBackslashEscapedWhitespace(), hasSafeHeredocSubstitution(), hasUnescapedChar(), isEscapedAtPosition() (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (27): awaitClassifierAutoApproval(), bashToolCheckExactMatchPermission(), bashToolCheckPermission(), bashToolHasPermission(), buildPendingClassifierCheck(), checkCommandAndSuggestRules(), checkEarlyExitDeny(), checkSandboxAutoAllow() (+19 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (8): checkComObject(), checkDangerousFilePathExecution(), checkEncodedCommand(), checkForEachMemberName(), checkPwshCommandOrFile(), checkStartProcess(), isPowerShellExecutable(), psExeHasParamAbbreviation()

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (23): astRedirectsToOutputRedirections(), checkDenyRuleForGuessedPath(), checkPathConstraints(), checkPathConstraintsForStatement(), createPathChecker(), dangerousRemovalDeny(), expandTilde(), extractPathsFromCommand() (+15 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (21): checkReadOnlyConstraints(), commandHasAnyGit(), commandWritesToGitInternalPaths(), containsUnquotedExpansion(), extractWritePathsFromSubcommand(), getCommandAllowlist(), isAllowlistedCommand(), isAllowlistedPipelineTail() (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.24
Nodes (17): extractMarkupText(), formatCallHierarchyItem(), formatDocumentSymbolNode(), formatDocumentSymbolResult(), formatFindReferencesResult(), formatGoToDefinitionResult(), formatHoverResult(), formatIncomingCallsResult() (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (6): callInner(), createImageResponse(), detectSessionFileType(), MaxFileReadTokenExceededError, readImageWithTokenBudget(), validateContentTokens()

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (2): parseAgentFromMarkdown(), parseHooksFromFrontmatter()

### Community 11 - "Community 11"
Cohesion: 0.35
Nodes (13): buildInheritedCliFlags(), ensureSession(), generateUniqueTeammateName(), getDefaultTeammateModel(), getTeammateCommand(), handleSpawn(), handleSpawnInProcess(), handleSpawnSeparateWindow() (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.27
Nodes (10): countSymbols(), countUniqueFiles(), countUniqueFilesFromCallItems(), countUniqueFilesFromIncomingCalls(), countUniqueFilesFromOutgoingCalls(), filterGitIgnoredLocations(), formatResult(), isLocationLink() (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.38
Nodes (10): checkAgentMemorySnapshot(), copySnapshotToLocal(), getSnapshotDirForAgent(), getSnapshotJsonPath(), getSyncedJsonPath(), initializeFromSnapshot(), markSnapshotSynced(), readJsonFile() (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.36
Nodes (9): classifyHandoffIfNeeded(), countToolUses(), emitTaskProgress(), extractPartialResult(), filterToolsForAgent(), finalizeAgentTool(), getLastToolUseName(), resolveAgentTools() (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.24
Nodes (3): getCommandTypeForLogging(), spawnBackgroundTask(), startBackgrounding()

### Community 16 - "Community 16"
Cohesion: 0.4
Nodes (9): checkSedConstraints(), containsDangerousOperations(), extractSedExpressions(), hasFileArgs(), isLinePrintingCommand(), isPrintCommand(), isSubstitutionCommand(), sedCommandIsAllowedByAllowlist() (+1 more)

### Community 17 - "Community 17"
Cohesion: 0.24
Nodes (3): getCommandTypeForLogging(), spawnBackgroundTask(), startBackgrounding()

### Community 18 - "Community 18"
Cohesion: 0.47
Nodes (8): extractCommandName(), filterRulesByContentsMatchingInput(), getSubCommandsForPermissionCheck(), matchingRulesForInput(), powershellToolCheckExactMatchPermission(), powershellToolCheckPermission(), powershellToolHasPermission(), suggestionForExactCommand()

### Community 19 - "Community 19"
Cohesion: 0.38
Nodes (9): detectGitOperation(), findPrInStdout(), gitCmdRe(), parseGitCommitId(), parseGitPushBranch(), parsePrNumberFromText(), parsePrUrl(), parseRefFromCommand() (+1 more)

### Community 20 - "Community 20"
Cohesion: 0.25
Nodes (2): findTeammateColor(), handleMessage()

### Community 21 - "Community 21"
Cohesion: 0.43
Nodes (6): getAgentMemoryDir(), getAgentMemoryEntrypoint(), getLocalAgentMemoryDir(), getMemoryScopeDisplay(), loadAgentMemoryPrompt(), sanitizeAgentTypeForPath()

### Community 22 - "Community 22"
Cohesion: 0.43
Nodes (6): checkPermissionMode(), isAcceptEditsAllowedCmdlet(), isFilesystemCommand(), isItemTypeParamAbbrev(), isSymlinkCreatingCommand(), validateCommandForMode()

### Community 23 - "Community 23"
Cohesion: 0.54
Nodes (7): isDotGitPathPS(), isGitInternalPathPS(), matchesDotGitPrefix(), matchesGitInternalPrefix(), normalizeGitPathArg(), resolveCwdReentry(), resolveEscapingPathToCwdRelative()

### Community 24 - "Community 24"
Cohesion: 0.32
Nodes (4): compileTermPatterns(), getDeferredToolsCacheKey(), maybeInvalidateCache(), searchToolsWithKeywords()

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 0.48
Nodes (4): extractBaseCommand(), getCommandSemantic(), heuristicallyExtractBaseCommand(), interpretCommandResult()

### Community 27 - "Community 27"
Cohesion: 0.38
Nodes (4): executeForkedSkill(), executeRemoteSkill(), extractUrlScheme(), isOfficialMarketplaceSkill()

### Community 28 - "Community 28"
Cohesion: 0.4
Nodes (2): buildChildMessage(), buildForkedMessages()

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 0.4
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 0.6
Nodes (3): bashToolCheckCommandOperatorPermissions(), checkCommandOperatorPermissions(), segmentedCommandPermissionResult()

### Community 32 - "Community 32"
Cohesion: 0.7
Nodes (4): debug(), getBridgeBaseUrl(), guessMimeType(), uploadBriefAttachment()

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (2): isSedInPlaceEdit(), parseSedEditCommand()

### Community 35 - "Community 35"
Cohesion: 0.83
Nodes (3): getImageCreator(), getImageProcessor(), unwrapDefault()

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (2): buildSyntheticOutputTool(), createSyntheticOutputTool()

### Community 37 - "Community 37"
Cohesion: 0.67
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 0.67
Nodes (0): 

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (2): areExplorePlanAgentsEnabled(), getBuiltInAgents()

### Community 41 - "Community 41"
Cohesion: 0.67
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (2): containsExcludedCommand(), shouldUseSandbox()

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (2): isBriefEnabled(), isBriefEntitled()

### Community 44 - "Community 44"
Cohesion: 0.67
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 0.67
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 0.67
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (2): classifyMcpToolForCollapse(), normalize()

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (2): createMcpAuthTool(), getConfigUrl()

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (2): isClmAllowedType(), normalizeTypeName()

### Community 51 - "Community 51"
Cohesion: 0.67
Nodes (0): 

### Community 52 - "Community 52"
Cohesion: 0.67
Nodes (0): 

### Community 53 - "Community 53"
Cohesion: 0.67
Nodes (0): 

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (0): 

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (0): 

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (0): 

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (0): 

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (0): 

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (0): 

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (0): 

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (0): 

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (0): 

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (0): 

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (0): 

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (0): 

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (0): 

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (0): 

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (0): 

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (0): 

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (0): 

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (0): 

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (0): 

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (0): 

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (0): 

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (0): 

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (0): 

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (0): 

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (0): 

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (0): 

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (0): 

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (0): 

### Community 88 - "Community 88"
Cohesion: 1.0
Nodes (0): 

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (0): 

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (0): 

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 54`** (2 nodes): `exploreAgent.ts`, `getExploreSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (2 nodes): `generalPurposeAgent.ts`, `getGeneralPurposeSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (2 nodes): `planAgent.ts`, `getPlanV2SystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (2 nodes): `constants.ts`, `isReplModeEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (2 nodes): `resumeAgent.ts`, `resumeAgentBackground()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (2 nodes): `commentLabel.ts`, `extractBashCommentLabel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (2 nodes): `destructiveCommandWarning.ts`, `getDestructiveCommandWarning()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (2 nodes): `FileEditTool.ts`, `readFileForEdit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (2 nodes): `limits.ts`, `getEnvMaxTokens()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `schemas.ts`, `isValidLSPOperation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (2 nodes): `symbolContext.ts`, `getSymbolAtPosition()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (2 nodes): `primitiveTools.ts`, `getReplPrimitiveTools()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (2 nodes): `TeamCreateTool.ts`, `generateUniqueTeamName()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (2 nodes): `preapproved.ts`, `isPreapprovedHost()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `statuslineSetup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `verificationAgent.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `toolName.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `EnterPlanModeTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `EnterWorktreeTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `ExitPlanModeV2Tool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `FileWriteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `GlobTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `ListMcpResourcesTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `MCPTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `NotebookEditTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `commonParameters.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `ReadMcpResourceTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `RemoteTriggerTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `CronCreateTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `CronDeleteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `CronListTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `TaskCreateTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `TaskGetTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (1 nodes): `TaskListTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `TaskStopTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `TaskUpdateTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `TeamDeleteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `TodoWriteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `TestingPermissionTool.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 11 inferred relationships involving `bashToolHasPermission()` (e.g. with `checkEarlyExitDeny()` and `buildPendingClassifierCheck()`) actually correct?**
  _`bashToolHasPermission()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `getPrompt()` (e.g. with `shouldInjectAgentListInMessages()` and `getBackgroundUsageNote()`) actually correct?**
  _`getPrompt()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `checkPathConstraintsForStatement()` (e.g. with `checkPathConstraints()` and `extractPathsFromCommand()`) actually correct?**
  _`checkPathConstraintsForStatement()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `handleSpawnSeparateWindow()` (e.g. with `resolveTeammateModel()` and `generateUniqueTeammateName()`) actually correct?**
  _`handleSpawnSeparateWindow()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `suggestionForExactCommand()` (e.g. with `extractPrefixBeforeHeredoc()` and `getSimpleCommandPrefix()`) actually correct?**
  _`suggestionForExactCommand()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._