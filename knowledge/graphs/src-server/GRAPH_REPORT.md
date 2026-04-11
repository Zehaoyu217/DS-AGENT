# Graph Report - /Users/jay/Developer/claude-code-agent/src/server  (2026-04-09)

## Corpus Check
- 79 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 484 nodes · 547 edges · 66 communities detected
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `SessionManager` - 17 edges
2. `SessionStore` - 14 edges
3. `SessionStore` - 13 edges
4. `AnalyticsStorage` - 11 edges
5. `ConversationRepository` - 11 edges
6. `MessageRepository` - 10 edges
7. `SessionRepository` - 10 edges
8. `SharedLinkRepository` - 10 edges
9. `UserRepository` - 9 edges
10. `DirectConnectSessionManager` - 9 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (2): SessionManager, UserHourlyRateLimiter

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (13): connect(), getTheme(), getWsUrl(), handleControlMessage(), initTerminal(), manualReconnect(), onDisconnect(), scheduleReconnect() (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (11): auditLog(), logAuthEvent(), logCommandExecution(), logFileAccess(), logPathTraversalBlocked(), logRateLimitExceeded(), sanitizeDetails(), checkDenylist() (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (3): getSession(), getSessionFromRequest(), SessionRepository

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (2): parseCookies(), SessionStore

### Community 5 - "Community 5"
Cohesion: 0.2
Nodes (1): SessionStore

### Community 6 - "Community 6"
Cohesion: 0.21
Nodes (5): connect(), createPostgresConnection(), createSqliteConnection(), getDbType(), getDefaultSqlitePath()

### Community 7 - "Community 7"
Cohesion: 0.3
Nodes (1): AnalyticsStorage

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (4): deleteLastAssistantMessage(), exportConversation(), getConversation(), getMessages()

### Community 9 - "Community 9"
Cohesion: 0.21
Nodes (3): isModuleNotFound(), loadSamlLibrary(), SamlAdapter

### Community 10 - "Community 10"
Cohesion: 0.21
Nodes (1): ConversationRepository

### Community 11 - "Community 11"
Cohesion: 0.24
Nodes (4): registerAnthropicCheck(), registerCheck(), registerDatabaseCheck(), registerRedisCheck()

### Community 12 - "Community 12"
Cohesion: 0.24
Nodes (4): MagicLinkAdapter, readSmtpConfig(), sendBareSmtp(), sendMail()

### Community 13 - "Community 13"
Cohesion: 0.2
Nodes (1): MessageRepository

### Community 14 - "Community 14"
Cohesion: 0.2
Nodes (1): SharedLinkRepository

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (1): DirectConnectSessionManager

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (3): computeCost(), CostTracker, getPricing()

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (2): fetchJSON(), OAuthAdapter

### Community 18 - "Community 18"
Cohesion: 0.24
Nodes (4): ConnectionRateLimiter, extractBearer(), optionalAuth(), requireAuth()

### Community 19 - "Community 19"
Cohesion: 0.27
Nodes (1): UserRepository

### Community 20 - "Community 20"
Cohesion: 0.22
Nodes (1): ApiError

### Community 21 - "Community 21"
Cohesion: 0.39
Nodes (8): FileService, globFiles(), grepFiles(), listDirectory(), readFile(), safePath(), statFile(), writeFile()

### Community 22 - "Community 22"
Cohesion: 0.22
Nodes (1): SSEStream

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (1): ToolUseRepository

### Community 24 - "Community 24"
Cohesion: 0.39
Nodes (6): decrypt(), decryptWithKey(), deriveKey(), encrypt(), encryptWithKey(), rotateEncryption()

### Community 25 - "Community 25"
Cohesion: 0.22
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 0.32
Nodes (1): ApiKeyAdapter

### Community 27 - "Community 27"
Cohesion: 0.43
Nodes (4): buildIndex(), excerpt(), highlight(), searchConversations()

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (2): csrfMiddleware(), parseCookies()

### Community 29 - "Community 29"
Cohesion: 0.38
Nodes (3): hasPermission(), resolveRole(), roleHasPermission()

### Community 30 - "Community 30"
Cohesion: 0.38
Nodes (1): TokenAuthAdapter

### Community 31 - "Community 31"
Cohesion: 0.53
Nodes (4): buildTools(), executeTool(), isAutoApproved(), streamMessage()

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (1): ExecService

### Community 33 - "Community 33"
Cohesion: 0.53
Nodes (4): decrypt(), deriveKey(), encrypt(), getDefaultKey()

### Community 34 - "Community 34"
Cohesion: 0.33
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 0.47
Nodes (1): UserStore

### Community 36 - "Community 36"
Cohesion: 0.7
Nodes (4): aggregate(), num(), str(), toYMD()

### Community 37 - "Community 37"
Cohesion: 0.4
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 0.5
Nodes (2): requestLogger(), requestLoggingMiddleware()

### Community 39 - "Community 39"
Cohesion: 0.8
Nodes (4): check(), keyFor(), rateLimitMessages(), rateLimitRequests()

### Community 40 - "Community 40"
Cohesion: 0.4
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 0.4
Nodes (1): ScrollbackBuffer

### Community 42 - "Community 42"
Cohesion: 0.83
Nodes (3): isValidRawEvent(), processBatch(), sanitizeProperties()

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 0.5
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 0.5
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 0.5
Nodes (1): DirectConnectError

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (2): scrubObject(), scrubString()

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (2): validatePath(), validatePathWithSymlinks()

### Community 49 - "Community 49"
Cohesion: 0.67
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 0.67
Nodes (0): 

### Community 51 - "Community 51"
Cohesion: 0.67
Nodes (0): 

### Community 52 - "Community 52"
Cohesion: 0.67
Nodes (0): 

### Community 53 - "Community 53"
Cohesion: 1.0
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

## Knowledge Gaps
- **2 isolated node(s):** `ExecService`, `FileService`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 53`** (2 nodes): `schema.ts`, `emptyStore()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (2 nodes): `cors.ts`, `cors()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (2 nodes): `request-id.ts`, `requestId()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (2 nodes): `exec.ts`, `createExecRouter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (2 nodes): `files.ts`, `createFilesRouter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (2 nodes): `search.ts`, `createSearchRouter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (2 nodes): `settings.ts`, `createSettingsRouter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (2 nodes): `seed.ts`, `seed()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (2 nodes): `auth.test.ts`, `mockReq()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `api-key.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `oauth.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `sqlite.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ExecService`, `FileService` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._