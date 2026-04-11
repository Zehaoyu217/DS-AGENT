# Graph Report - /Users/jay/Developer/claude-code-agent/src/cli  (2026-04-09)

## Corpus Check
- 19 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 215 nodes · 287 edges · 20 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 91 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `CCRClient` - 25 edges
2. `WebSocketTransport` - 22 edges
3. `StructuredIO` - 20 edges
4. `SSETransport` - 16 edges
5. `SerialBatchEventUploader` - 12 edges
6. `HybridTransport` - 10 edges
7. `WorkerStateUploader` - 7 edges
8. `runHeadless()` - 6 edges
9. `RemoteIO` - 6 edges
10. `handleMarketplaceError()` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (2): exitWithMessage(), StructuredIO

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (1): CCRClient

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (1): WebSocketTransport

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (11): emitLoadError(), getCanUseToolFn(), getStructuredIO(), handleMcpSetServers(), handleRewindFiles(), loadInitialMessages(), reconcileMcpServers(), removeInterruptedMessage() (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (3): convertSSEUrlToPostUrl(), parseSSEFrames(), SSETransport

### Community 5 - "Community 5"
Cohesion: 0.19
Nodes (2): RetryableError, SerialBatchEventUploader

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (7): handleMarketplaceError(), marketplaceAddHandler(), marketplaceListHandler(), marketplaceRemoveHandler(), marketplaceUpdateHandler(), pluginValidateHandler(), printValidationResult()

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (2): convertWsUrlToPostUrl(), HybridTransport

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (2): checkMcpServerHealth(), mcpGetHandler()

### Community 9 - "Community 9"
Cohesion: 0.36
Nodes (2): coalescePatches(), WorkerStateUploader

### Community 10 - "Community 10"
Cohesion: 0.32
Nodes (4): accumulateStreamEvents(), CCRInitError, clearStreamAccumulatorForMessage(), scopeKey()

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (1): RemoteIO

### Community 12 - "Community 12"
Cohesion: 0.53
Nodes (5): autoModeConfigHandler(), autoModeCritiqueHandler(), autoModeDefaultsHandler(), formatRulesForCritique(), writeRules()

### Community 13 - "Community 13"
Cohesion: 0.5
Nodes (2): authLogin(), installOAuthTokens()

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (2): agentsHandler(), formatAgent()

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (2): escapeJsLineTerminators(), ndjsonSafeStringify()

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 17`** (2 nodes): `util.tsx`, `setupTokenHandler()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (2 nodes): `transportUtils.ts`, `getTransportForUrl()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (2 nodes): `update.ts`, `update()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CCRClient` connect `Community 1` to `Community 10`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._