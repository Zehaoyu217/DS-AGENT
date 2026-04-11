# Graph Report - /Users/jay/Developer/claude-code-agent/src/bridge  (2026-04-09)

## Corpus Check
- 32 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 190 nodes · 225 edges · 32 communities detected
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `runBridgeLoop()` - 11 edges
2. `FlushGate` - 8 edges
3. `bridgeMain()` - 6 edges
4. `handleIngressMessage()` - 6 edges
5. `BoundedUUIDSet` - 5 edges
6. `readBridgePointer()` - 5 edges
7. `getBridgeDisabledReason()` - 4 edges
8. `isClaudeAISubscriber()` - 4 edges
9. `stopWorkWithRetry()` - 4 edges
10. `parseArgs()` - 4 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (19): addJitter(), BridgeHeadlessPermanentError, bridgeMain(), createHeadlessBridgeLogger(), fetchSessionTitle(), formatDelay(), isConnectionError(), isMultiSessionSpawnEnabled() (+11 more)

### Community 1 - "Community 1"
Cohesion: 0.21
Nodes (5): BoundedUUIDSet, handleIngressMessage(), isSDKControlRequest(), isSDKControlResponse(), isSDKMessage()

### Community 2 - "Community 2"
Cohesion: 0.24
Nodes (6): getBridgeDisabledReason(), getOauthAccountInfo(), hasProfileScope(), isBridgeEnabled(), isBridgeEnabledBlocking(), isClaudeAISubscriber()

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (0): 

### Community 4 - "Community 4"
Cohesion: 0.28
Nodes (4): BridgeFatalError, extractErrorTypeFromData(), handleErrorStatus(), isExpiredErrorType()

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (1): FlushGate

### Community 6 - "Community 6"
Cohesion: 0.42
Nodes (8): debug(), extractInboundAttachments(), prependPathRefs(), resolveAndPrepend(), resolveInboundAttachments(), resolveOne(), sanitizeFileName(), uploadsDir()

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (2): debugBody(), redactSecrets()

### Community 8 - "Community 8"
Cohesion: 0.57
Nodes (6): clearBridgePointer(), getBridgePointerPath(), readBridgePointer(), readBridgePointerAcrossWorktrees(), safeJsonParse(), writeBridgePointer()

### Community 9 - "Community 9"
Cohesion: 0.38
Nodes (3): extractActivities(), inputPreview(), toolSummary()

### Community 10 - "Community 10"
Cohesion: 0.33
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 0.53
Nodes (4): archiveSession(), initEnvLessBridgeCore(), oauthHeaders(), withRetry()

### Community 12 - "Community 12"
Cohesion: 0.47
Nodes (3): clearTrustedDeviceToken(), getTrustedDeviceToken(), isGateEnabled()

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 0.6
Nodes (4): getBridgeAccessToken(), getBridgeBaseUrl(), getBridgeBaseUrlOverride(), getBridgeTokenOverride()

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 0.5
Nodes (2): decodeJwtExpiry(), decodeJwtPayload()

### Community 17 - "Community 17"
Cohesion: 0.83
Nodes (3): createCodeSession(), fetchRemoteCredentials(), oauthHeaders()

### Community 18 - "Community 18"
Cohesion: 0.83
Nodes (3): checkEnvLessBridgeMinVersion(), getEnvLessBridgeConfig(), shouldShowAppUpgradeMessage()

### Community 19 - "Community 19"
Cohesion: 0.67
Nodes (2): extractInboundMessageFields(), normalizeImageBlocks()

### Community 20 - "Community 20"
Cohesion: 0.83
Nodes (3): getReplBridgeHandle(), getSelfBridgeCompatId(), setReplBridgeHandle()

### Community 21 - "Community 21"
Cohesion: 0.5
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (2): deriveTitle(), initReplBridge()

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (2): initBridgeCore(), startWorkPollLoop()

### Community 25 - "Community 25"
Cohesion: 0.67
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 26`** (2 nodes): `bridgePermissionCallbacks.ts`, `isBridgePermissionResponse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (2 nodes): `capacityWake.ts`, `createCapacityWake()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `pollConfig.ts`, `getPollIntervalConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `stub.ts`, `isBridgeAvailable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `pollConfigDefaults.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 10 inferred relationships involving `runBridgeLoop()` (e.g. with `stopWorkWithRetry()` and `safeSpawn()`) actually correct?**
  _`runBridgeLoop()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `bridgeMain()` (e.g. with `parseArgs()` and `printHelp()`) actually correct?**
  _`bridgeMain()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `handleIngressMessage()` (e.g. with `isSDKControlResponse()` and `isSDKControlRequest()`) actually correct?**
  _`handleIngressMessage()` has 5 INFERRED edges - model-reasoned connections that need verification._