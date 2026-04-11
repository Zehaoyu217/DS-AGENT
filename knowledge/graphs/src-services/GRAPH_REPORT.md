# Graph Report - /Users/jay/Developer/claude-code-agent/src/services  (2026-04-09)

## Corpus Check
- 136 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1183 nodes · 1820 edges · 114 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 734 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `FirstPartyEventLoggingExporter` - 24 edges
2. `ClaudeAuthProvider` - 22 edges
3. `getServerKey()` - 20 edges
4. `StreamingToolExecutor` - 19 edges
5. `DiagnosticTrackingService` - 15 edges
6. `AuthCodeListener` - 15 edges
7. `startSpeculation()` - 11 edges
8. `getAssistantMessageFromError()` - 11 edges
9. `fetchAndLoadPolicyLimits()` - 11 edges
10. `compactConversation()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `buildMagicDocsUpdatePrompt()` --calls--> `substituteVariables()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/services/MagicDocs/prompts.ts → /Users/jay/Developer/claude-code-agent/src/services/SessionMemory/prompts.ts
- `_resetPolicyLimitsForTesting()` --calls--> `stopBackgroundPolling()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/services/policyLimits/index.ts → /Users/jay/Developer/claude-code-agent/src/services/remoteManagedSettings/index.ts
- `computeChecksum()` --calls--> `sortKeysDeep()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/services/policyLimits/index.ts → /Users/jay/Developer/claude-code-agent/src/services/remoteManagedSettings/index.ts
- `startBackgroundPolling()` --calls--> `isPolicyLimitsEligible()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/services/remoteManagedSettings/index.ts → /Users/jay/Developer/claude-code-agent/src/services/policyLimits/index.ts
- `fetchPolicyLimits()` --calls--> `getAuthHeaders()`  [INFERRED]
  /Users/jay/Developer/claude-code-agent/src/services/policyLimits/index.ts → /Users/jay/Developer/claude-code-agent/src/services/teamMemorySync/index.ts

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (63): applyRemoteEntriesToLocal(), attachAnalyticsSink(), batchDeltaByBytes(), buildEntriesFromLocalFiles(), clearPolicyLimitsCache(), clearRemoteManagedSettingsCache(), computeChecksum(), computeChecksumFromSettings() (+55 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (47): buildFetch(), callIdeRpc(), callMCPTool(), clearMcpAuthCache(), clearServerCache(), computeDomainSeparator(), computeStructHash(), configureApiKeyHeaders() (+39 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (43): addMcpConfig(), addScopeToServers(), commandArraysMatch(), dedupClaudeAiMcpServers(), dedupPluginMcpServers(), deriveAddress(), expandEnvVars(), filterMcpServersByPolicy() (+35 more)

### Community 3 - "Community 3"
Cohesion: 0.1
Nodes (16): AuthenticationCancelledError, ClaudeAuthProvider, clearMcpClientConfig(), clearServerTokensFromLocalStorage(), createAuthFetch(), fetchAuthServerMetadata(), getMcpClientConfig(), getScopeFromMetadata() (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (25): base64URLEncode(), generateCodeChallenge(), generateCodeVerifier(), generateState(), camelToSnakeCase(), flushLogs(), getFlushIntervalMs(), scheduleFlush() (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (23): addCacheBreakpoints(), assistantMessageToMessageParam(), cleanupStream(), clearStreamIdleTimers(), configureEffortParams(), configureTaskBudgetParams(), getAPIMetadata(), getCacheControl() (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (24): checkGate_CACHED_OR_BLOCKING(), checkSecurityRestrictionGate(), checkStatsigFeatureGate_CACHED_MAY_BE_STALE(), getApiBaseUrlHost(), getConfigOverrides(), getDynamicConfig_BLOCKS_ON_INIT(), getDynamicConfig_CACHED_MAY_BE_STALE(), getEnvOverrides() (+16 more)

### Community 7 - "Community 7"
Cohesion: 0.18
Nodes (3): FirstPartyEventLoggingExporter, getAxiosErrorContext(), getStorageDir()

### Community 8 - "Community 8"
Cohesion: 0.1
Nodes (11): excludeCommandsByServer(), excludeResourcesByServer(), excludeStalePluginClients(), excludeToolsByServer(), extractAgentMcpServers(), getMcpServerScopeFromToolName(), isHTTPConfig(), isMcpTool() (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (17): CannotRetryError, FallbackTriggeredError, getDefaultMaxRetries(), getMaxRetries(), getRetryAfter(), getRetryAfterMs(), handleAwsCredentialError(), handleGcpCredentialError() (+9 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (16): get3PModelFallbackSuggestion(), getAssistantMessageFromError(), getImageTooLargeErrorMessage(), getOauthOrgNotAllowedErrorMessage(), getPdfInvalidErrorMessage(), getPdfPasswordProtectedErrorMessage(), getPdfTooLargeErrorMessage(), getPromptTooLongTokenGap() (+8 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (11): addExceededLimit(), applyMockHeaders(), checkMockFastModeRateLimit(), clearMockEarlyWarning(), clearMockHeaders(), getMockHeaders(), setMockEarlyWarning(), setMockHeader() (+3 more)

### Community 12 - "Community 12"
Cohesion: 0.15
Nodes (2): markToolUseAsComplete(), StreamingToolExecutor

### Community 13 - "Community 13"
Cohesion: 0.24
Nodes (17): abortSpeculation(), acceptSpeculation(), copyOverlayToMain(), countToolsInMessages(), createSpeculationFeedbackMessage(), generatePipelinedSuggestion(), getBoundaryDetail(), getBoundaryTool() (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.22
Nodes (16): addErrorNotificationIfNeeded(), annotateBoundaryWithPreservedSegment(), collectReadToolFilePaths(), compactConversation(), createAsyncAgentAttachmentsIfNeeded(), createCompactCanUseTool(), createPlanAttachmentIfNeeded(), createPlanModeAttachmentIfNeeded() (+8 more)

### Community 15 - "Community 15"
Cohesion: 0.21
Nodes (16): analyzeSectionSizes(), buildExtractAutoOnlyPrompt(), buildExtractCombinedPrompt(), buildMagicDocsUpdatePrompt(), buildSessionMemoryUpdatePrompt(), flushSessionSection(), generateSectionReminders(), getDefaultUpdatePrompt() (+8 more)

### Community 16 - "Community 16"
Cohesion: 0.21
Nodes (13): buildDiffableContent(), checkResponseForCacheBreak(), computeHash(), computePerToolHashes(), getCacheBreakDiffPath(), getSystemCharCount(), getTrackingKey(), isExcludedModel() (+5 more)

### Community 17 - "Community 17"
Cohesion: 0.17
Nodes (2): DiagnosticsTrackingError, DiagnosticTrackingService

### Community 18 - "Community 18"
Cohesion: 0.21
Nodes (14): assertInstallableScope(), disableAllPluginsOp(), disablePluginOp(), enablePluginOp(), findPluginByIdentifier(), findPluginInSettings(), getPluginInstallationFromV2(), getProjectPathForScope() (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.12
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (14): buildDownloadPath(), downloadAndSaveFile(), downloadFile(), downloadSessionFiles(), getDefaultApiBaseUrl(), listFilesCreatedAfter(), logDebug(), logDebugError() (+6 more)

### Community 21 - "Community 21"
Cohesion: 0.23
Nodes (11): cachedMicrocompactPath(), calculateToolResultTokens(), collectCompactableToolIds(), ensureCachedMCState(), estimateMessageTokens(), evaluateTimeBasedTrigger(), getCachedMCModule(), isMainThreadSource() (+3 more)

### Community 22 - "Community 22"
Cohesion: 0.17
Nodes (1): AuthCodeListener

### Community 23 - "Community 23"
Cohesion: 0.2
Nodes (11): buildProcessMetrics(), extractMcpToolDetails(), extractToolInputForTelemetry(), getAgentIdentification(), getEventMetadata(), getFileExtensionForAnalytics(), getFileExtensionsFromBashCommand(), isAnalyticsToolDetailsLoggingEnabled() (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.28
Nodes (12): cacheExtraUsageDisabledReason(), checkQuotaStatus(), computeNewLimitsFromHeaders(), computeTimeProgress(), emitStatusChange(), extractQuotaStatusFromError(), extractQuotaStatusFromHeaders(), extractRawUtilization() (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.3
Nodes (12): checkRecordingAvailability(), checkVoiceDependencies(), detectPackageManager(), hasCommand(), linuxHasAlsaCards(), loadAudioNapi(), probeArecord(), requestMicrophonePermission() (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (12): bytesPerTokenForFileType(), countMessagesTokensWithAPI(), countTokensViaHaikuFallback(), countTokensWithAPI(), hasThinkingBlocks(), roughTokenCountEstimation(), roughTokenCountEstimationForBlock(), roughTokenCountEstimationForContent() (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.28
Nodes (11): adjustIndexToPreserveAPIInvariants(), calculateMessagesToKeepIndex(), createCompactionResultFromSessionMemory(), getSessionMemoryCompactConfig(), getToolResultIds(), hasTextBlocks(), hasToolUseWithIds(), initSessionMemoryCompactConfig() (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.32
Nodes (8): executePromptSuggestion(), generateSuggestion(), getParentCacheSuppressReason(), getPromptVariant(), getSuggestionSuppressReason(), logSuggestionSuppressed(), shouldFilterSuggestion(), tryGenerateSuggestion()

### Community 29 - "Community 29"
Cohesion: 0.32
Nodes (10): getBatchConfig(), getEnvironmentForGrowthBook(), getEventSamplingConfig(), initialize1PEventLogging(), is1PEventLoggingEnabled(), logEventTo1P(), logEventTo1PAsync(), logGrowthBookExperimentTo1P() (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.24
Nodes (7): addApiRequestToCache(), appendToFile(), createDumpPromptsFetch(), dumpRequest(), getDumpPromptsPath(), hashString(), initFingerprint()

### Community 31 - "Community 31"
Cohesion: 0.23
Nodes (7): countModelVisibleMessagesSince(), drainer(), drainPendingExtraction(), extractWrittenPaths(), getWrittenFilePath(), hasMemoryWritesSince(), isModelVisibleMessage()

### Community 32 - "Community 32"
Cohesion: 0.26
Nodes (8): dehydrateValue(), mapAssistantMessage(), mapMessage(), mapMessages(), shouldUseVCR(), withFixture(), withTokenCountVCR(), withVCR()

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (6): countToolCallsSince(), createMemoryFileCanUseTool(), manuallyExtractSessionMemory(), setupSessionMemoryFile(), shouldExtractMemory(), updateLastSummarizedMessageIdIfSafe()

### Community 34 - "Community 34"
Cohesion: 0.25
Nodes (5): checkCachedPassesEligibility(), fetchAndStorePassesEligibility(), getCachedOrFetchPassesEligibility(), prefetchPassesEligibility(), shouldCheckForPasses()

### Community 35 - "Community 35"
Cohesion: 0.27
Nodes (7): appendSessionLog(), appendSessionLogImpl(), fetchSessionLogsFromUrl(), findLastUuid(), getOrCreateSequentialAppend(), getSessionLogs(), getSessionLogsViaOAuth()

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (2): SdkControlClientTransport, SdkControlServerTransport

### Community 37 - "Community 37"
Cohesion: 0.35
Nodes (9): discoverAuthorizationServer(), discoverProtectedResource(), exchangeJwtAuthGrant(), makeXaaFetch(), normalizeUrl(), performCrossAppAccess(), redactTokens(), requestJwtAuthorizationGrant() (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.33
Nodes (10): buildSchemaNotSentHint(), checkPermissionsAndCallTool(), classifyToolError(), decisionReasonToOTelSource(), findMcpServerConnection(), getMcpServerBaseUrlFromToolName(), getMcpServerType(), getNextImagePasteId() (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.33
Nodes (7): formatLimitReachedText(), getEarlyWarningText(), getLimitReachedText(), getRateLimitErrorMessage(), getRateLimitMessage(), getRateLimitWarning(), getWarningUpsellText()

### Community 40 - "Community 40"
Cohesion: 0.29
Nodes (7): executePush(), isPermanentFailure(), notifyTeamMemoryWrite(), schedulePush(), startFileWatcher(), _startFileWatcherForTesting(), startTeamMemoryWatcher()

### Community 41 - "Community 41"
Cohesion: 0.47
Nodes (8): detectGateway(), getAnthropicEnvMetadata(), getBuildAgeMinutes(), getErrorMessage(), logAPIError(), logAPIQuery(), logAPISuccess(), logAPISuccessAndDuration()

### Community 42 - "Community 42"
Cohesion: 0.28
Nodes (4): getLspServerManager(), initializeLspServerManager(), isLspConnected(), reinitializeLspServerManager()

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (7): extractConnectionErrorDetails(), extractNestedErrorMessage(), formatAPIError(), getSSLErrorHint(), hasNestedError(), sanitizeAPIError(), sanitizeMessageHTML()

### Community 44 - "Community 44"
Cohesion: 0.46
Nodes (7): disableAllPlugins(), disablePlugin(), enablePlugin(), handlePluginCommandError(), installPlugin(), uninstallPlugin(), updatePluginCli()

### Community 45 - "Community 45"
Cohesion: 0.46
Nodes (7): forceStopPreventSleep(), killCaffeinate(), spawnCaffeinate(), startPreventSleep(), startRestartInterval(), stopPreventSleep(), stopRestartInterval()

### Community 46 - "Community 46"
Cohesion: 0.38
Nodes (3): detectMagicDocHeader(), getMagicDocsAgent(), updateMagicDoc()

### Community 47 - "Community 47"
Cohesion: 0.43
Nodes (5): calculateShouldShowGrove(), checkGroveForNonInteractive(), fetchAndStoreGroveConfig(), isQualifiedForGrove(), markGroveNoticeViewed()

### Community 48 - "Community 48"
Cohesion: 0.48
Nodes (5): getConfig(), initAutoDream(), isForced(), isGateOpen(), makeDreamProgressWatcher()

### Community 49 - "Community 49"
Cohesion: 0.48
Nodes (5): lockPath(), readLastConsolidatedAt(), recordConsolidation(), rollbackConsolidationLock(), tryAcquireConsolidationLock()

### Community 50 - "Community 50"
Cohesion: 0.76
Nodes (6): autoCompactIfNeeded(), calculateTokenWarningState(), getAutoCompactThreshold(), getEffectiveContextWindowSize(), isAutoCompactEnabled(), shouldAutoCompact()

### Community 51 - "Community 51"
Cohesion: 0.33
Nodes (2): createLinkedTransportPair(), InProcessTransport

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (2): hashToId(), shortRequestId()

### Community 53 - "Community 53"
Cohesion: 0.38
Nodes (3): buildMcpToolName(), getMcpPrefix(), getToolNameForPermissionCheck()

### Community 54 - "Community 54"
Cohesion: 0.38
Nodes (1): OAuthService

### Community 55 - "Community 55"
Cohesion: 0.38
Nodes (3): getRemoteManagedSettingsSyncFromCache(), getSettingsPath(), loadSettings()

### Community 56 - "Community 56"
Cohesion: 0.29
Nodes (0): 

### Community 57 - "Community 57"
Cohesion: 0.47
Nodes (3): logEventAsyncImpl(), logEventImpl(), shouldTrackDatadog()

### Community 58 - "Community 58"
Cohesion: 0.4
Nodes (2): checkMetricsEnabled(), refreshMetricsStatus()

### Community 59 - "Community 59"
Cohesion: 0.4
Nodes (2): fetchOverageCreditGrant(), refreshOverageCreditGrantCache()

### Community 60 - "Community 60"
Cohesion: 0.33
Nodes (0): 

### Community 61 - "Community 61"
Cohesion: 0.67
Nodes (5): generateKittyId(), isAppleTerminalBellDisabled(), sendAuto(), sendNotification(), sendToChannel()

### Community 62 - "Community 62"
Cohesion: 0.53
Nodes (4): getCompiledRules(), getSecretLabel(), ruleIdToLabel(), scanForSecrets()

### Community 63 - "Community 63"
Cohesion: 0.5
Nodes (2): formatCompactSummary(), getCompactUserSummaryMessage()

### Community 64 - "Community 64"
Cohesion: 0.6
Nodes (3): findChannelEntry(), gateChannelServer(), getEffectiveChannelAllowlist()

### Community 65 - "Community 65"
Cohesion: 0.5
Nodes (2): normalizeUrl(), prefetchOfficialMcpUrls()

### Community 66 - "Community 66"
Cohesion: 0.4
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 0.4
Nodes (0): 

### Community 68 - "Community 68"
Cohesion: 0.6
Nodes (4): getCustomTips(), getRelevantTips(), isMarketplacePluginRelevant(), isOfficialMarketplaceInstalled()

### Community 69 - "Community 69"
Cohesion: 0.5
Nodes (0): 

### Community 70 - "Community 70"
Cohesion: 0.5
Nodes (0): 

### Community 71 - "Community 71"
Cohesion: 0.5
Nodes (0): 

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (2): getChannelAllowlist(), isChannelAllowlisted()

### Community 73 - "Community 73"
Cohesion: 0.5
Nodes (0): 

### Community 74 - "Community 74"
Cohesion: 0.83
Nodes (3): getMcpHeadersFromHelper(), getMcpServerHeaders(), isMcpServerFromProjectOrLocalSettings()

### Community 75 - "Community 75"
Cohesion: 0.67
Nodes (2): findAvailablePort(), getMcpOAuthCallbackPort()

### Community 76 - "Community 76"
Cohesion: 0.67
Nodes (2): readAutoModeEnabledState(), setupVscodeSdkMcp()

### Community 77 - "Community 77"
Cohesion: 0.67
Nodes (2): getTipToShowOnSpinner(), selectTipWithLongestTimeSinceShown()

### Community 78 - "Community 78"
Cohesion: 0.5
Nodes (0): 

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (3): fileNameWords(), getVoiceKeyterms(), splitIdentifier()

### Community 80 - "Community 80"
Cohesion: 0.67
Nodes (0): 

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (2): fetchBootstrapAPI(), fetchBootstrapData()

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (2): buildAwaySummaryPrompt(), generateAwaySummary()

### Community 83 - "Community 83"
Cohesion: 0.67
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 0.67
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 0.67
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 0.67
Nodes (0): 

### Community 87 - "Community 87"
Cohesion: 0.67
Nodes (0): 

### Community 88 - "Community 88"
Cohesion: 0.67
Nodes (0): 

### Community 89 - "Community 89"
Cohesion: 0.67
Nodes (0): 

### Community 90 - "Community 90"
Cohesion: 0.67
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 0.67
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (0): 

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (0): 

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (0): 

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (0): 

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (0): 

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (0): 

### Community 101 - "Community 101"
Cohesion: 1.0
Nodes (0): 

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (0): 

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (0): 

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (0): 

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (0): 

### Community 106 - "Community 106"
Cohesion: 1.0
Nodes (0): 

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (0): 

### Community 111 - "Community 111"
Cohesion: 1.0
Nodes (0): 

### Community 112 - "Community 112"
Cohesion: 1.0
Nodes (0): 

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **1 isolated node(s):** `DiagnosticsTrackingError`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 92`** (2 nodes): `sinkKillswitch.ts`, `isSinkKilled()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (2 nodes): `firstTokenDate.ts`, `fetchAndStoreClaudeCodeFirstTokenDate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (2 nodes): `ultrareviewQuota.ts`, `fetchUltrareviewQuota()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (2 nodes): `usage.ts`, `fetchUtilization()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (2 nodes): `consolidationPrompt.ts`, `buildConsolidationPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (2 nodes): `claudeAiLimitsHook.ts`, `useClaudeAiLimits()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (2 nodes): `apiMicrocompact.ts`, `getAPIContextManagement()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (2 nodes): `compactWarningHook.ts`, `useCompactWarningSuppression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (2 nodes): `grouping.ts`, `groupMessagesByApiRound()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (2 nodes): `postCompactCleanup.ts`, `runPostCompactCleanup()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (2 nodes): `timeBasedMCConfig.ts`, `getTimeBasedMCConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (2 nodes): `internalLogging.ts`, `logPermissionContextForAnts()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (2 nodes): `LSPClient.ts`, `createLSPClient()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (2 nodes): `LSPServerManager.ts`, `createLSPServerManager()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (2 nodes): `envExpansion.ts`, `expandEnvVarsInString()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (2 nodes): `normalization.ts`, `normalizeNameForMCP()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (2 nodes): `mcpServerApproval.tsx`, `handleMcpjsonServerApprovals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (2 nodes): `teamMemSecretGuard.ts`, `checkTeamMemSecrets()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (2 nodes): `toolHooks.ts`, `resolveHookPermissionDecision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (1 nodes): `emptyUsage.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (1 nodes): `types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 113`** (1 nodes): `securityCheck.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OAuthService` connect `Community 54` to `Community 0`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `getServerKey()` (e.g. with `hasMcpDiscoveryButNoToken()` and `revokeServerTokens()`) actually correct?**
  _`getServerKey()` has 19 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DiagnosticsTrackingError` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._