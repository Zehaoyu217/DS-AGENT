# Graph Report - /Users/jay/Developer/claude-code-agent/src  (2026-04-09)

## Corpus Check
- 1994 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 10801 nodes · 15224 edges · 1292 communities detected
- Extraction: 64% EXTRACTED · 36% INFERRED · 0% AMBIGUOUS · INFERRED: 5515 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Cursor` - 57 edges
2. `YogaLayoutNode` - 51 edges
3. `mk()` - 47 edges
4. `Ink` - 46 edges
5. `peek()` - 43 edges
6. `skipBlanks()` - 37 edges
7. `advance()` - 36 edges
8. `getProject()` - 34 edges
9. `Project` - 31 edges
10. `nextToken()` - 29 edges

## Surprising Connections (you probably didn't know these)
- `onChangeVerbose()` --calls--> `saveGlobalConfig()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/components/Settings/Config.tsx → /Users/jay/Developer/claude-code-agent/src/utils/config.ts
- `onChange()` --calls--> `saveGlobalConfig()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/components/Settings/Config.tsx → /Users/jay/Developer/claude-code-agent/src/utils/config.ts
- `checkPathConstraintsForStatement()` --calls--> `formatDirectoryList()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/PowerShellTool/pathValidation.ts → /Users/jay/Developer/claude-code-agent/src/utils/permissions/pathValidation.ts
- `getPrompt()` --calls--> `getSleepGuidance()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/AgentTool/prompt.ts → /Users/jay/Developer/claude-code-agent/src/tools/PowerShellTool/prompt.ts
- `getPrompt()` --calls--> `getEditionSection()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/tools/AgentTool/prompt.ts → /Users/jay/Developer/claude-code-agent/src/tools/PowerShellTool/prompt.ts

## Communities

### Community 0 - "Adddirpluginsettings"
Cohesion: 0.0
Nodes (261): backupTerminalPreferences(), checkAndRestoreTerminalBackup(), getTerminalPlistPath(), getTerminalRecoveryInfo(), markTerminalSetupComplete(), markTerminalSetupInProgress(), getRecordFilePath(), getTerminalSize() (+253 more)

### Community 1 - "Apiqueryhookhelper"
Cohesion: 0.01
Nodes (230): call(), createFork(), deriveFirstPrompt(), getUniqueForkName(), addCacheBreakpoints(), assistantMessageToMessageParam(), cleanupStream(), clearStreamIdleTimers() (+222 more)

### Community 2 - "Add Dir"
Cohesion: 0.01
Nodes (99): getAgentThemeColor(), _temp8(), companionReservedColumns(), CompanionSprite(), SpeechBubble(), spriteColWidth(), wrap(), checkAutoCompactDisabled() (+91 more)

### Community 3 - "Audit Log"
Cohesion: 0.02
Nodes (77): auditLog(), logAuthEvent(), logCommandExecution(), logFileAccess(), logPathTraversalBlocked(), logRateLimitExceeded(), sanitizeDetails(), checkDenylist() (+69 more)

### Community 4 - "Sessionstorage"
Cohesion: 0.03
Nodes (112): adoptResumedSessionFile(), appendEntryToFile(), applyPreservedSegmentRelinks(), applySnipRemovals(), buildAttributionSnapshotChain(), buildConversationChain(), buildFileHistorySnapshotChain(), cacheSessionTitle() (+104 more)

### Community 5 - "Abortcontroller"
Cohesion: 0.02
Nodes (83): createAbortController(), createChildAbortController(), axiosGetWithRetry(), createDefaultEnvironment(), fetchCodeSessionsFromSessionsAPI(), fetchSession(), filterSwarmFieldsFromSchema(), getOAuthHeaders() (+75 more)

### Community 6 - "Adapter"
Cohesion: 0.02
Nodes (40): parseCookies(), SessionStore, ApiKeyAdapter, AuthCodeListener, MagicLinkAdapter, readSmtpConfig(), sendBareSmtp(), sendMail() (+32 more)

### Community 7 - "Messages"
Cohesion: 0.03
Nodes (70): appendMessageTagToUserMessage(), baseCreateAssistantMessage(), buildMessageLookups(), contentHasToolReference(), createAssistantAPIErrorMessage(), createAssistantMessage(), createModelSwitchBreadcrumbs(), createSyntheticUserCaveatMessage() (+62 more)

### Community 8 - "Auth"
Cohesion: 0.03
Nodes (83): AuthenticationCancelledError, authLogin(), calculateApiKeyHelperTTL(), checkAndRefreshOAuthTokenIfNeeded(), checkAndRefreshOAuthTokenIfNeededImpl(), checkGcpCredentialsValid(), ClaudeAuthProvider, clearMcpClientConfig() (+75 more)

### Community 9 - "Desktopdeeplink"
Cohesion: 0.02
Nodes (53): buildDesktopDeepLink(), getDesktopInstallStatus(), getDesktopVersion(), isDesktopInstalled(), isDevMode(), openCurrentSessionInDesktop(), openDeepLink(), checkForReleaseNotes() (+45 more)

### Community 10 - "Diff"
Cohesion: 0.02
Nodes (59): escapeForDiff(), getPatchForDisplay(), getPatchFromContents(), DiffDialog(), turnDiffToDiffData(), cachedHighlight(), calculateWordDiffs(), formatDiff() (+51 more)

### Community 11 - "Utils"
Cohesion: 0.03
Nodes (54): applyCurlyDoubleQuotes(), applyCurlySingleQuotes(), applyEditToFile(), areFileEditsEquivalent(), areFileEditsInputsEquivalent(), buildImageToolResult(), checkDomainBlocklist(), DomainBlockedError (+46 more)

### Community 12 - "Cursor"
Cohesion: 0.05
Nodes (6): Cursor, isVimPunctuation(), isVimWhitespace(), isVimWordChar(), MeasuredText, WrappedLine

### Community 13 - "Index"
Cohesion: 0.04
Nodes (64): applyRemoteEntriesToLocal(), attachAnalyticsSink(), batchDeltaByBytes(), buildEntriesFromLocalFiles(), clearPolicyLimitsCache(), clearRemoteManagedSettingsCache(), computeChecksum(), computeChecksumFromSettings() (+56 more)

### Community 14 - "Config"
Cohesion: 0.04
Nodes (70): addMcpConfig(), addScopeToServers(), checkHasTrustDialogAccepted(), commandArraysMatch(), computeTrustDialogAccepted(), dedupClaudeAiMcpServers(), dedupPluginMcpServers(), deriveAddress() (+62 more)

### Community 15 - "Bashparser"
Cohesion: 0.15
Nodes (79): advance(), byteAt(), byteLengthUtf8(), checkBudget(), consumeKeyword(), isArithStop(), isBaseDigit(), isDigit() (+71 more)

### Community 16 - "Attachments"
Cohesion: 0.04
Nodes (40): collectRecentSuccessfulTools(), collectSurfacedMemories(), countAutoModeAttachmentsSinceLastExit(), countPlanModeAttachmentsSinceLastExit(), extractAgentMentions(), extractAtMentionedFiles(), extractMcpResourceMentions(), filterToBundledAndMcp() (+32 more)

### Community 17 - "Client"
Cohesion: 0.04
Nodes (47): buildFetch(), callIdeRpc(), callMCPTool(), clearMcpAuthCache(), clearServerCache(), computeDomainSeparator(), computeStructHash(), configureApiKeyHeaders() (+39 more)

### Community 18 - "Parser"
Cohesion: 0.06
Nodes (41): buildParseScript(), classifyCommandName(), ensureArray(), extractCommandArguments(), extractEnvVars(), findCommandNode(), getAllCommandNames(), getAllRedirections() (+33 more)

### Community 19 - "Hooks"
Cohesion: 0.06
Nodes (35): createBaseHookInput(), decisionReasonToString(), execCommandHook(), executeConfigChangeHooks(), executeCwdChangedHooks(), executeElicitationHooks(), executeElicitationResultHooks(), executeEnvHooks() (+27 more)

### Community 20 - "Prompt"
Cohesion: 0.05
Nodes (29): dedup(), formatAgentLine(), formatCommandDescription(), formatCommandsWithinBudget(), formatCompactSummary(), generateModelSection(), generatePrompt(), getBackgroundUsageNote() (+21 more)

### Community 21 - "Yoga"
Cohesion: 0.04
Nodes (1): YogaLayoutNode

### Community 22 - "Ink"
Cohesion: 0.07
Nodes (3): drainStdin(), Ink, makeAltScreenParkPatch()

### Community 23 - "Screen"
Cohesion: 0.08
Nodes (27): blitRegion(), cellAt(), cellAtCI(), cellAtIndex(), charInCellAt(), CharPool, clearRegion(), diff() (+19 more)

### Community 24 - "Errors"
Cohesion: 0.06
Nodes (28): AbortError, classifyAxiosError(), ClaudeError, ConfigParseError, errorMessage(), get3PModelFallbackSuggestion(), getAssistantMessageFromError(), getErrnoCode() (+20 more)

### Community 25 - "Prompts"
Cohesion: 0.09
Nodes (42): analyzeSectionSizes(), buildExtractAutoOnlyPrompt(), buildExtractCombinedPrompt(), buildMagicDocsUpdatePrompt(), buildSessionMemoryUpdatePrompt(), computeEnvInfo(), computeSimpleEnvInfo(), enhanceSystemPromptWithEnvDetails() (+34 more)

### Community 26 - "Model"
Cohesion: 0.08
Nodes (30): firstPartyNameToCanonical(), getBestModel(), getCanonicalName(), getClaudeAiUserDefaultModelDescription(), getDefaultHaikuModel(), getDefaultMainLoopModel(), getDefaultMainLoopModelSetting(), getDefaultOpusModel() (+22 more)

### Community 27 - "Settings"
Cohesion: 0.09
Nodes (32): consumeRawReadResult(), ensureMdmSettingsLoaded(), getAutoModeConfig(), getInitialSettings(), getManagedFileSettingsPresence(), getManagedSettingsFilePath(), getPolicySettingsOrigin(), getRelativeSettingsFilePathForSource() (+24 more)

### Community 28 - "Ide"
Cohesion: 0.09
Nodes (28): checkIdeConnection(), cleanupStaleIdeLockfiles(), detectIDEs(), detectRunningIDEs(), detectRunningIDEsCached(), detectRunningIDEsImpl(), findAvailableIDE(), getClaudeCodeVersion() (+20 more)

### Community 29 - "Marketplacemanager"
Cohesion: 0.14
Nodes (37): addMarketplaceSource(), cacheMarketplaceFromGit(), cacheMarketplaceFromUrl(), enhanceGitPullErrorMessages(), extractSshHost(), findSeedMarketplaceLocation(), getCachePathForSource(), getKnownMarketplacesFile() (+29 more)

### Community 30 - "Pluginloader"
Cohesion: 0.12
Nodes (36): assemblePluginLoadResult(), cachePlugin(), cachePluginSettings(), copyDir(), copyPluginToVersionedCache(), createPluginFromPath(), finishLoadingPluginFromPath(), generateTemporaryCacheNameForPlugin() (+28 more)

### Community 31 - "Filesystem"
Cohesion: 0.12
Nodes (35): allWorkingDirectories(), checkEditableInternalPath(), checkPathSafetyForAutoEdit(), checkReadableInternalPath(), checkReadPermissionForTool(), checkWritePermissionForTool(), ensureScratchpadDir(), generateSuggestions() (+27 more)

### Community 32 - "Permissionsetup"
Cohesion: 0.11
Nodes (34): checkAndDisableBypassPermissions(), findDangerousClassifierPermissions(), findOverlyBroadBashPermissions(), findOverlyBroadPowerShellPermissions(), formatPermissionSource(), getAutoModeEnabledState(), getAutoModeEnabledStateIfCached(), getAutoModeUnavailableNotification() (+26 more)

### Community 33 - "Yoloclassifier"
Cohesion: 0.11
Nodes (32): buildClaudeMdMessage(), buildToolLookup(), buildTranscriptEntries(), buildTranscriptForClassifier(), buildYoloSystemPrompt(), classifyYoloAction(), classifyYoloActionXml(), combineUsage() (+24 more)

### Community 34 - "Teammatemailbox"
Cohesion: 0.08
Nodes (11): clearMailbox(), createShutdownRequestMessage(), ensureInboxDir(), getInboxPath(), markMessageAsReadByIndex(), markMessagesAsRead(), markMessagesAsReadByPredicate(), readMailbox() (+3 more)

### Community 35 - "Insights"
Cohesion: 0.11
Nodes (32): aggregateData(), buildExportData(), detectMultiClauding(), escapeHtmlWithBold(), extractFacetsFromAPI(), extractToolStats(), formatTranscriptForFacets(), formatTranscriptWithSummarization() (+24 more)

### Community 36 - "Bashsecurity"
Cohesion: 0.08
Nodes (16): bashCommandIsSafe_DEPRECATED(), bashCommandIsSafeAsync_DEPRECATED(), extractQuotedContent(), hasBackslashEscapedOperator(), hasBackslashEscapedWhitespace(), hasSafeHeredocSubstitution(), hasUnescapedChar(), isEscapedAtPosition() (+8 more)

### Community 37 - "Gitfilesystem"
Cohesion: 0.14
Nodes (23): computeBranch(), computeDefaultBranch(), computeHead(), computeRemoteUrl(), getCachedBranch(), getCachedDefaultBranch(), getCachedHead(), getCachedRemoteUrl() (+15 more)

### Community 38 - "Perfettotracing"
Cohesion: 0.13
Nodes (30): buildTraceDocument(), closeOpenSpans(), emitPerfettoCounter(), emitPerfettoInstant(), emitProcessMetadata(), endInteractionPerfettoSpan(), endLLMRequestPerfettoSpan(), endToolPerfettoSpan() (+22 more)

### Community 39 - "Toolresultstorage"
Cohesion: 0.12
Nodes (30): applyToolResultBudget(), buildLargeToolResultMessage(), buildReplacement(), buildToolNameMap(), collectCandidatesByMessage(), collectCandidatesFromMessage(), contentSize(), createContentReplacementState() (+22 more)

### Community 40 - "Bashpermissions"
Cohesion: 0.14
Nodes (27): awaitClassifierAutoApproval(), bashToolCheckExactMatchPermission(), bashToolCheckPermission(), bashToolHasPermission(), buildPendingClassifierCheck(), checkCommandAndSuggestRules(), checkEarlyExitDeny(), checkSandboxAutoAllow() (+19 more)

### Community 41 - "Ccrclient"
Cohesion: 0.09
Nodes (5): accumulateStreamEvents(), CCRClient, CCRInitError, clearStreamAccumulatorForMessage(), scopeKey()

### Community 42 - "Permissions"
Cohesion: 0.12
Nodes (25): applyPermissionRulesToPermissionContext(), checkRuleBasedPermissions(), convertRulesToUpdates(), createPermissionRequestMessage(), filterDeniedAgents(), getAllowRules(), getAskRuleForTool(), getAskRules() (+17 more)

### Community 43 - "Tasks"
Cohesion: 0.17
Nodes (28): blockTask(), claimTask(), claimTaskWithBusyCheck(), clearLeaderTeamName(), createTask(), deleteTask(), ensureTaskListLockFile(), ensureTasksDir() (+20 more)

### Community 44 - "Installer"
Cohesion: 0.17
Nodes (29): atomicMoveToInstallPath(), attemptNpmUninstall(), checkInstall(), cleanupNpmInstallations(), cleanupOldVersions(), forceRemoveLock(), getBaseDirectories(), getBinaryName() (+21 more)

### Community 45 - "Pathvalidation"
Cohesion: 0.13
Nodes (25): astRedirectsToOutputRedirections(), checkDenyRuleForGuessedPath(), checkPathConstraints(), checkPathConstraintsForStatement(), createPathChecker(), dangerousRemovalDeny(), expandTilde(), extractPathsFromCommand() (+17 more)

### Community 46 - "Installedpluginsmanager"
Cohesion: 0.15
Nodes (25): addInstalledPlugin(), addPluginInstallation(), cleanupLegacyCache(), getGitCommitSha(), getInMemoryInstalledPlugins(), getInstalledPluginsFilePath(), getInstalledPluginsV2FilePath(), getPendingUpdateCount() (+17 more)

### Community 47 - "Powershellsecurity"
Cohesion: 0.09
Nodes (8): checkComObject(), checkDangerousFilePathExecution(), checkEncodedCommand(), checkForEachMemberName(), checkPwshCommandOrFile(), checkStartProcess(), isPowerShellExecutable(), psExeHasParamAbbreviation()

### Community 48 - "Growthbook"
Cohesion: 0.15
Nodes (24): checkGate_CACHED_OR_BLOCKING(), checkSecurityRestrictionGate(), checkStatsigFeatureGate_CACHED_MAY_BE_STALE(), getApiBaseUrlHost(), getConfigOverrides(), getDynamicConfig_BLOCKS_ON_INIT(), getDynamicConfig_CACHED_MAY_BE_STALE(), getEnvOverrides() (+16 more)

### Community 49 - "Claudemd"
Cohesion: 0.12
Nodes (23): clearMemoryFileCaches(), extractIncludePathsFromTokens(), getAllMemoryFilePaths(), getConditionalRulesForCwdLevelDirectory(), getExternalClaudeMdIncludes(), getManagedAndUserConditionalRules(), getMemoryFilesForNestedDirectory(), handleMemoryFileReadError() (+15 more)

### Community 50 - "Messagequeuemanager"
Cohesion: 0.13
Nodes (17): clearCommandQueue(), dequeue(), dequeueAll(), dequeueAllMatching(), dequeuePendingNotification(), enqueue(), enqueuePendingNotification(), extractImagesFromValue() (+9 more)

### Community 51 - "Collapsereadsearch"
Cohesion: 0.14
Nodes (24): collapseReadSearchGroups(), commandAsHint(), countToolUses(), createEmptyGroup(), getCollapsibleToolInfo(), getFilePathFromToolInput(), getFilePathsFromReadMessage(), getSearchOrReadFromContent() (+16 more)

### Community 52 - "Commitattribution"
Cohesion: 0.14
Nodes (23): attributionRestoreStateFromLog(), calculateCommitAttribution(), computeContentHash(), computeFileModificationState(), createEmptyAttributionState(), expandFilePath(), getAttributionRepoRoot(), getClientSurface() (+15 more)

### Community 53 - "Git"
Cohesion: 0.11
Nodes (17): captureUntrackedFiles(), findRemoteBase(), getBranch(), getFileStatus(), getGithubRepo(), getGitState(), getHead(), getIsClean() (+9 more)

### Community 54 - "Tmuxbackend"
Cohesion: 0.17
Nodes (6): acquirePaneCreationLock(), getTmuxColorName(), runTmuxInSwarm(), runTmuxInUserSession(), TmuxBackend, waitForPaneShellReady()

### Community 55 - "Worktree"
Cohesion: 0.14
Nodes (16): cleanupStaleAgentWorktrees(), copyWorktreeIncludeFiles(), createAgentWorktree(), createWorktreeForSession(), execIntoTmuxWorktree(), flattenSlug(), getOrCreateWorktree(), mkdirRecursive() (+8 more)

### Community 56 - "Sandbox Adapter"
Cohesion: 0.13
Nodes (17): addToExcludedCommands(), convertToSandboxRuntimeConfig(), getLinuxGlobPatternWarnings(), getSandboxEnabledSetting(), getSandboxUnavailableReason(), initialize(), isPlatformInEnabledList(), isSandboxingEnabled() (+9 more)

### Community 57 - "Diskoutput"
Cohesion: 0.14
Nodes (16): appendTaskOutput(), cleanupTaskOutput(), _clearOutputsForTest(), DiskTaskOutput, ensureOutputDir(), evictTaskOutput(), flushTaskOutput(), getOrCreateOutput() (+8 more)

### Community 58 - "Readonlyvalidation"
Cohesion: 0.14
Nodes (21): checkReadOnlyConstraints(), commandHasAnyGit(), commandWritesToGitInternalPaths(), containsUnquotedExpansion(), extractWritePathsFromSubcommand(), getCommandAllowlist(), isAllowlistedCommand(), isAllowlistedPipelineTail() (+13 more)

### Community 59 - "Withretry"
Cohesion: 0.11
Nodes (17): CannotRetryError, FallbackTriggeredError, getDefaultMaxRetries(), getMaxRetries(), getRetryAfter(), getRetryAfterMs(), handleAwsCredentialError(), handleGcpCredentialError() (+9 more)

### Community 60 - "Selection"
Cohesion: 0.12
Nodes (17): applySelectionOverlay(), captureScrolledRows(), charClass(), clearSelection(), comparePoints(), extendSelection(), extractRowText(), findPlainTextUrlAt() (+9 more)

### Community 61 - "Ast"
Cohesion: 0.24
Nodes (22): applyVarToScope(), collectCommands(), collectCommandSubstitution(), containsAnyPlaceholder(), extractSafeCatHeredoc(), maskBracesInQuotedContexts(), parseForSecurity(), parseForSecurityFromAst() (+14 more)

### Community 62 - "Effort"
Cohesion: 0.14
Nodes (20): call(), convertEffortValueToLevel(), executeEffort(), getDefaultEffortForModel(), getDisplayedEffortLevel(), getEffortEnvOverride(), getEffortLevelDescription(), getEffortSuffix() (+12 more)

### Community 63 - "Sessionstorageportable"
Cohesion: 0.16
Nodes (20): canonicalizePath(), captureCarry(), captureSnap(), compactBoundaryMarker(), extractJsonStringField(), extractLastJsonStringField(), finalizeOutput(), findProjectDir() (+12 more)

### Community 64 - "Session Manager"
Cohesion: 0.11
Nodes (2): SessionManager, UserHourlyRateLimiter

### Community 65 - "Structuredio"
Cohesion: 0.1
Nodes (2): exitWithMessage(), StructuredIO

### Community 66 - "Teamhelpers"
Cohesion: 0.19
Nodes (19): addHiddenPaneId(), cleanupTeamDirectories(), destroyWorktree(), getTeamDir(), getTeamFilePath(), killOrphanedTeammatePanes(), readTeamFile(), readTeamFileAsync() (+11 more)

### Community 67 - "Loadskillsdir"
Cohesion: 0.12
Nodes (10): buildNamespace(), createSkillCommand(), getCommandName(), getRegularCommandName(), getSkillCommandName(), isSkillFile(), loadSkillsFromCommandsDir(), parseHooksFromFrontmatter() (+2 more)

### Community 68 - "Modeloptions"
Cohesion: 0.18
Nodes (22): filterModelOptionsByAllowlist(), getCustomHaikuOption(), getCustomOpusOption(), getCustomSonnetOption(), getDefaultOptionForUser(), getHaiku35Option(), getHaiku45Option(), getHaikuOption() (+14 more)

### Community 69 - "Marketplacehelpers"
Cohesion: 0.13
Nodes (15): areSourcesEquivalentForBlocklist(), blockedConstraintMatches(), detectEmptyMarketplaceReason(), doesSourceMatchHostPattern(), extractGitHubRepoFromGitUrl(), extractHostFromSource(), formatFailureErrors(), formatFailureNames() (+7 more)

### Community 70 - "Filesuggestions"
Cohesion: 0.16
Nodes (19): collectDirectoryNames(), findCommonPrefix(), findLongestCommonPrefix(), findMatchingFiles(), generateFileSuggestions(), getClaudeConfigFiles(), getDirectoryNames(), getDirectoryNamesAsync() (+11 more)

### Community 71 - "Render Node To Output"
Cohesion: 0.15
Nodes (15): applyPaddingToText(), applyStylesToWrappedText(), blitEscapingAbsoluteDescendants(), buildCharToSegmentMap(), clipsBothAxes(), drainAdaptive(), drainProportional(), dropSubtreeCache() (+7 more)

### Community 72 - "Bridgemain"
Cohesion: 0.17
Nodes (19): addJitter(), BridgeHeadlessPermanentError, bridgeMain(), createHeadlessBridgeLogger(), fetchSessionTitle(), formatDelay(), isConnectionError(), isMultiSessionSpawnEnabled() (+11 more)

### Community 73 - "Websockettransport"
Cohesion: 0.15
Nodes (1): WebSocketTransport

### Community 74 - "Localagenttask"
Cohesion: 0.11
Nodes (8): backgroundAgentTask(), drainPendingMessages(), getProgressUpdate(), getTokenCountFromTracker(), isLocalAgentTask(), isPanelAgentTask(), killAllRunningAgentTasks(), killAsyncAgent()

### Community 75 - "Status"
Cohesion: 0.1
Nodes (3): buildPrimarySection(), buildSecondarySection(), Status()

### Community 76 - "Taskoutput"
Cohesion: 0.12
Nodes (1): TaskOutput

### Community 77 - "Voice"
Cohesion: 0.18
Nodes (16): checkRecordingAvailability(), checkVoiceDependencies(), detectPackageManager(), hasCommand(), linuxHasAlsaCards(), loadAudioNapi(), probeArecord(), requestMicrophonePermission() (+8 more)

### Community 78 - "Mockratelimits"
Cohesion: 0.12
Nodes (11): addExceededLimit(), applyMockHeaders(), checkMockFastModeRateLimit(), clearMockEarlyWarning(), clearMockHeaders(), getMockHeaders(), setMockEarlyWarning(), setMockHeader() (+3 more)

### Community 79 - "Csi"
Cohesion: 0.18
Nodes (18): csi(), cursorBack(), cursorDown(), cursorForward(), cursorMove(), cursorPosition(), cursorTo(), cursorUp() (+10 more)

### Community 80 - "Filestatecache"
Cohesion: 0.14
Nodes (6): cacheKeys(), cacheToObject(), cloneFileStateCache(), createFileStateCacheWithSizeLimit(), FileStateCache, mergeFileStateCaches()

### Community 81 - "Streamingtoolexecutor"
Cohesion: 0.15
Nodes (2): markToolUseAsComplete(), StreamingToolExecutor

### Community 82 - "Remoteagenttask"
Cohesion: 0.15
Nodes (13): enqueueRemoteNotification(), enqueueRemoteReviewFailureNotification(), enqueueRemoteReviewNotification(), enqueueUltraplanFailureNotification(), getRemoteTaskSessionUrl(), isRemoteTaskType(), markTaskNotified(), persistRemoteAgentMetadata() (+5 more)

### Community 83 - "Autoupdater"
Cohesion: 0.15
Nodes (13): acquireLock(), AutoUpdaterError, checkGlobalInstallPermissions(), getGcsDistTags(), getInstallationPrefix(), getLatestVersionFromGcs(), getLockFilePath(), getMaxVersion() (+5 more)

### Community 84 - "Parsedcommand"
Cohesion: 0.14
Nodes (7): buildParsedCommandFromRoot(), doParse(), extractPipePositions(), extractRedirectionNodes(), RegexParsedCommand_DEPRECATED, TreeSitterParsedCommand, visitNodes()

### Community 85 - "Commands"
Cohesion: 0.21
Nodes (17): addToken(), detectCommandSubstitution(), extractOutputRedirections(), filterControlOperators(), generatePlaceholders(), handleFileDescriptorRedirection(), handleRedirection(), hasDangerousExpansion() (+9 more)

### Community 86 - "Registry"
Cohesion: 0.16
Nodes (12): createITermBackend(), createTmuxBackend(), detectAndGetBackend(), ensureBackendsRegistered(), getBackendByType(), getInProcessBackend(), getPaneBackendExecutor(), getResolvedTeammateMode() (+4 more)

### Community 87 - "Fastmode"
Cohesion: 0.2
Nodes (15): getDisabledReasonMessage(), getFastModeRuntimeState(), getFastModeState(), getFastModeUnavailableReason(), getInitialFastModeSetting(), getOverageDisabledMessage(), handleFastModeOverageRejection(), isFastModeAvailable() (+7 more)

### Community 88 - "Toolsearch"
Cohesion: 0.19
Nodes (17): calculateDeferredToolDescriptionChars(), checkAutoThreshold(), extractDiscoveredToolNames(), getAutoToolSearchCharThreshold(), getAutoToolSearchPercentage(), getAutoToolSearchTokenThreshold(), getToolSearchMode(), getUnsupportedToolReferencePatterns() (+9 more)

### Community 89 - "Elicitationdialog"
Cohesion: 0.16
Nodes (9): commitTextField(), handleNavigation(), handleTextInputChange(), handleTextInputSubmit(), resolveFieldAsync(), setField(), unsetField(), updateValidationError() (+1 more)

### Community 90 - "Speculation"
Cohesion: 0.24
Nodes (17): abortSpeculation(), acceptSpeculation(), copyOverlayToMain(), countToolsInMessages(), createSpeculationFeedbackMessage(), generatePipelinedSuggestion(), getBoundaryDetail(), getBoundaryTool() (+9 more)

### Community 91 - "Log Update"
Cohesion: 0.19
Nodes (11): fullResetSequence_CAUSES_FLICKER(), LogUpdate, moveCursorTo(), needsWidthCompensation(), readLine(), renderFrame(), renderFrameSlice(), transitionHyperlink() (+3 more)

### Community 92 - "Ssetransport"
Cohesion: 0.16
Nodes (3): convertSSEUrlToPostUrl(), parseSSEFrames(), SSETransport

### Community 93 - "Imageresizer"
Cohesion: 0.22
Nodes (16): applyFormatOptimizations(), classifyImageError(), compressImageBlock(), compressImageBuffer(), compressImageBufferWithTokenLimit(), createCompressedImageResult(), createUltraCompressedJPEG(), detectImageFormatFromBase64() (+8 more)

### Community 94 - "Teleport"
Cohesion: 0.17
Nodes (15): checkoutBranch(), checkOutTeleportedSessionBranch(), createTeleportResumeSystemMessage(), createTeleportResumeUserMessage(), ensureUpstreamIsSet(), fetchFromOrigin(), generateTitleAndBranch(), getCurrentBranch() (+7 more)

### Community 95 - "Output"
Cohesion: 0.15
Nodes (8): flushBuffer(), intersectClip(), maxDefined(), minDefined(), Output, styledCharsWithGraphemeClustering(), stylesEqual(), writeLineToScreen()

### Community 96 - "Common"
Cohesion: 0.16
Nodes (7): detectAvailableBrowser(), getAllSocketPaths(), getSecureSocketPath(), getSocketDir(), getSocketName(), getUsername(), openInChrome()

### Community 97 - "Cleanup"
Cohesion: 0.28
Nodes (15): addCleanupResults(), cleanupNpmCacheForAnthropicPackages(), cleanupOldDebugLogs(), cleanupOldFileHistoryBackups(), cleanupOldFilesInDirectory(), cleanupOldMessageFiles(), cleanupOldMessageFilesInBackground(), cleanupOldPlanFiles() (+7 more)

### Community 98 - "Stringutils"
Cohesion: 0.12
Nodes (1): EndTruncatingAccumulator

### Community 99 - "Formatters"
Cohesion: 0.24
Nodes (17): extractMarkupText(), formatCallHierarchyItem(), formatDocumentSymbolNode(), formatDocumentSymbolResult(), formatFindReferencesResult(), formatGoToDefinitionResult(), formatHoverResult(), formatIncomingCallsResult() (+9 more)

### Community 100 - "Dom"
Cohesion: 0.2
Nodes (12): appendChildNode(), collectRemovedRects(), createTextNode(), insertBeforeNode(), markDirty(), removeChildNode(), setAttribute(), setStyle() (+4 more)

### Community 101 - "Focus"
Cohesion: 0.17
Nodes (6): collectTabbable(), FocusManager, getFocusManager(), getRootNode(), isInTree(), walkTree()

### Community 102 - "Analyzecontext"
Cohesion: 0.26
Nodes (15): analyzeContextUsage(), approximateMessageTokens(), countBuiltInToolTokens(), countCustomAgentTokens(), countMcpToolTokens(), countMemoryFileTokens(), countSkillTokens(), countSlashCommandTokens() (+7 more)

### Community 103 - "Mcpbhandler"
Cohesion: 0.26
Nodes (15): checkMcpbChanged(), downloadMcpb(), extractMcpbContents(), generateContentHash(), generateMcpConfig(), getMcpbCacheDir(), getMetadataPath(), isUrl() (+7 more)

### Community 104 - "Itermbackend"
Cohesion: 0.16
Nodes (5): acquirePaneCreationLock(), getLeaderSessionId(), ITermBackend, parseSplitOutput(), runIt2()

### Community 105 - "Bridge"
Cohesion: 0.12
Nodes (0): 

### Community 106 - "Diagnostictracking"
Cohesion: 0.17
Nodes (2): DiagnosticsTrackingError, DiagnosticTrackingService

### Community 107 - "Pluginoperations"
Cohesion: 0.21
Nodes (14): assertInstallableScope(), disableAllPluginsOp(), disablePluginOp(), enablePluginOp(), findPluginByIdentifier(), findPluginInSettings(), getPluginInstallationFromV2(), getProjectPathForScope() (+6 more)

### Community 108 - "Agentsdktypes"
Cohesion: 0.12
Nodes (1): AbortError

### Community 109 - "Sessionmemoryutils"
Cohesion: 0.12
Nodes (0): 

### Community 110 - "Filesapi"
Cohesion: 0.29
Nodes (14): buildDownloadPath(), downloadAndSaveFile(), downloadFile(), downloadSessionFiles(), getDefaultApiBaseUrl(), listFilesCreatedAfter(), logDebug(), logDebugError() (+6 more)

### Community 111 - "Microcompact"
Cohesion: 0.23
Nodes (11): cachedMicrocompactPath(), calculateToolResultTokens(), collectCompactableToolIds(), ensureCachedMCState(), estimateMessageTokens(), evaluateTimeBasedTrigger(), getCachedMCModule(), isMainThreadSource() (+3 more)

### Community 112 - "Terminal Event"
Cohesion: 0.12
Nodes (1): TerminalEvent

### Community 113 - "Osc"
Cohesion: 0.2
Nodes (11): copyNative(), link(), osc(), osc8Id(), parseOSC(), parseOscColor(), parseTabStatus(), setClipboard() (+3 more)

### Community 114 - "Loaduserbindings"
Cohesion: 0.25
Nodes (11): getDefaultParsedBindings(), getKeybindingsPath(), handleChange(), handleDelete(), initializeKeybindingWatcher(), isKeybindingBlockArray(), isKeybindingCustomizationEnabled(), loadKeybindings() (+3 more)

### Community 115 - "Chromenativehost"
Cohesion: 0.25
Nodes (5): ChromeMessageReader, ChromeNativeHost, log(), runChromeNativeHost(), sendChromeMessage()

### Community 116 - "Terminallauncher"
Cohesion: 0.27
Nodes (14): appleScriptQuote(), buildShellCommand(), cmdQuote(), detectLinuxTerminal(), detectMacosTerminal(), detectTerminal(), detectWindowsTerminal(), launchInTerminal() (+6 more)

### Community 117 - "Log"
Cohesion: 0.2
Nodes (8): addToInMemoryErrorLog(), attachErrorLogSink(), getErrorLogByIndex(), loadErrorLogs(), loadLogList(), logError(), logMCPDebug(), logMCPError()

### Community 118 - "Markdown"
Cohesion: 0.2
Nodes (10): applyMarkdown(), cachedLexer(), configureMarked(), formatToken(), getListNumber(), hasMarkdownSyntax(), linkifyIssueReferences(), MarkdownBody() (+2 more)

### Community 119 - "Elicitationvalidation"
Cohesion: 0.23
Nodes (13): getEnumLabel(), getEnumLabels(), getEnumValues(), getFormatHint(), getMultiSelectLabel(), getMultiSelectLabels(), getMultiSelectValues(), getZodSchema() (+5 more)

### Community 120 - "Commandsuggestions"
Cohesion: 0.24
Nodes (10): applyCommandSuggestion(), createCommandSuggestionItem(), formatCommand(), generateCommandSuggestions(), getBestCommandMatch(), getCommandFuse(), getCommandId(), hasCommandArgs() (+2 more)

### Community 121 - "Teammate"
Cohesion: 0.14
Nodes (2): getAgentId(), isTeamLead()

### Community 122 - "Tmuxsocket"
Cohesion: 0.21
Nodes (8): checkTmuxAvailable(), doInitialize(), ensureSocketInitialized(), execTmux(), getClaudeSocketName(), isSocketInitialized(), killTmuxServer(), setClaudeSocketInfo()

### Community 123 - "Scrollkeybindinghandler"
Cohesion: 0.17
Nodes (7): applyModalPagerAction(), initAndLogWheelAccel(), initWheelAccel(), jumpBy(), readScrollSpeedBase(), ScrollKeybindingHandler(), useDragToScroll()

### Community 124 - "Filereadtool"
Cohesion: 0.17
Nodes (6): callInner(), createImageResponse(), detectSessionFileType(), MaxFileReadTokenExceededError, readImageWithTokenBudget(), validateContentTokens()

### Community 125 - "Metadata"
Cohesion: 0.2
Nodes (11): buildProcessMetrics(), extractMcpToolDetails(), extractToolInputForTelemetry(), getAgentIdentification(), getEventMetadata(), getFileExtensionForAnalytics(), getFileExtensionsFromBashCommand(), isAnalyticsToolDetailsLoggingEnabled() (+3 more)

### Community 126 - "Claudeailimits"
Cohesion: 0.28
Nodes (12): cacheExtraUsageDisabledReason(), checkQuotaStatus(), computeNewLimitsFromHeaders(), computeTimeProgress(), emitStatusChange(), extractQuotaStatusFromError(), extractQuotaStatusFromHeaders(), extractRawUtilization() (+4 more)

### Community 127 - "User"
Cohesion: 0.17
Nodes (3): getEmailAsync(), initUser(), UserRepository

### Community 128 - "Serialbatcheventuploader"
Cohesion: 0.19
Nodes (2): RetryableError, SerialBatchEventUploader

### Community 129 - "Loadagentsdir"
Cohesion: 0.15
Nodes (2): parseAgentFromMarkdown(), parseHooksFromFrontmatter()

### Community 130 - "Spawnmultiagent"
Cohesion: 0.35
Nodes (13): buildInheritedCliFlags(), ensureSession(), generateUniqueTeammateName(), getDefaultTeammateModel(), getTeammateCommand(), handleSpawn(), handleSpawnInProcess(), handleSpawnSeparateWindow() (+5 more)

### Community 131 - "Tokenestimation"
Cohesion: 0.25
Nodes (12): bytesPerTokenForFileType(), countMessagesTokensWithAPI(), countTokensViaHaikuFallback(), countTokensWithAPI(), hasThinkingBlocks(), roughTokenCountEstimation(), roughTokenCountEstimationForBlock(), roughTokenCountEstimationForContent() (+4 more)

### Community 132 - "Usetypeahead"
Cohesion: 0.14
Nodes (0): 

### Community 133 - "Session Store"
Cohesion: 0.2
Nodes (1): SessionStore

### Community 134 - "Bridgemessaging"
Cohesion: 0.21
Nodes (5): BoundedUUIDSet, handleIngressMessage(), isSDKControlRequest(), isSDKControlResponse(), isSDKMessage()

### Community 135 - "Validate"
Cohesion: 0.24
Nodes (11): checkDuplicates(), checkReservedShortcuts(), formatWarning(), formatWarnings(), getUserBindingsForValidation(), isKeybindingBlockArray(), isValidContext(), validateBindings() (+3 more)

### Community 136 - "Ansitopng"
Cohesion: 0.24
Nodes (8): ansiToPng(), blitGlyph(), blitShade(), chunk(), crc32(), encodePng(), fillBackground(), roundCorners()

### Community 137 - "Betas"
Cohesion: 0.17
Nodes (2): filterAllowedSdkBetas(), partitionBetasByAllowlist()

### Community 138 - "Debug"
Cohesion: 0.19
Nodes (4): getDebugWriter(), logAntError(), logForDebugging(), shouldLogDebugMessage()

### Community 139 - "Envutils"
Cohesion: 0.21
Nodes (6): getDefaultVertexRegion(), getVertexRegionForModel(), isBareMode(), isEnvTruthy(), isRunningOnHomespace(), shouldMaintainProjectWorkingDir()

### Community 140 - "Errorlogsink"
Cohesion: 0.27
Nodes (9): appendToLog(), createJsonlWriter(), extractServerMessage(), getErrorsPath(), getLogWriter(), getMCPLogsPath(), logErrorImpl(), logMCPDebugImpl() (+1 more)

### Community 141 - "Plans"
Cohesion: 0.28
Nodes (10): copyPlanForFork(), copyPlanForResume(), findFileSnapshotEntry(), getPlan(), getPlanFilePath(), getPlanSlug(), getSlugFromLog(), persistFileSnapshotIfRemote() (+2 more)

### Community 142 - "Changedetector"
Cohesion: 0.26
Nodes (10): fanOut(), getSourceForPath(), getWatchTargets(), handleAdd(), handleChange(), handleDelete(), initialize(), notifyChange() (+2 more)

### Community 143 - "Slowoperations"
Cohesion: 0.18
Nodes (3): AntSlowLogger, buildDescription(), callerFrame()

### Community 144 - "Virtualmessagelist"
Cohesion: 0.23
Nodes (9): computeStickyPromptText(), highlight(), jump(), scan(), select(), step(), stickyPromptText(), StickyTracker() (+1 more)

### Community 145 - "Agentfileutils"
Cohesion: 0.33
Nodes (12): deleteAgentFromFile(), ensureAgentDirectoryExists(), formatAgentAsMarkdown(), getActualAgentFilePath(), getActualRelativeAgentFilePath(), getAgentDirectoryPath(), getNewAgentFilePath(), getNewRelativeAgentFilePath() (+4 more)

### Community 146 - "Conversation"
Cohesion: 0.19
Nodes (1): ConversationRepository

### Community 147 - "Sessionmemorycompact"
Cohesion: 0.28
Nodes (11): adjustIndexToPreserveAPIInvariants(), calculateMessagesToKeepIndex(), createCompactionResultFromSessionMemory(), getSessionMemoryCompactConfig(), getToolResultIds(), hasTextBlocks(), hasToolUseWithIds(), initSessionMemoryCompactConfig() (+3 more)

### Community 148 - "Usetasksv2"
Cohesion: 0.19
Nodes (4): getStore(), TasksV2Store, useTasksV2(), useTasksV2WithCollapseEffect()

### Community 149 - "Parse Keypress"
Cohesion: 0.29
Nodes (12): createNavKey(), createPasteKey(), decodeModifier(), inputToString(), isCtrlKey(), isShiftKey(), keycodeToName(), parseKeypress() (+4 more)

### Community 150 - "Terminal Querier"
Cohesion: 0.15
Nodes (1): TerminalQuerier

### Community 151 - "Connection"
Cohesion: 0.21
Nodes (5): connect(), createPostgresConnection(), createSqliteConnection(), getDbType(), getDefaultSqlitePath()

### Community 152 - "Message"
Cohesion: 0.17
Nodes (1): MessageRepository

### Community 153 - "Localshelltask"
Cohesion: 0.21
Nodes (5): backgroundAll(), backgroundExistingForegroundTask(), backgroundTask(), spawnShellTask(), startStallWatchdog()

### Community 154 - "Teammempaths"
Cohesion: 0.29
Nodes (10): getTeamMemPath(), isRealPathWithinTeamDir(), isTeamMemFile(), isTeamMemoryEnabled(), isTeamMemPath(), PathTraversalError, realpathDeepestExisting(), sanitizePathKey() (+2 more)

### Community 155 - "Executor"
Cohesion: 0.23
Nodes (7): animatedMove(), moveAndSettle(), readClipboardViaPbpaste(), releasePressed(), typeViaClipboard(), withModifiers(), writeClipboardViaPbcopy()

### Community 156 - "Format"
Cohesion: 0.26
Nodes (9): formatFileSize(), formatLogMetadata(), formatNumber(), formatRelativeTime(), formatRelativeTimeAgo(), formatResetText(), formatResetTime(), formatTokens() (+1 more)

### Community 157 - "Logov2Utils"
Cohesion: 0.17
Nodes (0): 

### Community 158 - "Mcpvalidation"
Cohesion: 0.35
Nodes (11): getContentSizeEstimate(), getMaxMcpOutputChars(), getMaxMcpOutputTokens(), getTruncationMessage(), isImageBlock(), isTextBlock(), mcpContentNeedsTruncation(), truncateContentBlocks() (+3 more)

### Community 159 - "Memoryfiledetection"
Cohesion: 0.33
Nodes (11): detectSessionFileType(), detectSessionPatternType(), isAgentMemFile(), isAutoManagedMemoryFile(), isAutoManagedMemoryPattern(), isAutoMemFile(), isMemoryDirectory(), isShellCommandTargetingMemory() (+3 more)

### Community 160 - "Pidlock"
Cohesion: 0.35
Nodes (10): acquireProcessLifetimeLock(), cleanupStaleLocks(), getAllLockInfo(), isClaudeProcess(), isLockActive(), isProcessRunning(), readLockContent(), tryAcquireLock() (+2 more)

### Community 161 - "Notebook"
Cohesion: 0.24
Nodes (8): cellContentToToolResult(), extractImage(), getToolResultFromCell(), isLargeOutputs(), processCell(), processOutput(), processOutputText(), readNotebook()

### Community 162 - "Validation"
Cohesion: 0.18
Nodes (2): formatZodError(), validateSettingsFileContent()

### Community 163 - "Statscache"
Cohesion: 0.27
Nodes (8): getEmptyCache(), getStatsCachePath(), getTodayDateString(), getYesterdayDateString(), loadStatsCache(), migrateStatsCache(), saveStatsCache(), toDateString()

### Community 164 - "Slackchannelsuggestions"
Cohesion: 0.27
Nodes (8): fetchChannels(), findReusableCacheEntry(), findSlackClient(), getSlackChannelSuggestions(), hasSlackMcpServer(), mcpQueryFor(), parseChannels(), unwrapResults()

### Community 165 - "Inprocessrunner"
Cohesion: 0.32
Nodes (10): findAvailableTask(), formatAsTeammateMessage(), formatTaskAsPrompt(), runInProcessTeammate(), sendIdleNotification(), sendMessageToLeader(), startInProcessTeammate(), tryClaimNextTask() (+2 more)

### Community 166 - "Terminalpanel"
Cohesion: 0.32
Nodes (2): getTerminalPanelSocket(), TerminalPanel

### Community 167 - "Agentsmenu"
Cohesion: 0.17
Nodes (0): 

### Community 168 - "Promptsuggestion"
Cohesion: 0.32
Nodes (8): executePromptSuggestion(), generateSuggestion(), getParentCacheSuppressReason(), getPromptVariant(), getSuggestionSuppressReason(), logSuggestionSuppressed(), shouldFilterSuggestion(), tryGenerateSuggestion()

### Community 169 - "Extractmemories"
Cohesion: 0.23
Nodes (7): countModelVisibleMessagesSince(), drainer(), drainPendingExtraction(), extractWrittenPaths(), getWrittenFilePath(), hasMemoryWritesSince(), isModelVisibleMessage()

### Community 170 - "Vcr"
Cohesion: 0.26
Nodes (8): dehydrateValue(), mapAssistantMessage(), mapMessage(), mapMessages(), shouldUseVCR(), withFixture(), withTokenCountVCR(), withVCR()

### Community 171 - "Useswarmpermissionpoller"
Cohesion: 0.2
Nodes (3): parsePermissionUpdates(), processMailboxPermissionResponse(), processResponse()

### Community 172 - "Styles"
Cohesion: 0.32
Nodes (11): applyBorderStyles(), applyDimensionStyles(), applyDisplayStyles(), applyFlexStyles(), applyGapStyles(), applyMarginStyles(), applyOverflowStyles(), applyPaddingStyles() (+3 more)

### Community 173 - "Storage"
Cohesion: 0.3
Nodes (1): AnalyticsStorage

### Community 174 - "Conversation Service"
Cohesion: 0.2
Nodes (4): deleteLastAssistantMessage(), exportConversation(), getConversation(), getMessages()

### Community 175 - "Bridgeenabled"
Cohesion: 0.24
Nodes (6): getBridgeDisabledReason(), getOauthAccountInfo(), hasProfileScope(), isBridgeEnabled(), isBridgeEnabledBlocking(), isClaudeAISubscriber()

### Community 176 - "Hybridtransport"
Cohesion: 0.29
Nodes (2): convertWsUrlToPostUrl(), HybridTransport

### Community 177 - "Paths"
Cohesion: 0.21
Nodes (4): getAutoMemPathOverride(), getAutoMemPathSetting(), hasAutoMemPathOverride(), validateMemoryPath()

### Community 178 - "Activitymanager"
Cohesion: 0.24
Nodes (1): ActivityManager

### Community 179 - "Advisor"
Cohesion: 0.31
Nodes (5): canUserConfigureAdvisor(), getAdvisorConfig(), getExperimentAdvisorModels(), getInitialAdvisorSetting(), isAdvisorEnabled()

### Community 180 - "Bashpipecommand"
Cohesion: 0.38
Nodes (10): buildCommandParts(), containsControlStructure(), findFirstPipeOperator(), isCommandSeparator(), isEnvironmentVariableAssignment(), isOperator(), joinContinuationLines(), quoteWithEvalStdinRedirect() (+2 more)

### Community 181 - "Treesitteranalysis"
Cohesion: 0.36
Nodes (10): analyzeCommand(), buildPositionSet(), collectQuoteSpans(), dropContainedSpans(), extractCompoundStructure(), extractDangerousPatterns(), extractQuoteContext(), hasActualOperatorNodes() (+2 more)

### Community 182 - "Computeruselock"
Cohesion: 0.42
Nodes (9): checkComputerUseLock(), getLockPath(), isComputerUseLock(), isProcessRunning(), readLock(), registerLockCleanup(), releaseComputerUseLock(), tryAcquireComputerUseLock() (+1 more)

### Community 183 - "Context"
Cohesion: 0.36
Nodes (9): call(), getContextWindowForModel(), getMaxThinkingTokensForModel(), getModelMaxOutputTokens(), getSonnet1mExpTreatmentEnabled(), has1mContext(), is1mContextDisabled(), modelSupports1M() (+1 more)

### Community 184 - "Registerprotocol"
Cohesion: 0.42
Nodes (10): ensureDeepLinkProtocolRegistered(), isProtocolHandlerCurrent(), linuxDesktopPath(), linuxExecLine(), registerLinux(), registerMacos(), registerProtocolHandler(), registerWindows() (+2 more)

### Community 185 - "Fullscreen"
Cohesion: 0.29
Nodes (6): isFullscreenActive(), isFullscreenEnvEnabled(), isTmuxControlMode(), isTmuxControlModeEnvHeuristic(), maybeGetTmuxMouseHint(), probeTmuxControlModeSync()

### Community 186 - "Gracefulshutdown"
Cohesion: 0.25
Nodes (6): cleanupTerminalModes(), CleanupTimeoutError, forceExit(), gracefulShutdown(), gracefulShutdownSync(), printResumeHint()

### Community 187 - "Filechangedwatcher"
Cohesion: 0.31
Nodes (8): dispose(), initializeFileChangedWatcher(), onCwdChangedForHooks(), resetFileChangedWatcherForTesting(), resolveWatchPaths(), restartWatching(), startWatching(), updateWatchPaths()

### Community 188 - "Sessionhooks"
Cohesion: 0.24
Nodes (5): addFunctionHook(), addHookToSession(), addSessionHook(), convertToHookMatchers(), getSessionHooks()

### Community 189 - "Imagestore"
Cohesion: 0.33
Nodes (7): cacheImagePath(), ensureImageStoreDir(), evictOldestIfAtCap(), getImagePath(), getImageStoreDir(), storeImage(), storeImages()

### Community 190 - "Download"
Cohesion: 0.27
Nodes (8): downloadAndVerifyBinary(), downloadVersion(), downloadVersionFromArtifactory(), downloadVersionFromBinaryRepo(), getLatestVersion(), getLatestVersionFromArtifactory(), getLatestVersionFromBinaryRepo(), StallTimeoutError

### Community 191 - "Cacheutils"
Cohesion: 0.36
Nodes (10): cleanupOrphanedPluginVersionsInBackground(), clearAllCaches(), clearAllPluginCaches(), getInstalledVersionPaths(), getOrphanedAtPath(), markPluginVersionOrphaned(), processOrphanedPluginVersion(), readSubdirs() (+2 more)

### Community 192 - "Mcppluginintegration"
Cohesion: 0.31
Nodes (8): addPluginScopeToServers(), buildMcpUserConfig(), getPluginMcpServers(), loadChannelUserConfig(), loadMcpServersFromFile(), loadMcpServersFromMcpb(), loadPluginMcpServers(), resolvePluginMcpEnvironment()

### Community 193 - "Processslashcommand"
Cohesion: 0.35
Nodes (10): executeForkedSlashCommand(), formatCommandInput(), formatCommandLoadingMetadata(), formatSkillLoadingMetadata(), formatSlashCommandLoadingMetadata(), getMessagesForPromptSlashCommand(), getMessagesForSlashCommand(), looksLikeCommand() (+2 more)

### Community 194 - "Ripgrep"
Cohesion: 0.29
Nodes (7): codesignRipgrepIfNecessary(), ripGrep(), ripgrepCommand(), ripGrepFileCount(), ripGrepRaw(), ripGrepStream(), RipgrepTimeoutError

### Community 195 - "Settingscache"
Cohesion: 0.18
Nodes (0): 

### Community 196 - "Prefix"
Cohesion: 0.29
Nodes (6): getCommandPrefixStatic(), getCompoundCommandPrefixesStatic(), handleWrapper(), isKnownSubcommand(), longestCommonPrefix(), toArray()

### Community 197 - "Panebackendexecutor"
Cohesion: 0.18
Nodes (1): PaneBackendExecutor

### Community 198 - "Tokens"
Cohesion: 0.36
Nodes (9): doesMostRecentAssistantMessageExceed200k(), finalContextTokensFromLastResponse(), getAssistantMessageId(), getCurrentUsage(), getTokenCountFromUsage(), getTokenUsage(), messageTokenCountFromLastAPIResponse(), tokenCountFromLastAPIResponse() (+1 more)

### Community 199 - "Ccrsession"
Cohesion: 0.27
Nodes (6): contentToText(), ExitPlanModeScanner, extractApprovedPlan(), extractTeleportPlan(), pollForApprovedExitPlanMode(), UltraplanPollError

### Community 200 - "Feedback"
Cohesion: 0.25
Nodes (6): createFallbackTitle(), createGitHubIssueUrl(), generateTitle(), redactSensitiveInfo(), sanitizeAndLogError(), submitFeedback()

### Community 201 - "Overagecreditupsell"
Cohesion: 0.29
Nodes (8): createOverageCreditFeed(), getFeedTitle(), getUsageText(), isEligibleForOverageCreditGrant(), maybeRefreshOverageCreditCache(), OverageCreditUpsell(), shouldShowOverageCreditUpsell(), _temp()

### Community 202 - "Grove"
Cohesion: 0.24
Nodes (5): calculateShouldShowGrove(), checkGroveForNonInteractive(), fetchAndStoreGroveConfig(), isQualifiedForGrove(), markGroveNoticeViewed()

### Community 203 - "Askuserquestionpermissionrequest"
Cohesion: 0.18
Nodes (0): 

### Community 204 - "Copy"
Cohesion: 0.33
Nodes (9): call(), collectRecentAssistantTexts(), copyOrWriteToFile(), CopyPicker(), extractCodeBlocks(), fileExtension(), _temp(), truncateLine() (+1 more)

### Community 205 - "Ultraplan"
Cohesion: 0.35
Nodes (9): buildAlreadyActiveMessage(), buildLaunchMessage(), buildSessionReadyMessage(), buildUltraplanPrompt(), call(), getUltraplanModel(), launchDetached(), launchUltraplan() (+1 more)

### Community 206 - "Agentmemorysnapshot"
Cohesion: 0.38
Nodes (10): checkAgentMemorySnapshot(), copySnapshotToLocal(), getSnapshotDirForAgent(), getSnapshotJsonPath(), getSyncedJsonPath(), initializeFromSnapshot(), markSnapshotSynced(), readJsonFile() (+2 more)

### Community 207 - "Sessionmemory"
Cohesion: 0.25
Nodes (6): countToolCallsSince(), createMemoryFileCanUseTool(), manuallyExtractSessionMemory(), setupSessionMemoryFile(), shouldExtractMemory(), updateLastSummarizedMessageIdIfSafe()

### Community 208 - "Referral"
Cohesion: 0.25
Nodes (5): checkCachedPassesEligibility(), fetchAndStorePassesEligibility(), getCachedOrFetchPassesEligibility(), prefetchPassesEligibility(), shouldCheckForPasses()

### Community 209 - "Sdkcontroltransport"
Cohesion: 0.18
Nodes (2): SdkControlClientTransport, SdkControlServerTransport

### Community 210 - "Xaa"
Cohesion: 0.35
Nodes (9): discoverAuthorizationServer(), discoverProtectedResource(), exchangeJwtAuthGrant(), makeXaaFetch(), normalizeUrl(), performCrossAppAccess(), redactTokens(), requestJwtAuthorizationGrant() (+1 more)

### Community 211 - "Toolexecution"
Cohesion: 0.33
Nodes (10): buildSchemaNotSentHint(), checkPermissionsAndCallTool(), classifyToolError(), decisionReasonToOTelSource(), findMcpServerConnection(), getMcpServerBaseUrlFromToolName(), getMcpServerType(), getNextImagePasteId() (+2 more)

### Community 212 - "Health"
Cohesion: 0.24
Nodes (4): registerAnthropicCheck(), registerCheck(), registerDatabaseCheck(), registerRedisCheck()

### Community 213 - "Shared Link"
Cohesion: 0.2
Nodes (1): SharedLinkRepository

### Community 214 - "Directconnectmanager"
Cohesion: 0.18
Nodes (1): DirectConnectSessionManager

### Community 215 - "Cost Tracker"
Cohesion: 0.25
Nodes (3): computeCost(), CostTracker, getPricing()

### Community 216 - "Bridgestatusutil"
Cohesion: 0.18
Nodes (0): 

### Community 217 - "Companion"
Cohesion: 0.4
Nodes (10): companionUserId(), getCompanion(), hashString(), mulberry32(), pick(), roll(), rollFrom(), rollRarity() (+2 more)

### Community 218 - "Queryguard"
Cohesion: 0.31
Nodes (1): QueryGuard

### Community 219 - "Shellcompletion"
Cohesion: 0.4
Nodes (9): findLastStringToken(), getBashCompletionCommand(), getCompletionsForShell(), getCompletionTypeFromPrefix(), getShellCompletions(), getZshCompletionCommand(), isCommandOperator(), isNewCommandContext() (+1 more)

### Community 220 - "Classifierapprovals"
Cohesion: 0.2
Nodes (0): 

### Community 221 - "Claudecodehints"
Cohesion: 0.22
Nodes (2): extractClaudeCodeHints(), firstCommandToken()

### Community 222 - "Concurrentsessions"
Cohesion: 0.38
Nodes (9): countConcurrentSessions(), envSessionKind(), getSessionsDir(), isBgSession(), registerSession(), updatePidFile(), updateSessionActivity(), updateSessionBridgeId() (+1 more)

### Community 223 - "Fsoperations"
Cohesion: 0.29
Nodes (5): getFsImplementation(), getPathsForPermissionCheck(), isDuplicatePath(), resolveDeepestExistingAncestorSync(), safeResolvePath()

### Community 224 - "Hookevents"
Cohesion: 0.36
Nodes (6): emit(), emitHookProgress(), emitHookResponse(), emitHookStarted(), shouldEmit(), startHookProgressInterval()

### Community 225 - "Mailbox"
Cohesion: 0.24
Nodes (1): Mailbox

### Community 226 - "Markdownconfigloader"
Cohesion: 0.29
Nodes (7): findMarkdownFilesNative(), getProjectDirsUpToHome(), loadMarkdownFiles(), parseAgentToolsFromFrontmatter(), parseSlashCommandToolsFromFrontmatter(), parseToolListString(), resolveStopBoundary()

### Community 227 - "Modelcost"
Cohesion: 0.36
Nodes (9): calculateCostFromTokens(), calculateUSDCost(), formatModelPricing(), formatPrice(), getModelCosts(), getModelPricingString(), getOpus46CostTier(), tokensToUSDCost() (+1 more)

### Community 228 - "Permissionmode"
Cohesion: 0.31
Nodes (6): getModeColor(), getModeConfig(), permissionModeShortTitle(), permissionModeSymbol(), permissionModeTitle(), toExternalPermissionMode()

### Community 229 - "Permissionsloader"
Cohesion: 0.36
Nodes (8): addPermissionRulesToSettings(), getEmptyPermissionSettingsJson(), getPermissionRulesForSource(), getSettingsForSourceLenient_FOR_EDITING_ONLY_NOT_FOR_READING(), loadAllPermissionRulesFromDisk(), settingsJsonToRules(), shouldAllowManagedPermissionRulesOnly(), shouldShowAlwaysAllowOptions()

### Community 230 - "Pluginflagging"
Cohesion: 0.44
Nodes (8): addFlaggedPlugin(), getFlaggedPluginsPath(), loadFlaggedPlugins(), markFlaggedPluginsSeen(), parsePluginsData(), readFromDisk(), removeFlaggedPlugin(), writeToDisk()

### Community 231 - "Sessionactivity"
Cohesion: 0.33
Nodes (7): clearIdleTimer(), registerSessionActivityCallback(), startHeartbeatTimer(), startIdleTimer(), startSessionActivity(), stopSessionActivity(), unregisterSessionActivityCallback()

### Community 232 - "Sessionrestore"
Cohesion: 0.33
Nodes (8): computeRestoredAttributionState(), computeStandaloneAgentContext(), extractTodosFromTranscript(), processResumedConversation(), refreshAgentDefinitionsForModeSwitch(), restoreAgentFromSession(), restoreSessionStateFromLog(), restoreWorktreeForResume()

### Community 233 - "Inprocessbackend"
Cohesion: 0.2
Nodes (1): InProcessBackend

### Community 234 - "Framework"
Cohesion: 0.29
Nodes (5): applyTaskOffsetsAndEvictions(), enqueueTaskNotification(), generateTaskAttachments(), getStatusText(), pollTasks()

### Community 235 - "Thinkback"
Cohesion: 0.24
Nodes (4): getMarketplaceName(), getPluginId(), playAnimation(), ThinkbackMenu()

### Community 236 - "Agenttoolutils"
Cohesion: 0.36
Nodes (9): classifyHandoffIfNeeded(), countToolUses(), emitTaskProgress(), extractPartialResult(), filterToolsForAgent(), finalizeAgentTool(), getLastToolUseName(), resolveAgentTools() (+1 more)

### Community 237 - "Bashtool"
Cohesion: 0.24
Nodes (3): getCommandTypeForLogging(), spawnBackgroundTask(), startBackgrounding()

### Community 238 - "Sedvalidation"
Cohesion: 0.4
Nodes (9): checkSedConstraints(), containsDangerousOperations(), extractSedExpressions(), hasFileArgs(), isLinePrintingCommand(), isPrintCommand(), isSubstitutionCommand(), sedCommandIsAllowedByAllowlist() (+1 more)

### Community 239 - "Powershelltool"
Cohesion: 0.24
Nodes (3): getCommandTypeForLogging(), spawnBackgroundTask(), startBackgrounding()

### Community 240 - "Powershellpermissions"
Cohesion: 0.47
Nodes (8): extractCommandName(), filterRulesByContentsMatchingInput(), getSubCommandsForPermissionCheck(), matchingRulesForInput(), powershellToolCheckExactMatchPermission(), powershellToolCheckPermission(), powershellToolHasPermission(), suggestionForExactCommand()

### Community 241 - "Gitoperationtracking"
Cohesion: 0.38
Nodes (9): detectGitOperation(), findPrInStdout(), gitCmdRe(), parseGitCommitId(), parseGitPushBranch(), parsePrNumberFromText(), parsePrUrl(), parseRefFromCommand() (+1 more)

### Community 242 - "Ratelimitmessages"
Cohesion: 0.33
Nodes (7): formatLimitReachedText(), getEarlyWarningText(), getLimitReachedText(), getRateLimitErrorMessage(), getRateLimitMessage(), getRateLimitWarning(), getWarningUpsellText()

### Community 243 - "Watcher"
Cohesion: 0.29
Nodes (7): executePush(), isPermanentFailure(), notifyTeamMemoryWrite(), schedulePush(), startFileWatcher(), _startFileWatcherForTesting(), startTeamMemoryWatcher()

### Community 244 - "Dispatcher"
Cohesion: 0.33
Nodes (5): collectListeners(), Dispatcher, getEventPriority(), getHandler(), processDispatchQueue()

### Community 245 - "Bundledskills"
Cohesion: 0.29
Nodes (5): extractBundledSkillFiles(), getBundledSkillExtractDir(), registerBundledSkill(), resolveSkillFilePath(), writeSkillFiles()

### Community 246 - "Circularbuffer"
Cohesion: 0.25
Nodes (1): CircularBuffer

### Community 247 - "Attribution"
Cohesion: 0.39
Nodes (7): countMemoryFileAccessFromEntries(), countUserPromptsFromEntries(), countUserPromptsInMessages(), getEnhancedPRAttribution(), getPRAttributionData(), getTranscriptStats(), isTerminalOutput()

### Community 248 - "Awsauthstatusmanager"
Cohesion: 0.33
Nodes (1): AwsAuthStatusManager

### Community 249 - "Preconditions"
Cohesion: 0.28
Nodes (3): checkGithubAppInstalled(), checkGithubTokenSynced(), checkRepoForRemoteAccess()

### Community 250 - "Shellsnapshot"
Cohesion: 0.42
Nodes (7): createArgv0ShellFunction(), createFindGrepShellIntegration(), createRipgrepShellIntegration(), getClaudeCodeSnapshotContent(), getConfigFile(), getSnapshotScript(), getUserSnapshotContent()

### Community 251 - "Doctordiagnostic"
Cohesion: 0.42
Nodes (8): detectConfigurationIssues(), detectLinuxGlobPatternWarnings(), detectMultipleInstallations(), getCurrentInstallationType(), getDoctorDiagnostic(), getInstallationPath(), getInvokedBinary(), getNormalizedPaths()

### Community 252 - "Frontmatterparser"
Cohesion: 0.25
Nodes (2): parseFrontmatter(), quoteProblematicValues()

### Community 253 - "Json"
Cohesion: 0.33
Nodes (5): parseJSONL(), parseJSONLBuffer(), parseJSONLBun(), parseJSONLString(), readJSONLFile()

### Community 254 - "Bashclassifier"
Cohesion: 0.22
Nodes (0): 

### Community 255 - "Permissionruleparser"
Cohesion: 0.36
Nodes (7): escapeRuleContent(), findFirstUnescapedChar(), findLastUnescapedChar(), normalizeLegacyToolName(), permissionRuleValueFromString(), permissionRuleValueToString(), unescapeRuleContent()

### Community 256 - "Plugindirectories"
Cohesion: 0.39
Nodes (7): deletePluginDataDir(), getPluginDataDir(), getPluginDataDirSize(), getPluginsDirectory(), getPluginsDirectoryName(), pluginDataDirPath(), sanitizePluginId()

### Community 257 - "Pluginoptionsstorage"
Cohesion: 0.31
Nodes (5): clearPluginOptionsCache(), deletePluginOptions(), getPluginStorageId(), getUnconfiguredOptions(), savePluginOptions()

### Community 258 - "Readeditcontext"
Cohesion: 0.44
Nodes (8): countNewlines(), indexOfWithin(), normalizeCRLF(), openForScan(), readCapped(), readEditContext(), scanForContext(), sliceContext()

### Community 259 - "Readfileinrange"
Cohesion: 0.28
Nodes (4): FileTooLargeError, readFileInRange(), readFileInRangeFast(), readFileInRangeStreaming()

### Community 260 - "Directorycompletion"
Cohesion: 0.33
Nodes (5): getDirectoryCompletions(), getPathCompletions(), parsePartialPath(), scanDirectory(), scanDirectoryForPaths()

### Community 261 - "It2Setup"
Cohesion: 0.25
Nodes (2): isIt2CliAvailable(), verifyIt2Setup()

### Community 262 - "Teammatelayoutmanager"
Cohesion: 0.31
Nodes (4): createTeammatePaneInSwarmView(), enablePaneBorderStatus(), getBackend(), sendCommandToPane()

### Community 263 - "Fast"
Cohesion: 0.31
Nodes (4): applyFastMode(), call(), FastModePicker(), handleFastModeShortcut()

### Community 264 - "X402"
Cohesion: 0.42
Nodes (8): call(), handleNetwork(), handleRemove(), handleSetLimit(), handleSetSession(), handleSetup(), handleStatus(), showHelp()

### Community 265 - "Sendmessagetool"
Cohesion: 0.25
Nodes (2): findTeammateColor(), handleMessage()

### Community 266 - "Logging"
Cohesion: 0.47
Nodes (8): detectGateway(), getAnthropicEnvMetadata(), getBuildAgeMinutes(), getErrorMessage(), logAPIError(), logAPIQuery(), logAPISuccess(), logAPISuccessAndDuration()

### Community 267 - "Manager"
Cohesion: 0.28
Nodes (4): getLspServerManager(), initializeLspServerManager(), isLspConnected(), reinitializeLspServerManager()

### Community 268 - "Error Handler"
Cohesion: 0.22
Nodes (1): ApiError

### Community 269 - "Sse"
Cohesion: 0.22
Nodes (1): SSEStream

### Community 270 - "Tool Use"
Cohesion: 0.22
Nodes (1): ToolUseRepository

### Community 271 - "Sanitize"
Cohesion: 0.22
Nodes (0): 

### Community 272 - "Bridgeapi"
Cohesion: 0.28
Nodes (4): BridgeFatalError, extractErrorTypeFromData(), handleErrorStatus(), isExpiredErrorType()

### Community 273 - "Flushgate"
Cohesion: 0.22
Nodes (1): FlushGate

### Community 274 - "Scheduleremoteagents"
Cohesion: 0.31
Nodes (6): buildPrompt(), formatConnectorsInfo(), formatSetupNotes(), getConnectedClaudeAIConnectors(), sanitizeConnectorName(), taggedIdToUUID()

### Community 275 - "Workerstateuploader"
Cohesion: 0.36
Nodes (2): coalescePatches(), WorkerStateUploader

### Community 276 - "Memdir"
Cohesion: 0.47
Nodes (8): buildAssistantDailyLogPrompt(), buildMemoryLines(), buildMemoryPrompt(), buildSearchingPastContextSection(), ensureMemoryDirExists(), loadMemoryPrompt(), logMemoryDirCounts(), truncateEntrypointContent()

### Community 277 - "Detectrepository"
Cohesion: 0.39
Nodes (5): detectCurrentRepository(), detectCurrentRepositoryWithHost(), looksLikeRealHostname(), parseGitHubRepository(), parseGitRemote()

### Community 278 - "Earlyinput"
Cohesion: 0.32
Nodes (3): consumeEarlyInput(), processChunk(), stopCapturingEarlyInput()

### Community 279 - "Gitconfigparser"
Cohesion: 0.46
Nodes (7): isKeyChar(), matchesSectionHeader(), parseConfigString(), parseGitConfigValue(), parseKeyValue(), parseValue(), trimTrailingWhitespace()

### Community 280 - "Asynchookregistry"
Cohesion: 0.25
Nodes (0): 

### Community 281 - "Hooksconfigsnapshot"
Cohesion: 0.36
Nodes (4): captureHooksConfigSnapshot(), getHooksConfigFromSnapshot(), getHooksFromAllowedSources(), updateHooksConfigSnapshot()

### Community 282 - "Ssrfguard"
Cohesion: 0.5
Nodes (7): expandIPv6Groups(), extractMappedIPv4(), isBlockedAddress(), isBlockedV4(), isBlockedV6(), ssrfError(), ssrfGuardedLookup()

### Community 283 - "Intl"
Cohesion: 0.32
Nodes (3): firstGrapheme(), getGraphemeSegmenter(), lastGrapheme()

### Community 284 - "Mcpwebsockettransport"
Cohesion: 0.32
Nodes (1): WebSocketTransport

### Community 285 - "Bedrock"
Cohesion: 0.36
Nodes (4): applyBedrockRegionPrefix(), extractModelIdFromArn(), getBedrockRegionPrefix(), isFoundationModel()

### Community 286 - "Modelstrings"
Cohesion: 0.46
Nodes (6): applyModelOverrides(), ensureModelStringsInitialized(), getBedrockModelStrings(), getBuiltinModelStrings(), getModelStrings(), initModelStrings()

### Community 287 - "Automodestate"
Cohesion: 0.25
Nodes (0): 

### Community 288 - "Dependencyresolver"
Cohesion: 0.29
Nodes (2): qualifyDependency(), verifyAndDemote()

### Community 289 - "Lsppluginintegration"
Cohesion: 0.5
Nodes (7): addPluginScopeToLspServers(), extractLspServersFromPlugins(), getPluginLspServers(), loadLspServersFromManifest(), loadPluginLspServers(), resolvePluginLspEnvironment(), validatePathWithinPlugin()

### Community 290 - "Pluginautoupdate"
Cohesion: 0.29
Nodes (2): updatePlugins(), updatePluginsForMarketplaces()

### Community 291 - "Queryprofiler"
Cohesion: 0.43
Nodes (7): endQueryProfile(), getPhaseSummary(), getQueryProfileReport(), getSlowWarning(), logQueryProfileReport(), queryCheckpoint(), startQueryProfile()

### Community 292 - "Sessionstate"
Cohesion: 0.25
Nodes (0): 

### Community 293 - "Specprefix"
Cohesion: 0.64
Nodes (7): buildPrefix(), calculateDepth(), findFirstSubcommand(), flagTakesArg(), isKnownSubcommand(), shouldStopAtArg(), toArray()

### Community 294 - "Detection"
Cohesion: 0.25
Nodes (0): 

### Community 295 - "Systemtheme"
Cohesion: 0.39
Nodes (6): detectFromColorFgBg(), getSystemThemeName(), hexComponent(), parseOscRgb(), resolveThemeSetting(), themeFromOscColor()

### Community 296 - "Thinking"
Cohesion: 0.25
Nodes (0): 

### Community 297 - "Tabs"
Cohesion: 0.25
Nodes (0): 

### Community 298 - "Hooksconfigmenu"
Cohesion: 0.25
Nodes (0): 

### Community 299 - "Assistanttoolusemessage"
Cohesion: 0.32
Nodes (3): AssistantToolUseMessage(), renderToolUseMessage(), renderToolUseProgressMessage()

### Community 300 - "Agentmemory"
Cohesion: 0.43
Nodes (6): getAgentMemoryDir(), getAgentMemoryEntrypoint(), getLocalAgentMemoryDir(), getMemoryScopeDisplay(), loadAgentMemoryPrompt(), sanitizeAgentTypeForPath()

### Community 301 - "Modevalidation"
Cohesion: 0.43
Nodes (6): checkPermissionMode(), isAcceptEditsAllowedCmdlet(), isFilesystemCommand(), isItemTypeParamAbbrev(), isSymlinkCreatingCommand(), validateCommandForMode()

### Community 302 - "Gitsafety"
Cohesion: 0.54
Nodes (7): isDotGitPathPS(), isGitInternalPathPS(), matchesDotGitPrefix(), matchesGitInternalPrefix(), normalizeGitPathArg(), resolveCwdReentry(), resolveEscapingPathToCwdRelative()

### Community 303 - "Toolsearchtool"
Cohesion: 0.32
Nodes (4): compileTermPatterns(), getDeferredToolsCacheKey(), maybeInvalidateCache(), searchToolsWithKeywords()

### Community 304 - "Errorutils"
Cohesion: 0.5
Nodes (7): extractConnectionErrorDetails(), extractNestedErrorMessage(), formatAPIError(), getSSLErrorHint(), hasNestedError(), sanitizeAPIError(), sanitizeMessageHTML()

### Community 305 - "Preventsleep"
Cohesion: 0.46
Nodes (7): forceStopPreventSleep(), killCaffeinate(), spawnCaffeinate(), startPreventSleep(), startRestartInterval(), stopPreventSleep(), stopRestartInterval()

### Community 306 - "Permissionlogging"
Cohesion: 0.5
Nodes (7): baseMetadata(), buildCodeEditToolAttributes(), isCodeEditingTool(), logApprovalEvent(), logPermissionDecision(), logRejectionEvent(), sourceToString()

### Community 307 - "App"
Cohesion: 0.36
Nodes (4): App(), handleMouseEvent(), processKeysInBatch(), resumeHandler()

### Community 308 - "Geometry"
Cohesion: 0.25
Nodes (0): 

### Community 309 - "Debugutils"
Cohesion: 0.29
Nodes (2): debugBody(), redactSecrets()

### Community 310 - "Claude Code Internal Event"
Cohesion: 0.29
Nodes (2): fromJsonTimestamp(), fromTimestamp()

### Community 311 - "Resolver"
Cohesion: 0.43
Nodes (5): buildKeystroke(), chordExactlyMatches(), chordPrefixMatches(), keystrokesEqual(), resolveKeyWithChordState()

### Community 312 - "Agentcontext"
Cohesion: 0.43
Nodes (4): consumeInvokingRequestId(), getAgentContext(), getSubagentLogName(), isSubagentContext()

### Community 313 - "Shellquoting"
Cohesion: 0.48
Nodes (5): containsHeredoc(), containsMultilineString(), hasStdinRedirect(), quoteShellCommand(), shouldAddStdinRedirect()

### Community 314 - "Toolrendering"
Cohesion: 0.29
Nodes (0): 

### Community 315 - "Appnames"
Cohesion: 0.48
Nodes (4): filterAppsForDescription(), sanitizeAppNames(), sanitizeCore(), sanitizeTrustedNames()

### Community 316 - "Wrapper"
Cohesion: 0.38
Nodes (4): buildSessionContext(), getOrBind(), runPermissionDialog(), tuc()

### Community 317 - "Cron"
Cohesion: 0.33
Nodes (2): expandField(), parseCronExpression()

### Community 318 - "Crontaskslock"
Cohesion: 0.67
Nodes (6): getLockPath(), readLock(), registerLockCleanup(), releaseSchedulerLock(), tryAcquireSchedulerLock(), tryCreateExclusive()

### Community 319 - "Envdynamic"
Cohesion: 0.38
Nodes (3): detectJetBrainsIDEFromParentProcessAsync(), getTerminalWithJetBrainsDetectionAsync(), initJetBrainsDetection()

### Community 320 - "Exechttphook"
Cohesion: 0.48
Nodes (5): execHttpHook(), getHttpHookPolicy(), getSandboxProxyConfig(), interpolateEnvVars(), sanitizeHeaderValue()

### Community 321 - "Managedenv"
Cohesion: 0.52
Nodes (6): applyConfigEnvironmentVariables(), applySafeConfigEnvironmentVariables(), filterSettingsEnv(), withoutCcdSpawnEnvKeys(), withoutHostManagedProviderVars(), withoutSSHTunnelVars()

### Community 322 - "Modelcapabilities"
Cohesion: 0.62
Nodes (6): getCacheDir(), getCachePath(), getModelCapability(), isModelCapabilitiesEligible(), refreshModelCapabilities(), sortForMatching()

### Community 323 - "Bypasspermissionskillswitch"
Cohesion: 0.29
Nodes (0): 

### Community 324 - "Shadowedruledetection"
Cohesion: 0.57
Nodes (6): detectUnreachableRules(), formatSource(), generateFixSuggestion(), isAllowRuleShadowedByAskRule(), isAllowRuleShadowedByDenyRule(), isSharedSettingSource()

### Community 325 - "Shellrulematching"
Cohesion: 0.38
Nodes (3): hasWildcards(), parsePermissionRule(), permissionRuleExtractPrefix()

### Community 326 - "Loadpluginhooks"
Cohesion: 0.33
Nodes (2): getPluginAffectingSettingsSnapshot(), setupPluginHookHotReload()

### Community 327 - "Schemas"
Cohesion: 0.29
Nodes (0): 

### Community 328 - "Streamlinedtransform"
Cohesion: 0.48
Nodes (5): accumulateToolUses(), categorizeToolName(), createEmptyToolCounts(), createStreamlinedTransformer(), getToolSummaryText()

### Community 329 - "It2Setupprompt"
Cohesion: 0.29
Nodes (0): 

### Community 330 - "Leaderpermissionbridge"
Cohesion: 0.29
Nodes (0): 

### Community 331 - "Texthighlighting"
Cohesion: 0.43
Nodes (3): HighlightSegmenter, reduceCodes(), segmentTextByHighlights()

### Community 332 - "Truncate"
Cohesion: 0.48
Nodes (5): truncate(), truncatePathMiddle(), truncateStartToWidth(), truncateToWidth(), truncateToWidthNoEllipsis()

### Community 333 - "Keyword"
Cohesion: 0.52
Nodes (6): findKeywordTriggerPositions(), findUltraplanTriggerPositions(), findUltrareviewTriggerPositions(), hasUltraplanKeyword(), hasUltrareviewKeyword(), replaceUltraplanKeyword()

### Community 334 - "Desktopupsellstartup"
Cohesion: 0.38
Nodes (3): getDesktopUpsellConfig(), isSupportedPlatform(), shouldShowDesktopUpsellStartup()

### Community 335 - "Usepostcompactsurvey"
Cohesion: 0.29
Nodes (0): 

### Community 336 - "Guestpassesupsell"
Cohesion: 0.38
Nodes (3): resetIfPassesRefreshed(), shouldShowGuestPassesUpsell(), _temp()

### Community 337 - "Messagerow"
Cohesion: 0.38
Nodes (3): allToolsResolved(), areMessageRowPropsEqual(), isMessageStreaming()

### Community 338 - "Themeprovider"
Cohesion: 0.29
Nodes (0): 

### Community 339 - "Chrome"
Cohesion: 0.29
Nodes (0): 

### Community 340 - "Mobile"
Cohesion: 0.29
Nodes (0): 

### Community 341 - "Commandsemantics"
Cohesion: 0.48
Nodes (4): extractBaseCommand(), getCommandSemantic(), heuristicallyExtractBaseCommand(), interpretCommandResult()

### Community 342 - "Magicdocs"
Cohesion: 0.38
Nodes (3): detectMagicDocHeader(), getMagicDocsAgent(), updateMagicDoc()

### Community 343 - "Autodream"
Cohesion: 0.48
Nodes (5): getConfig(), initAutoDream(), isForced(), isGateOpen(), makeDreamProgressWatcher()

### Community 344 - "Autocompact"
Cohesion: 0.76
Nodes (6): autoCompactIfNeeded(), calculateTokenWarningState(), getAutoCompactThreshold(), getEffectiveContextWindowSize(), isAutoCompactEnabled(), shouldAutoCompact()

### Community 345 - "Inprocesstransport"
Cohesion: 0.33
Nodes (2): createLinkedTransportPair(), InProcessTransport

### Community 346 - "Channelpermissions"
Cohesion: 0.33
Nodes (2): hashToId(), shortRequestId()

### Community 347 - "Mcpstringutils"
Cohesion: 0.38
Nodes (3): buildMcpToolName(), getMcpPrefix(), getToolNameForPermissionCheck()

### Community 348 - "Tracker"
Cohesion: 0.29
Nodes (0): 

### Community 349 - "Useteammateshutdownnotification"
Cohesion: 0.48
Nodes (5): foldShutdown(), foldSpawn(), makeShutdownNotif(), makeSpawnNotif(), parseCount()

### Community 350 - "Bidi"
Cohesion: 0.52
Nodes (6): getBidi(), hasRTLCharacters(), needsBidi(), reorderBidi(), reverseRange(), reverseRangeNumbers()

### Community 351 - "Search Service"
Cohesion: 0.43
Nodes (4): buildIndex(), excerpt(), highlight(), searchConversations()

### Community 352 - "Node"
Cohesion: 0.29
Nodes (0): 

### Community 353 - "Claudeapi"
Cohesion: 0.48
Nodes (4): buildInlineReference(), buildPrompt(), getFilesForLanguage(), processContent()

### Community 354 - "Inprocessteammatetask"
Cohesion: 0.33
Nodes (2): getAllInProcessTeammateTasks(), getRunningTeammatesSorted()

### Community 355 - "Overlaycontext"
Cohesion: 0.29
Nodes (0): 

### Community 356 - "Authfiledescriptor"
Cohesion: 0.6
Nodes (5): getApiKeyFromFileDescriptor(), getCredentialFromFd(), getOAuthTokenFromFileDescriptor(), maybePersistTokenForSubprocesses(), readTokenFromWellKnownFile()

### Community 357 - "Shellquote"
Cohesion: 0.4
Nodes (2): quote(), tryQuoteShellArgs()

### Community 358 - "Drainrunloop"
Cohesion: 0.47
Nodes (3): drainRunLoop(), release(), retain()

### Community 359 - "Doctorcontextwarnings"
Cohesion: 0.6
Nodes (5): checkAgentDescriptions(), checkClaudeMdFiles(), checkContextWarnings(), checkMcpTools(), checkUnreachableRules()

### Community 360 - "Filereadcache"
Cohesion: 0.33
Nodes (1): FileReadCache

### Community 361 - "Genericprocessutils"
Cohesion: 0.33
Nodes (0): 

### Community 362 - "Githubrepopathmapping"
Cohesion: 0.33
Nodes (0): 

### Community 363 - "Skillimprovement"
Cohesion: 0.4
Nodes (2): createSkillImprovementHook(), initSkillImprovement()

### Community 364 - "Idepathconversion"
Cohesion: 0.33
Nodes (1): WindowsToWSLConverter

### Community 365 - "Lockfile"
Cohesion: 0.6
Nodes (5): check(), getLockfile(), lock(), lockSync(), unlock()

### Community 366 - "Agent"
Cohesion: 0.47
Nodes (3): aliasMatchesParentTier(), getAgentModel(), getDefaultSubagentModel()

### Community 367 - "Modelallowlist"
Cohesion: 0.6
Nodes (5): familyHasSpecificEntries(), isModelAllowed(), modelBelongsToFamily(), modelMatchesVersionPrefix(), prefixMatchesModel()

### Community 368 - "Packagemanagers"
Cohesion: 0.33
Nodes (0): 

### Community 369 - "Hintrecommendation"
Cohesion: 0.33
Nodes (0): 

### Community 370 - "Pluginidentifier"
Cohesion: 0.33
Nodes (0): 

### Community 371 - "Queryhelpers"
Cohesion: 0.4
Nodes (2): extractBashToolsFromMessages(), extractCliName()

### Community 372 - "Keychainprefetch"
Cohesion: 0.4
Nodes (2): spawnSecurity(), startKeychainPrefetch()

### Community 373 - "Sessionfileaccesshooks"
Cohesion: 0.6
Nodes (4): getFilePathFromInput(), getSessionFileTypeFromInput(), handleSessionFileAccess(), isMemoryFileAccess()

### Community 374 - "Powershelldetection"
Cohesion: 0.53
Nodes (4): findPowerShell(), getCachedPowerShellPath(), getPowerShellEdition(), probePath()

### Community 375 - "Teammatemodesnapshot"
Cohesion: 0.4
Nodes (2): captureTeammateModeSnapshot(), getTeammateModeFromSnapshot()

### Community 376 - "Claudemdexternalincludesdialog"
Cohesion: 0.33
Nodes (0): 

### Community 377 - "Ideautoconnectdialog"
Cohesion: 0.33
Nodes (0): 

### Community 378 - "Channelsnotice"
Cohesion: 0.4
Nodes (2): findUnmatched(), _temp()

### Community 379 - "Notifications"
Cohesion: 0.33
Nodes (0): 

### Community 380 - "Outputline"
Cohesion: 0.53
Nodes (4): linkifyUrlsInText(), OutputLine(), stripUnderlineAnsi(), tryJsonFormatContent()

### Community 381 - "Btw"
Cohesion: 0.4
Nodes (2): buildCacheSafeParams(), stripInProgressAssistantMessage()

### Community 382 - "Supportedsettings"
Cohesion: 0.33
Nodes (0): 

### Community 383 - "Sink"
Cohesion: 0.47
Nodes (3): logEventAsyncImpl(), logEventImpl(), shouldTrackDatadog()

### Community 384 - "Metricsoptout"
Cohesion: 0.4
Nodes (2): checkMetricsEnabled(), refreshMetricsStatus()

### Community 385 - "Overagecreditgrant"
Cohesion: 0.4
Nodes (2): fetchOverageCreditGrant(), refreshOverageCreditGrantCache()

### Community 386 - "Elicitationhandler"
Cohesion: 0.33
Nodes (0): 

### Community 387 - "Notifier"
Cohesion: 0.67
Nodes (5): generateKittyId(), isAppleTerminalBellDisabled(), sendAuto(), sendNotification(), sendToChannel()

### Community 388 - "Secretscanner"
Cohesion: 0.53
Nodes (4): getCompiledRules(), getSecretLabel(), ruleIdToLabel(), scanForSecrets()

### Community 389 - "Usefastmodenotification"
Cohesion: 0.33
Nodes (0): 

### Community 390 - "Usemcpconnectivitystatus"
Cohesion: 0.33
Nodes (0): 

### Community 391 - "Colorize"
Cohesion: 0.47
Nodes (3): applyColor(), applyTextStyles(), colorize()

### Community 392 - "Terminal Focus State"
Cohesion: 0.33
Nodes (0): 

### Community 393 - "Claude Service"
Cohesion: 0.53
Nodes (4): buildTools(), executeTool(), isAutoApproved(), streamMessage()

### Community 394 - "Exec Service"
Cohesion: 0.33
Nodes (1): ExecService

### Community 395 - "User Store"
Cohesion: 0.47
Nodes (1): UserStore

### Community 396 - "Bridgedebug"
Cohesion: 0.33
Nodes (0): 

### Community 397 - "Remotebridgecore"
Cohesion: 0.53
Nodes (4): archiveSession(), initEnvLessBridgeCore(), oauthHeaders(), withRetry()

### Community 398 - "Trusteddevice"
Cohesion: 0.47
Nodes (3): clearTrustedDeviceToken(), getTrustedDeviceToken(), isGateEnabled()

### Community 399 - "Worksecret"
Cohesion: 0.33
Nodes (0): 

### Community 400 - "Automode"
Cohesion: 0.53
Nodes (5): autoModeConfigHandler(), autoModeCritiqueHandler(), autoModeDefaultsHandler(), formatRulesForCritique(), writeRules()

### Community 401 - "Keybindingcontext"
Cohesion: 0.4
Nodes (2): useOptionalKeybindingContext(), useRegisterKeybindingContext()

### Community 402 - "Match"
Cohesion: 0.6
Nodes (5): getInkModifiers(), getKeyName(), matchesBinding(), matchesKeystroke(), modifiersMatch()

### Community 403 - "Dreamtask"
Cohesion: 0.33
Nodes (0): 

### Community 404 - "Promptoverlaycontext"
Cohesion: 0.33
Nodes (0): 

### Community 405 - "Agentid"
Cohesion: 0.4
Nodes (0): 

### Community 406 - "Agenticsessionsearch"
Cohesion: 0.5
Nodes (2): extractTranscript(), logContainsQuery()

### Community 407 - "Argumentsubstitution"
Cohesion: 0.5
Nodes (2): parseArguments(), substituteArguments()

### Community 408 - "Autorunissue"
Cohesion: 0.4
Nodes (0): 

### Community 409 - "Aws"
Cohesion: 0.4
Nodes (0): 

### Community 410 - "Contextanalysis"
Cohesion: 0.5
Nodes (2): increment(), processBlock()

### Community 411 - "Helpers"
Cohesion: 0.6
Nodes (3): parseAndValidateManifestFromBytes(), parseAndValidateManifestFromText(), validateManifest()

### Community 412 - "Examplecommands"
Cohesion: 0.6
Nodes (3): getFrequentlyModifiedFiles(), isCoreFile(), pickDiverseCoreFiles()

### Community 413 - "Fileread"
Cohesion: 0.7
Nodes (4): detectEncodingForResolvedPath(), detectLineEndingsForString(), readFileSync(), readFileSyncWithMetadata()

### Community 414 - "Generators"
Cohesion: 0.5
Nodes (2): next(), returnValue()

### Community 415 - "Headlessprofiler"
Cohesion: 0.5
Nodes (2): clearHeadlessMarks(), headlessProfilerStartTurn()

### Community 416 - "Heatmap"
Cohesion: 0.7
Nodes (4): calculatePercentiles(), generateHeatmap(), getHeatmapChar(), getIntensity()

### Community 417 - "Hooksconfigmanager"
Cohesion: 0.4
Nodes (0): 

### Community 418 - "Imagevalidation"
Cohesion: 0.5
Nodes (3): ImageSizeError, isBase64ImageBlock(), validateImagesForAPI()

### Community 419 - "Inprocessteammatehelpers"
Cohesion: 0.5
Nodes (2): handlePlanApprovalResponse(), setAwaitingPlanApproval()

### Community 420 - "Mtls"
Cohesion: 0.4
Nodes (0): 

### Community 421 - "Denialtracking"
Cohesion: 0.4
Nodes (0): 

### Community 422 - "Permissionexplainer"
Cohesion: 0.7
Nodes (4): extractConversationContext(), formatToolInput(), generatePermissionExplanation(), isPermissionExplainerEnabled()

### Community 423 - "Planmodev2"
Cohesion: 0.4
Nodes (0): 

### Community 424 - "Fetchtelemetry"
Cohesion: 0.6
Nodes (3): extractHost(), isOfficialRepo(), logPluginFetch()

### Community 425 - "Staticprefix"
Cohesion: 0.7
Nodes (4): extractPrefixFromElement(), getCommandPrefixStatic(), getCompoundCommandPrefixesStatic(), wordAlignedLCP()

### Community 426 - "Privacylevel"
Cohesion: 0.6
Nodes (3): getPrivacyLevel(), isEssentialTrafficOnly(), isTelemetryDisabled()

### Community 427 - "Prompteditor"
Cohesion: 0.7
Nodes (4): editFileInEditor(), editPromptInEditor(), isGuiEditor(), recollapsePastedContent()

### Community 428 - "Sessionenvvars"
Cohesion: 0.4
Nodes (0): 

### Community 429 - "Sessioningressauth"
Cohesion: 0.6
Nodes (3): getSessionIngressAuthHeaders(), getSessionIngressAuthToken(), getTokenFromFileDescriptor()

### Community 430 - "Set"
Cohesion: 0.4
Nodes (0): 

### Community 431 - "Rawread"
Cohesion: 0.5
Nodes (2): fireRawRead(), startMdmRawRead()

### Community 432 - "Permissionvalidation"
Cohesion: 0.8
Nodes (4): countUnescapedChar(), hasUnescapedEmptyParens(), isEscaped(), validatePermissionRule()

### Community 433 - "Readonlycommandvalidation"
Cohesion: 0.5
Nodes (2): validateFlagArgument(), validateFlags()

### Community 434 - "Shellhistorycompletion"
Cohesion: 0.5
Nodes (2): getShellHistoryCommands(), getShellHistoryCompletion()

### Community 435 - "Teammatecontext"
Cohesion: 0.4
Nodes (0): 

### Community 436 - "Theme"
Cohesion: 0.4
Nodes (0): 

### Community 437 - "Tokenbudget"
Cohesion: 0.5
Nodes (2): parseBudgetMatch(), parseTokenBudget()

### Community 438 - "Toolerrors"
Cohesion: 0.5
Nodes (2): formatError(), getErrorParts()

### Community 439 - "Transcriptsearch"
Cohesion: 0.6
Nodes (3): computeSearchText(), renderableSearchText(), toolResultSearchText()

### Community 440 - "Consoleoauthflow"
Cohesion: 0.4
Nodes (0): 

### Community 441 - "Desktophandoff"
Cohesion: 0.4
Nodes (0): 

### Community 442 - "Animatedclawd"
Cohesion: 0.5
Nodes (2): AnimatedClawd(), useClawdAnimation()

### Community 443 - "Promptinputfootersuggestions"
Cohesion: 0.4
Nodes (0): 

### Community 444 - "Voiceindicator"
Cohesion: 0.4
Nodes (0): 

### Community 445 - "Inputmodes"
Cohesion: 0.5
Nodes (2): getModeFromInput(), getValueFromInput()

### Community 446 - "Sentryerrorboundary"
Cohesion: 0.4
Nodes (1): SentryErrorBoundary

### Community 447 - "Usage"
Cohesion: 0.4
Nodes (0): 

### Community 448 - "Statusline"
Cohesion: 0.4
Nodes (0): 

### Community 449 - "Colordiff"
Cohesion: 0.7
Nodes (4): expectColorDiff(), expectColorFile(), getColorModuleUnavailableReason(), getSyntaxTheme()

### Community 450 - "Validationerrorslist"
Cohesion: 0.4
Nodes (0): 

### Community 451 - "Confirmstep"
Cohesion: 0.4
Nodes (0): 

### Community 452 - "Selectmatchermode"
Cohesion: 0.4
Nodes (0): 

### Community 453 - "Viewhookmode"
Cohesion: 0.4
Nodes (0): 

### Community 454 - "Shutdownmessage"
Cohesion: 0.4
Nodes (0): 

### Community 455 - "Userresourceupdatemessage"
Cohesion: 0.6
Nodes (4): formatUri(), parseUpdates(), _temp(), UserResourceUpdateMessage()

### Community 456 - "Previewbox"
Cohesion: 0.4
Nodes (0): 

### Community 457 - "Usepermissionhandler"
Cohesion: 0.7
Nodes (4): handleAcceptOnce(), handleAcceptSession(), handleReject(), logPermissionEvent()

### Community 458 - "Recentdenialstab"
Cohesion: 0.4
Nodes (0): 

### Community 459 - "Skillsmenu"
Cohesion: 0.4
Nodes (0): 

### Community 460 - "Wizardprovider"
Cohesion: 0.4
Nodes (0): 

### Community 461 - "Exit"
Cohesion: 0.5
Nodes (2): call(), getRandomGoodbyeMessage()

### Community 462 - "Install"
Cohesion: 0.4
Nodes (0): 

### Community 463 - "Remote Setup"
Cohesion: 0.5
Nodes (2): errorMessage(), handleConfirm()

### Community 464 - "Agentdisplay"
Cohesion: 0.4
Nodes (0): 

### Community 465 - "Bashcommandhelpers"
Cohesion: 0.6
Nodes (3): bashToolCheckCommandOperatorPermissions(), checkCommandOperatorPermissions(), segmentedCommandPermissionResult()

### Community 466 - "Channelnotification"
Cohesion: 0.6
Nodes (3): findChannelEntry(), gateChannelServer(), getEffectiveChannelAllowlist()

### Community 467 - "Officialregistry"
Cohesion: 0.5
Nodes (2): normalizeUrl(), prefetchOfficialMcpUrls()

### Community 468 - "Ratelimitmocking"
Cohesion: 0.4
Nodes (0): 

### Community 469 - "Tipregistry"
Cohesion: 0.6
Nodes (4): getCustomTips(), getRelevantTips(), isMarketplacePluginRelevant(), isOfficialMarketplaceInstalled()

### Community 470 - "Usecanswitchtoexistingsubscription"
Cohesion: 0.5
Nodes (2): getExistingClaudeSubscription(), _temp2()

### Community 471 - "Useplugininstallationstatus"
Cohesion: 0.4
Nodes (0): 

### Community 472 - "Usenotifyaftertimeout"
Cohesion: 0.6
Nodes (3): getTimeSinceLastInteraction(), hasRecentInteraction(), shouldNotify()

### Community 473 - "Usevoiceintegration"
Cohesion: 0.5
Nodes (2): useVoiceKeybindingHandler(), VoiceKeybindingHandler()

### Community 474 - "Clearterminal"
Cohesion: 0.7
Nodes (4): getClearTerminalSequence(), isMintty(), isModernWindowsTerminal(), isWindowsTerminal()

### Community 475 - "Use Selection"
Cohesion: 0.4
Nodes (0): 

### Community 476 - "Stringwidth"
Cohesion: 0.7
Nodes (4): getEmojiWidth(), isZeroWidth(), needsSegmentation(), stringWidthJavaScript()

### Community 477 - "Aggregator"
Cohesion: 0.7
Nodes (4): aggregate(), num(), str(), toYMD()

### Community 478 - "Rate Limit"
Cohesion: 0.8
Nodes (4): check(), keyFor(), rateLimitMessages(), rateLimitRequests()

### Community 479 - "Metrics"
Cohesion: 0.4
Nodes (0): 

### Community 480 - "Scrollback Buffer"
Cohesion: 0.4
Nodes (1): ScrollbackBuffer

### Community 481 - "Bridgeconfig"
Cohesion: 0.6
Nodes (4): getBridgeAccessToken(), getBridgeBaseUrl(), getBridgeBaseUrlOverride(), getBridgeTokenOverride()

### Community 482 - "Createsession"
Cohesion: 0.4
Nodes (0): 

### Community 483 - "Jwtutils"
Cohesion: 0.5
Nodes (2): decodeJwtExpiry(), decodeJwtPayload()

### Community 484 - "Oauth"
Cohesion: 0.5
Nodes (2): fileSuffixForOauthConfig(), getOauthConfigType()

### Community 485 - "Product"
Cohesion: 0.7
Nodes (4): getClaudeAiBaseUrl(), getRemoteSessionUrl(), isRemoteSessionLocal(), isRemoteSessionStaging()

### Community 486 - "Systempromptsections"
Cohesion: 0.4
Nodes (0): 

### Community 487 - "Growthbook Experiment Event"
Cohesion: 0.5
Nodes (2): fromJsonTimestamp(), fromTimestamp()

### Community 488 - "Keybindingprovidersetup"
Cohesion: 0.5
Nodes (2): KeybindingSetup(), useKeybindingWarnings()

### Community 489 - "Memoryage"
Cohesion: 0.7
Nodes (4): memoryAge(), memoryAgeDays(), memoryFreshnessNote(), memoryFreshnessText()

### Community 490 - "Usebuddynotification"
Cohesion: 0.4
Nodes (0): 

### Community 491 - "Ansitosvg"
Cohesion: 0.83
Nodes (3): ansiToSvg(), get256Color(), parseAnsi()

### Community 492 - "Array"
Cohesion: 0.5
Nodes (0): 

### Community 493 - "Sleep"
Cohesion: 0.5
Nodes (0): 

### Community 494 - "Billing"
Cohesion: 0.5
Nodes (0): 

### Community 495 - "Browser"
Cohesion: 0.67
Nodes (2): openBrowser(), validateUrl()

### Community 496 - "Codeindexing"
Cohesion: 0.5
Nodes (0): 

### Community 497 - "Eschotkey"
Cohesion: 0.5
Nodes (0): 

### Community 498 - "Cronscheduler"
Cohesion: 0.5
Nodes (0): 

### Community 499 - "Cwd"
Cohesion: 0.67
Nodes (2): getCwd(), pwd()

### Community 500 - "Debugfilter"
Cohesion: 0.83
Nodes (3): extractDebugCategories(), shouldShowDebugCategories(), shouldShowDebugMessage()

### Community 501 - "Parsedeeplink"
Cohesion: 0.67
Nodes (2): containsControlChars(), parseDeepLink()

### Community 502 - "Protocolhandler"
Cohesion: 0.83
Nodes (3): handleDeepLinkUri(), handleUrlSchemeLaunch(), resolveCwd()

### Community 503 - "Displaytags"
Cohesion: 0.5
Nodes (0): 

### Community 504 - "Execfilenothrow"
Cohesion: 0.67
Nodes (2): execFileNoThrow(), execFileNoThrowWithCwd()

### Community 505 - "Exportrenderer"
Cohesion: 0.67
Nodes (2): renderMessagesToPlainText(), streamRenderedMessages()

### Community 506 - "Formatbrieftimestamp"
Cohesion: 0.83
Nodes (3): formatBriefTimestamp(), getLocale(), startOfDay()

### Community 507 - "Fpstracker"
Cohesion: 0.5
Nodes (1): FpsTracker

### Community 508 - "Grouptooluses"
Cohesion: 0.83
Nodes (3): applyGrouping(), getToolsWithGrouping(), getToolUseInfo()

### Community 509 - "Hash"
Cohesion: 0.5
Nodes (0): 

### Community 510 - "Hookhelpers"
Cohesion: 0.5
Nodes (0): 

### Community 511 - "Postsamplinghooks"
Cohesion: 0.5
Nodes (0): 

### Community 512 - "Memoize"
Cohesion: 0.5
Nodes (0): 

### Community 513 - "Antmodels"
Cohesion: 0.83
Nodes (3): getAntModelOverrideConfig(), getAntModels(), resolveAntModel()

### Community 514 - "Check1Maccess"
Cohesion: 0.83
Nodes (3): checkOpus1mAccess(), checkSonnet1mAccess(), isExtraUsageEnabled()

### Community 515 - "Providers"
Cohesion: 0.67
Nodes (2): getAPIProvider(), getAPIProviderForStatsig()

### Community 516 - "Validatemodel"
Cohesion: 0.83
Nodes (3): get3PFallbackSuggestion(), handleValidationError(), validateModel()

### Community 517 - "Pdfutils"
Cohesion: 0.5
Nodes (0): 

### Community 518 - "Getnextpermissionmode"
Cohesion: 0.83
Nodes (3): canCycleToAuto(), cyclePermissionMode(), getNextPermissionMode()

### Community 519 - "Gitavailability"
Cohesion: 0.5
Nodes (0): 

### Community 520 - "Refresh"
Cohesion: 0.5
Nodes (0): 

### Community 521 - "Preflightchecks"
Cohesion: 0.5
Nodes (0): 

### Community 522 - "Profilerbase"
Cohesion: 0.67
Nodes (2): formatMs(), formatTimelineLine()

### Community 523 - "Queueprocessor"
Cohesion: 0.67
Nodes (2): isSlashCommand(), processQueueIfReady()

### Community 524 - "Sessionstart"
Cohesion: 0.5
Nodes (0): 

### Community 525 - "Internalwrites"
Cohesion: 0.5
Nodes (0): 

### Community 526 - "Toolvalidationconfig"
Cohesion: 0.5
Nodes (0): 

### Community 527 - "Sidequestion"
Cohesion: 0.67
Nodes (2): extractSideQuestionResponse(), runSideQuestion()

### Community 528 - "Sliceansi"
Cohesion: 0.67
Nodes (2): filterStartCodes(), sliceAnsi()

### Community 529 - "Streamjsonstdoutguard"
Cohesion: 0.67
Nodes (2): installStreamJsonStdoutGuard(), isJsonLine()

### Community 530 - "Spawnutils"
Cohesion: 0.5
Nodes (0): 

### Community 531 - "Taggedid"
Cohesion: 0.83
Nodes (3): base58Encode(), toTaggedId(), uuidToBigInt()

### Community 532 - "Teammemoryops"
Cohesion: 0.5
Nodes (0): 

### Community 533 - "Toolpool"
Cohesion: 0.67
Nodes (2): applyCoordinatorToolFilter(), mergeAndFilterTools()

### Community 534 - "Undercover"
Cohesion: 0.67
Nodes (2): isUndercover(), shouldShowUndercoverAutoNotice()

### Community 535 - "Bypasspermissionsmodedialog"
Cohesion: 0.5
Nodes (0): 

### Community 536 - "Contextvisualization"
Cohesion: 0.5
Nodes (0): 

### Community 537 - "Devbar"
Cohesion: 0.67
Nodes (2): DevBar(), shouldShowDevBar()

### Community 538 - "Devchannelsdialog"
Cohesion: 0.5
Nodes (0): 

### Community 539 - "Ideonboardingdialog"
Cohesion: 0.83
Nodes (3): hasIdeOnboardingDialogBeenShown(), IdeOnboardingDialog(), markDialogAsShown()

### Community 540 - "Keybindingwarnings"
Cohesion: 0.5
Nodes (0): 

### Community 541 - "Condensedlogo"
Cohesion: 0.5
Nodes (0): 

### Community 542 - "Voicemodenotice"
Cohesion: 0.5
Nodes (0): 

### Community 543 - "Onboarding"
Cohesion: 0.83
Nodes (3): goToNextStep(), handleApiKeyDone(), handleThemeSelection()

### Community 544 - "Promptinputqueuedcommands"
Cohesion: 0.67
Nodes (2): createOverflowNotificationMessage(), processQueuedCommands()

### Community 545 - "Inputpaste"
Cohesion: 0.83
Nodes (3): formatTruncatedTextRef(), maybeTruncateInput(), maybeTruncateMessageForInput()

### Community 546 - "Sandboxviolationexpandedview"
Cohesion: 0.5
Nodes (0): 

### Community 547 - "Sessionbackgroundhint"
Cohesion: 0.5
Nodes (0): 

### Community 548 - "Tagtabs"
Cohesion: 0.5
Nodes (0): 

### Community 549 - "Workflowmultiselectdialog"
Cohesion: 0.5
Nodes (0): 

### Community 550 - "Selecthookmode"
Cohesion: 0.5
Nodes (0): 

### Community 551 - "Planapprovalmessage"
Cohesion: 0.5
Nodes (0): 

### Community 552 - "Taskassignmentmessage"
Cohesion: 0.5
Nodes (0): 

### Community 553 - "Bashtooluseoptions"
Cohesion: 0.67
Nodes (2): bashToolUseOptions(), descriptionAlreadyExists()

### Community 554 - "Filesystempermissionrequest"
Cohesion: 0.67
Nodes (2): FilesystemPermissionRequest(), pathFromToolUse()

### Community 555 - "Permissionrequest"
Cohesion: 0.83
Nodes (3): getNotificationMessage(), permissionComponentForTool(), PermissionRequest()

### Community 556 - "Sandboxdependenciestab"
Cohesion: 0.5
Nodes (0): 

### Community 557 - "Shelldetaildialog"
Cohesion: 0.5
Nodes (0): 

### Community 558 - "Teamstatus"
Cohesion: 0.5
Nodes (0): 

### Community 559 - "Treeselect"
Cohesion: 0.5
Nodes (0): 

### Community 560 - "Agents"
Cohesion: 0.67
Nodes (2): agentsHandler(), formatAgent()

### Community 561 - "Context Noninteractive"
Cohesion: 0.83
Nodes (3): call(), collectContextData(), formatContextAsMarkdownTable()

### Community 562 - "Logout"
Cohesion: 0.83
Nodes (3): call(), clearAuthRelatedCaches(), performLogout()

### Community 563 - "Reviewremote"
Cohesion: 0.5
Nodes (0): 

### Community 564 - "Ultrareviewcommand"
Cohesion: 0.83
Nodes (3): call(), contentBlocksToString(), launchAndDone()

### Community 565 - "Askuserquestiontool"
Cohesion: 0.5
Nodes (0): 

### Community 566 - "Imageprocessor"
Cohesion: 0.83
Nodes (3): getImageCreator(), getImageProcessor(), unwrapDefault()

### Community 567 - "Syntheticoutputtool"
Cohesion: 0.67
Nodes (2): buildSyntheticOutputTool(), createSyntheticOutputTool()

### Community 568 - "Adminrequests"
Cohesion: 0.5
Nodes (0): 

### Community 569 - "Passivefeedback"
Cohesion: 0.5
Nodes (0): 

### Community 570 - "Mcpconnectionmanager"
Cohesion: 0.5
Nodes (0): 

### Community 571 - "Channelallowlist"
Cohesion: 0.67
Nodes (2): getChannelAllowlist(), isChannelAllowlisted()

### Community 572 - "Claudeai"
Cohesion: 0.5
Nodes (0): 

### Community 573 - "Headershelper"
Cohesion: 0.83
Nodes (3): getMcpHeadersFromHelper(), getMcpServerHeaders(), isMcpServerFromProjectOrLocalSettings()

### Community 574 - "Vscodesdkmcp"
Cohesion: 0.67
Nodes (2): readAutoModeEnabledState(), setupVscodeSdkMcp()

### Community 575 - "Tipscheduler"
Cohesion: 0.67
Nodes (2): getTipToShowOnSpinner(), selectTipWithLongestTimeSinceShown()

### Community 576 - "Toolorchestration"
Cohesion: 0.5
Nodes (0): 

### Community 577 - "Useidestatusindicator"
Cohesion: 0.5
Nodes (0): 

### Community 578 - "Useinstallmessages"
Cohesion: 0.5
Nodes (0): 

### Community 579 - "Uselspinitializationnotification"
Cohesion: 0.5
Nodes (0): 

### Community 580 - "Usemodelmigrationnotifications"
Cohesion: 0.5
Nodes (0): 

### Community 581 - "Permissioncontext"
Cohesion: 0.5
Nodes (0): 

### Community 582 - "Usecanusetool"
Cohesion: 0.5
Nodes (0): 

### Community 583 - "Usechromeextensionnotification"
Cohesion: 0.67
Nodes (2): getChromeFlag(), _temp()

### Community 584 - "Useissueflagbanner"
Cohesion: 0.5
Nodes (0): 

### Community 585 - "Usepromptsfromclaudeinchrome"
Cohesion: 0.5
Nodes (0): 

### Community 586 - "Usesearchinput"
Cohesion: 0.5
Nodes (0): 

### Community 587 - "Usetasklistwatcher"
Cohesion: 0.5
Nodes (0): 

### Community 588 - "Usetextinput"
Cohesion: 0.67
Nodes (2): mapInput(), useTextInput()

### Community 589 - "Usevoice"
Cohesion: 0.5
Nodes (0): 

### Community 590 - "Ansi"
Cohesion: 0.5
Nodes (0): 

### Community 591 - "Clockcontext"
Cohesion: 0.67
Nodes (2): createClock(), _temp()

### Community 592 - "Erroroverview"
Cohesion: 0.83
Nodes (3): cleanupPath(), ErrorOverview(), getStackUtils()

### Community 593 - "Event"
Cohesion: 0.5
Nodes (1): Event

### Community 594 - "Input Event"
Cohesion: 0.67
Nodes (2): InputEvent, parseKey()

### Community 595 - "Keyboard Event"
Cohesion: 0.67
Nodes (2): KeyboardEvent, keyFromParsed()

### Community 596 - "Hit Test"
Cohesion: 0.83
Nodes (3): dispatchClick(), dispatchHover(), hitTest()

### Community 597 - "Render Border"
Cohesion: 0.83
Nodes (3): embedTextInBorder(), renderBorder(), styleBorderLine()

### Community 598 - "Render To Screen"
Cohesion: 0.5
Nodes (0): 

### Community 599 - "Sgr"
Cohesion: 0.83
Nodes (3): applySGR(), parseExtendedColor(), parseParams()

### Community 600 - "Wrap Text"
Cohesion: 0.83
Nodes (3): sliceFit(), truncate(), wrapText()

### Community 601 - "Conversations"
Cohesion: 0.5
Nodes (0): 

### Community 602 - "Createdirectconnectsession"
Cohesion: 0.5
Nodes (1): DirectConnectError

### Community 603 - "Scrubber"
Cohesion: 0.67
Nodes (2): scrubObject(), scrubString()

### Community 604 - "Codesessionapi"
Cohesion: 0.83
Nodes (3): createCodeSession(), fetchRemoteCredentials(), oauthHeaders()

### Community 605 - "Envlessbridgeconfig"
Cohesion: 0.83
Nodes (3): checkEnvLessBridgeMinVersion(), getEnvLessBridgeConfig(), shouldShowAppUpgradeMessage()

### Community 606 - "Replbridgehandle"
Cohesion: 0.83
Nodes (3): getReplBridgeHandle(), getSelfBridgeCompatId(), setReplBridgeHandle()

### Community 607 - "Sessionidcompat"
Cohesion: 0.5
Nodes (0): 

### Community 608 - "System"
Cohesion: 0.67
Nodes (2): getAttributionHeader(), isAttributionHeaderEnabled()

### Community 609 - "Ids"
Cohesion: 0.5
Nodes (0): 

### Community 610 - "Reservedshortcuts"
Cohesion: 0.5
Nodes (0): 

### Community 611 - "Stoptask"
Cohesion: 0.5
Nodes (1): StopTaskError

### Community 612 - "Modalcontext"
Cohesion: 0.5
Nodes (0): 

### Community 613 - "Sprites"
Cohesion: 0.5
Nodes (0): 

### Community 614 - "Agentswarmsenabled"
Cohesion: 1.0
Nodes (2): isAgentSwarmsEnabled(), isAgentTeamsFlagSet()

### Community 615 - "Authportable"
Cohesion: 0.67
Nodes (0): 

### Community 616 - "Automodedenials"
Cohesion: 0.67
Nodes (0): 

### Community 617 - "Binarycheck"
Cohesion: 0.67
Nodes (0): 

### Community 618 - "Bundledmode"
Cohesion: 0.67
Nodes (0): 

### Community 619 - "Cacertsconfig"
Cohesion: 1.0
Nodes (2): applyExtraCACertsFromConfig(), getExtraCertsPathFromConfig()

### Community 620 - "Cleanupregistry"
Cohesion: 0.67
Nodes (0): 

### Community 621 - "Cliargs"
Cohesion: 0.67
Nodes (0): 

### Community 622 - "Collapsebackgroundbashnotifications"
Cohesion: 1.0
Nodes (2): collapseBackgroundBashNotifications(), isCompletedBackgroundBash()

### Community 623 - "Collapsehooksummaries"
Cohesion: 1.0
Nodes (2): collapseHookSummaries(), isLabeledHookSummary()

### Community 624 - "Collapseteammateshutdowns"
Cohesion: 1.0
Nodes (2): collapseTeammateShutdowns(), isTeammateShutdownAttachment()

### Community 625 - "Commandlifecycle"
Cohesion: 0.67
Nodes (0): 

### Community 626 - "Directmembermessage"
Cohesion: 0.67
Nodes (0): 

### Community 627 - "Embeddedtools"
Cohesion: 0.67
Nodes (0): 

### Community 628 - "Ghprstatus"
Cohesion: 1.0
Nodes (2): deriveReviewState(), fetchPrStatus()

### Community 629 - "Datetimeparser"
Cohesion: 0.67
Nodes (0): 

### Community 630 - "Mcpinstructionsdelta"
Cohesion: 0.67
Nodes (0): 

### Community 631 - "Aliases"
Cohesion: 0.67
Nodes (0): 

### Community 632 - "Contextwindowupgradecheck"
Cohesion: 1.0
Nodes (2): getAvailableUpgrade(), getUpgradeMessage()

### Community 633 - "Deprecation"
Cohesion: 1.0
Nodes (2): getDeprecatedModelInfo(), getModelDeprecationWarning()

### Community 634 - "Modifiers"
Cohesion: 0.67
Nodes (0): 

### Community 635 - "Classifiershared"
Cohesion: 0.67
Nodes (0): 

### Community 636 - "Pluginblocklist"
Cohesion: 1.0
Nodes (2): detectAndUninstallDelistedPlugins(), detectDelistedPlugins()

### Community 637 - "Promptcategory"
Cohesion: 0.67
Nodes (0): 

### Community 638 - "Querycontext"
Cohesion: 1.0
Nodes (2): buildSideQuestionFallbackParams(), fetchSystemPromptParts()

### Community 639 - "Renderoptions"
Cohesion: 1.0
Nodes (2): getBaseRenderOptions(), getStdinOverride()

### Community 640 - "Sanitization"
Cohesion: 1.0
Nodes (2): partiallySanitizeUnicode(), recursivelySanitizeUnicode()

### Community 641 - "Macoskeychainstorage"
Cohesion: 0.67
Nodes (0): 

### Community 642 - "Sessiontitle"
Cohesion: 0.67
Nodes (0): 

### Community 643 - "Pluginonlypolicy"
Cohesion: 0.67
Nodes (0): 

### Community 644 - "Sidequery"
Cohesion: 1.0
Nodes (2): extractFirstUserMessageText(), sideQuery()

### Community 645 - "Subprocessenv"
Cohesion: 0.67
Nodes (0): 

### Community 646 - "Skillusagetracking"
Cohesion: 0.67
Nodes (0): 

### Community 647 - "Reconnection"
Cohesion: 0.67
Nodes (0): 

### Community 648 - "Spawninprocess"
Cohesion: 0.67
Nodes (0): 

### Community 649 - "Systemprompt"
Cohesion: 1.0
Nodes (2): buildEffectiveSystemPrompt(), isProactiveActive_SAFE_TO_CALL_ANYWHERE()

### Community 650 - "Outputformatting"
Cohesion: 1.0
Nodes (2): formatTaskOutput(), getMaxTaskOutputLength()

### Community 651 - "Environments"
Cohesion: 0.67
Nodes (0): 

### Community 652 - "Gitbundle"
Cohesion: 1.0
Nodes (2): _bundleWithFallback(), createAndUploadGitBundle()

### Community 653 - "Timeouts"
Cohesion: 1.0
Nodes (2): getDefaultBashTimeoutMs(), getMaxBashTimeoutMs()

### Community 654 - "Toolschemacache"
Cohesion: 0.67
Nodes (0): 

### Community 655 - "Userpromptkeywords"
Cohesion: 0.67
Nodes (0): 

### Community 656 - "Which"
Cohesion: 0.67
Nodes (0): 

### Community 657 - "Workloadcontext"
Cohesion: 0.67
Nodes (0): 

### Community 658 - "Xml"
Cohesion: 1.0
Nodes (2): escapeXml(), escapeXmlAttr()

### Community 659 - "Ctrlotoexpand"
Cohesion: 0.67
Nodes (0): 

### Community 660 - "Option Map"
Cohesion: 0.67
Nodes (1): OptionMap

### Community 661 - "Effortindicator"
Cohesion: 1.0
Nodes (2): effortLevelToSymbol(), getEffortNotificationText()

### Community 662 - "Exitflow"
Cohesion: 1.0
Nodes (2): ExitFlow(), getRandomGoodbyeMessage()

### Community 663 - "Fasticon"
Cohesion: 0.67
Nodes (0): 

### Community 664 - "Feedbacksurvey"
Cohesion: 0.67
Nodes (0): 

### Community 665 - "Feedbacksurveyview"
Cohesion: 0.67
Nodes (0): 

### Community 666 - "Transcriptshareprompt"
Cohesion: 0.67
Nodes (0): 

### Community 667 - "Usememorysurvey"
Cohesion: 0.67
Nodes (0): 

### Community 668 - "Idlereturndialog"
Cohesion: 1.0
Nodes (2): formatIdleDuration(), IdleReturnDialog()

### Community 669 - "Invalidconfigdialog"
Cohesion: 0.67
Nodes (0): 

### Community 670 - "Clawd"
Cohesion: 0.67
Nodes (0): 

### Community 671 - "Emergencytip"
Cohesion: 0.67
Nodes (0): 

### Community 672 - "Feed"
Cohesion: 0.67
Nodes (0): 

### Community 673 - "Feedcolumn"
Cohesion: 0.67
Nodes (0): 

### Community 674 - "Logov2"
Cohesion: 0.67
Nodes (0): 

### Community 675 - "Opus1Mmergenotice"
Cohesion: 0.67
Nodes (0): 

### Community 676 - "Mcpservermultiselectdialog"
Cohesion: 0.67
Nodes (0): 

### Community 677 - "Managedsettingssecuritydialog"
Cohesion: 0.67
Nodes (0): 

### Community 678 - "Markdowntable"
Cohesion: 0.67
Nodes (0): 

### Community 679 - "Messagemodel"
Cohesion: 0.67
Nodes (0): 

### Community 680 - "Messageresponse"
Cohesion: 0.67
Nodes (0): 

### Community 681 - "Messagetimestamp"
Cohesion: 0.67
Nodes (0): 

### Community 682 - "Nativeautoupdater"
Cohesion: 0.67
Nodes (0): 

### Community 683 - "Passes"
Cohesion: 0.67
Nodes (0): 

### Community 684 - "Prbadge"
Cohesion: 1.0
Nodes (2): getPrStatusColor(), PrBadge()

### Community 685 - "Promptinputhelpmenu"
Cohesion: 1.0
Nodes (2): formatShortcut(), PromptInputHelpMenu()

### Community 686 - "Useswarmbanner"
Cohesion: 1.0
Nodes (2): toThemeColor(), useSwarmBanner()

### Community 687 - "Remotecallout"
Cohesion: 0.67
Nodes (0): 

### Community 688 - "Resumetask"
Cohesion: 0.67
Nodes (0): 

### Community 689 - "Teammateviewheader"
Cohesion: 0.67
Nodes (0): 

### Community 690 - "Teleportrepomismatchdialog"
Cohesion: 0.67
Nodes (0): 

### Community 691 - "Tokenwarning"
Cohesion: 0.67
Nodes (0): 

### Community 692 - "Vimtextinput"
Cohesion: 0.67
Nodes (0): 

### Community 693 - "Worktreeexitdialog"
Cohesion: 0.67
Nodes (0): 

### Community 694 - "Validateagent"
Cohesion: 1.0
Nodes (2): validateAgent(), validateAgentType()

### Community 695 - "Byline"
Cohesion: 0.67
Nodes (0): 

### Community 696 - "Fuzzypicker"
Cohesion: 0.67
Nodes (0): 

### Community 697 - "Themedbox"
Cohesion: 1.0
Nodes (2): resolveColor(), ThemedBox()

### Community 698 - "Themedtext"
Cohesion: 1.0
Nodes (2): resolveColor(), ThemedText()

### Community 699 - "Mcpsettings"
Cohesion: 0.67
Nodes (0): 

### Community 700 - "Mcptooldetailview"
Cohesion: 0.67
Nodes (0): 

### Community 701 - "Reconnecthelpers"
Cohesion: 0.67
Nodes (0): 

### Community 702 - "Ratelimitmessage"
Cohesion: 1.0
Nodes (2): getUpsellMessage(), RateLimitMessage()

### Community 703 - "Systemapierrormessage"
Cohesion: 0.67
Nodes (0): 

### Community 704 - "Useragentnotificationmessage"
Cohesion: 1.0
Nodes (2): getStatusColor(), UserAgentNotificationMessage()

### Community 705 - "Userchannelmessage"
Cohesion: 1.0
Nodes (2): displayServerName(), UserChannelMessage()

### Community 706 - "Usermemoryinputmessage"
Cohesion: 1.0
Nodes (2): getSavingMessage(), UserMemoryInputMessage()

### Community 707 - "Usertextmessage"
Cohesion: 0.67
Nodes (0): 

### Community 708 - "Teammemcollapsed"
Cohesion: 0.67
Nodes (0): 

### Community 709 - "Use Multiple Choice State"
Cohesion: 0.67
Nodes (0): 

### Community 710 - "Enterplanmodepermissionrequest"
Cohesion: 0.67
Nodes (0): 

### Community 711 - "Permissionprompt"
Cohesion: 0.67
Nodes (0): 

### Community 712 - "Powershellpermissionrequest"
Cohesion: 0.67
Nodes (0): 

### Community 713 - "Skillpermissionrequest"
Cohesion: 0.67
Nodes (0): 

### Community 714 - "Webfetchpermissionrequest"
Cohesion: 1.0
Nodes (2): inputToPermissionRuleContent(), WebFetchPermissionRequest()

### Community 715 - "Addpermissionrules"
Cohesion: 0.67
Nodes (0): 

### Community 716 - "Sandboxconfigtab"
Cohesion: 0.67
Nodes (0): 

### Community 717 - "Sandboxoverridestab"
Cohesion: 0.67
Nodes (0): 

### Community 718 - "Expandshelloutputcontext"
Cohesion: 0.67
Nodes (0): 

### Community 719 - "Remotesessionprogress"
Cohesion: 0.67
Nodes (0): 

### Community 720 - "Shellprogress"
Cohesion: 0.67
Nodes (0): 

### Community 721 - "Setupgithubactions"
Cohesion: 1.0
Nodes (2): createWorkflowFile(), setupGitHubActions()

### Community 722 - "Plan"
Cohesion: 0.67
Nodes (0): 

### Community 723 - "Pluginerrors"
Cohesion: 0.67
Nodes (0): 

### Community 724 - "Pluginoptionsflow"
Cohesion: 0.67
Nodes (0): 

### Community 725 - "Plugin"
Cohesion: 0.67
Nodes (0): 

### Community 726 - "Plugindetailshelpers"
Cohesion: 0.67
Nodes (0): 

### Community 727 - "Rate Limit Options"
Cohesion: 0.67
Nodes (0): 

### Community 728 - "Release Notes"
Cohesion: 1.0
Nodes (2): call(), formatReleaseNotes()

### Community 729 - "Reload Plugins"
Cohesion: 1.0
Nodes (2): call(), n()

### Community 730 - "Agenttool"
Cohesion: 0.67
Nodes (0): 

### Community 731 - "Agentcolormanager"
Cohesion: 0.67
Nodes (0): 

### Community 732 - "Claudecodeguideagent"
Cohesion: 0.67
Nodes (0): 

### Community 733 - "Builtinagents"
Cohesion: 1.0
Nodes (2): areExplorePlanAgentsEnabled(), getBuiltInAgents()

### Community 734 - "Bashtoolresultmessage"
Cohesion: 0.67
Nodes (0): 

### Community 735 - "Shouldusesandbox"
Cohesion: 1.0
Nodes (2): containsExcludedCommand(), shouldUseSandbox()

### Community 736 - "Brieftool"
Cohesion: 1.0
Nodes (2): isBriefEnabled(), isBriefEntitled()

### Community 737 - "Configtool"
Cohesion: 0.67
Nodes (0): 

### Community 738 - "Exitworktreetool"
Cohesion: 0.67
Nodes (0): 

### Community 739 - "Greptool"
Cohesion: 0.67
Nodes (0): 

### Community 740 - "Classifyforcollapse"
Cohesion: 1.0
Nodes (2): classifyMcpToolForCollapse(), normalize()

### Community 741 - "Mcpauthtool"
Cohesion: 1.0
Nodes (2): createMcpAuthTool(), getConfigUrl()

### Community 742 - "Clmtypes"
Cohesion: 1.0
Nodes (2): isClmAllowedType(), normalizeTypeName()

### Community 743 - "Taskoutputtool"
Cohesion: 0.67
Nodes (0): 

### Community 744 - "Webfetchtool"
Cohesion: 0.67
Nodes (0): 

### Community 745 - "Websearchtool"
Cohesion: 0.67
Nodes (0): 

### Community 746 - "Agentsummary"
Cohesion: 0.67
Nodes (0): 

### Community 747 - "Bootstrap"
Cohesion: 1.0
Nodes (2): fetchBootstrapAPI(), fetchBootstrapData()

### Community 748 - "Awaysummary"
Cohesion: 1.0
Nodes (2): buildAwaySummaryPrompt(), generateAwaySummary()

### Community 749 - "Compactwarningstate"
Cohesion: 0.67
Nodes (0): 

### Community 750 - "Getoauthprofile"
Cohesion: 0.67
Nodes (0): 

### Community 751 - "Plugininstallationmanager"
Cohesion: 0.67
Nodes (0): 

### Community 752 - "Synccache"
Cohesion: 0.67
Nodes (0): 

### Community 753 - "Tiphistory"
Cohesion: 0.67
Nodes (0): 

### Community 754 - "Toolusesummarygenerator"
Cohesion: 0.67
Nodes (0): 

### Community 755 - "Paymentfetch"
Cohesion: 0.67
Nodes (0): 

### Community 756 - "Usenpmdeprecationnotification"
Cohesion: 0.67
Nodes (0): 

### Community 757 - "Usepluginautoupdatenotification"
Cohesion: 0.67
Nodes (0): 

### Community 758 - "Usesettingserrors"
Cohesion: 0.67
Nodes (0): 

### Community 759 - "Usearrowkeyhistory"
Cohesion: 0.67
Nodes (0): 

### Community 760 - "Useawaysummary"
Cohesion: 0.67
Nodes (0): 

### Community 761 - "Usebackgroundtasknavigation"
Cohesion: 0.67
Nodes (0): 

### Community 762 - "Usecopyonselect"
Cohesion: 0.67
Nodes (0): 

### Community 763 - "Usemergedclients"
Cohesion: 0.67
Nodes (0): 

### Community 764 - "Useofficialmarketplacenotification"
Cohesion: 0.67
Nodes (0): 

### Community 765 - "Usescheduledtasks"
Cohesion: 0.67
Nodes (0): 

### Community 766 - "Usevirtualscroll"
Cohesion: 0.67
Nodes (0): 

### Community 767 - "Button"
Cohesion: 0.67
Nodes (0): 

### Community 768 - "Click Event"
Cohesion: 0.67
Nodes (1): ClickEvent

### Community 769 - "Focus Event"
Cohesion: 0.67
Nodes (1): FocusEvent

### Community 770 - "Terminal Focus Event"
Cohesion: 0.67
Nodes (1): TerminalFocusEvent

### Community 771 - "Frame"
Cohesion: 0.67
Nodes (0): 

### Community 772 - "Use Interval"
Cohesion: 0.67
Nodes (0): 

### Community 773 - "Use Tab Status"
Cohesion: 0.67
Nodes (0): 

### Community 774 - "Node Cache"
Cohesion: 0.67
Nodes (0): 

### Community 775 - "Squash Text Nodes"
Cohesion: 0.67
Nodes (0): 

### Community 776 - "Dec"
Cohesion: 0.67
Nodes (0): 

### Community 777 - "Tokenize"
Cohesion: 0.67
Nodes (0): 

### Community 778 - "Router"
Cohesion: 0.67
Nodes (0): 

### Community 779 - "Session Manager Test"
Cohesion: 0.67
Nodes (0): 

### Community 780 - "Bridgeui"
Cohesion: 0.67
Nodes (0): 

### Community 781 - "Initreplbridge"
Cohesion: 1.0
Nodes (2): deriveTitle(), initReplBridge()

### Community 782 - "Replbridgetransport"
Cohesion: 0.67
Nodes (0): 

### Community 783 - "Batch"
Cohesion: 0.67
Nodes (0): 

### Community 784 - "Loop"
Cohesion: 0.67
Nodes (0): 

### Community 785 - "Loremipsum"
Cohesion: 0.67
Nodes (0): 

### Community 786 - "Skillify"
Cohesion: 0.67
Nodes (0): 

### Community 787 - "Updateconfig"
Cohesion: 0.67
Nodes (0): 

### Community 788 - "Mcpskillbuilders"
Cohesion: 0.67
Nodes (0): 

### Community 789 - "Ndjsonsafestringify"
Cohesion: 1.0
Nodes (2): escapeJsLineTerminators(), ndjsonSafeStringify()

### Community 790 - "Timestamp"
Cohesion: 0.67
Nodes (0): 

### Community 791 - "Template"
Cohesion: 1.0
Nodes (2): filterReservedShortcuts(), generateKeybindingsTemplate()

### Community 792 - "Usekeybinding"
Cohesion: 0.67
Nodes (0): 

### Community 793 - "Killshelltasks"
Cohesion: 1.0
Nodes (2): killShellTasksForAgent(), killTask()

### Community 794 - "Pilllabel"
Cohesion: 0.67
Nodes (0): 

### Community 795 - "Queuedmessagecontext"
Cohesion: 0.67
Nodes (0): 

### Community 796 - "Fpsmetrics"
Cohesion: 0.67
Nodes (0): 

### Community 797 - "Findrelevantmemories"
Cohesion: 1.0
Nodes (2): findRelevantMemories(), selectRelevantMemories()

### Community 798 - "Apipreconnect"
Cohesion: 1.0
Nodes (0): 

### Community 799 - "Remotesession"
Cohesion: 1.0
Nodes (0): 

### Community 800 - "Backgroundhousekeeping"
Cohesion: 1.0
Nodes (0): 

### Community 801 - "Shellprefix"
Cohesion: 1.0
Nodes (0): 

### Community 802 - "Bufferedwriter"
Cohesion: 1.0
Nodes (0): 

### Community 803 - "Cacerts"
Cohesion: 1.0
Nodes (0): 

### Community 804 - "Classifierapprovalshook"
Cohesion: 1.0
Nodes (0): 

### Community 805 - "Combinedabortsignal"
Cohesion: 1.0
Nodes (0): 

### Community 806 - "Inputloader"
Cohesion: 1.0
Nodes (0): 

### Community 807 - "Swiftloader"
Cohesion: 1.0
Nodes (0): 

### Community 808 - "Contentarray"
Cohesion: 1.0
Nodes (0): 

### Community 809 - "Controlmessagecompat"
Cohesion: 1.0
Nodes (0): 

### Community 810 - "Cronjitterconfig"
Cohesion: 1.0
Nodes (0): 

### Community 811 - "Terminalpreference"
Cohesion: 1.0
Nodes (0): 

### Community 812 - "Envvalidation"
Cohesion: 1.0
Nodes (0): 

### Community 813 - "Execfilenothrowportable"
Cohesion: 1.0
Nodes (0): 

### Community 814 - "Execsyncwrapper"
Cohesion: 1.0
Nodes (0): 

### Community 815 - "Extrausage"
Cohesion: 1.0
Nodes (0): 

### Community 816 - "Findexecutable"
Cohesion: 1.0
Nodes (0): 

### Community 817 - "Gitsettings"
Cohesion: 1.0
Nodes (0): 

### Community 818 - "Ghauthstatus"
Cohesion: 1.0
Nodes (0): 

### Community 819 - "Highlightmatch"
Cohesion: 1.0
Nodes (0): 

### Community 820 - "Registerfrontmatterhooks"
Cohesion: 1.0
Nodes (0): 

### Community 821 - "Registerskillhooks"
Cohesion: 1.0
Nodes (0): 

### Community 822 - "Horizontalscroll"
Cohesion: 1.0
Nodes (0): 

### Community 823 - "Hyperlink"
Cohesion: 1.0
Nodes (0): 

### Community 824 - "Idletimeout"
Cohesion: 1.0
Nodes (0): 

### Community 825 - "Immediatecommand"
Cohesion: 1.0
Nodes (0): 

### Community 826 - "Jsonread"
Cohesion: 1.0
Nodes (0): 

### Community 827 - "Keyboardshortcuts"
Cohesion: 1.0
Nodes (0): 

### Community 828 - "Lazyschema"
Cohesion: 1.0
Nodes (0): 

### Community 829 - "Managedenvconstants"
Cohesion: 1.0
Nodes (0): 

### Community 830 - "Versions"
Cohesion: 1.0
Nodes (0): 

### Community 831 - "Messagepredicates"
Cohesion: 1.0
Nodes (0): 

### Community 832 - "Objectgroupby"
Cohesion: 1.0
Nodes (0): 

### Community 833 - "Peeraddress"
Cohesion: 1.0
Nodes (0): 

### Community 834 - "Permissionprompttoolresultschema"
Cohesion: 1.0
Nodes (0): 

### Community 835 - "Permissionresult"
Cohesion: 1.0
Nodes (0): 

### Community 836 - "Classifierdecision"
Cohesion: 1.0
Nodes (0): 

### Community 837 - "Platform"
Cohesion: 1.0
Nodes (0): 

### Community 838 - "Headlessplugininstall"
Cohesion: 1.0
Nodes (0): 

### Community 839 - "Managedplugins"
Cohesion: 1.0
Nodes (0): 

### Community 840 - "Performstartupchecks"
Cohesion: 1.0
Nodes (0): 

### Community 841 - "Pluginpolicy"
Cohesion: 1.0
Nodes (0): 

### Community 842 - "Dangerouscmdlets"
Cohesion: 1.0
Nodes (0): 

### Community 843 - "Sandbox Ui Utils"
Cohesion: 1.0
Nodes (0): 

### Community 844 - "Fallbackstorage"
Cohesion: 1.0
Nodes (0): 

### Community 845 - "Semanticboolean"
Cohesion: 1.0
Nodes (0): 

### Community 846 - "Semanticnumber"
Cohesion: 1.0
Nodes (0): 

### Community 847 - "Sequential"
Cohesion: 1.0
Nodes (0): 

### Community 848 - "Allerrors"
Cohesion: 1.0
Nodes (0): 

### Community 849 - "Applysettingschange"
Cohesion: 1.0
Nodes (0): 

### Community 850 - "Schemaoutput"
Cohesion: 1.0
Nodes (0): 

### Community 851 - "Validateedittool"
Cohesion: 1.0
Nodes (0): 

### Community 852 - "Validationtips"
Cohesion: 1.0
Nodes (0): 

### Community 853 - "Outputlimits"
Cohesion: 1.0
Nodes (0): 

### Community 854 - "Resolvedefaultshell"
Cohesion: 1.0
Nodes (0): 

### Community 855 - "Shelltoolutils"
Cohesion: 1.0
Nodes (0): 

### Community 856 - "Signal"
Cohesion: 1.0
Nodes (0): 

### Community 857 - "Sinks"
Cohesion: 1.0
Nodes (0): 

### Community 858 - "Slashcommandparsing"
Cohesion: 1.0
Nodes (0): 

### Community 859 - "Standaloneagent"
Cohesion: 1.0
Nodes (0): 

### Community 860 - "Statusnoticehelpers"
Cohesion: 1.0
Nodes (0): 

### Community 861 - "Teammateinit"
Cohesion: 1.0
Nodes (0): 

### Community 862 - "Teammatemodel"
Cohesion: 1.0
Nodes (0): 

### Community 863 - "Systemprompttype"
Cohesion: 1.0
Nodes (0): 

### Community 864 - "Sdkprogress"
Cohesion: 1.0
Nodes (0): 

### Community 865 - "Teamdiscovery"
Cohesion: 1.0
Nodes (0): 

### Community 866 - "Skillloadedevent"
Cohesion: 1.0
Nodes (0): 

### Community 867 - "Environmentselection"
Cohesion: 1.0
Nodes (0): 

### Community 868 - "Unarylogging"
Cohesion: 1.0
Nodes (0): 

### Community 869 - "Useragent"
Cohesion: 1.0
Nodes (0): 

### Community 870 - "Withresolvers"
Cohesion: 1.0
Nodes (0): 

### Community 871 - "Worktreemodeenabled"
Cohesion: 1.0
Nodes (0): 

### Community 872 - "Yaml"
Cohesion: 1.0
Nodes (0): 

### Community 873 - "Zodtojsonschema"
Cohesion: 1.0
Nodes (0): 

### Community 874 - "Autoupdaterwrapper"
Cohesion: 1.0
Nodes (0): 

### Community 875 - "Awsauthstatusbox"
Cohesion: 1.0
Nodes (0): 

### Community 876 - "Basetextinput"
Cohesion: 1.0
Nodes (0): 

### Community 877 - "Channeldowngradedialog"
Cohesion: 1.0
Nodes (0): 

### Community 878 - "Pluginhintmenu"
Cohesion: 1.0
Nodes (0): 

### Community 879 - "Claudeinchromeonboarding"
Cohesion: 1.0
Nodes (0): 

### Community 880 - "Clickableimageref"
Cohesion: 1.0
Nodes (0): 

### Community 881 - "Compactsummary"
Cohesion: 1.0
Nodes (0): 

### Community 882 - "Configurableshortcuthint"
Cohesion: 1.0
Nodes (0): 

### Community 883 - "Costthresholddialog"
Cohesion: 1.0
Nodes (0): 

### Community 884 - "Select Option"
Cohesion: 1.0
Nodes (0): 

### Community 885 - "Use Select Input"
Cohesion: 1.0
Nodes (0): 

### Community 886 - "Use Select State"
Cohesion: 1.0
Nodes (0): 

### Community 887 - "Fallbacktooluseerrormessage"
Cohesion: 1.0
Nodes (0): 

### Community 888 - "Fallbacktooluserejectedmessage"
Cohesion: 1.0
Nodes (0): 

### Community 889 - "Submittranscriptshare"
Cohesion: 1.0
Nodes (0): 

### Community 890 - "Usedebounceddigitinput"
Cohesion: 1.0
Nodes (0): 

### Community 891 - "Usefeedbacksurvey"
Cohesion: 1.0
Nodes (0): 

### Community 892 - "Filepathlink"
Cohesion: 1.0
Nodes (0): 

### Community 893 - "General"
Cohesion: 1.0
Nodes (0): 

### Community 894 - "Helpv2"
Cohesion: 1.0
Nodes (0): 

### Community 895 - "Historysearchdialog"
Cohesion: 1.0
Nodes (0): 

### Community 896 - "Interruptedbyuser"
Cohesion: 1.0
Nodes (0): 

### Community 897 - "Invalidsettingsdialog"
Cohesion: 1.0
Nodes (0): 

### Community 898 - "Animatedasterisk"
Cohesion: 1.0
Nodes (0): 

### Community 899 - "Welcomev2"
Cohesion: 1.0
Nodes (0): 

### Community 900 - "Lsprecommendationmenu"
Cohesion: 1.0
Nodes (0): 

### Community 901 - "Mcpserverapprovaldialog"
Cohesion: 1.0
Nodes (0): 

### Community 902 - "Mcpserverdesktopimportdialog"
Cohesion: 1.0
Nodes (0): 

### Community 903 - "Mcpserverdialogcopy"
Cohesion: 1.0
Nodes (0): 

### Community 904 - "Memoryusageindicator"
Cohesion: 1.0
Nodes (0): 

### Community 905 - "Offscreenfreeze"
Cohesion: 1.0
Nodes (0): 

### Community 906 - "Outputstylepicker"
Cohesion: 1.0
Nodes (0): 

### Community 907 - "Packagemanagerautoupdater"
Cohesion: 1.0
Nodes (0): 

### Community 908 - "Pressentertocontinue"
Cohesion: 1.0
Nodes (0): 

### Community 909 - "Issueflagbanner"
Cohesion: 1.0
Nodes (0): 

### Community 910 - "Promptinputfooter"
Cohesion: 1.0
Nodes (0): 

### Community 911 - "Sandboxpromptfooterhint"
Cohesion: 1.0
Nodes (0): 

### Community 912 - "Usemaybetruncateinput"
Cohesion: 1.0
Nodes (0): 

### Community 913 - "Usepromptinputplaceholder"
Cohesion: 1.0
Nodes (0): 

### Community 914 - "Useshowfasticonhint"
Cohesion: 1.0
Nodes (0): 

### Community 915 - "Searchbox"
Cohesion: 1.0
Nodes (0): 

### Community 916 - "Flashingchar"
Cohesion: 1.0
Nodes (0): 

### Community 917 - "Glimmermessage"
Cohesion: 1.0
Nodes (0): 

### Community 918 - "Shimmerchar"
Cohesion: 1.0
Nodes (0): 

### Community 919 - "Spinnerglyph"
Cohesion: 1.0
Nodes (0): 

### Community 920 - "Useshimmeranimation"
Cohesion: 1.0
Nodes (0): 

### Community 921 - "Usestalledanimation"
Cohesion: 1.0
Nodes (0): 

### Community 922 - "Statusnotices"
Cohesion: 1.0
Nodes (0): 

### Community 923 - "Teleportresumewrapper"
Cohesion: 1.0
Nodes (0): 

### Community 924 - "Textinput"
Cohesion: 1.0
Nodes (0): 

### Community 925 - "Themepicker"
Cohesion: 1.0
Nodes (0): 

### Community 926 - "Tooluseloader"
Cohesion: 1.0
Nodes (0): 

### Community 927 - "Agentnavigationfooter"
Cohesion: 1.0
Nodes (0): 

### Community 928 - "Modelselector"
Cohesion: 1.0
Nodes (0): 

### Community 929 - "Generateagent"
Cohesion: 1.0
Nodes (0): 

### Community 930 - "Createagentwizard"
Cohesion: 1.0
Nodes (0): 

### Community 931 - "Colorstep"
Cohesion: 1.0
Nodes (0): 

### Community 932 - "Confirmstepwrapper"
Cohesion: 1.0
Nodes (0): 

### Community 933 - "Descriptionstep"
Cohesion: 1.0
Nodes (0): 

### Community 934 - "Generatestep"
Cohesion: 1.0
Nodes (0): 

### Community 935 - "Locationstep"
Cohesion: 1.0
Nodes (0): 

### Community 936 - "Memorystep"
Cohesion: 1.0
Nodes (0): 

### Community 937 - "Methodstep"
Cohesion: 1.0
Nodes (0): 

### Community 938 - "Modelstep"
Cohesion: 1.0
Nodes (0): 

### Community 939 - "Promptstep"
Cohesion: 1.0
Nodes (0): 

### Community 940 - "Toolsstep"
Cohesion: 1.0
Nodes (0): 

### Community 941 - "Typestep"
Cohesion: 1.0
Nodes (0): 

### Community 942 - "Divider"
Cohesion: 1.0
Nodes (0): 

### Community 943 - "Keyboardshortcuthint"
Cohesion: 1.0
Nodes (0): 

### Community 944 - "Loadingstate"
Cohesion: 1.0
Nodes (0): 

### Community 945 - "Pane"
Cohesion: 1.0
Nodes (0): 

### Community 946 - "Progressbar"
Cohesion: 1.0
Nodes (0): 

### Community 947 - "Ratchet"
Cohesion: 1.0
Nodes (0): 

### Community 948 - "Capabilitiessection"
Cohesion: 1.0
Nodes (0): 

### Community 949 - "Mcpparsingwarnings"
Cohesion: 1.0
Nodes (0): 

### Community 950 - "Assistantredactedthinkingmessage"
Cohesion: 1.0
Nodes (0): 

### Community 951 - "Assistanttextmessage"
Cohesion: 1.0
Nodes (0): 

### Community 952 - "Assistantthinkingmessage"
Cohesion: 1.0
Nodes (0): 

### Community 953 - "Compactboundarymessage"
Cohesion: 1.0
Nodes (0): 

### Community 954 - "Groupedtoolusecontent"
Cohesion: 1.0
Nodes (0): 

### Community 955 - "Hookprogressmessage"
Cohesion: 1.0
Nodes (0): 

### Community 956 - "Userbashinputmessage"
Cohesion: 1.0
Nodes (0): 

### Community 957 - "Userbashoutputmessage"
Cohesion: 1.0
Nodes (0): 

### Community 958 - "Userimagemessage"
Cohesion: 1.0
Nodes (0): 

### Community 959 - "Userplanmessage"
Cohesion: 1.0
Nodes (0): 

### Community 960 - "Userpromptmessage"
Cohesion: 1.0
Nodes (0): 

### Community 961 - "Rejectedplanmessage"
Cohesion: 1.0
Nodes (0): 

### Community 962 - "Rejectedtoolusemessage"
Cohesion: 1.0
Nodes (0): 

### Community 963 - "Usertoolcanceledmessage"
Cohesion: 1.0
Nodes (0): 

### Community 964 - "Usertoolerrormessage"
Cohesion: 1.0
Nodes (0): 

### Community 965 - "Usertoolrejectmessage"
Cohesion: 1.0
Nodes (0): 

### Community 966 - "Usertoolresultmessage"
Cohesion: 1.0
Nodes (0): 

### Community 967 - "Nullrenderingattachments"
Cohesion: 1.0
Nodes (0): 

### Community 968 - "Teammemsaved"
Cohesion: 1.0
Nodes (0): 

### Community 969 - "Idediffconfig"
Cohesion: 1.0
Nodes (0): 

### Community 970 - "Usefilepermissiondialog"
Cohesion: 1.0
Nodes (0): 

### Community 971 - "Filewritetooldiff"
Cohesion: 1.0
Nodes (0): 

### Community 972 - "Permissiondialog"
Cohesion: 1.0
Nodes (0): 

### Community 973 - "Permissionrequesttitle"
Cohesion: 1.0
Nodes (0): 

### Community 974 - "Permissionruleexplanation"
Cohesion: 1.0
Nodes (0): 

### Community 975 - "Powershelltooluseoptions"
Cohesion: 1.0
Nodes (0): 

### Community 976 - "Sandboxpermissionrequest"
Cohesion: 1.0
Nodes (0): 

### Community 977 - "Workerbadge"
Cohesion: 1.0
Nodes (0): 

### Community 978 - "Workerpendingpermission"
Cohesion: 1.0
Nodes (0): 

### Community 979 - "Permissionruledescription"
Cohesion: 1.0
Nodes (0): 

### Community 980 - "Removeworkspacedirectory"
Cohesion: 1.0
Nodes (0): 

### Community 981 - "Useshellpermissionfeedback"
Cohesion: 1.0
Nodes (0): 

### Community 982 - "Sandboxdoctorsection"
Cohesion: 1.0
Nodes (0): 

### Community 983 - "Sandboxsettings"
Cohesion: 1.0
Nodes (0): 

### Community 984 - "Shelltimedisplay"
Cohesion: 1.0
Nodes (0): 

### Community 985 - "Asyncagentdetaildialog"
Cohesion: 1.0
Nodes (0): 

### Community 986 - "Backgroundtask"
Cohesion: 1.0
Nodes (0): 

### Community 987 - "Inprocessteammatedetaildialog"
Cohesion: 1.0
Nodes (0): 

### Community 988 - "Rendertoolactivity"
Cohesion: 1.0
Nodes (0): 

### Community 989 - "Orderedlist"
Cohesion: 1.0
Nodes (0): 

### Community 990 - "Orderedlistitem"
Cohesion: 1.0
Nodes (0): 

### Community 991 - "Wizarddialoglayout"
Cohesion: 1.0
Nodes (0): 

### Community 992 - "Wizardnavigationfooter"
Cohesion: 1.0
Nodes (0): 

### Community 993 - "Usewizard"
Cohesion: 1.0
Nodes (0): 

### Community 994 - "Bridge Kick"
Cohesion: 1.0
Nodes (0): 

### Community 995 - "Brief"
Cohesion: 1.0
Nodes (0): 

### Community 996 - "Caches"
Cohesion: 1.0
Nodes (0): 

### Community 997 - "Clear"
Cohesion: 1.0
Nodes (0): 

### Community 998 - "Commit Push Pr"
Cohesion: 1.0
Nodes (0): 

### Community 999 - "Commit"
Cohesion: 1.0
Nodes (0): 

### Community 1000 - "Cost"
Cohesion: 1.0
Nodes (0): 

### Community 1001 - "Createmovedtoplugincommand"
Cohesion: 1.0
Nodes (0): 

### Community 1002 - "Desktop"
Cohesion: 1.0
Nodes (0): 

### Community 1003 - "Doctor"
Cohesion: 1.0
Nodes (0): 

### Community 1004 - "Extra Usage Core"
Cohesion: 1.0
Nodes (0): 

### Community 1005 - "Extra Usage Noninteractive"
Cohesion: 1.0
Nodes (0): 

### Community 1006 - "Extra Usage"
Cohesion: 1.0
Nodes (0): 

### Community 1007 - "Heapdump"
Cohesion: 1.0
Nodes (0): 

### Community 1008 - "Apikeystep"
Cohesion: 1.0
Nodes (0): 

### Community 1009 - "Checkexistingsecretstep"
Cohesion: 1.0
Nodes (0): 

### Community 1010 - "Checkgithubstep"
Cohesion: 1.0
Nodes (0): 

### Community 1011 - "Chooserepostep"
Cohesion: 1.0
Nodes (0): 

### Community 1012 - "Existingworkflowstep"
Cohesion: 1.0
Nodes (0): 

### Community 1013 - "Oauthflowstep"
Cohesion: 1.0
Nodes (0): 

### Community 1014 - "Install Github App"
Cohesion: 1.0
Nodes (0): 

### Community 1015 - "Install Slack App"
Cohesion: 1.0
Nodes (0): 

### Community 1016 - "Addcommand"
Cohesion: 1.0
Nodes (0): 

### Community 1017 - "Xaaidpcommand"
Cohesion: 1.0
Nodes (0): 

### Community 1018 - "Memory"
Cohesion: 1.0
Nodes (0): 

### Community 1019 - "Output Style"
Cohesion: 1.0
Nodes (0): 

### Community 1020 - "Addmarketplace"
Cohesion: 1.0
Nodes (0): 

### Community 1021 - "Parseargs"
Cohesion: 1.0
Nodes (0): 

### Community 1022 - "Usepagination"
Cohesion: 1.0
Nodes (0): 

### Community 1023 - "Privacy Settings"
Cohesion: 1.0
Nodes (0): 

### Community 1024 - "Remote Env"
Cohesion: 1.0
Nodes (0): 

### Community 1025 - "Generatesessionname"
Cohesion: 1.0
Nodes (0): 

### Community 1026 - "Ultrareviewenabled"
Cohesion: 1.0
Nodes (0): 

### Community 1027 - "Review"
Cohesion: 1.0
Nodes (0): 

### Community 1028 - "Rewind"
Cohesion: 1.0
Nodes (0): 

### Community 1029 - "Security Review"
Cohesion: 1.0
Nodes (0): 

### Community 1030 - "Skills"
Cohesion: 1.0
Nodes (0): 

### Community 1031 - "Stickers"
Cohesion: 1.0
Nodes (0): 

### Community 1032 - "Upgrade"
Cohesion: 1.0
Nodes (0): 

### Community 1033 - "Version"
Cohesion: 1.0
Nodes (0): 

### Community 1034 - "Vim"
Cohesion: 1.0
Nodes (0): 

### Community 1035 - "Exploreagent"
Cohesion: 1.0
Nodes (0): 

### Community 1036 - "Generalpurposeagent"
Cohesion: 1.0
Nodes (0): 

### Community 1037 - "Planagent"
Cohesion: 1.0
Nodes (0): 

### Community 1038 - "Resumeagent"
Cohesion: 1.0
Nodes (0): 

### Community 1039 - "Commentlabel"
Cohesion: 1.0
Nodes (0): 

### Community 1040 - "Destructivecommandwarning"
Cohesion: 1.0
Nodes (0): 

### Community 1041 - "Limits"
Cohesion: 1.0
Nodes (0): 

### Community 1042 - "Symbolcontext"
Cohesion: 1.0
Nodes (0): 

### Community 1043 - "Primitivetools"
Cohesion: 1.0
Nodes (0): 

### Community 1044 - "Teamcreatetool"
Cohesion: 1.0
Nodes (0): 

### Community 1045 - "Preapproved"
Cohesion: 1.0
Nodes (0): 

### Community 1046 - "Sinkkillswitch"
Cohesion: 1.0
Nodes (0): 

### Community 1047 - "Firsttokendate"
Cohesion: 1.0
Nodes (0): 

### Community 1048 - "Ultrareviewquota"
Cohesion: 1.0
Nodes (0): 

### Community 1049 - "Consolidationprompt"
Cohesion: 1.0
Nodes (0): 

### Community 1050 - "Claudeailimitshook"
Cohesion: 1.0
Nodes (0): 

### Community 1051 - "Apimicrocompact"
Cohesion: 1.0
Nodes (0): 

### Community 1052 - "Compactwarninghook"
Cohesion: 1.0
Nodes (0): 

### Community 1053 - "Grouping"
Cohesion: 1.0
Nodes (0): 

### Community 1054 - "Postcompactcleanup"
Cohesion: 1.0
Nodes (0): 

### Community 1055 - "Timebasedmcconfig"
Cohesion: 1.0
Nodes (0): 

### Community 1056 - "Internallogging"
Cohesion: 1.0
Nodes (0): 

### Community 1057 - "Lspclient"
Cohesion: 1.0
Nodes (0): 

### Community 1058 - "Envexpansion"
Cohesion: 1.0
Nodes (0): 

### Community 1059 - "Normalization"
Cohesion: 1.0
Nodes (0): 

### Community 1060 - "Mcpserverapproval"
Cohesion: 1.0
Nodes (0): 

### Community 1061 - "Teammemsecretguard"
Cohesion: 1.0
Nodes (0): 

### Community 1062 - "Toolhooks"
Cohesion: 1.0
Nodes (0): 

### Community 1063 - "Useautomodeunavailablenotification"
Cohesion: 1.0
Nodes (0): 

### Community 1064 - "Usedeprecationwarningnotification"
Cohesion: 1.0
Nodes (0): 

### Community 1065 - "Useratelimitwarningnotification"
Cohesion: 1.0
Nodes (0): 

### Community 1066 - "Usestartupnotification"
Cohesion: 1.0
Nodes (0): 

### Community 1067 - "Renderplaceholder"
Cohesion: 1.0
Nodes (0): 

### Community 1068 - "Coordinatorhandler"
Cohesion: 1.0
Nodes (0): 

### Community 1069 - "Swarmworkerhandler"
Cohesion: 1.0
Nodes (0): 

### Community 1070 - "Useafterfirstrender"
Cohesion: 1.0
Nodes (0): 

### Community 1071 - "Useapikeyverification"
Cohesion: 1.0
Nodes (0): 

### Community 1072 - "Useblink"
Cohesion: 1.0
Nodes (0): 

### Community 1073 - "Usecancelrequest"
Cohesion: 1.0
Nodes (0): 

### Community 1074 - "Useclaudecodehintrecommendation"
Cohesion: 1.0
Nodes (0): 

### Community 1075 - "Useclipboardimagehint"
Cohesion: 1.0
Nodes (0): 

### Community 1076 - "Usecommandkeybindings"
Cohesion: 1.0
Nodes (0): 

### Community 1077 - "Usecommandqueue"
Cohesion: 1.0
Nodes (0): 

### Community 1078 - "Usedeferredhookmessages"
Cohesion: 1.0
Nodes (0): 

### Community 1079 - "Usedirectconnect"
Cohesion: 1.0
Nodes (0): 

### Community 1080 - "Usedoublepress"
Cohesion: 1.0
Nodes (0): 

### Community 1081 - "Usedynamicconfig"
Cohesion: 1.0
Nodes (0): 

### Community 1082 - "Useelapsedtime"
Cohesion: 1.0
Nodes (0): 

### Community 1083 - "Useexitonctrlcd"
Cohesion: 1.0
Nodes (0): 

### Community 1084 - "Useexitonctrlcdwithkeybindings"
Cohesion: 1.0
Nodes (0): 

### Community 1085 - "Usefilehistorysnapshotinit"
Cohesion: 1.0
Nodes (0): 

### Community 1086 - "Useglobalkeybindings"
Cohesion: 1.0
Nodes (0): 

### Community 1087 - "Usehistorysearch"
Cohesion: 1.0
Nodes (0): 

### Community 1088 - "Useideintegration"
Cohesion: 1.0
Nodes (0): 

### Community 1089 - "Useideatmentioned"
Cohesion: 1.0
Nodes (0): 

### Community 1090 - "Useideconnectionstatus"
Cohesion: 1.0
Nodes (0): 

### Community 1091 - "Useidelogging"
Cohesion: 1.0
Nodes (0): 

### Community 1092 - "Useideselection"
Cohesion: 1.0
Nodes (0): 

### Community 1093 - "Useinputbuffer"
Cohesion: 1.0
Nodes (0): 

### Community 1094 - "Usemailboxbridge"
Cohesion: 1.0
Nodes (0): 

### Community 1095 - "Usemainloopmodel"
Cohesion: 1.0
Nodes (0): 

### Community 1096 - "Usemanageplugins"
Cohesion: 1.0
Nodes (0): 

### Community 1097 - "Usememoryusage"
Cohesion: 1.0
Nodes (0): 

### Community 1098 - "Usemergedcommands"
Cohesion: 1.0
Nodes (0): 

### Community 1099 - "Usemergedtools"
Cohesion: 1.0
Nodes (0): 

### Community 1100 - "Usemindisplaytime"
Cohesion: 1.0
Nodes (0): 

### Community 1101 - "Useprstatus"
Cohesion: 1.0
Nodes (0): 

### Community 1102 - "Usepromptsuggestion"
Cohesion: 1.0
Nodes (0): 

### Community 1103 - "Usequeueprocessor"
Cohesion: 1.0
Nodes (0): 

### Community 1104 - "Useremotesession"
Cohesion: 1.0
Nodes (0): 

### Community 1105 - "Usereplbridge"
Cohesion: 1.0
Nodes (0): 

### Community 1106 - "Usesessionbackgrounding"
Cohesion: 1.0
Nodes (0): 

### Community 1107 - "Usesettings"
Cohesion: 1.0
Nodes (0): 

### Community 1108 - "Usesettingschange"
Cohesion: 1.0
Nodes (0): 

### Community 1109 - "Useskillimprovementsurvey"
Cohesion: 1.0
Nodes (0): 

### Community 1110 - "Useskillschange"
Cohesion: 1.0
Nodes (0): 

### Community 1111 - "Useswarminitialization"
Cohesion: 1.0
Nodes (0): 

### Community 1112 - "Useteammateviewautoexit"
Cohesion: 1.0
Nodes (0): 

### Community 1113 - "Useteleportresume"
Cohesion: 1.0
Nodes (0): 

### Community 1114 - "Useterminalsize"
Cohesion: 1.0
Nodes (0): 

### Community 1115 - "Usetimeout"
Cohesion: 1.0
Nodes (0): 

### Community 1116 - "Useviminput"
Cohesion: 1.0
Nodes (0): 

### Community 1117 - "Usevoiceenabled"
Cohesion: 1.0
Nodes (0): 

### Community 1118 - "Alternatescreen"
Cohesion: 1.0
Nodes (0): 

### Community 1119 - "Box"
Cohesion: 1.0
Nodes (0): 

### Community 1120 - "Link"
Cohesion: 1.0
Nodes (0): 

### Community 1121 - "Newline"
Cohesion: 1.0
Nodes (0): 

### Community 1122 - "Noselect"
Cohesion: 1.0
Nodes (0): 

### Community 1123 - "Rawansi"
Cohesion: 1.0
Nodes (0): 

### Community 1124 - "Scrollbox"
Cohesion: 1.0
Nodes (0): 

### Community 1125 - "Spacer"
Cohesion: 1.0
Nodes (0): 

### Community 1126 - "Terminalfocuscontext"
Cohesion: 1.0
Nodes (0): 

### Community 1127 - "Text"
Cohesion: 1.0
Nodes (0): 

### Community 1128 - "Get Max Width"
Cohesion: 1.0
Nodes (0): 

### Community 1129 - "Use Animation Frame"
Cohesion: 1.0
Nodes (0): 

### Community 1130 - "Use App"
Cohesion: 1.0
Nodes (0): 

### Community 1131 - "Use Declared Cursor"
Cohesion: 1.0
Nodes (0): 

### Community 1132 - "Use Input"
Cohesion: 1.0
Nodes (0): 

### Community 1133 - "Use Search Highlight"
Cohesion: 1.0
Nodes (0): 

### Community 1134 - "Use Stdin"
Cohesion: 1.0
Nodes (0): 

### Community 1135 - "Use Terminal Focus"
Cohesion: 1.0
Nodes (0): 

### Community 1136 - "Use Terminal Title"
Cohesion: 1.0
Nodes (0): 

### Community 1137 - "Use Terminal Viewport"
Cohesion: 1.0
Nodes (0): 

### Community 1138 - "Engine"
Cohesion: 1.0
Nodes (0): 

### Community 1139 - "Line Width Cache"
Cohesion: 1.0
Nodes (0): 

### Community 1140 - "Measure Element"
Cohesion: 1.0
Nodes (0): 

### Community 1141 - "Measure Text"
Cohesion: 1.0
Nodes (0): 

### Community 1142 - "Optimizer"
Cohesion: 1.0
Nodes (0): 

### Community 1143 - "Renderer"
Cohesion: 1.0
Nodes (0): 

### Community 1144 - "Searchhighlight"
Cohesion: 1.0
Nodes (0): 

### Community 1145 - "Supports Hyperlinks"
Cohesion: 2.0
Nodes (0): 

### Community 1146 - "Tabstops"
Cohesion: 1.0
Nodes (0): 

### Community 1147 - "Esc"
Cohesion: 1.0
Nodes (0): 

### Community 1148 - "Useterminalnotification"
Cohesion: 1.0
Nodes (0): 

### Community 1149 - "Warn"
Cohesion: 1.0
Nodes (0): 

### Community 1150 - "Widest Line"
Cohesion: 1.0
Nodes (0): 

### Community 1151 - "Schema"
Cohesion: 1.0
Nodes (0): 

### Community 1152 - "Cors"
Cohesion: 1.0
Nodes (0): 

### Community 1153 - "Request Id"
Cohesion: 1.0
Nodes (0): 

### Community 1154 - "Exec"
Cohesion: 1.0
Nodes (0): 

### Community 1155 - "Search"
Cohesion: 1.0
Nodes (0): 

### Community 1156 - "Seed"
Cohesion: 1.0
Nodes (0): 

### Community 1157 - "Auth Test"
Cohesion: 1.0
Nodes (0): 

### Community 1158 - "Bridgepermissioncallbacks"
Cohesion: 1.0
Nodes (0): 

### Community 1159 - "Capacitywake"
Cohesion: 1.0
Nodes (0): 

### Community 1160 - "Pollconfig"
Cohesion: 1.0
Nodes (0): 

### Community 1161 - "Stub"
Cohesion: 1.0
Nodes (0): 

### Community 1162 - "Keys"
Cohesion: 1.0
Nodes (0): 

### Community 1163 - "Spinnerverbs"
Cohesion: 1.0
Nodes (0): 

### Community 1164 - "Claudeinchrome"
Cohesion: 1.0
Nodes (0): 

### Community 1165 - "Remember"
Cohesion: 1.0
Nodes (0): 

### Community 1166 - "Simplify"
Cohesion: 1.0
Nodes (0): 

### Community 1167 - "Stuck"
Cohesion: 1.0
Nodes (0): 

### Community 1168 - "Verify"
Cohesion: 1.0
Nodes (0): 

### Community 1169 - "Transportutils"
Cohesion: 1.0
Nodes (0): 

### Community 1170 - "Update"
Cohesion: 1.0
Nodes (0): 

### Community 1171 - "Connectortext"
Cohesion: 1.0
Nodes (0): 

### Community 1172 - "Shortcutformat"
Cohesion: 1.0
Nodes (0): 

### Community 1173 - "Useshortcutdisplay"
Cohesion: 1.0
Nodes (0): 

### Community 1174 - "Guards"
Cohesion: 1.0
Nodes (0): 

### Community 1175 - "Migrateautoupdatestosettings"
Cohesion: 1.0
Nodes (0): 

### Community 1176 - "Migratebypasspermissionsacceptedtosettings"
Cohesion: 1.0
Nodes (0): 

### Community 1177 - "Migrateenableallprojectmcpserverstosettings"
Cohesion: 1.0
Nodes (0): 

### Community 1178 - "Migratefennectoopus"
Cohesion: 1.0
Nodes (0): 

### Community 1179 - "Migratelegacyopustocurrent"
Cohesion: 1.0
Nodes (0): 

### Community 1180 - "Migrateopustoopus1M"
Cohesion: 1.0
Nodes (0): 

### Community 1181 - "Migratereplbridgeenabledtoremotecontrolatstartup"
Cohesion: 1.0
Nodes (0): 

### Community 1182 - "Migratesonnet1Mtosonnet45"
Cohesion: 1.0
Nodes (0): 

### Community 1183 - "Migratesonnet45Tosonnet46"
Cohesion: 1.0
Nodes (0): 

### Community 1184 - "Resetautomodeoptinfordefaultoffer"
Cohesion: 1.0
Nodes (0): 

### Community 1185 - "Resetprotoopusdefault"
Cohesion: 1.0
Nodes (0): 

### Community 1186 - "Cli"
Cohesion: 1.0
Nodes (0): 

### Community 1187 - "Memorytypes"
Cohesion: 1.0
Nodes (0): 

### Community 1188 - "Teammemprompts"
Cohesion: 1.0
Nodes (0): 

### Community 1189 - "Alias"
Cohesion: 1.0
Nodes (0): 

### Community 1190 - "Nohup"
Cohesion: 1.0
Nodes (0): 

### Community 1191 - "Pyright"
Cohesion: 1.0
Nodes (0): 

### Community 1192 - "Srun"
Cohesion: 1.0
Nodes (0): 

### Community 1193 - "Time"
Cohesion: 1.0
Nodes (0): 

### Community 1194 - "Timeout"
Cohesion: 1.0
Nodes (0): 

### Community 1195 - "Configconstants"
Cohesion: 1.0
Nodes (0): 

### Community 1196 - "Configs"
Cohesion: 1.0
Nodes (0): 

### Community 1197 - "Modelsupportoverrides"
Cohesion: 1.0
Nodes (0): 

### Community 1198 - "Permissionrule"
Cohesion: 1.0
Nodes (0): 

### Community 1199 - "Permissionupdateschema"
Cohesion: 1.0
Nodes (0): 

### Community 1200 - "Dangerouspatterns"
Cohesion: 1.0
Nodes (0): 

### Community 1201 - "Officialmarketplace"
Cohesion: 1.0
Nodes (0): 

### Community 1202 - "Shellprovider"
Cohesion: 1.0
Nodes (0): 

### Community 1203 - "Teammatepromptaddendum"
Cohesion: 1.0
Nodes (0): 

### Community 1204 - "Agentprogressline"
Cohesion: 1.0
Nodes (0): 

### Community 1205 - "Approveapikey"
Cohesion: 1.0
Nodes (0): 

### Community 1206 - "Automodeoptindialog"
Cohesion: 1.0
Nodes (0): 

### Community 1207 - "Bashmodeprogress"
Cohesion: 1.0
Nodes (0): 

### Community 1208 - "Select Input Option"
Cohesion: 1.0
Nodes (0): 

### Community 1209 - "Effortcallout"
Cohesion: 1.0
Nodes (0): 

### Community 1210 - "Highlightedcode"
Cohesion: 1.0
Nodes (0): 

### Community 1211 - "Modelpicker"
Cohesion: 1.0
Nodes (0): 

### Community 1212 - "Historysearchinput"
Cohesion: 1.0
Nodes (0): 

### Community 1213 - "Shimmeredinput"
Cohesion: 1.0
Nodes (0): 

### Community 1214 - "Skillimprovementsurvey"
Cohesion: 1.0
Nodes (0): 

### Community 1215 - "Teammateselecthint"
Cohesion: 1.0
Nodes (0): 

### Community 1216 - "Teleporterror"
Cohesion: 1.0
Nodes (0): 

### Community 1217 - "Thinkingtoggle"
Cohesion: 1.0
Nodes (0): 

### Community 1218 - "Trustdialog"
Cohesion: 1.0
Nodes (0): 

### Community 1219 - "Dialog"
Cohesion: 1.0
Nodes (0): 

### Community 1220 - "Promptdialog"
Cohesion: 1.0
Nodes (0): 

### Community 1221 - "Mcptoollistview"
Cohesion: 1.0
Nodes (0): 

### Community 1222 - "Userlocalcommandoutputmessage"
Cohesion: 1.0
Nodes (0): 

### Community 1223 - "Fallbackpermissionrequest"
Cohesion: 1.0
Nodes (0): 

### Community 1224 - "Permissionexplanation"
Cohesion: 1.0
Nodes (0): 

### Community 1225 - "Shellprogressmessage"
Cohesion: 1.0
Nodes (0): 

### Community 1226 - "Dreamdetaildialog"
Cohesion: 1.0
Nodes (0): 

### Community 1227 - "Help"
Cohesion: 1.0
Nodes (0): 

### Community 1228 - "Init Verifiers"
Cohesion: 1.0
Nodes (0): 

### Community 1229 - "Creatingstep"
Cohesion: 1.0
Nodes (0): 

### Community 1230 - "Errorstep"
Cohesion: 1.0
Nodes (0): 

### Community 1231 - "Successstep"
Cohesion: 1.0
Nodes (0): 

### Community 1232 - "Login"
Cohesion: 1.0
Nodes (0): 

### Community 1233 - "Ultrareviewoveragedialog"
Cohesion: 1.0
Nodes (0): 

### Community 1234 - "Statuslinesetup"
Cohesion: 1.0
Nodes (0): 

### Community 1235 - "Verificationagent"
Cohesion: 1.0
Nodes (0): 

### Community 1236 - "Toolname"
Cohesion: 1.0
Nodes (0): 

### Community 1237 - "Enterplanmodetool"
Cohesion: 1.0
Nodes (0): 

### Community 1238 - "Enterworktreetool"
Cohesion: 1.0
Nodes (0): 

### Community 1239 - "Exitplanmodev2Tool"
Cohesion: 1.0
Nodes (0): 

### Community 1240 - "Globtool"
Cohesion: 1.0
Nodes (0): 

### Community 1241 - "Listmcpresourcestool"
Cohesion: 1.0
Nodes (0): 

### Community 1242 - "Mcptool"
Cohesion: 1.0
Nodes (0): 

### Community 1243 - "Commonparameters"
Cohesion: 1.0
Nodes (0): 

### Community 1244 - "Readmcpresourcetool"
Cohesion: 1.0
Nodes (0): 

### Community 1245 - "Remotetriggertool"
Cohesion: 1.0
Nodes (0): 

### Community 1246 - "Croncreatetool"
Cohesion: 1.0
Nodes (0): 

### Community 1247 - "Crondeletetool"
Cohesion: 1.0
Nodes (0): 

### Community 1248 - "Cronlisttool"
Cohesion: 1.0
Nodes (0): 

### Community 1249 - "Taskcreatetool"
Cohesion: 1.0
Nodes (0): 

### Community 1250 - "Taskgettool"
Cohesion: 1.0
Nodes (0): 

### Community 1251 - "Tasklisttool"
Cohesion: 1.0
Nodes (0): 

### Community 1252 - "Taskstoptool"
Cohesion: 1.0
Nodes (0): 

### Community 1253 - "Taskupdatetool"
Cohesion: 1.0
Nodes (0): 

### Community 1254 - "Teamdeletetool"
Cohesion: 1.0
Nodes (0): 

### Community 1255 - "Todowritetool"
Cohesion: 1.0
Nodes (0): 

### Community 1256 - "Testingpermissiontool"
Cohesion: 1.0
Nodes (0): 

### Community 1257 - "Emptyusage"
Cohesion: 1.0
Nodes (0): 

### Community 1258 - "Securitycheck"
Cohesion: 1.0
Nodes (0): 

### Community 1259 - "Appcontext"
Cohesion: 1.0
Nodes (0): 

### Community 1260 - "Cursordeclarationcontext"
Cohesion: 1.0
Nodes (0): 

### Community 1261 - "Stdincontext"
Cohesion: 1.0
Nodes (0): 

### Community 1262 - "Terminalsizecontext"
Cohesion: 1.0
Nodes (0): 

### Community 1263 - "Event Handlers"
Cohesion: 1.0
Nodes (0): 

### Community 1264 - "Global D"
Cohesion: 1.0
Nodes (0): 

### Community 1265 - "Instances"
Cohesion: 1.0
Nodes (0): 

### Community 1266 - "Termio"
Cohesion: 1.0
Nodes (0): 

### Community 1267 - "Wrapansi"
Cohesion: 1.0
Nodes (0): 

### Community 1268 - "Api Key"
Cohesion: 1.0
Nodes (0): 

### Community 1269 - "Sqlite"
Cohesion: 1.0
Nodes (0): 

### Community 1270 - "Pollconfigdefaults"
Cohesion: 1.0
Nodes (0): 

### Community 1271 - "Apilimits"
Cohesion: 1.0
Nodes (0): 

### Community 1272 - "Cyberriskinstruction"
Cohesion: 1.0
Nodes (0): 

### Community 1273 - "Errorids"
Cohesion: 1.0
Nodes (0): 

### Community 1274 - "Github App"
Cohesion: 1.0
Nodes (0): 

### Community 1275 - "Querysource"
Cohesion: 1.0
Nodes (0): 

### Community 1276 - "Toollimits"
Cohesion: 1.0
Nodes (0): 

### Community 1277 - "Tools"
Cohesion: 1.0
Nodes (0): 

### Community 1278 - "Turncompletionverbs"
Cohesion: 1.0
Nodes (0): 

### Community 1279 - "Claudeapicontent"
Cohesion: 1.0
Nodes (0): 

### Community 1280 - "Verifycontent"
Cohesion: 1.0
Nodes (0): 

### Community 1281 - "Bun Bundle D"
Cohesion: 1.0
Nodes (0): 

### Community 1282 - "Bun Globals D"
Cohesion: 1.0
Nodes (0): 

### Community 1283 - "Macro D"
Cohesion: 1.0
Nodes (0): 

### Community 1284 - "Defaultbindings"
Cohesion: 1.0
Nodes (0): 

### Community 1285 - "Sandboxtypes"
Cohesion: 1.0
Nodes (0): 

### Community 1286 - "Controlschemas"
Cohesion: 1.0
Nodes (0): 

### Community 1287 - "Coreschemas"
Cohesion: 1.0
Nodes (0): 

### Community 1288 - "Coretypes Generated"
Cohesion: 1.0
Nodes (0): 

### Community 1289 - "Coretypes"
Cohesion: 1.0
Nodes (0): 

### Community 1290 - "Runtimetypes"
Cohesion: 1.0
Nodes (0): 

### Community 1291 - "Tooltypes"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **8 isolated node(s):** `GcpCredentialsTimeoutError`, `AutoUpdaterError`, `MalformedCommandError`, `TelemetryTimeoutError`, `DiagnosticsTrackingError` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Apipreconnect`** (2 nodes): `apiPreconnect.ts`, `preconnectAnthropicApi()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Remotesession`** (2 nodes): `remoteSession.ts`, `checkBackgroundRemoteSessionEligibility()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backgroundhousekeeping`** (2 nodes): `backgroundHousekeeping.ts`, `startBackgroundHousekeeping()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shellprefix`** (2 nodes): `shellPrefix.ts`, `formatShellPrefixCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bufferedwriter`** (2 nodes): `bufferedWriter.ts`, `createBufferedWriter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cacerts`** (2 nodes): `caCerts.ts`, `clearCACertsCache()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Classifierapprovalshook`** (2 nodes): `classifierApprovalsHook.ts`, `useIsClassifierChecking()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Combinedabortsignal`** (2 nodes): `combinedAbortSignal.ts`, `createCombinedAbortSignal()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Inputloader`** (2 nodes): `inputLoader.ts`, `requireComputerUseInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Swiftloader`** (2 nodes): `swiftLoader.ts`, `requireComputerUseSwift()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Contentarray`** (2 nodes): `contentArray.ts`, `insertBlockAfterToolResults()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Controlmessagecompat`** (2 nodes): `controlMessageCompat.ts`, `normalizeControlMessageKeys()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cronjitterconfig`** (2 nodes): `cronJitterConfig.ts`, `getCronJitterConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Terminalpreference`** (2 nodes): `terminalPreference.ts`, `updateDeepLinkTerminalPreference()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Envvalidation`** (2 nodes): `envValidation.ts`, `validateBoundedIntEnvVar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Execfilenothrowportable`** (2 nodes): `execFileNoThrowPortable.ts`, `execSyncWithDefaults_DEPRECATED()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Execsyncwrapper`** (2 nodes): `execSyncWrapper.ts`, `execSync_DEPRECATED()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extrausage`** (2 nodes): `extraUsage.ts`, `isBilledAsExtraUsage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Findexecutable`** (2 nodes): `findExecutable.ts`, `findExecutable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gitsettings`** (2 nodes): `gitSettings.ts`, `shouldIncludeGitInstructions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ghauthstatus`** (2 nodes): `ghAuthStatus.ts`, `getGhAuthStatus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Highlightmatch`** (2 nodes): `highlightMatch.tsx`, `highlightMatch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Registerfrontmatterhooks`** (2 nodes): `registerFrontmatterHooks.ts`, `registerFrontmatterHooks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Registerskillhooks`** (2 nodes): `registerSkillHooks.ts`, `registerSkillHooks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Horizontalscroll`** (2 nodes): `horizontalScroll.ts`, `calculateHorizontalScrollWindow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hyperlink`** (2 nodes): `hyperlink.ts`, `createHyperlink()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Idletimeout`** (2 nodes): `idleTimeout.ts`, `createIdleTimeoutManager()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Immediatecommand`** (2 nodes): `immediateCommand.ts`, `shouldInferenceConfigCommandBeImmediate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Jsonread`** (2 nodes): `jsonRead.ts`, `stripBOM()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Keyboardshortcuts`** (2 nodes): `keyboardShortcuts.ts`, `isMacosOptionChar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Lazyschema`** (2 nodes): `lazySchema.ts`, `lazySchema()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Managedenvconstants`** (2 nodes): `managedEnvConstants.ts`, `isProviderManagedEnvVar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Versions`** (2 nodes): `versions.ts`, `projectIsInGitRepo()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Messagepredicates`** (2 nodes): `messagePredicates.ts`, `isHumanTurn()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Objectgroupby`** (2 nodes): `objectGroupBy.ts`, `objectGroupBy()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Peeraddress`** (2 nodes): `peerAddress.ts`, `parseAddress()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionprompttoolresultschema`** (2 nodes): `PermissionPromptToolResultSchema.ts`, `permissionPromptToolResultToPermissionDecision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionresult`** (2 nodes): `PermissionResult.ts`, `getRuleBehaviorDescription()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Classifierdecision`** (2 nodes): `classifierDecision.ts`, `isAutoModeAllowlistedTool()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Platform`** (2 nodes): `platform.ts`, `detectVcs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Headlessplugininstall`** (2 nodes): `headlessPluginInstall.ts`, `installPluginsForHeadless()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Managedplugins`** (2 nodes): `managedPlugins.ts`, `getManagedPluginNames()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Performstartupchecks`** (2 nodes): `performStartupChecks.tsx`, `performStartupChecks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pluginpolicy`** (2 nodes): `pluginPolicy.ts`, `isPluginBlockedByPolicy()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dangerouscmdlets`** (2 nodes): `dangerousCmdlets.ts`, `aliasesOf()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sandbox Ui Utils`** (2 nodes): `sandbox-ui-utils.ts`, `removeSandboxViolationTags()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fallbackstorage`** (2 nodes): `fallbackStorage.ts`, `createFallbackStorage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Semanticboolean`** (2 nodes): `semanticBoolean.ts`, `semanticBoolean()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Semanticnumber`** (2 nodes): `semanticNumber.ts`, `semanticNumber()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sequential`** (2 nodes): `sequential.ts`, `sequential()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Allerrors`** (2 nodes): `allErrors.ts`, `getSettingsWithAllErrors()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Applysettingschange`** (2 nodes): `applySettingsChange.ts`, `applySettingsChange()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Schemaoutput`** (2 nodes): `schemaOutput.ts`, `generateSettingsJSONSchema()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Validateedittool`** (2 nodes): `validateEditTool.ts`, `validateInputForSettingsFileEdit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Validationtips`** (2 nodes): `validationTips.ts`, `getValidationTip()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Outputlimits`** (2 nodes): `outputLimits.ts`, `getMaxOutputLength()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resolvedefaultshell`** (2 nodes): `resolveDefaultShell.ts`, `resolveDefaultShell()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shelltoolutils`** (2 nodes): `shellToolUtils.ts`, `isPowerShellToolEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Signal`** (2 nodes): `signal.ts`, `createSignal()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sinks`** (2 nodes): `sinks.ts`, `initSinks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Slashcommandparsing`** (2 nodes): `slashCommandParsing.ts`, `parseSlashCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Standaloneagent`** (2 nodes): `standaloneAgent.ts`, `getStandaloneAgentName()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Statusnoticehelpers`** (2 nodes): `statusNoticeHelpers.ts`, `getAgentDescriptionsTotalTokens()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammateinit`** (2 nodes): `teammateInit.ts`, `initializeTeammateHooks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammatemodel`** (2 nodes): `teammateModel.ts`, `getHardcodedTeammateModelFallback()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Systemprompttype`** (2 nodes): `systemPromptType.ts`, `asSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sdkprogress`** (2 nodes): `sdkProgress.ts`, `emitTaskProgress()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teamdiscovery`** (2 nodes): `teamDiscovery.ts`, `getTeammateStatuses()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Skillloadedevent`** (2 nodes): `skillLoadedEvent.ts`, `logSkillsLoaded()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Environmentselection`** (2 nodes): `environmentSelection.ts`, `getEnvironmentSelectionInfo()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Unarylogging`** (2 nodes): `unaryLogging.ts`, `logUnaryEvent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useragent`** (2 nodes): `userAgent.ts`, `getClaudeCodeUserAgent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Withresolvers`** (2 nodes): `withResolvers.ts`, `withResolvers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Worktreemodeenabled`** (2 nodes): `worktreeModeEnabled.ts`, `isWorktreeModeEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Yaml`** (2 nodes): `yaml.ts`, `parseYaml()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Zodtojsonschema`** (2 nodes): `zodToJsonSchema.ts`, `zodToJsonSchema()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Autoupdaterwrapper`** (2 nodes): `AutoUpdaterWrapper.tsx`, `AutoUpdaterWrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Awsauthstatusbox`** (2 nodes): `AwsAuthStatusBox.tsx`, `AwsAuthStatusBox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Basetextinput`** (2 nodes): `BaseTextInput.tsx`, `BaseTextInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Channeldowngradedialog`** (2 nodes): `ChannelDowngradeDialog.tsx`, `ChannelDowngradeDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pluginhintmenu`** (2 nodes): `PluginHintMenu.tsx`, `PluginHintMenu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claudeinchromeonboarding`** (2 nodes): `ClaudeInChromeOnboarding.tsx`, `ClaudeInChromeOnboarding()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Clickableimageref`** (2 nodes): `ClickableImageRef.tsx`, `ClickableImageRef()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Compactsummary`** (2 nodes): `CompactSummary.tsx`, `CompactSummary()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Configurableshortcuthint`** (2 nodes): `ConfigurableShortcutHint.tsx`, `ConfigurableShortcutHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Costthresholddialog`** (2 nodes): `CostThresholdDialog.tsx`, `CostThresholdDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Select Option`** (2 nodes): `select-option.tsx`, `SelectOption()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Select Input`** (2 nodes): `use-select-input.ts`, `useSelectInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Select State`** (2 nodes): `use-select-state.ts`, `useSelectState()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fallbacktooluseerrormessage`** (2 nodes): `FallbackToolUseErrorMessage.tsx`, `FallbackToolUseErrorMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fallbacktooluserejectedmessage`** (2 nodes): `FallbackToolUseRejectedMessage.tsx`, `FallbackToolUseRejectedMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Submittranscriptshare`** (2 nodes): `submitTranscriptShare.ts`, `submitTranscriptShare()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usedebounceddigitinput`** (2 nodes): `useDebouncedDigitInput.ts`, `useDebouncedDigitInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usefeedbacksurvey`** (2 nodes): `useFeedbackSurvey.tsx`, `useFeedbackSurvey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Filepathlink`** (2 nodes): `FilePathLink.tsx`, `FilePathLink()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `General`** (2 nodes): `General.tsx`, `General()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Helpv2`** (2 nodes): `HelpV2.tsx`, `HelpV2()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Historysearchdialog`** (2 nodes): `HistorySearchDialog.tsx`, `HistorySearchDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Interruptedbyuser`** (2 nodes): `InterruptedByUser.tsx`, `InterruptedByUser()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Invalidsettingsdialog`** (2 nodes): `InvalidSettingsDialog.tsx`, `InvalidSettingsDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Animatedasterisk`** (2 nodes): `AnimatedAsterisk.tsx`, `AnimatedAsterisk()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Welcomev2`** (2 nodes): `WelcomeV2.tsx`, `WelcomeV2()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Lsprecommendationmenu`** (2 nodes): `LspRecommendationMenu.tsx`, `LspRecommendationMenu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcpserverapprovaldialog`** (2 nodes): `MCPServerApprovalDialog.tsx`, `MCPServerApprovalDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcpserverdesktopimportdialog`** (2 nodes): `MCPServerDesktopImportDialog.tsx`, `MCPServerDesktopImportDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcpserverdialogcopy`** (2 nodes): `MCPServerDialogCopy.tsx`, `MCPServerDialogCopy()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Memoryusageindicator`** (2 nodes): `MemoryUsageIndicator.tsx`, `MemoryUsageIndicator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Offscreenfreeze`** (2 nodes): `OffscreenFreeze.tsx`, `OffscreenFreeze()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Outputstylepicker`** (2 nodes): `OutputStylePicker.tsx`, `mapConfigsToOptions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Packagemanagerautoupdater`** (2 nodes): `PackageManagerAutoUpdater.tsx`, `PackageManagerAutoUpdater()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pressentertocontinue`** (2 nodes): `PressEnterToContinue.tsx`, `PressEnterToContinue()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issueflagbanner`** (2 nodes): `IssueFlagBanner.tsx`, `IssueFlagBanner()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Promptinputfooter`** (2 nodes): `PromptInputFooter.tsx`, `PromptInputFooter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sandboxpromptfooterhint`** (2 nodes): `SandboxPromptFooterHint.tsx`, `SandboxPromptFooterHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemaybetruncateinput`** (2 nodes): `useMaybeTruncateInput.ts`, `useMaybeTruncateInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usepromptinputplaceholder`** (2 nodes): `usePromptInputPlaceholder.ts`, `usePromptInputPlaceholder()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useshowfasticonhint`** (2 nodes): `useShowFastIconHint.ts`, `useShowFastIconHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Searchbox`** (2 nodes): `SearchBox.tsx`, `SearchBox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Flashingchar`** (2 nodes): `FlashingChar.tsx`, `FlashingChar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Glimmermessage`** (2 nodes): `GlimmerMessage.tsx`, `GlimmerMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shimmerchar`** (2 nodes): `ShimmerChar.tsx`, `ShimmerChar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Spinnerglyph`** (2 nodes): `SpinnerGlyph.tsx`, `SpinnerGlyph()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useshimmeranimation`** (2 nodes): `useShimmerAnimation.ts`, `useShimmerAnimation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usestalledanimation`** (2 nodes): `useStalledAnimation.ts`, `useStalledAnimation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Statusnotices`** (2 nodes): `StatusNotices.tsx`, `StatusNotices()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teleportresumewrapper`** (2 nodes): `TeleportResumeWrapper.tsx`, `TeleportResumeWrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Textinput`** (2 nodes): `TextInput.tsx`, `TextInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Themepicker`** (2 nodes): `ThemePicker.tsx`, `ThemePicker()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tooluseloader`** (2 nodes): `ToolUseLoader.tsx`, `ToolUseLoader()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Agentnavigationfooter`** (2 nodes): `AgentNavigationFooter.tsx`, `AgentNavigationFooter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Modelselector`** (2 nodes): `ModelSelector.tsx`, `ModelSelector()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Generateagent`** (2 nodes): `generateAgent.ts`, `generateAgent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Createagentwizard`** (2 nodes): `CreateAgentWizard.tsx`, `CreateAgentWizard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Colorstep`** (2 nodes): `ColorStep.tsx`, `ColorStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Confirmstepwrapper`** (2 nodes): `ConfirmStepWrapper.tsx`, `ConfirmStepWrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Descriptionstep`** (2 nodes): `DescriptionStep.tsx`, `DescriptionStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Generatestep`** (2 nodes): `GenerateStep.tsx`, `handleGenerate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Locationstep`** (2 nodes): `LocationStep.tsx`, `LocationStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Memorystep`** (2 nodes): `MemoryStep.tsx`, `MemoryStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Methodstep`** (2 nodes): `MethodStep.tsx`, `MethodStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Modelstep`** (2 nodes): `ModelStep.tsx`, `ModelStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Promptstep`** (2 nodes): `PromptStep.tsx`, `PromptStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Toolsstep`** (2 nodes): `ToolsStep.tsx`, `ToolsStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Typestep`** (2 nodes): `TypeStep.tsx`, `TypeStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Divider`** (2 nodes): `Divider.tsx`, `Divider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Keyboardshortcuthint`** (2 nodes): `KeyboardShortcutHint.tsx`, `let()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Loadingstate`** (2 nodes): `LoadingState.tsx`, `LoadingState()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pane`** (2 nodes): `Pane.tsx`, `Pane()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Progressbar`** (2 nodes): `ProgressBar.tsx`, `ProgressBar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ratchet`** (2 nodes): `Ratchet.tsx`, `Ratchet()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Capabilitiessection`** (2 nodes): `CapabilitiesSection.tsx`, `CapabilitiesSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcpparsingwarnings`** (2 nodes): `McpParsingWarnings.tsx`, `McpConfigErrorSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Assistantredactedthinkingmessage`** (2 nodes): `AssistantRedactedThinkingMessage.tsx`, `AssistantRedactedThinkingMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Assistanttextmessage`** (2 nodes): `AssistantTextMessage.tsx`, `InvalidApiKeyMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Assistantthinkingmessage`** (2 nodes): `AssistantThinkingMessage.tsx`, `AssistantThinkingMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Compactboundarymessage`** (2 nodes): `CompactBoundaryMessage.tsx`, `CompactBoundaryMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Groupedtoolusecontent`** (2 nodes): `GroupedToolUseContent.tsx`, `GroupedToolUseContent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hookprogressmessage`** (2 nodes): `HookProgressMessage.tsx`, `HookProgressMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Userbashinputmessage`** (2 nodes): `UserBashInputMessage.tsx`, `UserBashInputMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Userbashoutputmessage`** (2 nodes): `UserBashOutputMessage.tsx`, `UserBashOutputMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Userimagemessage`** (2 nodes): `UserImageMessage.tsx`, `UserImageMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Userplanmessage`** (2 nodes): `UserPlanMessage.tsx`, `UserPlanMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Userpromptmessage`** (2 nodes): `UserPromptMessage.tsx`, `UserPromptMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rejectedplanmessage`** (2 nodes): `RejectedPlanMessage.tsx`, `RejectedPlanMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rejectedtoolusemessage`** (2 nodes): `RejectedToolUseMessage.tsx`, `RejectedToolUseMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usertoolcanceledmessage`** (2 nodes): `UserToolCanceledMessage.tsx`, `UserToolCanceledMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usertoolerrormessage`** (2 nodes): `UserToolErrorMessage.tsx`, `UserToolErrorMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usertoolrejectmessage`** (2 nodes): `UserToolRejectMessage.tsx`, `UserToolRejectMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usertoolresultmessage`** (2 nodes): `UserToolResultMessage.tsx`, `UserToolResultMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Nullrenderingattachments`** (2 nodes): `nullRenderingAttachments.ts`, `isNullRenderingAttachment()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammemsaved`** (2 nodes): `teamMemSaved.ts`, `teamMemSavedPart()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Idediffconfig`** (2 nodes): `ideDiffConfig.ts`, `createSingleEditDiffConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usefilepermissiondialog`** (2 nodes): `useFilePermissionDialog.ts`, `useFilePermissionDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Filewritetooldiff`** (2 nodes): `FileWriteToolDiff.tsx`, `FileWriteToolDiff()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissiondialog`** (2 nodes): `PermissionDialog.tsx`, `PermissionDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionrequesttitle`** (2 nodes): `PermissionRequestTitle.tsx`, `PermissionRequestTitle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionruleexplanation`** (2 nodes): `PermissionRuleExplanation.tsx`, `stringsForDecisionReason()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Powershelltooluseoptions`** (2 nodes): `powershellToolUseOptions.tsx`, `powershellToolUseOptions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sandboxpermissionrequest`** (2 nodes): `SandboxPermissionRequest.tsx`, `SandboxPermissionRequest()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workerbadge`** (2 nodes): `WorkerBadge.tsx`, `WorkerBadge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workerpendingpermission`** (2 nodes): `WorkerPendingPermission.tsx`, `WorkerPendingPermission()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionruledescription`** (2 nodes): `PermissionRuleDescription.tsx`, `PermissionRuleDescription()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Removeworkspacedirectory`** (2 nodes): `RemoveWorkspaceDirectory.tsx`, `RemoveWorkspaceDirectory()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useshellpermissionfeedback`** (2 nodes): `useShellPermissionFeedback.ts`, `useShellPermissionFeedback()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sandboxdoctorsection`** (2 nodes): `SandboxDoctorSection.tsx`, `SandboxDoctorSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sandboxsettings`** (2 nodes): `SandboxSettings.tsx`, `getCurrentMode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shelltimedisplay`** (2 nodes): `ShellTimeDisplay.tsx`, `ShellTimeDisplay()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Asyncagentdetaildialog`** (2 nodes): `AsyncAgentDetailDialog.tsx`, `AsyncAgentDetailDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backgroundtask`** (2 nodes): `BackgroundTask.tsx`, `BackgroundTask()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Inprocessteammatedetaildialog`** (2 nodes): `InProcessTeammateDetailDialog.tsx`, `InProcessTeammateDetailDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rendertoolactivity`** (2 nodes): `renderToolActivity.tsx`, `renderToolActivity()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Orderedlist`** (2 nodes): `OrderedList.tsx`, `OrderedListComponent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Orderedlistitem`** (2 nodes): `OrderedListItem.tsx`, `OrderedListItem()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wizarddialoglayout`** (2 nodes): `WizardDialogLayout.tsx`, `WizardDialogLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wizardnavigationfooter`** (2 nodes): `WizardNavigationFooter.tsx`, `WizardNavigationFooter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usewizard`** (2 nodes): `useWizard.ts`, `useWizard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bridge Kick`** (2 nodes): `bridge-kick.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Brief`** (2 nodes): `brief.ts`, `getBriefConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Caches`** (2 nodes): `caches.ts`, `clearSessionCaches()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Clear`** (2 nodes): `clear.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Commit Push Pr`** (2 nodes): `commit-push-pr.ts`, `getPromptContent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Commit`** (2 nodes): `commit.ts`, `getPromptContent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cost`** (2 nodes): `cost.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Createmovedtoplugincommand`** (2 nodes): `createMovedToPluginCommand.ts`, `createMovedToPluginCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Desktop`** (2 nodes): `desktop.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Doctor`** (2 nodes): `doctor.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extra Usage Core`** (2 nodes): `extra-usage-core.ts`, `runExtraUsage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extra Usage Noninteractive`** (2 nodes): `extra-usage-noninteractive.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extra Usage`** (2 nodes): `extra-usage.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Heapdump`** (2 nodes): `heapdump.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Apikeystep`** (2 nodes): `ApiKeyStep.tsx`, `ApiKeyStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Checkexistingsecretstep`** (2 nodes): `CheckExistingSecretStep.tsx`, `CheckExistingSecretStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Checkgithubstep`** (2 nodes): `CheckGitHubStep.tsx`, `CheckGitHubStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chooserepostep`** (2 nodes): `ChooseRepoStep.tsx`, `ChooseRepoStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Existingworkflowstep`** (2 nodes): `ExistingWorkflowStep.tsx`, `ExistingWorkflowStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Oauthflowstep`** (2 nodes): `OAuthFlowStep.tsx`, `OAuthFlowStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Install Github App`** (2 nodes): `install-github-app.tsx`, `InstallGitHubApp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Install Slack App`** (2 nodes): `install-slack-app.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Addcommand`** (2 nodes): `addCommand.ts`, `registerMcpAddCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Xaaidpcommand`** (2 nodes): `xaaIdpCommand.ts`, `registerMcpXaaIdpCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Memory`** (2 nodes): `memory.tsx`, `MemoryCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Output Style`** (2 nodes): `output-style.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Addmarketplace`** (2 nodes): `AddMarketplace.tsx`, `AddMarketplace()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Parseargs`** (2 nodes): `parseArgs.ts`, `parsePluginArgs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usepagination`** (2 nodes): `usePagination.ts`, `usePagination()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Privacy Settings`** (2 nodes): `privacy-settings.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Remote Env`** (2 nodes): `remote-env.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Generatesessionname`** (2 nodes): `generateSessionName.ts`, `generateSessionName()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ultrareviewenabled`** (2 nodes): `ultrareviewEnabled.ts`, `isUltrareviewEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Review`** (2 nodes): `review.ts`, `LOCAL_REVIEW_PROMPT()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rewind`** (2 nodes): `rewind.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Security Review`** (2 nodes): `security-review.ts`, `getPromptWhileMarketplaceIsPrivate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Skills`** (2 nodes): `skills.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Stickers`** (2 nodes): `stickers.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Upgrade`** (2 nodes): `upgrade.tsx`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Version`** (2 nodes): `version.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vim`** (2 nodes): `vim.ts`, `call()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Exploreagent`** (2 nodes): `exploreAgent.ts`, `getExploreSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Generalpurposeagent`** (2 nodes): `generalPurposeAgent.ts`, `getGeneralPurposeSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Planagent`** (2 nodes): `planAgent.ts`, `getPlanV2SystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resumeagent`** (2 nodes): `resumeAgent.ts`, `resumeAgentBackground()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Commentlabel`** (2 nodes): `commentLabel.ts`, `extractBashCommentLabel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Destructivecommandwarning`** (2 nodes): `destructiveCommandWarning.ts`, `getDestructiveCommandWarning()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Limits`** (2 nodes): `limits.ts`, `getEnvMaxTokens()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Symbolcontext`** (2 nodes): `symbolContext.ts`, `getSymbolAtPosition()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Primitivetools`** (2 nodes): `primitiveTools.ts`, `getReplPrimitiveTools()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teamcreatetool`** (2 nodes): `TeamCreateTool.ts`, `generateUniqueTeamName()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Preapproved`** (2 nodes): `preapproved.ts`, `isPreapprovedHost()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sinkkillswitch`** (2 nodes): `sinkKillswitch.ts`, `isSinkKilled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Firsttokendate`** (2 nodes): `firstTokenDate.ts`, `fetchAndStoreClaudeCodeFirstTokenDate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ultrareviewquota`** (2 nodes): `ultrareviewQuota.ts`, `fetchUltrareviewQuota()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Consolidationprompt`** (2 nodes): `consolidationPrompt.ts`, `buildConsolidationPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claudeailimitshook`** (2 nodes): `claudeAiLimitsHook.ts`, `useClaudeAiLimits()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Apimicrocompact`** (2 nodes): `apiMicrocompact.ts`, `getAPIContextManagement()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Compactwarninghook`** (2 nodes): `compactWarningHook.ts`, `useCompactWarningSuppression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Grouping`** (2 nodes): `grouping.ts`, `groupMessagesByApiRound()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Postcompactcleanup`** (2 nodes): `postCompactCleanup.ts`, `runPostCompactCleanup()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Timebasedmcconfig`** (2 nodes): `timeBasedMCConfig.ts`, `getTimeBasedMCConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Internallogging`** (2 nodes): `internalLogging.ts`, `logPermissionContextForAnts()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Lspclient`** (2 nodes): `LSPClient.ts`, `createLSPClient()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Envexpansion`** (2 nodes): `envExpansion.ts`, `expandEnvVarsInString()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Normalization`** (2 nodes): `normalization.ts`, `normalizeNameForMCP()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcpserverapproval`** (2 nodes): `mcpServerApproval.tsx`, `handleMcpjsonServerApprovals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammemsecretguard`** (2 nodes): `teamMemSecretGuard.ts`, `checkTeamMemSecrets()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Toolhooks`** (2 nodes): `toolHooks.ts`, `resolveHookPermissionDecision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useautomodeunavailablenotification`** (2 nodes): `useAutoModeUnavailableNotification.ts`, `useAutoModeUnavailableNotification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usedeprecationwarningnotification`** (2 nodes): `useDeprecationWarningNotification.tsx`, `useDeprecationWarningNotification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useratelimitwarningnotification`** (2 nodes): `useRateLimitWarningNotification.tsx`, `useRateLimitWarningNotification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usestartupnotification`** (2 nodes): `useStartupNotification.ts`, `useStartupNotification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Renderplaceholder`** (2 nodes): `renderPlaceholder.ts`, `renderPlaceholder()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Coordinatorhandler`** (2 nodes): `coordinatorHandler.ts`, `handleCoordinatorPermission()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Swarmworkerhandler`** (2 nodes): `swarmWorkerHandler.ts`, `handleSwarmWorkerPermission()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useafterfirstrender`** (2 nodes): `useAfterFirstRender.ts`, `useAfterFirstRender()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useapikeyverification`** (2 nodes): `useApiKeyVerification.ts`, `useApiKeyVerification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useblink`** (2 nodes): `useBlink.ts`, `useBlink()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usecancelrequest`** (2 nodes): `useCancelRequest.ts`, `CancelRequestHandler()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useclaudecodehintrecommendation`** (2 nodes): `useClaudeCodeHintRecommendation.tsx`, `useClaudeCodeHintRecommendation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useclipboardimagehint`** (2 nodes): `useClipboardImageHint.ts`, `useClipboardImageHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usecommandkeybindings`** (2 nodes): `useCommandKeybindings.tsx`, `CommandKeybindingHandlers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usecommandqueue`** (2 nodes): `useCommandQueue.ts`, `useCommandQueue()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usedeferredhookmessages`** (2 nodes): `useDeferredHookMessages.ts`, `useDeferredHookMessages()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usedirectconnect`** (2 nodes): `useDirectConnect.ts`, `useDirectConnect()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usedoublepress`** (2 nodes): `useDoublePress.ts`, `useDoublePress()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usedynamicconfig`** (2 nodes): `useDynamicConfig.ts`, `useDynamicConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useelapsedtime`** (2 nodes): `useElapsedTime.ts`, `useElapsedTime()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useexitonctrlcd`** (2 nodes): `useExitOnCtrlCD.ts`, `useExitOnCtrlCD()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useexitonctrlcdwithkeybindings`** (2 nodes): `useExitOnCtrlCDWithKeybindings.ts`, `useExitOnCtrlCDWithKeybindings()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usefilehistorysnapshotinit`** (2 nodes): `useFileHistorySnapshotInit.ts`, `useFileHistorySnapshotInit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useglobalkeybindings`** (2 nodes): `useGlobalKeybindings.tsx`, `GlobalKeybindingHandlers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usehistorysearch`** (2 nodes): `useHistorySearch.ts`, `useHistorySearch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useideintegration`** (2 nodes): `useIDEIntegration.tsx`, `useIDEIntegration()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useideatmentioned`** (2 nodes): `useIdeAtMentioned.ts`, `useIdeAtMentioned()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useideconnectionstatus`** (2 nodes): `useIdeConnectionStatus.ts`, `useIdeConnectionStatus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useidelogging`** (2 nodes): `useIdeLogging.ts`, `useIdeLogging()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useideselection`** (2 nodes): `useIdeSelection.ts`, `useIdeSelection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useinputbuffer`** (2 nodes): `useInputBuffer.ts`, `useInputBuffer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemailboxbridge`** (2 nodes): `useMailboxBridge.ts`, `useMailboxBridge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemainloopmodel`** (2 nodes): `useMainLoopModel.ts`, `useMainLoopModel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemanageplugins`** (2 nodes): `useManagePlugins.ts`, `useManagePlugins()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usememoryusage`** (2 nodes): `useMemoryUsage.ts`, `useMemoryUsage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemergedcommands`** (2 nodes): `useMergedCommands.ts`, `useMergedCommands()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemergedtools`** (2 nodes): `useMergedTools.ts`, `useMergedTools()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usemindisplaytime`** (2 nodes): `useMinDisplayTime.ts`, `useMinDisplayTime()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useprstatus`** (2 nodes): `usePrStatus.ts`, `usePrStatus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usepromptsuggestion`** (2 nodes): `usePromptSuggestion.ts`, `usePromptSuggestion()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usequeueprocessor`** (2 nodes): `useQueueProcessor.ts`, `useQueueProcessor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useremotesession`** (2 nodes): `useRemoteSession.ts`, `useRemoteSession()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usereplbridge`** (2 nodes): `useReplBridge.tsx`, `useReplBridge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usesessionbackgrounding`** (2 nodes): `useSessionBackgrounding.ts`, `useSessionBackgrounding()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usesettings`** (2 nodes): `useSettings.ts`, `useSettings()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usesettingschange`** (2 nodes): `useSettingsChange.ts`, `useSettingsChange()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useskillimprovementsurvey`** (2 nodes): `useSkillImprovementSurvey.ts`, `useSkillImprovementSurvey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useskillschange`** (2 nodes): `useSkillsChange.ts`, `useSkillsChange()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useswarminitialization`** (2 nodes): `useSwarmInitialization.ts`, `useSwarmInitialization()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useteammateviewautoexit`** (2 nodes): `useTeammateViewAutoExit.ts`, `useTeammateViewAutoExit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useteleportresume`** (2 nodes): `useTeleportResume.tsx`, `useTeleportResume()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useterminalsize`** (2 nodes): `useTerminalSize.ts`, `useTerminalSize()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usetimeout`** (2 nodes): `useTimeout.ts`, `useTimeout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useviminput`** (2 nodes): `useVimInput.ts`, `useVimInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Usevoiceenabled`** (2 nodes): `useVoiceEnabled.ts`, `useVoiceEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Alternatescreen`** (2 nodes): `AlternateScreen.tsx`, `AlternateScreen()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Box`** (2 nodes): `Box.tsx`, `Box()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Link`** (2 nodes): `Link.tsx`, `Link()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Newline`** (2 nodes): `Newline.tsx`, `Newline()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Noselect`** (2 nodes): `NoSelect.tsx`, `NoSelect()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rawansi`** (2 nodes): `RawAnsi.tsx`, `RawAnsi()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scrollbox`** (2 nodes): `ScrollBox.tsx`, `ScrollBox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Spacer`** (2 nodes): `Spacer.tsx`, `Spacer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Terminalfocuscontext`** (2 nodes): `TerminalFocusContext.tsx`, `TerminalFocusProvider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Text`** (2 nodes): `Text.tsx`, `Text()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Get Max Width`** (2 nodes): `get-max-width.ts`, `getMaxWidth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Animation Frame`** (2 nodes): `use-animation-frame.ts`, `useAnimationFrame()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use App`** (2 nodes): `use-app.ts`, `useApp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Declared Cursor`** (2 nodes): `use-declared-cursor.ts`, `useDeclaredCursor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Input`** (2 nodes): `use-input.ts`, `useInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Search Highlight`** (2 nodes): `use-search-highlight.ts`, `useSearchHighlight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Stdin`** (2 nodes): `use-stdin.ts`, `useStdin()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Terminal Focus`** (2 nodes): `use-terminal-focus.ts`, `useTerminalFocus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Terminal Title`** (2 nodes): `use-terminal-title.ts`, `useTerminalTitle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Use Terminal Viewport`** (2 nodes): `use-terminal-viewport.ts`, `useTerminalViewport()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Engine`** (2 nodes): `engine.ts`, `createLayoutNode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Line Width Cache`** (2 nodes): `line-width-cache.ts`, `lineWidth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Measure Element`** (2 nodes): `measure-element.ts`, `measureElement()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Measure Text`** (2 nodes): `measure-text.ts`, `measureText()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Optimizer`** (2 nodes): `optimizer.ts`, `optimize()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Renderer`** (2 nodes): `renderer.ts`, `createRenderer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Searchhighlight`** (2 nodes): `searchHighlight.ts`, `applySearchHighlight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Supports Hyperlinks`** (2 nodes): `supports-hyperlinks.ts`, `supportsHyperlinks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tabstops`** (2 nodes): `tabstops.ts`, `expandTabs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Esc`** (2 nodes): `esc.ts`, `parseEsc()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useterminalnotification`** (2 nodes): `useTerminalNotification.ts`, `useTerminalNotification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Warn`** (2 nodes): `warn.ts`, `ifNotInteger()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Widest Line`** (2 nodes): `widest-line.ts`, `widestLine()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Schema`** (2 nodes): `schema.ts`, `emptyStore()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cors`** (2 nodes): `cors.ts`, `cors()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Request Id`** (2 nodes): `request-id.ts`, `requestId()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Exec`** (2 nodes): `exec.ts`, `createExecRouter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Search`** (2 nodes): `search.ts`, `createSearchRouter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Seed`** (2 nodes): `seed.ts`, `seed()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Auth Test`** (2 nodes): `auth.test.ts`, `mockReq()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bridgepermissioncallbacks`** (2 nodes): `bridgePermissionCallbacks.ts`, `isBridgePermissionResponse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Capacitywake`** (2 nodes): `capacityWake.ts`, `createCapacityWake()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pollconfig`** (2 nodes): `pollConfig.ts`, `getPollIntervalConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Stub`** (2 nodes): `stub.ts`, `isBridgeAvailable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Keys`** (2 nodes): `keys.ts`, `getGrowthBookClientKey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Spinnerverbs`** (2 nodes): `spinnerVerbs.ts`, `getSpinnerVerbs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claudeinchrome`** (2 nodes): `claudeInChrome.ts`, `registerClaudeInChromeSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Remember`** (2 nodes): `remember.ts`, `registerRememberSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Simplify`** (2 nodes): `simplify.ts`, `registerSimplifySkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Stuck`** (2 nodes): `stuck.ts`, `registerStuckSkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Verify`** (2 nodes): `verify.ts`, `registerVerifySkill()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Transportutils`** (2 nodes): `transportUtils.ts`, `getTransportForUrl()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Update`** (2 nodes): `update.ts`, `update()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Connectortext`** (2 nodes): `connectorText.ts`, `isConnectorTextBlock()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shortcutformat`** (2 nodes): `shortcutFormat.ts`, `getShortcutDisplay()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Useshortcutdisplay`** (2 nodes): `useShortcutDisplay.ts`, `useShortcutDisplay()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Guards`** (2 nodes): `guards.ts`, `isLocalShellTask()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migrateautoupdatestosettings`** (2 nodes): `migrateAutoUpdatesToSettings.ts`, `migrateAutoUpdatesToSettings()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migratebypasspermissionsacceptedtosettings`** (2 nodes): `migrateBypassPermissionsAcceptedToSettings.ts`, `migrateBypassPermissionsAcceptedToSettings()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migrateenableallprojectmcpserverstosettings`** (2 nodes): `migrateEnableAllProjectMcpServersToSettings.ts`, `migrateEnableAllProjectMcpServersToSettings()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migratefennectoopus`** (2 nodes): `migrateFennecToOpus.ts`, `migrateFennecToOpus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migratelegacyopustocurrent`** (2 nodes): `migrateLegacyOpusToCurrent.ts`, `migrateLegacyOpusToCurrent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migrateopustoopus1M`** (2 nodes): `migrateOpusToOpus1m.ts`, `migrateOpusToOpus1m()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migratereplbridgeenabledtoremotecontrolatstartup`** (2 nodes): `migrateReplBridgeEnabledToRemoteControlAtStartup.ts`, `migrateReplBridgeEnabledToRemoteControlAtStartup()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migratesonnet1Mtosonnet45`** (2 nodes): `migrateSonnet1mToSonnet45.ts`, `migrateSonnet1mToSonnet45()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migratesonnet45Tosonnet46`** (2 nodes): `migrateSonnet45ToSonnet46.ts`, `migrateSonnet45ToSonnet46()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resetautomodeoptinfordefaultoffer`** (2 nodes): `resetAutoModeOptInForDefaultOffer.ts`, `resetAutoModeOptInForDefaultOffer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resetprotoopusdefault`** (2 nodes): `resetProToOpusDefault.ts`, `resetProToOpusDefault()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cli`** (2 nodes): `cli.tsx`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Memorytypes`** (2 nodes): `memoryTypes.ts`, `parseMemoryType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammemprompts`** (2 nodes): `teamMemPrompts.ts`, `buildCombinedMemoryPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Alias`** (1 nodes): `alias.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Nohup`** (1 nodes): `nohup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pyright`** (1 nodes): `pyright.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Srun`** (1 nodes): `srun.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Time`** (1 nodes): `time.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Timeout`** (1 nodes): `timeout.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Configconstants`** (1 nodes): `configConstants.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Configs`** (1 nodes): `configs.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Modelsupportoverrides`** (1 nodes): `modelSupportOverrides.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionrule`** (1 nodes): `PermissionRule.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionupdateschema`** (1 nodes): `PermissionUpdateSchema.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dangerouspatterns`** (1 nodes): `dangerousPatterns.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Officialmarketplace`** (1 nodes): `officialMarketplace.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shellprovider`** (1 nodes): `shellProvider.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammatepromptaddendum`** (1 nodes): `teammatePromptAddendum.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Agentprogressline`** (1 nodes): `AgentProgressLine.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Approveapikey`** (1 nodes): `ApproveApiKey.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Automodeoptindialog`** (1 nodes): `AutoModeOptInDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bashmodeprogress`** (1 nodes): `BashModeProgress.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Select Input Option`** (1 nodes): `select-input-option.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Effortcallout`** (1 nodes): `EffortCallout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Highlightedcode`** (1 nodes): `HighlightedCode.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Modelpicker`** (1 nodes): `ModelPicker.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Historysearchinput`** (1 nodes): `HistorySearchInput.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shimmeredinput`** (1 nodes): `ShimmeredInput.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Skillimprovementsurvey`** (1 nodes): `SkillImprovementSurvey.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teammateselecthint`** (1 nodes): `teammateSelectHint.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teleporterror`** (1 nodes): `TeleportError.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Thinkingtoggle`** (1 nodes): `ThinkingToggle.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Trustdialog`** (1 nodes): `TrustDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dialog`** (1 nodes): `Dialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Promptdialog`** (1 nodes): `PromptDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcptoollistview`** (1 nodes): `MCPToolListView.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Userlocalcommandoutputmessage`** (1 nodes): `UserLocalCommandOutputMessage.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fallbackpermissionrequest`** (1 nodes): `FallbackPermissionRequest.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissionexplanation`** (1 nodes): `PermissionExplanation.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shellprogressmessage`** (1 nodes): `ShellProgressMessage.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dreamdetaildialog`** (1 nodes): `DreamDetailDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Help`** (1 nodes): `help.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Init Verifiers`** (1 nodes): `init-verifiers.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Creatingstep`** (1 nodes): `CreatingStep.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Errorstep`** (1 nodes): `ErrorStep.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Successstep`** (1 nodes): `SuccessStep.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Login`** (1 nodes): `login.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ultrareviewoveragedialog`** (1 nodes): `UltrareviewOverageDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Statuslinesetup`** (1 nodes): `statuslineSetup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Verificationagent`** (1 nodes): `verificationAgent.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Toolname`** (1 nodes): `toolName.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Enterplanmodetool`** (1 nodes): `EnterPlanModeTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Enterworktreetool`** (1 nodes): `EnterWorktreeTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Exitplanmodev2Tool`** (1 nodes): `ExitPlanModeV2Tool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Globtool`** (1 nodes): `GlobTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Listmcpresourcestool`** (1 nodes): `ListMcpResourcesTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mcptool`** (1 nodes): `MCPTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Commonparameters`** (1 nodes): `commonParameters.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Readmcpresourcetool`** (1 nodes): `ReadMcpResourceTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Remotetriggertool`** (1 nodes): `RemoteTriggerTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Croncreatetool`** (1 nodes): `CronCreateTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crondeletetool`** (1 nodes): `CronDeleteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cronlisttool`** (1 nodes): `CronListTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Taskcreatetool`** (1 nodes): `TaskCreateTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Taskgettool`** (1 nodes): `TaskGetTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tasklisttool`** (1 nodes): `TaskListTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Taskstoptool`** (1 nodes): `TaskStopTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Taskupdatetool`** (1 nodes): `TaskUpdateTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Teamdeletetool`** (1 nodes): `TeamDeleteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Todowritetool`** (1 nodes): `TodoWriteTool.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Testingpermissiontool`** (1 nodes): `TestingPermissionTool.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Emptyusage`** (1 nodes): `emptyUsage.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Securitycheck`** (1 nodes): `securityCheck.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Appcontext`** (1 nodes): `AppContext.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cursordeclarationcontext`** (1 nodes): `CursorDeclarationContext.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Stdincontext`** (1 nodes): `StdinContext.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Terminalsizecontext`** (1 nodes): `TerminalSizeContext.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Event Handlers`** (1 nodes): `event-handlers.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Global D`** (1 nodes): `global.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Instances`** (1 nodes): `instances.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Termio`** (1 nodes): `termio.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wrapansi`** (1 nodes): `wrapAnsi.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Api Key`** (1 nodes): `api-key.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sqlite`** (1 nodes): `sqlite.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pollconfigdefaults`** (1 nodes): `pollConfigDefaults.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Apilimits`** (1 nodes): `apiLimits.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cyberriskinstruction`** (1 nodes): `cyberRiskInstruction.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Errorids`** (1 nodes): `errorIds.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Github App`** (1 nodes): `github-app.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Querysource`** (1 nodes): `querySource.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Toollimits`** (1 nodes): `toolLimits.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tools`** (1 nodes): `tools.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Turncompletionverbs`** (1 nodes): `turnCompletionVerbs.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claudeapicontent`** (1 nodes): `claudeApiContent.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Verifycontent`** (1 nodes): `verifyContent.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bun Bundle D`** (1 nodes): `bun-bundle.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bun Globals D`** (1 nodes): `bun-globals.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Macro D`** (1 nodes): `macro.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Defaultbindings`** (1 nodes): `defaultBindings.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Sandboxtypes`** (1 nodes): `sandboxTypes.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Controlschemas`** (1 nodes): `controlSchemas.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Coreschemas`** (1 nodes): `coreSchemas.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Coretypes Generated`** (1 nodes): `coreTypes.generated.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Coretypes`** (1 nodes): `coreTypes.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Runtimetypes`** (1 nodes): `runtimeTypes.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tooltypes`** (1 nodes): `toolTypes.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 46 inferred relationships involving `mk()` (e.g. with `checkBudget()` and `sliceBytes()`) actually correct?**
  _`mk()` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `peek()` (e.g. with `nextToken()` and `parseCommand()`) actually correct?**
  _`peek()` has 42 INFERRED edges - model-reasoned connections that need verification._
- **What connects `GcpCredentialsTimeoutError`, `AutoUpdaterError`, `MalformedCommandError` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Adddirpluginsettings` be split into smaller, more focused modules?**
  _Cohesion score 0.0 - nodes in this community are weakly interconnected._
- **Should `Apiqueryhookhelper` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Add Dir` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Audit Log` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._