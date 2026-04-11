# Graph Report - /Users/jay/Developer/claude-code-agent/src/utils  (2026-04-09)

## Corpus Check
- 565 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4874 nodes · 7990 edges · 442 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 3449 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Cursor` - 57 edges
2. `mk()` - 47 edges
3. `peek()` - 43 edges
4. `skipBlanks()` - 37 edges
5. `advance()` - 36 edges
6. `getProject()` - 34 edges
7. `Project` - 31 edges
8. `nextToken()` - 29 edges
9. `leaf()` - 25 edges
10. `saveLex()` - 24 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.01
Nodes (166): backupTerminalPreferences(), checkAndRestoreTerminalBackup(), getTerminalPlistPath(), getTerminalRecoveryInfo(), markTerminalSetupComplete(), markTerminalSetupInProgress(), getRecordFilePath(), getTerminalSize() (+158 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (106): deserializeMessages(), deserializeMessagesWithInterruptDetection(), detectTurnInterruption(), isTerminalToolResult(), loadConversationForResume(), loadMessagesFromJsonlPath(), restoreSkillStateFromMessages(), hashFileContent() (+98 more)

### Community 2 - "Community 2"
Cohesion: 0.03
Nodes (112): adoptResumedSessionFile(), appendEntryToFile(), applyPreservedSegmentRelinks(), applySnipRemovals(), buildAttributionSnapshotChain(), buildConversationChain(), buildFileHistorySnapshotChain(), cacheSessionTitle() (+104 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (70): appendMessageTagToUserMessage(), baseCreateAssistantMessage(), buildMessageLookups(), contentHasToolReference(), createAssistantAPIErrorMessage(), createAssistantMessage(), createModelSwitchBreadcrumbs(), createSyntheticUserCaveatMessage() (+62 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (6): Cursor, isVimPunctuation(), isVimWhitespace(), isVimWordChar(), MeasuredText, WrappedLine

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (79): advance(), byteAt(), byteLengthUtf8(), checkBudget(), consumeKeyword(), isArithStop(), isBaseDigit(), isDigit() (+71 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (48): createAbortController(), createChildAbortController(), axiosGetWithRetry(), fetchCodeSessionsFromSessionsAPI(), fetchSession(), filterSwarmFieldsFromSchema(), getOAuthHeaders(), isTransientNetworkError() (+40 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (40): collectRecentSuccessfulTools(), collectSurfacedMemories(), countAutoModeAttachmentsSinceLastExit(), countPlanModeAttachmentsSinceLastExit(), extractAgentMentions(), extractAtMentionedFiles(), extractMcpResourceMentions(), filterToBundledAndMcp() (+32 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (61): calculateApiKeyHelperTTL(), checkAndRefreshOAuthTokenIfNeeded(), checkAndRefreshOAuthTokenIfNeededImpl(), checkGcpCredentialsValid(), clearOAuthTokenCache(), _executeApiKeyHelper(), GcpCredentialsTimeoutError, getAccountInformation() (+53 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (33): createBaseHookInput(), execCommandHook(), executeConfigChangeHooks(), executeCwdChangedHooks(), executeElicitationHooks(), executeElicitationResultHooks(), executeEnvHooks(), executeFileChangedHooks() (+25 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (7): AbortedShellCommand, prependStderr(), ShellCommandImpl, StreamWrapper, renderToAnsiString(), renderToString(), Stream

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (37): escapeForDiff(), getPatchForDisplay(), getPatchFromContents(), applySnapshot(), checkOriginFileChanged(), compareStatsAndContent(), computeDiffStatsForFile(), copyFileHistoryForResume() (+29 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (37): addMarketplaceSource(), cacheMarketplaceFromGit(), cacheMarketplaceFromUrl(), enhanceGitPullErrorMessages(), extractSshHost(), findSeedMarketplaceLocation(), getCachePathForSource(), getKnownMarketplacesFile() (+29 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (36): assemblePluginLoadResult(), cachePlugin(), cachePluginSettings(), copyDir(), copyPluginToVersionedCache(), createPluginFromPath(), finishLoadingPluginFromPath(), generateTemporaryCacheNameForPlugin() (+28 more)

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (27): buildParseScript(), classifyCommandName(), ensureArray(), extractCommandArguments(), extractEnvVars(), findCommandNode(), getAllCommandNames(), getAllRedirections() (+19 more)

### Community 15 - "Community 15"
Cohesion: 0.1
Nodes (28): checkIdeConnection(), cleanupStaleIdeLockfiles(), detectIDEs(), detectRunningIDEs(), detectRunningIDEsCached(), detectRunningIDEsImpl(), findAvailableIDE(), getClaudeCodeVersion() (+20 more)

### Community 16 - "Community 16"
Cohesion: 0.12
Nodes (35): allWorkingDirectories(), checkEditableInternalPath(), checkPathSafetyForAutoEdit(), checkReadableInternalPath(), checkReadPermissionForTool(), checkWritePermissionForTool(), ensureScratchpadDir(), generateSuggestions() (+27 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (34): checkAndDisableBypassPermissions(), findDangerousClassifierPermissions(), findOverlyBroadBashPermissions(), findOverlyBroadPowerShellPermissions(), formatPermissionSource(), getAutoModeEnabledState(), getAutoModeEnabledStateIfCached(), getAutoModeUnavailableNotification() (+26 more)

### Community 18 - "Community 18"
Cohesion: 0.11
Nodes (32): consumeRawReadResult(), ensureMdmSettingsLoaded(), getAutoModeConfig(), getInitialSettings(), getManagedFileSettingsPresence(), getManagedSettingsFilePath(), getPolicySettingsOrigin(), getRelativeSettingsFilePathForSource() (+24 more)

### Community 19 - "Community 19"
Cohesion: 0.11
Nodes (25): checkHasTrustDialogAccepted(), computeTrustDialogAccepted(), enableConfigs(), findMostRecentBackup(), getAutoUpdaterDisabledReason(), getConfig(), getConfigBackupDir(), getCurrentProjectConfig() (+17 more)

### Community 20 - "Community 20"
Cohesion: 0.11
Nodes (32): buildClaudeMdMessage(), buildToolLookup(), buildTranscriptEntries(), buildTranscriptForClassifier(), buildYoloSystemPrompt(), classifyYoloAction(), classifyYoloActionXml(), combineUsage() (+24 more)

### Community 21 - "Community 21"
Cohesion: 0.08
Nodes (11): clearMailbox(), createShutdownRequestMessage(), ensureInboxDir(), getInboxPath(), markMessageAsReadByIndex(), markMessagesAsRead(), markMessagesAsReadByPredicate(), readMailbox() (+3 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (23): computeBranch(), computeDefaultBranch(), computeHead(), computeRemoteUrl(), getCachedBranch(), getCachedDefaultBranch(), getCachedHead(), getCachedRemoteUrl() (+15 more)

### Community 23 - "Community 23"
Cohesion: 0.13
Nodes (30): buildTraceDocument(), closeOpenSpans(), emitPerfettoCounter(), emitPerfettoInstant(), emitProcessMetadata(), endInteractionPerfettoSpan(), endLLMRequestPerfettoSpan(), endToolPerfettoSpan() (+22 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (30): applyToolResultBudget(), buildLargeToolResultMessage(), buildReplacement(), buildToolNameMap(), collectCandidatesByMessage(), collectCandidatesFromMessage(), contentSize(), createContentReplacementState() (+22 more)

### Community 25 - "Community 25"
Cohesion: 0.17
Nodes (29): atomicMoveToInstallPath(), attemptNpmUninstall(), checkInstall(), cleanupNpmInstallations(), cleanupOldVersions(), forceRemoveLock(), getBaseDirectories(), getBinaryName() (+21 more)

### Community 26 - "Community 26"
Cohesion: 0.15
Nodes (25): addInstalledPlugin(), addPluginInstallation(), cleanupLegacyCache(), getGitCommitSha(), getInMemoryInstalledPlugins(), getInstalledPluginsFilePath(), getInstalledPluginsV2FilePath(), getPendingUpdateCount() (+17 more)

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (28): blockTask(), claimTask(), claimTaskWithBusyCheck(), clearLeaderTeamName(), createTask(), deleteTask(), ensureTaskListLockFile(), ensureTasksDir() (+20 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (27): firstPartyNameToCanonical(), getBestModel(), getCanonicalName(), getClaudeAiUserDefaultModelDescription(), getDefaultHaikuModel(), getDefaultMainLoopModel(), getDefaultMainLoopModelSetting(), getDefaultOpusModel() (+19 more)

### Community 29 - "Community 29"
Cohesion: 0.12
Nodes (23): clearMemoryFileCaches(), extractIncludePathsFromTokens(), getAllMemoryFilePaths(), getConditionalRulesForCwdLevelDirectory(), getExternalClaudeMdIncludes(), getManagedAndUserConditionalRules(), getMemoryFilesForNestedDirectory(), handleMemoryFileReadError() (+15 more)

### Community 30 - "Community 30"
Cohesion: 0.13
Nodes (17): clearCommandQueue(), dequeue(), dequeueAll(), dequeueAllMatching(), dequeuePendingNotification(), enqueue(), enqueuePendingNotification(), extractImagesFromValue() (+9 more)

### Community 31 - "Community 31"
Cohesion: 0.14
Nodes (23): buildDesktopDeepLink(), getDesktopInstallStatus(), getDesktopVersion(), isDesktopInstalled(), isDevMode(), openCurrentSessionInDesktop(), openDeepLink(), checkForReleaseNotes() (+15 more)

### Community 32 - "Community 32"
Cohesion: 0.14
Nodes (24): collapseReadSearchGroups(), commandAsHint(), countToolUses(), createEmptyGroup(), getCollapsibleToolInfo(), getFilePathFromToolInput(), getFilePathsFromReadMessage(), getSearchOrReadFromContent() (+16 more)

### Community 33 - "Community 33"
Cohesion: 0.14
Nodes (23): attributionRestoreStateFromLog(), calculateCommitAttribution(), computeContentHash(), computeFileModificationState(), createEmptyAttributionState(), expandFilePath(), getAttributionRepoRoot(), getClientSurface() (+15 more)

### Community 34 - "Community 34"
Cohesion: 0.17
Nodes (6): acquirePaneCreationLock(), getTmuxColorName(), runTmuxInSwarm(), runTmuxInUserSession(), TmuxBackend, waitForPaneShellReady()

### Community 35 - "Community 35"
Cohesion: 0.14
Nodes (16): cleanupStaleAgentWorktrees(), copyWorktreeIncludeFiles(), createAgentWorktree(), createWorktreeForSession(), execIntoTmuxWorktree(), flattenSlug(), getOrCreateWorktree(), mkdirRecursive() (+8 more)

### Community 36 - "Community 36"
Cohesion: 0.13
Nodes (17): addToExcludedCommands(), convertToSandboxRuntimeConfig(), getLinuxGlobPatternWarnings(), getSandboxEnabledSetting(), getSandboxUnavailableReason(), initialize(), isPlatformInEnabledList(), isSandboxingEnabled() (+9 more)

### Community 37 - "Community 37"
Cohesion: 0.14
Nodes (16): appendTaskOutput(), cleanupTaskOutput(), _clearOutputsForTest(), DiskTaskOutput, ensureOutputDir(), evictTaskOutput(), flushTaskOutput(), getOrCreateOutput() (+8 more)

### Community 38 - "Community 38"
Cohesion: 0.24
Nodes (22): applyVarToScope(), collectCommands(), collectCommandSubstitution(), containsAnyPlaceholder(), extractSafeCatHeredoc(), maskBracesInQuotedContexts(), parseForSecurity(), parseForSecurityFromAst() (+14 more)

### Community 39 - "Community 39"
Cohesion: 0.16
Nodes (22): applyPermissionRulesToPermissionContext(), checkRuleBasedPermissions(), convertRulesToUpdates(), createPermissionRequestMessage(), filterDeniedAgents(), getAllowRules(), getAskRuleForTool(), getAskRules() (+14 more)

### Community 40 - "Community 40"
Cohesion: 0.16
Nodes (20): canonicalizePath(), captureCarry(), captureSnap(), compactBoundaryMarker(), extractJsonStringField(), extractLastJsonStringField(), finalizeOutput(), findProjectDir() (+12 more)

### Community 41 - "Community 41"
Cohesion: 0.16
Nodes (21): cleanupOldResolutions(), createPermissionRequest(), deleteResolvedPermission(), ensurePermissionDirsAsync(), generateRequestId(), getLeaderName(), getPendingDir(), getPendingRequestPath() (+13 more)

### Community 42 - "Community 42"
Cohesion: 0.09
Nodes (12): AbortError, classifyAxiosError(), ClaudeError, ConfigParseError, errorMessage(), getErrnoCode(), isENOENT(), isFsInaccessible() (+4 more)

### Community 43 - "Community 43"
Cohesion: 0.19
Nodes (19): addHiddenPaneId(), cleanupTeamDirectories(), destroyWorktree(), getTeamDir(), getTeamFilePath(), killOrphanedTeammatePanes(), readTeamFile(), readTeamFileAsync() (+11 more)

### Community 44 - "Community 44"
Cohesion: 0.1
Nodes (8): addLineNumbers(), getAbsoluteAndRelativePaths(), getDisplayPath(), isCompactLinePrefixEnabled(), normalizePathForComparison(), pathsEqual(), writeFileSyncAndFlush_DEPRECATED(), writeTextContent()

### Community 45 - "Community 45"
Cohesion: 0.18
Nodes (22): filterModelOptionsByAllowlist(), getCustomHaikuOption(), getCustomOpusOption(), getCustomSonnetOption(), getDefaultOptionForUser(), getHaiku35Option(), getHaiku45Option(), getHaikuOption() (+14 more)

### Community 46 - "Community 46"
Cohesion: 0.13
Nodes (15): areSourcesEquivalentForBlocklist(), blockedConstraintMatches(), detectEmptyMarketplaceReason(), doesSourceMatchHostPattern(), extractGitHubRepoFromGitUrl(), extractHostFromSource(), formatFailureErrors(), formatFailureNames() (+7 more)

### Community 47 - "Community 47"
Cohesion: 0.26
Nodes (22): addToolContentEvent(), createSpanAttributes(), endHookSpan(), endInteractionSpan(), endLLMRequestSpan(), endToolBlockedOnUserSpan(), endToolExecutionSpan(), endToolSpan() (+14 more)

### Community 48 - "Community 48"
Cohesion: 0.12
Nodes (1): TaskOutput

### Community 49 - "Community 49"
Cohesion: 0.14
Nodes (6): cacheKeys(), cacheToObject(), cloneFileStateCache(), createFileStateCacheWithSizeLimit(), FileStateCache, mergeFileStateCaches()

### Community 50 - "Community 50"
Cohesion: 0.15
Nodes (9): configureGlobalAgents(), createAxiosInstance(), createHttpsProxyAgent(), getAWSClientProxyConfig(), getProxyFetchOptions(), getProxyUrl(), getWebSocketProxyAgent(), getWebSocketProxyUrl() (+1 more)

### Community 51 - "Community 51"
Cohesion: 0.14
Nodes (7): buildParsedCommandFromRoot(), doParse(), extractPipePositions(), extractRedirectionNodes(), RegexParsedCommand_DEPRECATED, TreeSitterParsedCommand, visitNodes()

### Community 52 - "Community 52"
Cohesion: 0.21
Nodes (17): addToken(), detectCommandSubstitution(), extractOutputRedirections(), filterControlOperators(), generatePlaceholders(), handleFileDescriptorRedirection(), handleRedirection(), hasDangerousExpansion() (+9 more)

### Community 53 - "Community 53"
Cohesion: 0.16
Nodes (12): createITermBackend(), createTmuxBackend(), detectAndGetBackend(), ensureBackendsRegistered(), getBackendByType(), getInProcessBackend(), getPaneBackendExecutor(), getResolvedTeammateMode() (+4 more)

### Community 54 - "Community 54"
Cohesion: 0.2
Nodes (15): getDisabledReasonMessage(), getFastModeRuntimeState(), getFastModeState(), getFastModeUnavailableReason(), getInitialFastModeSetting(), getOverageDisabledMessage(), handleFastModeOverageRejection(), isFastModeAvailable() (+7 more)

### Community 55 - "Community 55"
Cohesion: 0.19
Nodes (17): calculateDeferredToolDescriptionChars(), checkAutoThreshold(), extractDiscoveredToolNames(), getAutoToolSearchCharThreshold(), getAutoToolSearchPercentage(), getAutoToolSearchTokenThreshold(), getToolSearchMode(), getUnsupportedToolReferencePatterns() (+9 more)

### Community 56 - "Community 56"
Cohesion: 0.16
Nodes (13): acquireLock(), AutoUpdaterError, checkGlobalInstallPermissions(), getGcsDistTags(), getInstallationPrefix(), getLatestVersionFromGcs(), getLockFilePath(), getMaxVersion() (+5 more)

### Community 57 - "Community 57"
Cohesion: 0.22
Nodes (16): applyFormatOptimizations(), classifyImageError(), compressImageBlock(), compressImageBuffer(), compressImageBufferWithTokenLimit(), createCompressedImageResult(), createUltraCompressedJPEG(), detectImageFormatFromBase64() (+8 more)

### Community 58 - "Community 58"
Cohesion: 0.13
Nodes (6): getChicagoCoordinateMode(), getChicagoEnabled(), getChicagoSubGates(), hasRequiredSubscription(), readConfig(), DebugLogger

### Community 59 - "Community 59"
Cohesion: 0.17
Nodes (15): checkoutBranch(), checkOutTeleportedSessionBranch(), createTeleportResumeSystemMessage(), createTeleportResumeUserMessage(), ensureUpstreamIsSet(), fetchFromOrigin(), generateTitleAndBranch(), getCurrentBranch() (+7 more)

### Community 60 - "Community 60"
Cohesion: 0.28
Nodes (15): addCleanupResults(), cleanupNpmCacheForAnthropicPackages(), cleanupOldDebugLogs(), cleanupOldFileHistoryBackups(), cleanupOldFilesInDirectory(), cleanupOldMessageFiles(), cleanupOldMessageFilesInBackground(), cleanupOldPlanFiles() (+7 more)

### Community 61 - "Community 61"
Cohesion: 0.21
Nodes (16): convertEffortValueToLevel(), getDefaultEffortForModel(), getDisplayedEffortLevel(), getEffortEnvOverride(), getEffortLevelDescription(), getEffortSuffix(), getEffortValueDescription(), getInitialEffortSetting() (+8 more)

### Community 62 - "Community 62"
Cohesion: 0.12
Nodes (1): EndTruncatingAccumulator

### Community 63 - "Community 63"
Cohesion: 0.26
Nodes (15): analyzeContextUsage(), approximateMessageTokens(), countBuiltInToolTokens(), countCustomAgentTokens(), countMcpToolTokens(), countMemoryFileTokens(), countSkillTokens(), countSlashCommandTokens() (+7 more)

### Community 64 - "Community 64"
Cohesion: 0.26
Nodes (15): checkMcpbChanged(), downloadMcpb(), extractMcpbContents(), generateContentHash(), generateMcpConfig(), getMcpbCacheDir(), getMetadataPath(), isUrl() (+7 more)

### Community 65 - "Community 65"
Cohesion: 0.18
Nodes (10): atomicWriteToZipCache(), collectFilesForZip(), convertDirectoryToZipInPlace(), createZipFromDirectory(), getPluginZipCachePath(), getZipCacheInstalledPluginsPath(), getZipCacheKnownMarketplacesPath(), getZipCacheMarketplacesDir() (+2 more)

### Community 66 - "Community 66"
Cohesion: 0.16
Nodes (5): acquirePaneCreationLock(), getLeaderSessionId(), ITermBackend, parseSplitOutput(), runIt2()

### Community 67 - "Community 67"
Cohesion: 0.25
Nodes (5): ChromeMessageReader, ChromeNativeHost, log(), runChromeNativeHost(), sendChromeMessage()

### Community 68 - "Community 68"
Cohesion: 0.21
Nodes (9): createChromeContext(), createComputerUseMcpServerForCli(), DebugLogger, getChromeBridgeUrl(), isLocalBridge(), isPermissionMode(), runClaudeInChromeMcpServer(), runComputerUseMcpServer() (+1 more)

### Community 69 - "Community 69"
Cohesion: 0.27
Nodes (14): appleScriptQuote(), buildShellCommand(), cmdQuote(), detectLinuxTerminal(), detectMacosTerminal(), detectTerminal(), detectWindowsTerminal(), launchInTerminal() (+6 more)

### Community 70 - "Community 70"
Cohesion: 0.2
Nodes (8): addToInMemoryErrorLog(), attachErrorLogSink(), getErrorLogByIndex(), loadErrorLogs(), loadLogList(), logError(), logMCPDebug(), logMCPError()

### Community 71 - "Community 71"
Cohesion: 0.23
Nodes (13): getEnumLabel(), getEnumLabels(), getEnumValues(), getFormatHint(), getMultiSelectLabel(), getMultiSelectLabels(), getMultiSelectValues(), getZodSchema() (+5 more)

### Community 72 - "Community 72"
Cohesion: 0.24
Nodes (10): applyCommandSuggestion(), createCommandSuggestionItem(), formatCommand(), generateCommandSuggestions(), getBestCommandMatch(), getCommandFuse(), getCommandId(), hasCommandArgs() (+2 more)

### Community 73 - "Community 73"
Cohesion: 0.14
Nodes (2): getAgentId(), isTeamLead()

### Community 74 - "Community 74"
Cohesion: 0.21
Nodes (8): checkTmuxAvailable(), doInitialize(), ensureSocketInitialized(), execTmux(), getClaudeSocketName(), isSocketInitialized(), killTmuxServer(), setClaudeSocketInfo()

### Community 75 - "Community 75"
Cohesion: 0.3
Nodes (12): addCronTask(), getCronFilePath(), hasCronTasksSync(), jitteredNextCronRunMs(), jitterFrac(), listAllCronTasks(), markCronTasksFired(), nextCronRunMs() (+4 more)

### Community 76 - "Community 76"
Cohesion: 0.24
Nodes (8): ansiToPng(), blitGlyph(), blitShade(), chunk(), crc32(), encodePng(), fillBackground(), roundCorners()

### Community 77 - "Community 77"
Cohesion: 0.17
Nodes (2): filterAllowedSdkBetas(), partitionBetasByAllowlist()

### Community 78 - "Community 78"
Cohesion: 0.21
Nodes (6): getDefaultVertexRegion(), getVertexRegionForModel(), isBareMode(), isEnvTruthy(), isRunningOnHomespace(), shouldMaintainProjectWorkingDir()

### Community 79 - "Community 79"
Cohesion: 0.27
Nodes (9): appendToLog(), createJsonlWriter(), extractServerMessage(), getErrorsPath(), getLogWriter(), getMCPLogsPath(), logErrorImpl(), logMCPDebugImpl() (+1 more)

### Community 80 - "Community 80"
Cohesion: 0.28
Nodes (10): copyPlanForFork(), copyPlanForResume(), findFileSnapshotEntry(), getPlan(), getPlanFilePath(), getPlanSlug(), getSlugFromLog(), persistFileSnapshotIfRemote() (+2 more)

### Community 81 - "Community 81"
Cohesion: 0.26
Nodes (10): fanOut(), getSourceForPath(), getWatchTargets(), handleAdd(), handleChange(), handleDelete(), initialize(), notifyChange() (+2 more)

### Community 82 - "Community 82"
Cohesion: 0.18
Nodes (3): AntSlowLogger, buildDescription(), callerFrame()

### Community 83 - "Community 83"
Cohesion: 0.23
Nodes (7): animatedMove(), moveAndSettle(), readClipboardViaPbpaste(), releasePressed(), typeViaClipboard(), withModifiers(), writeClipboardViaPbcopy()

### Community 84 - "Community 84"
Cohesion: 0.26
Nodes (9): formatFileSize(), formatLogMetadata(), formatNumber(), formatRelativeTime(), formatRelativeTimeAgo(), formatResetText(), formatResetTime(), formatTokens() (+1 more)

### Community 85 - "Community 85"
Cohesion: 0.17
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 0.35
Nodes (11): getContentSizeEstimate(), getMaxMcpOutputChars(), getMaxMcpOutputTokens(), getTruncationMessage(), isImageBlock(), isTextBlock(), mcpContentNeedsTruncation(), truncateContentBlocks() (+3 more)

### Community 87 - "Community 87"
Cohesion: 0.33
Nodes (11): detectSessionFileType(), detectSessionPatternType(), isAgentMemFile(), isAutoManagedMemoryFile(), isAutoManagedMemoryPattern(), isAutoMemFile(), isMemoryDirectory(), isShellCommandTargetingMemory() (+3 more)

### Community 88 - "Community 88"
Cohesion: 0.35
Nodes (10): acquireProcessLifetimeLock(), cleanupStaleLocks(), getAllLockInfo(), isClaudeProcess(), isLockActive(), isProcessRunning(), readLockContent(), tryAcquireLock() (+2 more)

### Community 89 - "Community 89"
Cohesion: 0.24
Nodes (8): cellContentToToolResult(), extractImage(), getToolResultFromCell(), isLargeOutputs(), processCell(), processOutput(), processOutputText(), readNotebook()

### Community 90 - "Community 90"
Cohesion: 0.3
Nodes (9): collectMarkdown(), detectManifestType(), formatZodErrors(), validateComponentFile(), validateHooksJson(), validateManifest(), validateMarketplaceManifest(), validatePluginContents() (+1 more)

### Community 91 - "Community 91"
Cohesion: 0.35
Nodes (9): aggregateClaudeCodeStats(), aggregateClaudeCodeStatsForRange(), cacheToStats(), calculateStreaks(), extractShotCountFromMessages(), getAllSessionFiles(), getEmptyStats(), processedStatsToClaudeCodeStats() (+1 more)

### Community 92 - "Community 92"
Cohesion: 0.27
Nodes (8): fetchChannels(), findReusableCacheEntry(), findSlackClient(), getSlackChannelSuggestions(), hasSlackMcpServer(), mcpQueryFor(), parseChannels(), unwrapResults()

### Community 93 - "Community 93"
Cohesion: 0.32
Nodes (10): findAvailableTask(), formatAsTeammateMessage(), formatTaskAsPrompt(), runInProcessTeammate(), sendIdleNotification(), sendMessageToLeader(), startInProcessTeammate(), tryClaimNextTask() (+2 more)

### Community 94 - "Community 94"
Cohesion: 0.32
Nodes (2): getTerminalPanelSocket(), TerminalPanel

### Community 95 - "Community 95"
Cohesion: 0.24
Nodes (1): ActivityManager

### Community 96 - "Community 96"
Cohesion: 0.38
Nodes (10): buildCommandParts(), containsControlStructure(), findFirstPipeOperator(), isCommandSeparator(), isEnvironmentVariableAssignment(), isOperator(), joinContinuationLines(), quoteWithEvalStdinRedirect() (+2 more)

### Community 97 - "Community 97"
Cohesion: 0.29
Nodes (6): getCommandPrefixStatic(), getCompoundCommandPrefixesStatic(), handleWrapper(), isKnownSubcommand(), longestCommonPrefix(), toArray()

### Community 98 - "Community 98"
Cohesion: 0.36
Nodes (10): analyzeCommand(), buildPositionSet(), collectQuoteSpans(), dropContainedSpans(), extractCompoundStructure(), extractDangerousPatterns(), extractQuoteContext(), hasActualOperatorNodes() (+2 more)

### Community 99 - "Community 99"
Cohesion: 0.29
Nodes (8): createWrapperScript(), getNativeMessagingHostsDirs(), installChromeNativeHostManifest(), isChromeExtensionInstalled(), isChromeExtensionInstalled_CACHED_MAY_BE_STALE(), registerWindowsNativeHosts(), setupClaudeInChrome(), shouldAutoEnableClaudeInChrome()

### Community 100 - "Community 100"
Cohesion: 0.42
Nodes (9): checkComputerUseLock(), getLockPath(), isComputerUseLock(), isProcessRunning(), readLock(), registerLockCleanup(), releaseComputerUseLock(), tryAcquireComputerUseLock() (+1 more)

### Community 101 - "Community 101"
Cohesion: 0.42
Nodes (10): ensureDeepLinkProtocolRegistered(), isProtocolHandlerCurrent(), linuxDesktopPath(), linuxExecLine(), registerLinux(), registerMacos(), registerProtocolHandler(), registerWindows() (+2 more)

### Community 102 - "Community 102"
Cohesion: 0.29
Nodes (6): isFullscreenActive(), isFullscreenEnvEnabled(), isTmuxControlMode(), isTmuxControlModeEnvHeuristic(), maybeGetTmuxMouseHint(), probeTmuxControlModeSync()

### Community 103 - "Community 103"
Cohesion: 0.25
Nodes (6): cleanupTerminalModes(), CleanupTimeoutError, forceExit(), gracefulShutdown(), gracefulShutdownSync(), printResumeHint()

### Community 104 - "Community 104"
Cohesion: 0.24
Nodes (5): addFunctionHook(), addHookToSession(), addSessionHook(), convertToHookMatchers(), getSessionHooks()

### Community 105 - "Community 105"
Cohesion: 0.33
Nodes (7): cacheImagePath(), ensureImageStoreDir(), evictOldestIfAtCap(), getImagePath(), getImageStoreDir(), storeImage(), storeImages()

### Community 106 - "Community 106"
Cohesion: 0.27
Nodes (8): downloadAndVerifyBinary(), downloadVersion(), downloadVersionFromArtifactory(), downloadVersionFromBinaryRepo(), getLatestVersion(), getLatestVersionFromArtifactory(), getLatestVersionFromBinaryRepo(), StallTimeoutError

### Community 107 - "Community 107"
Cohesion: 0.36
Nodes (10): cleanupOrphanedPluginVersionsInBackground(), clearAllCaches(), clearAllPluginCaches(), getInstalledVersionPaths(), getOrphanedAtPath(), markPluginVersionOrphaned(), processOrphanedPluginVersion(), readSubdirs() (+2 more)

### Community 108 - "Community 108"
Cohesion: 0.29
Nodes (7): extractFromServerConfigRecord(), extractLspInfoFromManifest(), getLspPluginsFromMarketplaces(), getMatchingLspPlugins(), isLspRecommendationsDisabled(), isOfficialMarketplace(), isRecord()

### Community 109 - "Community 109"
Cohesion: 0.31
Nodes (8): addPluginScopeToServers(), buildMcpUserConfig(), getPluginMcpServers(), loadChannelUserConfig(), loadMcpServersFromFile(), loadMcpServersFromMcpb(), loadPluginMcpServers(), resolvePluginMcpEnvironment()

### Community 110 - "Community 110"
Cohesion: 0.35
Nodes (10): executeForkedSlashCommand(), formatCommandInput(), formatCommandLoadingMetadata(), formatSkillLoadingMetadata(), formatSlashCommandLoadingMetadata(), getMessagesForPromptSlashCommand(), getMessagesForSlashCommand(), looksLikeCommand() (+2 more)

### Community 111 - "Community 111"
Cohesion: 0.29
Nodes (7): codesignRipgrepIfNecessary(), ripGrep(), ripgrepCommand(), ripGrepFileCount(), ripGrepRaw(), ripGrepStream(), RipgrepTimeoutError

### Community 112 - "Community 112"
Cohesion: 0.18
Nodes (0): 

### Community 113 - "Community 113"
Cohesion: 0.18
Nodes (0): 

### Community 114 - "Community 114"
Cohesion: 0.18
Nodes (1): PaneBackendExecutor

### Community 115 - "Community 115"
Cohesion: 0.36
Nodes (9): doesMostRecentAssistantMessageExceed200k(), finalContextTokensFromLastResponse(), getAssistantMessageId(), getCurrentUsage(), getTokenCountFromUsage(), getTokenUsage(), messageTokenCountFromLastAPIResponse(), tokenCountFromLastAPIResponse() (+1 more)

### Community 116 - "Community 116"
Cohesion: 0.27
Nodes (6): contentToText(), ExitPlanModeScanner, extractApprovedPlan(), extractTeleportPlan(), pollForApprovedExitPlanMode(), UltraplanPollError

### Community 117 - "Community 117"
Cohesion: 0.31
Nodes (1): QueryGuard

### Community 118 - "Community 118"
Cohesion: 0.36
Nodes (5): canUserConfigureAdvisor(), getAdvisorConfig(), getExperimentAdvisorModels(), getInitialAdvisorSetting(), isAdvisorEnabled()

### Community 119 - "Community 119"
Cohesion: 0.4
Nodes (9): findLastStringToken(), getBashCompletionCommand(), getCompletionsForShell(), getCompletionTypeFromPrefix(), getShellCompletions(), getZshCompletionCommand(), isCommandOperator(), isNewCommandContext() (+1 more)

### Community 120 - "Community 120"
Cohesion: 0.2
Nodes (0): 

### Community 121 - "Community 121"
Cohesion: 0.22
Nodes (2): extractClaudeCodeHints(), firstCommandToken()

### Community 122 - "Community 122"
Cohesion: 0.38
Nodes (9): countConcurrentSessions(), envSessionKind(), getSessionsDir(), isBgSession(), registerSession(), updatePidFile(), updateSessionActivity(), updateSessionBridgeId() (+1 more)

### Community 123 - "Community 123"
Cohesion: 0.29
Nodes (5): getFsImplementation(), getPathsForPermissionCheck(), isDuplicatePath(), resolveDeepestExistingAncestorSync(), safeResolvePath()

### Community 124 - "Community 124"
Cohesion: 0.36
Nodes (6): emit(), emitHookProgress(), emitHookResponse(), emitHookStarted(), shouldEmit(), startHookProgressInterval()

### Community 125 - "Community 125"
Cohesion: 0.33
Nodes (8): applySortAndLimit(), gatherAllCandidates(), gatherProjectCandidates(), listCandidates(), listSessionsImpl(), parseSessionInfoFromLite(), readAllAndSort(), readCandidate()

### Community 126 - "Community 126"
Cohesion: 0.29
Nodes (7): findMarkdownFilesNative(), getProjectDirsUpToHome(), loadMarkdownFiles(), parseAgentToolsFromFrontmatter(), parseSlashCommandToolsFromFrontmatter(), parseToolListString(), resolveStopBoundary()

### Community 127 - "Community 127"
Cohesion: 0.36
Nodes (9): calculateCostFromTokens(), calculateUSDCost(), formatModelPricing(), formatPrice(), getModelCosts(), getModelPricingString(), getOpus46CostTier(), tokensToUSDCost() (+1 more)

### Community 128 - "Community 128"
Cohesion: 0.31
Nodes (6): getModeColor(), getModeConfig(), permissionModeShortTitle(), permissionModeSymbol(), permissionModeTitle(), toExternalPermissionMode()

### Community 129 - "Community 129"
Cohesion: 0.36
Nodes (8): addPermissionRulesToSettings(), getEmptyPermissionSettingsJson(), getPermissionRulesForSource(), getSettingsForSourceLenient_FOR_EDITING_ONLY_NOT_FOR_READING(), loadAllPermissionRulesFromDisk(), settingsJsonToRules(), shouldAllowManagedPermissionRulesOnly(), shouldShowAlwaysAllowOptions()

### Community 130 - "Community 130"
Cohesion: 0.36
Nodes (7): collectMarkdownFiles(), createPluginCommand(), getCommandNameFromFile(), isSkillFile(), loadCommandsFromDirectory(), loadSkillsFromDirectory(), transformPluginSkillFiles()

### Community 131 - "Community 131"
Cohesion: 0.44
Nodes (8): addFlaggedPlugin(), getFlaggedPluginsPath(), loadFlaggedPlugins(), markFlaggedPluginsSeen(), parsePluginsData(), readFromDisk(), removeFlaggedPlugin(), writeToDisk()

### Community 132 - "Community 132"
Cohesion: 0.33
Nodes (7): clearIdleTimer(), registerSessionActivityCallback(), startHeartbeatTimer(), startIdleTimer(), startSessionActivity(), stopSessionActivity(), unregisterSessionActivityCallback()

### Community 133 - "Community 133"
Cohesion: 0.22
Nodes (2): formatZodError(), validateSettingsFileContent()

### Community 134 - "Community 134"
Cohesion: 0.2
Nodes (1): InProcessBackend

### Community 135 - "Community 135"
Cohesion: 0.29
Nodes (5): applyTaskOffsetsAndEvictions(), enqueueTaskNotification(), generateTaskAttachments(), getStatusText(), pollTasks()

### Community 136 - "Community 136"
Cohesion: 0.25
Nodes (1): CircularBuffer

### Community 137 - "Community 137"
Cohesion: 0.39
Nodes (7): countMemoryFileAccessFromEntries(), countUserPromptsFromEntries(), countUserPromptsInMessages(), getEnhancedPRAttribution(), getPRAttributionData(), getTranscriptStats(), isTerminalOutput()

### Community 138 - "Community 138"
Cohesion: 0.33
Nodes (1): AwsAuthStatusManager

### Community 139 - "Community 139"
Cohesion: 0.28
Nodes (3): checkGithubAppInstalled(), checkGithubTokenSynced(), checkRepoForRemoteAccess()

### Community 140 - "Community 140"
Cohesion: 0.47
Nodes (7): getContextWindowForModel(), getMaxThinkingTokensForModel(), getModelMaxOutputTokens(), getSonnet1mExpTreatmentEnabled(), has1mContext(), is1mContextDisabled(), modelSupports1M()

### Community 141 - "Community 141"
Cohesion: 0.42
Nodes (8): detectConfigurationIssues(), detectLinuxGlobPatternWarnings(), detectMultipleInstallations(), getCurrentInstallationType(), getDoctorDiagnostic(), getInstallationPath(), getInvokedBinary(), getNormalizedPaths()

### Community 142 - "Community 142"
Cohesion: 0.25
Nodes (2): parseFrontmatter(), quoteProblematicValues()

### Community 143 - "Community 143"
Cohesion: 0.33
Nodes (5): parseJSONL(), parseJSONLBuffer(), parseJSONLBun(), parseJSONLString(), readJSONLFile()

### Community 144 - "Community 144"
Cohesion: 0.36
Nodes (7): applyMarkdown(), configureMarked(), formatToken(), getListNumber(), linkifyIssueReferences(), numberToLetter(), numberToRoman()

### Community 145 - "Community 145"
Cohesion: 0.33
Nodes (7): applyPermissionUpdate(), applyPermissionUpdates(), extractRules(), hasRules(), persistPermissionUpdate(), persistPermissionUpdates(), supportsPersistence()

### Community 146 - "Community 146"
Cohesion: 0.22
Nodes (0): 

### Community 147 - "Community 147"
Cohesion: 0.36
Nodes (7): escapeRuleContent(), findFirstUnescapedChar(), findLastUnescapedChar(), normalizeLegacyToolName(), permissionRuleValueFromString(), permissionRuleValueToString(), unescapeRuleContent()

### Community 148 - "Community 148"
Cohesion: 0.39
Nodes (7): deletePluginDataDir(), getPluginDataDir(), getPluginDataDirSize(), getPluginsDirectory(), getPluginsDirectoryName(), pluginDataDirPath(), sanitizePluginId()

### Community 149 - "Community 149"
Cohesion: 0.31
Nodes (5): clearPluginOptionsCache(), deletePluginOptions(), getPluginStorageId(), getUnconfiguredOptions(), savePluginOptions()

### Community 150 - "Community 150"
Cohesion: 0.44
Nodes (8): countNewlines(), indexOfWithin(), normalizeCRLF(), openForScan(), readCapped(), readEditContext(), scanForContext(), sliceContext()

### Community 151 - "Community 151"
Cohesion: 0.28
Nodes (4): FileTooLargeError, readFileInRange(), readFileInRangeFast(), readFileInRangeStreaming()

### Community 152 - "Community 152"
Cohesion: 0.25
Nodes (2): isIt2CliAvailable(), verifyIt2Setup()

### Community 153 - "Community 153"
Cohesion: 0.31
Nodes (4): createTeammatePaneInSwarmView(), enablePaneBorderStatus(), getBackend(), sendCommandToPane()

### Community 154 - "Community 154"
Cohesion: 0.46
Nodes (7): checkAutoCompactDisabled(), checkLargeToolResults(), checkMemoryBloat(), checkNearCapacity(), checkReadResultBloat(), generateContextSuggestions(), getLargeToolSuggestion()

### Community 155 - "Community 155"
Cohesion: 0.39
Nodes (5): detectCurrentRepository(), detectCurrentRepositoryWithHost(), looksLikeRealHostname(), parseGitHubRepository(), parseGitRemote()

### Community 156 - "Community 156"
Cohesion: 0.32
Nodes (3): consumeEarlyInput(), processChunk(), stopCapturingEarlyInput()

### Community 157 - "Community 157"
Cohesion: 0.25
Nodes (0): 

### Community 158 - "Community 158"
Cohesion: 0.36
Nodes (4): captureHooksConfigSnapshot(), getHooksConfigFromSnapshot(), getHooksFromAllowedSources(), updateHooksConfigSnapshot()

### Community 159 - "Community 159"
Cohesion: 0.5
Nodes (7): expandIPv6Groups(), extractMappedIPv4(), isBlockedAddress(), isBlockedV4(), isBlockedV6(), ssrfError(), ssrfGuardedLookup()

### Community 160 - "Community 160"
Cohesion: 0.32
Nodes (3): firstGrapheme(), getGraphemeSegmenter(), lastGrapheme()

### Community 161 - "Community 161"
Cohesion: 0.32
Nodes (1): Mailbox

### Community 162 - "Community 162"
Cohesion: 0.32
Nodes (1): WebSocketTransport

### Community 163 - "Community 163"
Cohesion: 0.36
Nodes (4): applyBedrockRegionPrefix(), extractModelIdFromArn(), getBedrockRegionPrefix(), isFoundationModel()

### Community 164 - "Community 164"
Cohesion: 0.46
Nodes (6): applyModelOverrides(), ensureModelStringsInitialized(), getBedrockModelStrings(), getBuiltinModelStrings(), getModelStrings(), initModelStrings()

### Community 165 - "Community 165"
Cohesion: 0.25
Nodes (0): 

### Community 166 - "Community 166"
Cohesion: 0.29
Nodes (2): qualifyDependency(), verifyAndDemote()

### Community 167 - "Community 167"
Cohesion: 0.5
Nodes (7): addPluginScopeToLspServers(), extractLspServersFromPlugins(), getPluginLspServers(), loadLspServersFromManifest(), loadPluginLspServers(), resolvePluginLspEnvironment(), validatePathWithinPlugin()

### Community 168 - "Community 168"
Cohesion: 0.29
Nodes (2): updatePlugins(), updatePluginsForMarketplaces()

### Community 169 - "Community 169"
Cohesion: 0.36
Nodes (5): handleEPIPE(), registerProcessOutputErrorHandlers(), writeOut(), writeToStderr(), writeToStdout()

### Community 170 - "Community 170"
Cohesion: 0.43
Nodes (7): endQueryProfile(), getPhaseSummary(), getQueryProfileReport(), getSlowWarning(), logQueryProfileReport(), queryCheckpoint(), startQueryProfile()

### Community 171 - "Community 171"
Cohesion: 0.25
Nodes (0): 

### Community 172 - "Community 172"
Cohesion: 0.64
Nodes (7): buildPrefix(), calculateDepth(), findFirstSubcommand(), flagTakesArg(), isKnownSubcommand(), shouldStopAtArg(), toArray()

### Community 173 - "Community 173"
Cohesion: 0.25
Nodes (0): 

### Community 174 - "Community 174"
Cohesion: 0.39
Nodes (6): detectFromColorFgBg(), getSystemThemeName(), hexComponent(), parseOscRgb(), resolveThemeSetting(), themeFromOscColor()

### Community 175 - "Community 175"
Cohesion: 0.25
Nodes (0): 

### Community 176 - "Community 176"
Cohesion: 0.43
Nodes (4): consumeInvokingRequestId(), getAgentContext(), getSubagentLogName(), isSubagentContext()

### Community 177 - "Community 177"
Cohesion: 0.48
Nodes (5): containsHeredoc(), containsMultilineString(), hasStdinRedirect(), quoteShellCommand(), shouldAddStdinRedirect()

### Community 178 - "Community 178"
Cohesion: 0.29
Nodes (0): 

### Community 179 - "Community 179"
Cohesion: 0.48
Nodes (4): filterAppsForDescription(), sanitizeAppNames(), sanitizeCore(), sanitizeTrustedNames()

### Community 180 - "Community 180"
Cohesion: 0.38
Nodes (4): buildSessionContext(), getOrBind(), runPermissionDialog(), tuc()

### Community 181 - "Community 181"
Cohesion: 0.33
Nodes (2): expandField(), parseCronExpression()

### Community 182 - "Community 182"
Cohesion: 0.38
Nodes (3): detectJetBrainsIDEFromParentProcessAsync(), getTerminalWithJetBrainsDetectionAsync(), initJetBrainsDetection()

### Community 183 - "Community 183"
Cohesion: 0.48
Nodes (5): findModifiedFiles(), getEntryParentPath(), hasParentPath(), hasPath(), logDebug()

### Community 184 - "Community 184"
Cohesion: 0.48
Nodes (5): execHttpHook(), getHttpHookPolicy(), getSandboxProxyConfig(), interpolateEnvVars(), sanitizeHeaderValue()

### Community 185 - "Community 185"
Cohesion: 0.52
Nodes (6): applyConfigEnvironmentVariables(), applySafeConfigEnvironmentVariables(), filterSettingsEnv(), withoutCcdSpawnEnvKeys(), withoutHostManagedProviderVars(), withoutSSHTunnelVars()

### Community 186 - "Community 186"
Cohesion: 0.62
Nodes (6): getCacheDir(), getCachePath(), getModelCapability(), isModelCapabilitiesEligible(), refreshModelCapabilities(), sortForMatching()

### Community 187 - "Community 187"
Cohesion: 0.29
Nodes (0): 

### Community 188 - "Community 188"
Cohesion: 0.57
Nodes (6): detectUnreachableRules(), formatSource(), generateFixSuggestion(), isAllowRuleShadowedByAskRule(), isAllowRuleShadowedByDenyRule(), isSharedSettingSource()

### Community 189 - "Community 189"
Cohesion: 0.38
Nodes (3): hasWildcards(), parsePermissionRule(), permissionRuleExtractPrefix()

### Community 190 - "Community 190"
Cohesion: 0.33
Nodes (2): getPluginAffectingSettingsSnapshot(), setupPluginHookHotReload()

### Community 191 - "Community 191"
Cohesion: 0.48
Nodes (5): readMarketplaceJsonContent(), readZipCacheKnownMarketplaces(), saveMarketplaceJsonToZipCache(), syncMarketplacesToZipCache(), writeZipCacheKnownMarketplaces()

### Community 192 - "Community 192"
Cohesion: 0.43
Nodes (4): getReport(), getStartupPerfLogPath(), logStartupPerf(), profileReport()

### Community 193 - "Community 193"
Cohesion: 0.48
Nodes (5): accumulateToolUses(), categorizeToolName(), createEmptyToolCounts(), createStreamlinedTransformer(), getToolSummaryText()

### Community 194 - "Community 194"
Cohesion: 0.29
Nodes (0): 

### Community 195 - "Community 195"
Cohesion: 0.29
Nodes (0): 

### Community 196 - "Community 196"
Cohesion: 0.43
Nodes (3): HighlightSegmenter, reduceCodes(), segmentTextByHighlights()

### Community 197 - "Community 197"
Cohesion: 0.48
Nodes (5): truncate(), truncatePathMiddle(), truncateStartToWidth(), truncateToWidth(), truncateToWidthNoEllipsis()

### Community 198 - "Community 198"
Cohesion: 0.52
Nodes (6): findKeywordTriggerPositions(), findUltraplanTriggerPositions(), findUltrareviewTriggerPositions(), hasUltraplanKeyword(), hasUltrareviewKeyword(), replaceUltraplanKeyword()

### Community 199 - "Community 199"
Cohesion: 0.6
Nodes (5): getApiKeyFromFileDescriptor(), getCredentialFromFd(), getOAuthTokenFromFileDescriptor(), maybePersistTokenForSubprocesses(), readTokenFromWellKnownFile()

### Community 200 - "Community 200"
Cohesion: 0.4
Nodes (2): quote(), tryQuoteShellArgs()

### Community 201 - "Community 201"
Cohesion: 0.47
Nodes (3): drainRunLoop(), release(), retain()

### Community 202 - "Community 202"
Cohesion: 0.6
Nodes (5): checkAgentDescriptions(), checkClaudeMdFiles(), checkContextWarnings(), checkMcpTools(), checkUnreachableRules()

### Community 203 - "Community 203"
Cohesion: 0.33
Nodes (1): FileReadCache

### Community 204 - "Community 204"
Cohesion: 0.33
Nodes (0): 

### Community 205 - "Community 205"
Cohesion: 0.33
Nodes (0): 

### Community 206 - "Community 206"
Cohesion: 0.4
Nodes (2): createSkillImprovementHook(), initSkillImprovement()

### Community 207 - "Community 207"
Cohesion: 0.33
Nodes (1): WindowsToWSLConverter

### Community 208 - "Community 208"
Cohesion: 0.6
Nodes (5): check(), getLockfile(), lock(), lockSync(), unlock()

### Community 209 - "Community 209"
Cohesion: 0.47
Nodes (3): aliasMatchesParentTier(), getAgentModel(), getDefaultSubagentModel()

### Community 210 - "Community 210"
Cohesion: 0.6
Nodes (5): familyHasSpecificEntries(), isModelAllowed(), modelBelongsToFamily(), modelMatchesVersionPrefix(), prefixMatchesModel()

### Community 211 - "Community 211"
Cohesion: 0.33
Nodes (0): 

### Community 212 - "Community 212"
Cohesion: 0.33
Nodes (0): 

### Community 213 - "Community 213"
Cohesion: 0.33
Nodes (0): 

### Community 214 - "Community 214"
Cohesion: 0.33
Nodes (0): 

### Community 215 - "Community 215"
Cohesion: 0.4
Nodes (2): extractBashToolsFromMessages(), extractCliName()

### Community 216 - "Community 216"
Cohesion: 0.4
Nodes (2): spawnSecurity(), startKeychainPrefetch()

### Community 217 - "Community 217"
Cohesion: 0.6
Nodes (4): getFilePathFromInput(), getSessionFileTypeFromInput(), handleSessionFileAccess(), isMemoryFileAccess()

### Community 218 - "Community 218"
Cohesion: 0.53
Nodes (4): findPowerShell(), getCachedPowerShellPath(), getPowerShellEdition(), probePath()

### Community 219 - "Community 219"
Cohesion: 0.4
Nodes (2): captureTeammateModeSnapshot(), getTeammateModeFromSnapshot()

### Community 220 - "Community 220"
Cohesion: 0.4
Nodes (2): getEmailAsync(), initUser()

### Community 221 - "Community 221"
Cohesion: 0.4
Nodes (0): 

### Community 222 - "Community 222"
Cohesion: 0.5
Nodes (2): extractTranscript(), logContainsQuery()

### Community 223 - "Community 223"
Cohesion: 0.5
Nodes (2): parseArguments(), substituteArguments()

### Community 224 - "Community 224"
Cohesion: 0.4
Nodes (0): 

### Community 225 - "Community 225"
Cohesion: 0.4
Nodes (0): 

### Community 226 - "Community 226"
Cohesion: 0.5
Nodes (2): increment(), processBlock()

### Community 227 - "Community 227"
Cohesion: 0.6
Nodes (3): parseAndValidateManifestFromBytes(), parseAndValidateManifestFromText(), validateManifest()

### Community 228 - "Community 228"
Cohesion: 0.6
Nodes (3): getFrequentlyModifiedFiles(), isCoreFile(), pickDiverseCoreFiles()

### Community 229 - "Community 229"
Cohesion: 0.7
Nodes (4): detectEncodingForResolvedPath(), detectLineEndingsForString(), readFileSync(), readFileSyncWithMetadata()

### Community 230 - "Community 230"
Cohesion: 0.5
Nodes (2): next(), returnValue()

### Community 231 - "Community 231"
Cohesion: 0.5
Nodes (2): clearHeadlessMarks(), headlessProfilerStartTurn()

### Community 232 - "Community 232"
Cohesion: 0.7
Nodes (4): calculatePercentiles(), generateHeatmap(), getHeatmapChar(), getIntensity()

### Community 233 - "Community 233"
Cohesion: 0.4
Nodes (0): 

### Community 234 - "Community 234"
Cohesion: 0.5
Nodes (3): ImageSizeError, isBase64ImageBlock(), validateImagesForAPI()

### Community 235 - "Community 235"
Cohesion: 0.5
Nodes (2): handlePlanApprovalResponse(), setAwaitingPlanApproval()

### Community 236 - "Community 236"
Cohesion: 0.4
Nodes (0): 

### Community 237 - "Community 237"
Cohesion: 0.4
Nodes (0): 

### Community 238 - "Community 238"
Cohesion: 0.7
Nodes (4): extractConversationContext(), formatToolInput(), generatePermissionExplanation(), isPermissionExplainerEnabled()

### Community 239 - "Community 239"
Cohesion: 0.4
Nodes (0): 

### Community 240 - "Community 240"
Cohesion: 0.6
Nodes (3): extractHost(), isOfficialRepo(), logPluginFetch()

### Community 241 - "Community 241"
Cohesion: 0.7
Nodes (4): extractPrefixFromElement(), getCommandPrefixStatic(), getCompoundCommandPrefixesStatic(), wordAlignedLCP()

### Community 242 - "Community 242"
Cohesion: 0.6
Nodes (3): getPrivacyLevel(), isEssentialTrafficOnly(), isTelemetryDisabled()

### Community 243 - "Community 243"
Cohesion: 0.7
Nodes (4): editFileInEditor(), editPromptInEditor(), isGuiEditor(), recollapsePastedContent()

### Community 244 - "Community 244"
Cohesion: 0.4
Nodes (0): 

### Community 245 - "Community 245"
Cohesion: 0.6
Nodes (3): getSessionIngressAuthHeaders(), getSessionIngressAuthToken(), getTokenFromFileDescriptor()

### Community 246 - "Community 246"
Cohesion: 0.4
Nodes (0): 

### Community 247 - "Community 247"
Cohesion: 0.5
Nodes (2): fireRawRead(), startMdmRawRead()

### Community 248 - "Community 248"
Cohesion: 0.8
Nodes (4): countUnescapedChar(), hasUnescapedEmptyParens(), isEscaped(), validatePermissionRule()

### Community 249 - "Community 249"
Cohesion: 0.5
Nodes (2): validateFlagArgument(), validateFlags()

### Community 250 - "Community 250"
Cohesion: 0.5
Nodes (2): getShellHistoryCommands(), getShellHistoryCompletion()

### Community 251 - "Community 251"
Cohesion: 0.4
Nodes (0): 

### Community 252 - "Community 252"
Cohesion: 0.5
Nodes (2): parseBudgetMatch(), parseTokenBudget()

### Community 253 - "Community 253"
Cohesion: 0.5
Nodes (2): formatError(), getErrorParts()

### Community 254 - "Community 254"
Cohesion: 0.6
Nodes (3): computeSearchText(), renderableSearchText(), toolResultSearchText()

### Community 255 - "Community 255"
Cohesion: 0.83
Nodes (3): ansiToSvg(), get256Color(), parseAnsi()

### Community 256 - "Community 256"
Cohesion: 0.5
Nodes (0): 

### Community 257 - "Community 257"
Cohesion: 0.5
Nodes (0): 

### Community 258 - "Community 258"
Cohesion: 0.67
Nodes (2): openBrowser(), validateUrl()

### Community 259 - "Community 259"
Cohesion: 0.5
Nodes (0): 

### Community 260 - "Community 260"
Cohesion: 0.5
Nodes (0): 

### Community 261 - "Community 261"
Cohesion: 0.5
Nodes (0): 

### Community 262 - "Community 262"
Cohesion: 0.67
Nodes (2): getCwd(), pwd()

### Community 263 - "Community 263"
Cohesion: 0.83
Nodes (3): extractDebugCategories(), shouldShowDebugCategories(), shouldShowDebugMessage()

### Community 264 - "Community 264"
Cohesion: 0.67
Nodes (2): containsControlChars(), parseDeepLink()

### Community 265 - "Community 265"
Cohesion: 0.83
Nodes (3): handleDeepLinkUri(), handleUrlSchemeLaunch(), resolveCwd()

### Community 266 - "Community 266"
Cohesion: 0.5
Nodes (0): 

### Community 267 - "Community 267"
Cohesion: 0.67
Nodes (2): execFileNoThrow(), execFileNoThrowWithCwd()

### Community 268 - "Community 268"
Cohesion: 0.67
Nodes (2): renderMessagesToPlainText(), streamRenderedMessages()

### Community 269 - "Community 269"
Cohesion: 0.83
Nodes (3): formatBriefTimestamp(), getLocale(), startOfDay()

### Community 270 - "Community 270"
Cohesion: 0.5
Nodes (1): FpsTracker

### Community 271 - "Community 271"
Cohesion: 0.83
Nodes (3): applyGrouping(), getToolsWithGrouping(), getToolUseInfo()

### Community 272 - "Community 272"
Cohesion: 0.5
Nodes (0): 

### Community 273 - "Community 273"
Cohesion: 0.5
Nodes (0): 

### Community 274 - "Community 274"
Cohesion: 0.5
Nodes (0): 

### Community 275 - "Community 275"
Cohesion: 0.5
Nodes (0): 

### Community 276 - "Community 276"
Cohesion: 0.83
Nodes (3): getAntModelOverrideConfig(), getAntModels(), resolveAntModel()

### Community 277 - "Community 277"
Cohesion: 0.83
Nodes (3): checkOpus1mAccess(), checkSonnet1mAccess(), isExtraUsageEnabled()

### Community 278 - "Community 278"
Cohesion: 0.67
Nodes (2): getAPIProvider(), getAPIProviderForStatsig()

### Community 279 - "Community 279"
Cohesion: 0.83
Nodes (3): get3PFallbackSuggestion(), handleValidationError(), validateModel()

### Community 280 - "Community 280"
Cohesion: 0.5
Nodes (0): 

### Community 281 - "Community 281"
Cohesion: 0.83
Nodes (3): canCycleToAuto(), cyclePermissionMode(), getNextPermissionMode()

### Community 282 - "Community 282"
Cohesion: 0.5
Nodes (0): 

### Community 283 - "Community 283"
Cohesion: 0.5
Nodes (0): 

### Community 284 - "Community 284"
Cohesion: 0.5
Nodes (0): 

### Community 285 - "Community 285"
Cohesion: 0.67
Nodes (2): formatMs(), formatTimelineLine()

### Community 286 - "Community 286"
Cohesion: 0.67
Nodes (2): isSlashCommand(), processQueueIfReady()

### Community 287 - "Community 287"
Cohesion: 0.5
Nodes (0): 

### Community 288 - "Community 288"
Cohesion: 0.5
Nodes (0): 

### Community 289 - "Community 289"
Cohesion: 0.5
Nodes (0): 

### Community 290 - "Community 290"
Cohesion: 0.67
Nodes (2): extractSideQuestionResponse(), runSideQuestion()

### Community 291 - "Community 291"
Cohesion: 0.5
Nodes (0): 

### Community 292 - "Community 292"
Cohesion: 0.67
Nodes (2): filterStartCodes(), sliceAnsi()

### Community 293 - "Community 293"
Cohesion: 0.67
Nodes (2): installStreamJsonStdoutGuard(), isJsonLine()

### Community 294 - "Community 294"
Cohesion: 0.5
Nodes (0): 

### Community 295 - "Community 295"
Cohesion: 0.83
Nodes (3): base58Encode(), toTaggedId(), uuidToBigInt()

### Community 296 - "Community 296"
Cohesion: 0.5
Nodes (0): 

### Community 297 - "Community 297"
Cohesion: 0.67
Nodes (2): renderTruncatedContent(), wrapText()

### Community 298 - "Community 298"
Cohesion: 0.67
Nodes (2): applyCoordinatorToolFilter(), mergeAndFilterTools()

### Community 299 - "Community 299"
Cohesion: 0.67
Nodes (2): isUndercover(), shouldShowUndercoverAutoNotice()

### Community 300 - "Community 300"
Cohesion: 1.0
Nodes (2): isAgentSwarmsEnabled(), isAgentTeamsFlagSet()

### Community 301 - "Community 301"
Cohesion: 0.67
Nodes (0): 

### Community 302 - "Community 302"
Cohesion: 0.67
Nodes (0): 

### Community 303 - "Community 303"
Cohesion: 0.67
Nodes (0): 

### Community 304 - "Community 304"
Cohesion: 0.67
Nodes (0): 

### Community 305 - "Community 305"
Cohesion: 1.0
Nodes (2): applyExtraCACertsFromConfig(), getExtraCertsPathFromConfig()

### Community 306 - "Community 306"
Cohesion: 0.67
Nodes (0): 

### Community 307 - "Community 307"
Cohesion: 0.67
Nodes (0): 

### Community 308 - "Community 308"
Cohesion: 1.0
Nodes (2): collapseBackgroundBashNotifications(), isCompletedBackgroundBash()

### Community 309 - "Community 309"
Cohesion: 1.0
Nodes (2): collapseHookSummaries(), isLabeledHookSummary()

### Community 310 - "Community 310"
Cohesion: 1.0
Nodes (2): collapseTeammateShutdowns(), isTeammateShutdownAttachment()

### Community 311 - "Community 311"
Cohesion: 0.67
Nodes (0): 

### Community 312 - "Community 312"
Cohesion: 0.67
Nodes (0): 

### Community 313 - "Community 313"
Cohesion: 0.67
Nodes (0): 

### Community 314 - "Community 314"
Cohesion: 1.0
Nodes (2): deriveReviewState(), fetchPrStatus()

### Community 315 - "Community 315"
Cohesion: 0.67
Nodes (0): 

### Community 316 - "Community 316"
Cohesion: 0.67
Nodes (0): 

### Community 317 - "Community 317"
Cohesion: 0.67
Nodes (0): 

### Community 318 - "Community 318"
Cohesion: 1.0
Nodes (2): getAvailableUpgrade(), getUpgradeMessage()

### Community 319 - "Community 319"
Cohesion: 1.0
Nodes (2): getDeprecatedModelInfo(), getModelDeprecationWarning()

### Community 320 - "Community 320"
Cohesion: 0.67
Nodes (0): 

### Community 321 - "Community 321"
Cohesion: 0.67
Nodes (0): 

### Community 322 - "Community 322"
Cohesion: 1.0
Nodes (2): detectAndUninstallDelistedPlugins(), detectDelistedPlugins()

### Community 323 - "Community 323"
Cohesion: 0.67
Nodes (0): 

### Community 324 - "Community 324"
Cohesion: 1.0
Nodes (2): buildSideQuestionFallbackParams(), fetchSystemPromptParts()

### Community 325 - "Community 325"
Cohesion: 1.0
Nodes (2): getBaseRenderOptions(), getStdinOverride()

### Community 326 - "Community 326"
Cohesion: 1.0
Nodes (2): partiallySanitizeUnicode(), recursivelySanitizeUnicode()

### Community 327 - "Community 327"
Cohesion: 0.67
Nodes (0): 

### Community 328 - "Community 328"
Cohesion: 0.67
Nodes (0): 

### Community 329 - "Community 329"
Cohesion: 0.67
Nodes (0): 

### Community 330 - "Community 330"
Cohesion: 1.0
Nodes (2): extractFirstUserMessageText(), sideQuery()

### Community 331 - "Community 331"
Cohesion: 0.67
Nodes (0): 

### Community 332 - "Community 332"
Cohesion: 0.67
Nodes (0): 

### Community 333 - "Community 333"
Cohesion: 0.67
Nodes (0): 

### Community 334 - "Community 334"
Cohesion: 0.67
Nodes (0): 

### Community 335 - "Community 335"
Cohesion: 1.0
Nodes (2): buildEffectiveSystemPrompt(), isProactiveActive_SAFE_TO_CALL_ANYWHERE()

### Community 336 - "Community 336"
Cohesion: 1.0
Nodes (2): formatTaskOutput(), getMaxTaskOutputLength()

### Community 337 - "Community 337"
Cohesion: 0.67
Nodes (0): 

### Community 338 - "Community 338"
Cohesion: 1.0
Nodes (2): _bundleWithFallback(), createAndUploadGitBundle()

### Community 339 - "Community 339"
Cohesion: 0.67
Nodes (0): 

### Community 340 - "Community 340"
Cohesion: 1.0
Nodes (2): getDefaultBashTimeoutMs(), getMaxBashTimeoutMs()

### Community 341 - "Community 341"
Cohesion: 0.67
Nodes (0): 

### Community 342 - "Community 342"
Cohesion: 0.67
Nodes (0): 

### Community 343 - "Community 343"
Cohesion: 0.67
Nodes (0): 

### Community 344 - "Community 344"
Cohesion: 0.67
Nodes (0): 

### Community 345 - "Community 345"
Cohesion: 1.0
Nodes (2): escapeXml(), escapeXmlAttr()

### Community 346 - "Community 346"
Cohesion: 1.0
Nodes (0): 

### Community 347 - "Community 347"
Cohesion: 1.0
Nodes (0): 

### Community 348 - "Community 348"
Cohesion: 1.0
Nodes (0): 

### Community 349 - "Community 349"
Cohesion: 1.0
Nodes (0): 

### Community 350 - "Community 350"
Cohesion: 1.0
Nodes (0): 

### Community 351 - "Community 351"
Cohesion: 1.0
Nodes (0): 

### Community 352 - "Community 352"
Cohesion: 1.0
Nodes (0): 

### Community 353 - "Community 353"
Cohesion: 1.0
Nodes (0): 

### Community 354 - "Community 354"
Cohesion: 1.0
Nodes (0): 

### Community 355 - "Community 355"
Cohesion: 1.0
Nodes (0): 

### Community 356 - "Community 356"
Cohesion: 1.0
Nodes (0): 

### Community 357 - "Community 357"
Cohesion: 1.0
Nodes (0): 

### Community 358 - "Community 358"
Cohesion: 1.0
Nodes (0): 

### Community 359 - "Community 359"
Cohesion: 1.0
Nodes (0): 

### Community 360 - "Community 360"
Cohesion: 1.0
Nodes (0): 

### Community 361 - "Community 361"
Cohesion: 1.0
Nodes (0): 

### Community 362 - "Community 362"
Cohesion: 1.0
Nodes (0): 

### Community 363 - "Community 363"
Cohesion: 1.0
Nodes (0): 

### Community 364 - "Community 364"
Cohesion: 1.0
Nodes (0): 

### Community 365 - "Community 365"
Cohesion: 1.0
Nodes (0): 

### Community 366 - "Community 366"
Cohesion: 1.0
Nodes (0): 

### Community 367 - "Community 367"
Cohesion: 1.0
Nodes (0): 

### Community 368 - "Community 368"
Cohesion: 1.0
Nodes (0): 

### Community 369 - "Community 369"
Cohesion: 1.0
Nodes (0): 

### Community 370 - "Community 370"
Cohesion: 1.0
Nodes (0): 

### Community 371 - "Community 371"
Cohesion: 1.0
Nodes (0): 

### Community 372 - "Community 372"
Cohesion: 1.0
Nodes (0): 

### Community 373 - "Community 373"
Cohesion: 1.0
Nodes (0): 

### Community 374 - "Community 374"
Cohesion: 1.0
Nodes (0): 

### Community 375 - "Community 375"
Cohesion: 1.0
Nodes (0): 

### Community 376 - "Community 376"
Cohesion: 1.0
Nodes (0): 

### Community 377 - "Community 377"
Cohesion: 1.0
Nodes (0): 

### Community 378 - "Community 378"
Cohesion: 1.0
Nodes (0): 

### Community 379 - "Community 379"
Cohesion: 1.0
Nodes (0): 

### Community 380 - "Community 380"
Cohesion: 1.0
Nodes (0): 

### Community 381 - "Community 381"
Cohesion: 1.0
Nodes (0): 

### Community 382 - "Community 382"
Cohesion: 1.0
Nodes (0): 

### Community 383 - "Community 383"
Cohesion: 1.0
Nodes (0): 

### Community 384 - "Community 384"
Cohesion: 1.0
Nodes (0): 

### Community 385 - "Community 385"
Cohesion: 1.0
Nodes (0): 

### Community 386 - "Community 386"
Cohesion: 1.0
Nodes (0): 

### Community 387 - "Community 387"
Cohesion: 1.0
Nodes (0): 

### Community 388 - "Community 388"
Cohesion: 1.0
Nodes (0): 

### Community 389 - "Community 389"
Cohesion: 1.0
Nodes (0): 

### Community 390 - "Community 390"
Cohesion: 1.0
Nodes (0): 

### Community 391 - "Community 391"
Cohesion: 1.0
Nodes (0): 

### Community 392 - "Community 392"
Cohesion: 1.0
Nodes (0): 

### Community 393 - "Community 393"
Cohesion: 1.0
Nodes (0): 

### Community 394 - "Community 394"
Cohesion: 1.0
Nodes (0): 

### Community 395 - "Community 395"
Cohesion: 1.0
Nodes (0): 

### Community 396 - "Community 396"
Cohesion: 1.0
Nodes (0): 

### Community 397 - "Community 397"
Cohesion: 1.0
Nodes (0): 

### Community 398 - "Community 398"
Cohesion: 1.0
Nodes (0): 

### Community 399 - "Community 399"
Cohesion: 1.0
Nodes (0): 

### Community 400 - "Community 400"
Cohesion: 1.0
Nodes (0): 

### Community 401 - "Community 401"
Cohesion: 1.0
Nodes (0): 

### Community 402 - "Community 402"
Cohesion: 1.0
Nodes (0): 

### Community 403 - "Community 403"
Cohesion: 1.0
Nodes (0): 

### Community 404 - "Community 404"
Cohesion: 1.0
Nodes (0): 

### Community 405 - "Community 405"
Cohesion: 1.0
Nodes (0): 

### Community 406 - "Community 406"
Cohesion: 1.0
Nodes (0): 

### Community 407 - "Community 407"
Cohesion: 1.0
Nodes (0): 

### Community 408 - "Community 408"
Cohesion: 1.0
Nodes (0): 

### Community 409 - "Community 409"
Cohesion: 1.0
Nodes (0): 

### Community 410 - "Community 410"
Cohesion: 1.0
Nodes (0): 

### Community 411 - "Community 411"
Cohesion: 1.0
Nodes (0): 

### Community 412 - "Community 412"
Cohesion: 1.0
Nodes (0): 

### Community 413 - "Community 413"
Cohesion: 1.0
Nodes (0): 

### Community 414 - "Community 414"
Cohesion: 1.0
Nodes (0): 

### Community 415 - "Community 415"
Cohesion: 1.0
Nodes (0): 

### Community 416 - "Community 416"
Cohesion: 1.0
Nodes (0): 

### Community 417 - "Community 417"
Cohesion: 1.0
Nodes (0): 

### Community 418 - "Community 418"
Cohesion: 1.0
Nodes (0): 

### Community 419 - "Community 419"
Cohesion: 1.0
Nodes (0): 

### Community 420 - "Community 420"
Cohesion: 1.0
Nodes (0): 

### Community 421 - "Community 421"
Cohesion: 1.0
Nodes (0): 

### Community 422 - "Community 422"
Cohesion: 1.0
Nodes (0): 

### Community 423 - "Community 423"
Cohesion: 1.0
Nodes (0): 

### Community 424 - "Community 424"
Cohesion: 1.0
Nodes (0): 

### Community 425 - "Community 425"
Cohesion: 1.0
Nodes (0): 

### Community 426 - "Community 426"
Cohesion: 1.0
Nodes (0): 

### Community 427 - "Community 427"
Cohesion: 1.0
Nodes (0): 

### Community 428 - "Community 428"
Cohesion: 1.0
Nodes (0): 

### Community 429 - "Community 429"
Cohesion: 1.0
Nodes (0): 

### Community 430 - "Community 430"
Cohesion: 1.0
Nodes (0): 

### Community 431 - "Community 431"
Cohesion: 1.0
Nodes (0): 

### Community 432 - "Community 432"
Cohesion: 1.0
Nodes (0): 

### Community 433 - "Community 433"
Cohesion: 1.0
Nodes (0): 

### Community 434 - "Community 434"
Cohesion: 1.0
Nodes (0): 

### Community 435 - "Community 435"
Cohesion: 1.0
Nodes (0): 

### Community 436 - "Community 436"
Cohesion: 1.0
Nodes (0): 

### Community 437 - "Community 437"
Cohesion: 1.0
Nodes (0): 

### Community 438 - "Community 438"
Cohesion: 1.0
Nodes (0): 

### Community 439 - "Community 439"
Cohesion: 1.0
Nodes (0): 

### Community 440 - "Community 440"
Cohesion: 1.0
Nodes (0): 

### Community 441 - "Community 441"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **4 isolated node(s):** `GcpCredentialsTimeoutError`, `AutoUpdaterError`, `MalformedCommandError`, `TelemetryTimeoutError`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 346`** (2 nodes): `apiPreconnect.ts`, `preconnectAnthropicApi()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 347`** (2 nodes): `remoteSession.ts`, `checkBackgroundRemoteSessionEligibility()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 348`** (2 nodes): `backgroundHousekeeping.ts`, `startBackgroundHousekeeping()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 349`** (2 nodes): `shellPrefix.ts`, `formatShellPrefixCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 350`** (2 nodes): `index.ts`, `getSecureStorage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 351`** (2 nodes): `bufferedWriter.ts`, `createBufferedWriter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 352`** (2 nodes): `caCerts.ts`, `clearCACertsCache()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 353`** (2 nodes): `classifierApprovalsHook.ts`, `useIsClassifierChecking()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 354`** (2 nodes): `prompt.ts`, `getChromeSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 355`** (2 nodes): `combinedAbortSignal.ts`, `createCombinedAbortSignal()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 356`** (2 nodes): `inputLoader.ts`, `requireComputerUseInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 357`** (2 nodes): `swiftLoader.ts`, `requireComputerUseSwift()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 358`** (2 nodes): `contentArray.ts`, `insertBlockAfterToolResults()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 359`** (2 nodes): `controlMessageCompat.ts`, `normalizeControlMessageKeys()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 360`** (2 nodes): `cronJitterConfig.ts`, `getCronJitterConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 361`** (2 nodes): `terminalPreference.ts`, `updateDeepLinkTerminalPreference()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 362`** (2 nodes): `envValidation.ts`, `validateBoundedIntEnvVar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 363`** (2 nodes): `execFileNoThrowPortable.ts`, `execSyncWithDefaults_DEPRECATED()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 364`** (2 nodes): `execSyncWrapper.ts`, `execSync_DEPRECATED()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 365`** (2 nodes): `extraUsage.ts`, `isBilledAsExtraUsage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 366`** (2 nodes): `findExecutable.ts`, `findExecutable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 367`** (2 nodes): `getWorktreePathsPortable.ts`, `getWorktreePathsPortable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 368`** (2 nodes): `gitSettings.ts`, `shouldIncludeGitInstructions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 369`** (2 nodes): `ghAuthStatus.ts`, `getGhAuthStatus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 370`** (2 nodes): `highlightMatch.tsx`, `highlightMatch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (2 nodes): `registerFrontmatterHooks.ts`, `registerFrontmatterHooks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 372`** (2 nodes): `registerSkillHooks.ts`, `registerSkillHooks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 373`** (2 nodes): `horizontalScroll.ts`, `calculateHorizontalScrollWindow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 374`** (2 nodes): `hyperlink.ts`, `createHyperlink()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 375`** (2 nodes): `idleTimeout.ts`, `createIdleTimeoutManager()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (2 nodes): `immediateCommand.ts`, `shouldInferenceConfigCommandBeImmediate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 377`** (2 nodes): `ink.ts`, `toInkColor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 378`** (2 nodes): `jsonRead.ts`, `stripBOM()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 379`** (2 nodes): `keyboardShortcuts.ts`, `isMacosOptionChar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 380`** (2 nodes): `lazySchema.ts`, `lazySchema()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 381`** (2 nodes): `managedEnvConstants.ts`, `isProviderManagedEnvVar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 382`** (2 nodes): `versions.ts`, `projectIsInGitRepo()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 383`** (2 nodes): `messagePredicates.ts`, `isHumanTurn()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 384`** (2 nodes): `objectGroupBy.ts`, `objectGroupBy()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 385`** (2 nodes): `peerAddress.ts`, `parseAddress()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 386`** (2 nodes): `PermissionPromptToolResultSchema.ts`, `permissionPromptToolResultToPermissionDecision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 387`** (2 nodes): `PermissionResult.ts`, `getRuleBehaviorDescription()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 388`** (2 nodes): `classifierDecision.ts`, `isAutoModeAllowlistedTool()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 389`** (2 nodes): `platform.ts`, `detectVcs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 390`** (2 nodes): `headlessPluginInstall.ts`, `installPluginsForHeadless()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 391`** (2 nodes): `managedPlugins.ts`, `getManagedPluginNames()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 392`** (2 nodes): `performStartupChecks.tsx`, `performStartupChecks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 393`** (2 nodes): `pluginPolicy.ts`, `isPluginBlockedByPolicy()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 394`** (2 nodes): `dangerousCmdlets.ts`, `aliasesOf()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 395`** (2 nodes): `sandbox-ui-utils.ts`, `removeSandboxViolationTags()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 396`** (2 nodes): `fallbackStorage.ts`, `createFallbackStorage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 397`** (2 nodes): `semanticBoolean.ts`, `semanticBoolean()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 398`** (2 nodes): `semanticNumber.ts`, `semanticNumber()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 399`** (2 nodes): `sequential.ts`, `sequential()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 400`** (2 nodes): `allErrors.ts`, `getSettingsWithAllErrors()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 401`** (2 nodes): `applySettingsChange.ts`, `applySettingsChange()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 402`** (2 nodes): `schemaOutput.ts`, `generateSettingsJSONSchema()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 403`** (2 nodes): `validateEditTool.ts`, `validateInputForSettingsFileEdit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 404`** (2 nodes): `validationTips.ts`, `getValidationTip()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 405`** (2 nodes): `outputLimits.ts`, `getMaxOutputLength()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 406`** (2 nodes): `resolveDefaultShell.ts`, `resolveDefaultShell()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 407`** (2 nodes): `shellToolUtils.ts`, `isPowerShellToolEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 408`** (2 nodes): `signal.ts`, `createSignal()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 409`** (2 nodes): `sinks.ts`, `initSinks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 410`** (2 nodes): `slashCommandParsing.ts`, `parseSlashCommand()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 411`** (2 nodes): `standaloneAgent.ts`, `getStandaloneAgentName()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (2 nodes): `statusNoticeHelpers.ts`, `getAgentDescriptionsTotalTokens()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 413`** (2 nodes): `teammateInit.ts`, `initializeTeammateHooks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 414`** (2 nodes): `teammateModel.ts`, `getHardcodedTeammateModelFallback()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 415`** (2 nodes): `systemPromptType.ts`, `asSystemPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 416`** (2 nodes): `sdkProgress.ts`, `emitTaskProgress()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 417`** (2 nodes): `teamDiscovery.ts`, `getTeammateStatuses()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 418`** (2 nodes): `skillLoadedEvent.ts`, `logSkillsLoaded()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 419`** (2 nodes): `environmentSelection.ts`, `getEnvironmentSelectionInfo()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 420`** (2 nodes): `treeify.ts`, `treeify()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 421`** (2 nodes): `unaryLogging.ts`, `logUnaryEvent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 422`** (2 nodes): `userAgent.ts`, `getClaudeCodeUserAgent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 423`** (2 nodes): `withResolvers.ts`, `withResolvers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 424`** (2 nodes): `worktreeModeEnabled.ts`, `isWorktreeModeEnabled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 425`** (2 nodes): `yaml.ts`, `parseYaml()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 426`** (2 nodes): `zodToJsonSchema.ts`, `zodToJsonSchema()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 427`** (1 nodes): `alias.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 428`** (1 nodes): `nohup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 429`** (1 nodes): `pyright.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 430`** (1 nodes): `srun.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 431`** (1 nodes): `time.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 432`** (1 nodes): `timeout.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 433`** (1 nodes): `configConstants.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 434`** (1 nodes): `configs.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 435`** (1 nodes): `modelSupportOverrides.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `PermissionRule.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 437`** (1 nodes): `PermissionUpdateSchema.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 438`** (1 nodes): `dangerousPatterns.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (1 nodes): `officialMarketplace.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 440`** (1 nodes): `shellProvider.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 441`** (1 nodes): `teammatePromptAddendum.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 46 inferred relationships involving `mk()` (e.g. with `checkBudget()` and `sliceBytes()`) actually correct?**
  _`mk()` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `peek()` (e.g. with `nextToken()` and `parseCommand()`) actually correct?**
  _`peek()` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `skipBlanks()` (e.g. with `advance()` and `nextToken()`) actually correct?**
  _`skipBlanks()` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `advance()` (e.g. with `skipBlanks()` and `nextToken()`) actually correct?**
  _`advance()` has 35 INFERRED edges - model-reasoned connections that need verification._
- **What connects `GcpCredentialsTimeoutError`, `AutoUpdaterError`, `MalformedCommandError` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._