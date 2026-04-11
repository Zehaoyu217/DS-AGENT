# Graph Report - /Users/jay/Developer/claude-code-agent/src/tasks  (2026-04-09)

## Corpus Check
- 12 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 94 nodes · 108 edges · 11 communities detected
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `markTaskNotified()` - 5 edges
2. `restoreRemoteAgentTasksImpl()` - 5 edges
3. `isLocalAgentTask()` - 4 edges
4. `startStallWatchdog()` - 4 edges
5. `registerMainSessionTask()` - 3 edges
6. `backgroundTask()` - 3 edges
7. `enqueueUltraplanFailureNotification()` - 3 edges
8. `registerRemoteAgentTask()` - 3 edges
9. `startRemoteSessionPolling()` - 3 edges
10. `getAllInProcessTeammateTasks()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (8): backgroundAgentTask(), drainPendingMessages(), getProgressUpdate(), getTokenCountFromTracker(), isLocalAgentTask(), isPanelAgentTask(), killAllRunningAgentTasks(), killAsyncAgent()

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (13): enqueueRemoteNotification(), enqueueRemoteReviewFailureNotification(), enqueueRemoteReviewNotification(), enqueueUltraplanFailureNotification(), getRemoteTaskSessionUrl(), isRemoteTaskType(), markTaskNotified(), persistRemoteAgentMetadata() (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.21
Nodes (5): backgroundAll(), backgroundExistingForegroundTask(), backgroundTask(), spawnShellTask(), startStallWatchdog()

### Community 3 - "Community 3"
Cohesion: 0.36
Nodes (5): completeMainSessionTask(), enqueueMainSessionNotification(), generateMainSessionTaskId(), registerMainSessionTask(), startBackgroundSession()

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (2): getAllInProcessTeammateTasks(), getRunningTeammatesSorted()

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (0): 

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (1): StopTaskError

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): killShellTasksForAgent(), killTask()

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 10`** (2 nodes): `guards.ts`, `isLocalShellTask()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 4 inferred relationships involving `markTaskNotified()` (e.g. with `enqueueRemoteNotification()` and `enqueueUltraplanFailureNotification()`) actually correct?**
  _`markTaskNotified()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `restoreRemoteAgentTasksImpl()` (e.g. with `restoreRemoteAgentTasks()` and `removeRemoteAgentMetadata()`) actually correct?**
  _`restoreRemoteAgentTasksImpl()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `isLocalAgentTask()` (e.g. with `isPanelAgentTask()` and `drainPendingMessages()`) actually correct?**
  _`isLocalAgentTask()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `startStallWatchdog()` (e.g. with `spawnShellTask()` and `backgroundTask()`) actually correct?**
  _`startStallWatchdog()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `registerMainSessionTask()` (e.g. with `generateMainSessionTaskId()` and `startBackgroundSession()`) actually correct?**
  _`registerMainSessionTask()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._