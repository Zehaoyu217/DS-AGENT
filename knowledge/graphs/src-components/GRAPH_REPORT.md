# Graph Report - /Users/jay/Developer/claude-code-agent/src/components  (2026-04-09)

## Corpus Check
- 389 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1310 nodes · 1079 edges · 378 communities detected
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 147 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `commitTextField()` - 6 edges
2. `formatDiff()` - 5 edges
3. `getAgentDirectoryPath()` - 5 edges
4. `saveAgentToFile()` - 5 edges
5. `handleNavigation()` - 5 edges
6. `updateValidationError()` - 5 edges
7. `SentryErrorBoundary` - 4 edges
8. `getColorModuleUnavailableReason()` - 4 edges
9. `getRelativeAgentDirectoryPath()` - 4 edges
10. `getActualAgentFilePath()` - 4 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (17): extractDangerousSettings(), getApiKeyHelperSources(), getAwsCommandsSources(), getBashPermissionSources(), getDangerousEnvVarsSources(), getGcpCommandsSources(), getHooksSources(), getOtelHeadersHelperSources() (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (9): commitTextField(), handleNavigation(), handleTextInputChange(), handleTextInputSubmit(), resolveFieldAsync(), setField(), unsetField(), updateValidationError() (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (0): 

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (2): getAgentThemeColor(), _temp8()

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (7): applyModalPagerAction(), initAndLogWheelAccel(), initWheelAccel(), jumpBy(), readScrollSpeedBase(), ScrollKeybindingHandler(), useDragToScroll()

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (0): 

### Community 6 - "Community 6"
Cohesion: 0.23
Nodes (9): computeStickyPromptText(), highlight(), jump(), scan(), select(), step(), stickyPromptText(), StickyTracker() (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (12): deleteAgentFromFile(), ensureAgentDirectoryExists(), formatAgentAsMarkdown(), getActualAgentFilePath(), getActualRelativeAgentFilePath(), getAgentDirectoryPath(), getNewAgentFilePath(), getNewRelativeAgentFilePath() (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.19
Nodes (4): copyTextOf(), isNavigableMessage(), stripSystemReminders(), toolCallOf()

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (3): extractDirectories(), extractMode(), SuggestionDisplay()

### Community 10 - "Community 10"
Cohesion: 0.26
Nodes (9): cachedHighlight(), calculateWordDiffs(), formatDiff(), generateWordDiffElements(), Highlighted(), numberDiffLines(), processAdjacentLines(), StructuredDiffFallback() (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (3): getMcpServerBuckets(), getToolBuckets(), ToolSelector()

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (8): createOverageCreditFeed(), getFeedTitle(), getUsageText(), isEligibleForOverageCreditGrant(), maybeRefreshOverageCreditCache(), OverageCreditUpsell(), shouldShowOverageCreditUpsell(), _temp()

### Community 14 - "Community 14"
Cohesion: 0.22
Nodes (3): buildPrimarySection(), buildSecondarySection(), Status()

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (6): createFallbackTitle(), createGitHubIssueUrl(), generateTitle(), redactSensitiveInfo(), sanitizeAndLogError(), submitFeedback()

### Community 18 - "Community 18"
Cohesion: 0.2
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 0.32
Nodes (4): buildLogLabel(), extractSnippet(), LogSelector(), normalizeAndTruncateToWidth()

### Community 20 - "Community 20"
Cohesion: 0.25
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 0.25
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 0.32
Nodes (3): AssistantToolUseMessage(), renderToolUseMessage(), renderToolUseProgressMessage()

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (2): CoordinatorTaskPanel(), getVisibleAgentTasks()

### Community 24 - "Community 24"
Cohesion: 0.38
Nodes (3): getDesktopUpsellConfig(), isSupportedPlatform(), shouldShowDesktopUpsellStartup()

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 0.38
Nodes (3): resetIfPassesRefreshed(), shouldShowGuestPassesUpsell(), _temp()

### Community 27 - "Community 27"
Cohesion: 0.38
Nodes (3): cachedLexer(), hasMarkdownSyntax(), MarkdownBody()

### Community 28 - "Community 28"
Cohesion: 0.38
Nodes (3): allToolsResolved(), areMessageRowPropsEqual(), isMessageStreaming()

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 0.43
Nodes (4): autoNameSessionFromPlan(), buildPermissionUpdates(), handleKeyDown(), handleResponse()

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 0.47
Nodes (3): assistantHasVisibleText(), computeUnseenDivider(), countUnseenAssistantTurns()

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 0.4
Nodes (2): findUnmatched(), _temp()

### Community 35 - "Community 35"
Cohesion: 0.33
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 0.47
Nodes (3): onChange(), onChangeVerbose(), saveGlobalConfig()

### Community 37 - "Community 37"
Cohesion: 0.33
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 0.4
Nodes (2): createAllTimeStatsPromise(), Stats()

### Community 39 - "Community 39"
Cohesion: 0.33
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 0.53
Nodes (4): linkifyUrlsInText(), OutputLine(), stripUnderlineAnsi(), tryJsonFormatContent()

### Community 41 - "Community 41"
Cohesion: 0.47
Nodes (4): formatToolUseSummary(), handleKeyDown(), handleTeleport(), UltraplanSessionDetail()

### Community 42 - "Community 42"
Cohesion: 0.33
Nodes (0): 

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 0.4
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 0.4
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 0.5
Nodes (2): AnimatedClawd(), useClawdAnimation()

### Community 47 - "Community 47"
Cohesion: 0.4
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 0.4
Nodes (0): 

### Community 49 - "Community 49"
Cohesion: 0.4
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 0.4
Nodes (0): 

### Community 51 - "Community 51"
Cohesion: 0.5
Nodes (2): getModeFromInput(), getValueFromInput()

### Community 52 - "Community 52"
Cohesion: 0.4
Nodes (1): SentryErrorBoundary

### Community 53 - "Community 53"
Cohesion: 0.4
Nodes (0): 

### Community 54 - "Community 54"
Cohesion: 0.7
Nodes (4): expectColorDiff(), expectColorFile(), getColorModuleUnavailableReason(), getSyntaxTheme()

### Community 55 - "Community 55"
Cohesion: 0.4
Nodes (0): 

### Community 56 - "Community 56"
Cohesion: 0.4
Nodes (0): 

### Community 57 - "Community 57"
Cohesion: 0.4
Nodes (0): 

### Community 58 - "Community 58"
Cohesion: 0.4
Nodes (0): 

### Community 59 - "Community 59"
Cohesion: 0.4
Nodes (0): 

### Community 60 - "Community 60"
Cohesion: 0.4
Nodes (0): 

### Community 61 - "Community 61"
Cohesion: 0.6
Nodes (4): formatUri(), parseUpdates(), _temp(), UserResourceUpdateMessage()

### Community 62 - "Community 62"
Cohesion: 0.5
Nodes (2): parseTeammateMessages(), UserTeammateMessage()

### Community 63 - "Community 63"
Cohesion: 0.4
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 0.4
Nodes (0): 

### Community 65 - "Community 65"
Cohesion: 0.7
Nodes (4): handleAcceptOnce(), handleAcceptSession(), handleReject(), logPermissionEvent()

### Community 66 - "Community 66"
Cohesion: 0.4
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 0.4
Nodes (0): 

### Community 68 - "Community 68"
Cohesion: 0.4
Nodes (0): 

### Community 69 - "Community 69"
Cohesion: 0.4
Nodes (0): 

### Community 70 - "Community 70"
Cohesion: 0.4
Nodes (0): 

### Community 71 - "Community 71"
Cohesion: 0.5
Nodes (0): 

### Community 72 - "Community 72"
Cohesion: 0.5
Nodes (0): 

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (2): createDefaultState(), useSelectNavigation()

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (2): DevBar(), shouldShowDevBar()

### Community 75 - "Community 75"
Cohesion: 0.5
Nodes (0): 

### Community 76 - "Community 76"
Cohesion: 0.5
Nodes (0): 

### Community 77 - "Community 77"
Cohesion: 0.83
Nodes (3): hasIdeOnboardingDialogBeenShown(), IdeOnboardingDialog(), markDialogAsShown()

### Community 78 - "Community 78"
Cohesion: 0.5
Nodes (0): 

### Community 79 - "Community 79"
Cohesion: 0.5
Nodes (0): 

### Community 80 - "Community 80"
Cohesion: 0.5
Nodes (0): 

### Community 81 - "Community 81"
Cohesion: 0.5
Nodes (0): 

### Community 82 - "Community 82"
Cohesion: 0.83
Nodes (3): goToNextStep(), handleApiKeyDone(), handleThemeSelection()

### Community 83 - "Community 83"
Cohesion: 0.5
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 0.67
Nodes (2): navigateFooter(), selectFooterItem()

### Community 85 - "Community 85"
Cohesion: 0.67
Nodes (2): getTeammateThemeColor(), PromptInputModeIndicator()

### Community 86 - "Community 86"
Cohesion: 0.67
Nodes (2): createOverflowNotificationMessage(), processQueuedCommands()

### Community 87 - "Community 87"
Cohesion: 0.83
Nodes (3): formatTruncatedTextRef(), maybeTruncateInput(), maybeTruncateMessageForInput()

### Community 88 - "Community 88"
Cohesion: 0.5
Nodes (0): 

### Community 89 - "Community 89"
Cohesion: 0.5
Nodes (0): 

### Community 90 - "Community 90"
Cohesion: 0.5
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 0.5
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 0.5
Nodes (0): 

### Community 93 - "Community 93"
Cohesion: 0.5
Nodes (0): 

### Community 94 - "Community 94"
Cohesion: 0.5
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 0.5
Nodes (0): 

### Community 96 - "Community 96"
Cohesion: 0.83
Nodes (3): getScopeHeading(), groupServersByScope(), MCPListPanel()

### Community 97 - "Community 97"
Cohesion: 0.5
Nodes (0): 

### Community 98 - "Community 98"
Cohesion: 0.5
Nodes (0): 

### Community 99 - "Community 99"
Cohesion: 0.5
Nodes (0): 

### Community 100 - "Community 100"
Cohesion: 0.5
Nodes (0): 

### Community 101 - "Community 101"
Cohesion: 0.67
Nodes (2): bashToolUseOptions(), descriptionAlreadyExists()

### Community 102 - "Community 102"
Cohesion: 0.83
Nodes (3): getFilePermissionOptions(), isInClaudeFolder(), isInGlobalClaudeFolder()

### Community 103 - "Community 103"
Cohesion: 0.67
Nodes (2): FilesystemPermissionRequest(), pathFromToolUse()

### Community 104 - "Community 104"
Cohesion: 0.83
Nodes (3): getNotificationMessage(), permissionComponentForTool(), PermissionRequest()

### Community 105 - "Community 105"
Cohesion: 0.5
Nodes (0): 

### Community 106 - "Community 106"
Cohesion: 0.67
Nodes (2): decisionReasonToString(), permissionResultToLog()

### Community 107 - "Community 107"
Cohesion: 0.5
Nodes (0): 

### Community 108 - "Community 108"
Cohesion: 0.5
Nodes (0): 

### Community 109 - "Community 109"
Cohesion: 0.5
Nodes (0): 

### Community 110 - "Community 110"
Cohesion: 0.5
Nodes (0): 

### Community 111 - "Community 111"
Cohesion: 0.5
Nodes (0): 

### Community 112 - "Community 112"
Cohesion: 0.67
Nodes (0): 

### Community 113 - "Community 113"
Cohesion: 0.67
Nodes (1): OptionMap

### Community 114 - "Community 114"
Cohesion: 1.0
Nodes (2): effortLevelToSymbol(), getEffortNotificationText()

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (2): ExitFlow(), getRandomGoodbyeMessage()

### Community 116 - "Community 116"
Cohesion: 0.67
Nodes (0): 

### Community 117 - "Community 117"
Cohesion: 0.67
Nodes (0): 

### Community 118 - "Community 118"
Cohesion: 0.67
Nodes (0): 

### Community 119 - "Community 119"
Cohesion: 0.67
Nodes (0): 

### Community 120 - "Community 120"
Cohesion: 0.67
Nodes (0): 

### Community 121 - "Community 121"
Cohesion: 0.67
Nodes (0): 

### Community 122 - "Community 122"
Cohesion: 1.0
Nodes (2): formatIdleDuration(), IdleReturnDialog()

### Community 123 - "Community 123"
Cohesion: 0.67
Nodes (0): 

### Community 124 - "Community 124"
Cohesion: 0.67
Nodes (0): 

### Community 125 - "Community 125"
Cohesion: 0.67
Nodes (0): 

### Community 126 - "Community 126"
Cohesion: 0.67
Nodes (0): 

### Community 127 - "Community 127"
Cohesion: 0.67
Nodes (0): 

### Community 128 - "Community 128"
Cohesion: 0.67
Nodes (0): 

### Community 129 - "Community 129"
Cohesion: 0.67
Nodes (0): 

### Community 130 - "Community 130"
Cohesion: 0.67
Nodes (0): 

### Community 131 - "Community 131"
Cohesion: 0.67
Nodes (0): 

### Community 132 - "Community 132"
Cohesion: 0.67
Nodes (0): 

### Community 133 - "Community 133"
Cohesion: 0.67
Nodes (0): 

### Community 134 - "Community 134"
Cohesion: 0.67
Nodes (0): 

### Community 135 - "Community 135"
Cohesion: 0.67
Nodes (0): 

### Community 136 - "Community 136"
Cohesion: 0.67
Nodes (0): 

### Community 137 - "Community 137"
Cohesion: 0.67
Nodes (0): 

### Community 138 - "Community 138"
Cohesion: 1.0
Nodes (2): getPrStatusColor(), PrBadge()

### Community 139 - "Community 139"
Cohesion: 1.0
Nodes (2): formatShortcut(), PromptInputHelpMenu()

### Community 140 - "Community 140"
Cohesion: 1.0
Nodes (2): toThemeColor(), useSwarmBanner()

### Community 141 - "Community 141"
Cohesion: 0.67
Nodes (0): 

### Community 142 - "Community 142"
Cohesion: 0.67
Nodes (0): 

### Community 143 - "Community 143"
Cohesion: 0.67
Nodes (0): 

### Community 144 - "Community 144"
Cohesion: 1.0
Nodes (2): getMessagePreview(), TeammateSpinnerLine()

### Community 145 - "Community 145"
Cohesion: 0.67
Nodes (0): 

### Community 146 - "Community 146"
Cohesion: 1.0
Nodes (2): computeGutterWidth(), renderColorDiff()

### Community 147 - "Community 147"
Cohesion: 0.67
Nodes (0): 

### Community 148 - "Community 148"
Cohesion: 0.67
Nodes (0): 

### Community 149 - "Community 149"
Cohesion: 0.67
Nodes (0): 

### Community 150 - "Community 150"
Cohesion: 0.67
Nodes (0): 

### Community 151 - "Community 151"
Cohesion: 0.67
Nodes (0): 

### Community 152 - "Community 152"
Cohesion: 0.67
Nodes (0): 

### Community 153 - "Community 153"
Cohesion: 1.0
Nodes (2): validateAgent(), validateAgentType()

### Community 154 - "Community 154"
Cohesion: 0.67
Nodes (0): 

### Community 155 - "Community 155"
Cohesion: 0.67
Nodes (0): 

### Community 156 - "Community 156"
Cohesion: 1.0
Nodes (2): resolveColor(), ThemedBox()

### Community 157 - "Community 157"
Cohesion: 1.0
Nodes (2): resolveColor(), ThemedText()

### Community 158 - "Community 158"
Cohesion: 1.0
Nodes (2): DiffDialog(), turnDiffToDiffData()

### Community 159 - "Community 159"
Cohesion: 0.67
Nodes (0): 

### Community 160 - "Community 160"
Cohesion: 0.67
Nodes (0): 

### Community 161 - "Community 161"
Cohesion: 0.67
Nodes (0): 

### Community 162 - "Community 162"
Cohesion: 0.67
Nodes (0): 

### Community 163 - "Community 163"
Cohesion: 1.0
Nodes (2): getRelativeMemoryPath(), MemoryUpdateNotification()

### Community 164 - "Community 164"
Cohesion: 1.0
Nodes (2): getUpsellMessage(), RateLimitMessage()

### Community 165 - "Community 165"
Cohesion: 0.67
Nodes (0): 

### Community 166 - "Community 166"
Cohesion: 1.0
Nodes (2): getStatusColor(), UserAgentNotificationMessage()

### Community 167 - "Community 167"
Cohesion: 1.0
Nodes (2): displayServerName(), UserChannelMessage()

### Community 168 - "Community 168"
Cohesion: 1.0
Nodes (2): getSavingMessage(), UserMemoryInputMessage()

### Community 169 - "Community 169"
Cohesion: 0.67
Nodes (0): 

### Community 170 - "Community 170"
Cohesion: 0.67
Nodes (0): 

### Community 171 - "Community 171"
Cohesion: 0.67
Nodes (0): 

### Community 172 - "Community 172"
Cohesion: 0.67
Nodes (0): 

### Community 173 - "Community 173"
Cohesion: 0.67
Nodes (0): 

### Community 174 - "Community 174"
Cohesion: 0.67
Nodes (0): 

### Community 175 - "Community 175"
Cohesion: 0.67
Nodes (0): 

### Community 176 - "Community 176"
Cohesion: 0.67
Nodes (0): 

### Community 177 - "Community 177"
Cohesion: 0.67
Nodes (0): 

### Community 178 - "Community 178"
Cohesion: 0.67
Nodes (0): 

### Community 179 - "Community 179"
Cohesion: 1.0
Nodes (2): inputToPermissionRuleContent(), WebFetchPermissionRequest()

### Community 180 - "Community 180"
Cohesion: 0.67
Nodes (0): 

### Community 181 - "Community 181"
Cohesion: 0.67
Nodes (0): 

### Community 182 - "Community 182"
Cohesion: 0.67
Nodes (0): 

### Community 183 - "Community 183"
Cohesion: 0.67
Nodes (0): 

### Community 184 - "Community 184"
Cohesion: 0.67
Nodes (0): 

### Community 185 - "Community 185"
Cohesion: 0.67
Nodes (0): 

### Community 186 - "Community 186"
Cohesion: 0.67
Nodes (0): 

### Community 187 - "Community 187"
Cohesion: 0.67
Nodes (0): 

### Community 188 - "Community 188"
Cohesion: 1.0
Nodes (0): 

### Community 189 - "Community 189"
Cohesion: 1.0
Nodes (0): 

### Community 190 - "Community 190"
Cohesion: 1.0
Nodes (0): 

### Community 191 - "Community 191"
Cohesion: 1.0
Nodes (0): 

### Community 192 - "Community 192"
Cohesion: 1.0
Nodes (0): 

### Community 193 - "Community 193"
Cohesion: 1.0
Nodes (0): 

### Community 194 - "Community 194"
Cohesion: 1.0
Nodes (0): 

### Community 195 - "Community 195"
Cohesion: 1.0
Nodes (0): 

### Community 196 - "Community 196"
Cohesion: 1.0
Nodes (0): 

### Community 197 - "Community 197"
Cohesion: 1.0
Nodes (0): 

### Community 198 - "Community 198"
Cohesion: 1.0
Nodes (0): 

### Community 199 - "Community 199"
Cohesion: 1.0
Nodes (0): 

### Community 200 - "Community 200"
Cohesion: 1.0
Nodes (0): 

### Community 201 - "Community 201"
Cohesion: 1.0
Nodes (0): 

### Community 202 - "Community 202"
Cohesion: 1.0
Nodes (0): 

### Community 203 - "Community 203"
Cohesion: 1.0
Nodes (0): 

### Community 204 - "Community 204"
Cohesion: 1.0
Nodes (0): 

### Community 205 - "Community 205"
Cohesion: 1.0
Nodes (0): 

### Community 206 - "Community 206"
Cohesion: 1.0
Nodes (0): 

### Community 207 - "Community 207"
Cohesion: 1.0
Nodes (0): 

### Community 208 - "Community 208"
Cohesion: 1.0
Nodes (0): 

### Community 209 - "Community 209"
Cohesion: 1.0
Nodes (0): 

### Community 210 - "Community 210"
Cohesion: 1.0
Nodes (0): 

### Community 211 - "Community 211"
Cohesion: 1.0
Nodes (0): 

### Community 212 - "Community 212"
Cohesion: 1.0
Nodes (0): 

### Community 213 - "Community 213"
Cohesion: 1.0
Nodes (0): 

### Community 214 - "Community 214"
Cohesion: 1.0
Nodes (0): 

### Community 215 - "Community 215"
Cohesion: 1.0
Nodes (0): 

### Community 216 - "Community 216"
Cohesion: 1.0
Nodes (0): 

### Community 217 - "Community 217"
Cohesion: 1.0
Nodes (0): 

### Community 218 - "Community 218"
Cohesion: 1.0
Nodes (0): 

### Community 219 - "Community 219"
Cohesion: 1.0
Nodes (0): 

### Community 220 - "Community 220"
Cohesion: 1.0
Nodes (0): 

### Community 221 - "Community 221"
Cohesion: 1.0
Nodes (0): 

### Community 222 - "Community 222"
Cohesion: 1.0
Nodes (0): 

### Community 223 - "Community 223"
Cohesion: 1.0
Nodes (0): 

### Community 224 - "Community 224"
Cohesion: 1.0
Nodes (0): 

### Community 225 - "Community 225"
Cohesion: 1.0
Nodes (0): 

### Community 226 - "Community 226"
Cohesion: 1.0
Nodes (0): 

### Community 227 - "Community 227"
Cohesion: 1.0
Nodes (0): 

### Community 228 - "Community 228"
Cohesion: 1.0
Nodes (0): 

### Community 229 - "Community 229"
Cohesion: 1.0
Nodes (0): 

### Community 230 - "Community 230"
Cohesion: 1.0
Nodes (0): 

### Community 231 - "Community 231"
Cohesion: 1.0
Nodes (0): 

### Community 232 - "Community 232"
Cohesion: 1.0
Nodes (0): 

### Community 233 - "Community 233"
Cohesion: 1.0
Nodes (0): 

### Community 234 - "Community 234"
Cohesion: 1.0
Nodes (0): 

### Community 235 - "Community 235"
Cohesion: 1.0
Nodes (0): 

### Community 236 - "Community 236"
Cohesion: 1.0
Nodes (0): 

### Community 237 - "Community 237"
Cohesion: 1.0
Nodes (0): 

### Community 238 - "Community 238"
Cohesion: 1.0
Nodes (0): 

### Community 239 - "Community 239"
Cohesion: 1.0
Nodes (0): 

### Community 240 - "Community 240"
Cohesion: 1.0
Nodes (0): 

### Community 241 - "Community 241"
Cohesion: 1.0
Nodes (0): 

### Community 242 - "Community 242"
Cohesion: 1.0
Nodes (0): 

### Community 243 - "Community 243"
Cohesion: 1.0
Nodes (0): 

### Community 244 - "Community 244"
Cohesion: 1.0
Nodes (0): 

### Community 245 - "Community 245"
Cohesion: 1.0
Nodes (0): 

### Community 246 - "Community 246"
Cohesion: 1.0
Nodes (0): 

### Community 247 - "Community 247"
Cohesion: 1.0
Nodes (0): 

### Community 248 - "Community 248"
Cohesion: 1.0
Nodes (0): 

### Community 249 - "Community 249"
Cohesion: 1.0
Nodes (0): 

### Community 250 - "Community 250"
Cohesion: 1.0
Nodes (0): 

### Community 251 - "Community 251"
Cohesion: 1.0
Nodes (0): 

### Community 252 - "Community 252"
Cohesion: 1.0
Nodes (0): 

### Community 253 - "Community 253"
Cohesion: 1.0
Nodes (0): 

### Community 254 - "Community 254"
Cohesion: 1.0
Nodes (0): 

### Community 255 - "Community 255"
Cohesion: 1.0
Nodes (0): 

### Community 256 - "Community 256"
Cohesion: 1.0
Nodes (0): 

### Community 257 - "Community 257"
Cohesion: 1.0
Nodes (0): 

### Community 258 - "Community 258"
Cohesion: 1.0
Nodes (0): 

### Community 259 - "Community 259"
Cohesion: 1.0
Nodes (0): 

### Community 260 - "Community 260"
Cohesion: 1.0
Nodes (0): 

### Community 261 - "Community 261"
Cohesion: 1.0
Nodes (0): 

### Community 262 - "Community 262"
Cohesion: 1.0
Nodes (0): 

### Community 263 - "Community 263"
Cohesion: 1.0
Nodes (0): 

### Community 264 - "Community 264"
Cohesion: 1.0
Nodes (0): 

### Community 265 - "Community 265"
Cohesion: 1.0
Nodes (0): 

### Community 266 - "Community 266"
Cohesion: 1.0
Nodes (0): 

### Community 267 - "Community 267"
Cohesion: 1.0
Nodes (0): 

### Community 268 - "Community 268"
Cohesion: 1.0
Nodes (0): 

### Community 269 - "Community 269"
Cohesion: 1.0
Nodes (0): 

### Community 270 - "Community 270"
Cohesion: 1.0
Nodes (0): 

### Community 271 - "Community 271"
Cohesion: 1.0
Nodes (0): 

### Community 272 - "Community 272"
Cohesion: 1.0
Nodes (0): 

### Community 273 - "Community 273"
Cohesion: 1.0
Nodes (0): 

### Community 274 - "Community 274"
Cohesion: 1.0
Nodes (0): 

### Community 275 - "Community 275"
Cohesion: 1.0
Nodes (0): 

### Community 276 - "Community 276"
Cohesion: 1.0
Nodes (0): 

### Community 277 - "Community 277"
Cohesion: 1.0
Nodes (0): 

### Community 278 - "Community 278"
Cohesion: 1.0
Nodes (0): 

### Community 279 - "Community 279"
Cohesion: 1.0
Nodes (0): 

### Community 280 - "Community 280"
Cohesion: 1.0
Nodes (0): 

### Community 281 - "Community 281"
Cohesion: 1.0
Nodes (0): 

### Community 282 - "Community 282"
Cohesion: 1.0
Nodes (0): 

### Community 283 - "Community 283"
Cohesion: 1.0
Nodes (0): 

### Community 284 - "Community 284"
Cohesion: 1.0
Nodes (0): 

### Community 285 - "Community 285"
Cohesion: 1.0
Nodes (0): 

### Community 286 - "Community 286"
Cohesion: 1.0
Nodes (0): 

### Community 287 - "Community 287"
Cohesion: 1.0
Nodes (0): 

### Community 288 - "Community 288"
Cohesion: 1.0
Nodes (0): 

### Community 289 - "Community 289"
Cohesion: 1.0
Nodes (0): 

### Community 290 - "Community 290"
Cohesion: 1.0
Nodes (0): 

### Community 291 - "Community 291"
Cohesion: 1.0
Nodes (0): 

### Community 292 - "Community 292"
Cohesion: 1.0
Nodes (0): 

### Community 293 - "Community 293"
Cohesion: 1.0
Nodes (0): 

### Community 294 - "Community 294"
Cohesion: 1.0
Nodes (0): 

### Community 295 - "Community 295"
Cohesion: 1.0
Nodes (0): 

### Community 296 - "Community 296"
Cohesion: 1.0
Nodes (0): 

### Community 297 - "Community 297"
Cohesion: 1.0
Nodes (0): 

### Community 298 - "Community 298"
Cohesion: 1.0
Nodes (0): 

### Community 299 - "Community 299"
Cohesion: 1.0
Nodes (0): 

### Community 300 - "Community 300"
Cohesion: 1.0
Nodes (0): 

### Community 301 - "Community 301"
Cohesion: 1.0
Nodes (0): 

### Community 302 - "Community 302"
Cohesion: 1.0
Nodes (0): 

### Community 303 - "Community 303"
Cohesion: 1.0
Nodes (0): 

### Community 304 - "Community 304"
Cohesion: 1.0
Nodes (0): 

### Community 305 - "Community 305"
Cohesion: 1.0
Nodes (0): 

### Community 306 - "Community 306"
Cohesion: 1.0
Nodes (0): 

### Community 307 - "Community 307"
Cohesion: 1.0
Nodes (0): 

### Community 308 - "Community 308"
Cohesion: 1.0
Nodes (0): 

### Community 309 - "Community 309"
Cohesion: 1.0
Nodes (0): 

### Community 310 - "Community 310"
Cohesion: 1.0
Nodes (0): 

### Community 311 - "Community 311"
Cohesion: 1.0
Nodes (0): 

### Community 312 - "Community 312"
Cohesion: 1.0
Nodes (0): 

### Community 313 - "Community 313"
Cohesion: 1.0
Nodes (0): 

### Community 314 - "Community 314"
Cohesion: 1.0
Nodes (0): 

### Community 315 - "Community 315"
Cohesion: 1.0
Nodes (0): 

### Community 316 - "Community 316"
Cohesion: 1.0
Nodes (0): 

### Community 317 - "Community 317"
Cohesion: 1.0
Nodes (0): 

### Community 318 - "Community 318"
Cohesion: 1.0
Nodes (0): 

### Community 319 - "Community 319"
Cohesion: 1.0
Nodes (0): 

### Community 320 - "Community 320"
Cohesion: 1.0
Nodes (0): 

### Community 321 - "Community 321"
Cohesion: 1.0
Nodes (0): 

### Community 322 - "Community 322"
Cohesion: 1.0
Nodes (0): 

### Community 323 - "Community 323"
Cohesion: 1.0
Nodes (0): 

### Community 324 - "Community 324"
Cohesion: 1.0
Nodes (0): 

### Community 325 - "Community 325"
Cohesion: 1.0
Nodes (0): 

### Community 326 - "Community 326"
Cohesion: 1.0
Nodes (0): 

### Community 327 - "Community 327"
Cohesion: 1.0
Nodes (0): 

### Community 328 - "Community 328"
Cohesion: 1.0
Nodes (0): 

### Community 329 - "Community 329"
Cohesion: 1.0
Nodes (0): 

### Community 330 - "Community 330"
Cohesion: 1.0
Nodes (0): 

### Community 331 - "Community 331"
Cohesion: 1.0
Nodes (0): 

### Community 332 - "Community 332"
Cohesion: 1.0
Nodes (0): 

### Community 333 - "Community 333"
Cohesion: 1.0
Nodes (0): 

### Community 334 - "Community 334"
Cohesion: 1.0
Nodes (0): 

### Community 335 - "Community 335"
Cohesion: 1.0
Nodes (0): 

### Community 336 - "Community 336"
Cohesion: 1.0
Nodes (0): 

### Community 337 - "Community 337"
Cohesion: 1.0
Nodes (0): 

### Community 338 - "Community 338"
Cohesion: 1.0
Nodes (0): 

### Community 339 - "Community 339"
Cohesion: 1.0
Nodes (0): 

### Community 340 - "Community 340"
Cohesion: 1.0
Nodes (0): 

### Community 341 - "Community 341"
Cohesion: 1.0
Nodes (0): 

### Community 342 - "Community 342"
Cohesion: 1.0
Nodes (0): 

### Community 343 - "Community 343"
Cohesion: 1.0
Nodes (0): 

### Community 344 - "Community 344"
Cohesion: 1.0
Nodes (0): 

### Community 345 - "Community 345"
Cohesion: 1.0
Nodes (0): 

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

## Knowledge Gaps
- **Thin community `Community 188`** (2 nodes): `App.tsx`, `App()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 189`** (2 nodes): `AutoUpdater.tsx`, `AutoUpdater()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 190`** (2 nodes): `AutoUpdaterWrapper.tsx`, `AutoUpdaterWrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 191`** (2 nodes): `AwsAuthStatusBox.tsx`, `AwsAuthStatusBox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 192`** (2 nodes): `BaseTextInput.tsx`, `BaseTextInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 193`** (2 nodes): `ChannelDowngradeDialog.tsx`, `ChannelDowngradeDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 194`** (2 nodes): `PluginHintMenu.tsx`, `PluginHintMenu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 195`** (2 nodes): `ClaudeInChromeOnboarding.tsx`, `ClaudeInChromeOnboarding()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 196`** (2 nodes): `ClickableImageRef.tsx`, `ClickableImageRef()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 197`** (2 nodes): `CompactSummary.tsx`, `CompactSummary()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 198`** (2 nodes): `ConfigurableShortcutHint.tsx`, `ConfigurableShortcutHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (2 nodes): `ContextSuggestions.tsx`, `ContextSuggestions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 200`** (2 nodes): `CostThresholdDialog.tsx`, `CostThresholdDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 201`** (2 nodes): `SelectMulti.tsx`, `String()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (2 nodes): `select-option.tsx`, `SelectOption()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (2 nodes): `use-multi-select-state.ts`, `useMultiSelectState()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (2 nodes): `use-select-input.ts`, `useSelectInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 205`** (2 nodes): `use-select-state.ts`, `useSelectState()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (2 nodes): `ExportDialog.tsx`, `ExportDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (2 nodes): `FallbackToolUseErrorMessage.tsx`, `FallbackToolUseErrorMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (2 nodes): `FallbackToolUseRejectedMessage.tsx`, `FallbackToolUseRejectedMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (2 nodes): `submitTranscriptShare.ts`, `submitTranscriptShare()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 210`** (2 nodes): `useDebouncedDigitInput.ts`, `useDebouncedDigitInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 211`** (2 nodes): `useFeedbackSurvey.tsx`, `useFeedbackSurvey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 212`** (2 nodes): `useSurveyState.tsx`, `useSurveyState()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 213`** (2 nodes): `FileEditToolUpdatedMessage.tsx`, `if()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (2 nodes): `FileEditToolUseRejectedMessage.tsx`, `FileEditToolUseRejectedMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (2 nodes): `FilePathLink.tsx`, `FilePathLink()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (2 nodes): `GlobalSearchDialog.tsx`, `truncatePathMiddle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (2 nodes): `General.tsx`, `General()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (2 nodes): `HelpV2.tsx`, `HelpV2()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (2 nodes): `HistorySearchDialog.tsx`, `HistorySearchDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (2 nodes): `IdeStatusIndicator.tsx`, `IdeStatusIndicator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (2 nodes): `InterruptedByUser.tsx`, `InterruptedByUser()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (2 nodes): `InvalidSettingsDialog.tsx`, `InvalidSettingsDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (2 nodes): `LanguagePicker.tsx`, `LanguagePicker()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (2 nodes): `AnimatedAsterisk.tsx`, `AnimatedAsterisk()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (2 nodes): `WelcomeV2.tsx`, `WelcomeV2()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (2 nodes): `LspRecommendationMenu.tsx`, `LspRecommendationMenu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (2 nodes): `MCPServerApprovalDialog.tsx`, `MCPServerApprovalDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 228`** (2 nodes): `MCPServerDesktopImportDialog.tsx`, `MCPServerDesktopImportDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (2 nodes): `MCPServerDialogCopy.tsx`, `MCPServerDialogCopy()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (2 nodes): `MemoryUsageIndicator.tsx`, `MemoryUsageIndicator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (2 nodes): `NotebookEditToolUseRejectedMessage.tsx`, `NotebookEditToolUseRejectedMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (2 nodes): `OffscreenFreeze.tsx`, `OffscreenFreeze()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (2 nodes): `OutputStylePicker.tsx`, `mapConfigsToOptions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (2 nodes): `PackageManagerAutoUpdater.tsx`, `PackageManagerAutoUpdater()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (2 nodes): `Passes.tsx`, `loadPassesData()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (2 nodes): `PressEnterToContinue.tsx`, `PressEnterToContinue()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (2 nodes): `IssueFlagBanner.tsx`, `IssueFlagBanner()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (2 nodes): `PromptInputFooter.tsx`, `PromptInputFooter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (2 nodes): `PromptInputStashNotice.tsx`, `PromptInputStashNotice()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (2 nodes): `SandboxPromptFooterHint.tsx`, `SandboxPromptFooterHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (2 nodes): `useMaybeTruncateInput.ts`, `useMaybeTruncateInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (2 nodes): `usePromptInputPlaceholder.ts`, `usePromptInputPlaceholder()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (2 nodes): `useShowFastIconHint.ts`, `useShowFastIconHint()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (2 nodes): `SearchBox.tsx`, `SearchBox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (2 nodes): `SessionPreview.tsx`, `SessionPreview()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (2 nodes): `ShowInIDEPrompt.tsx`, `ShowInIDEPrompt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (2 nodes): `FlashingChar.tsx`, `FlashingChar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (2 nodes): `GlimmerMessage.tsx`, `GlimmerMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (2 nodes): `ShimmerChar.tsx`, `ShimmerChar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (2 nodes): `SpinnerAnimationRow.tsx`, `toInkColor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (2 nodes): `SpinnerGlyph.tsx`, `SpinnerGlyph()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (2 nodes): `useShimmerAnimation.ts`, `useShimmerAnimation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (2 nodes): `useStalledAnimation.ts`, `useStalledAnimation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 254`** (2 nodes): `StatusNotices.tsx`, `StatusNotices()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 255`** (2 nodes): `StructuredDiffList.tsx`, `StructuredDiffList()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (2 nodes): `TaskListV2.tsx`, `byIdAsc()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (2 nodes): `TeleportResumeWrapper.tsx`, `TeleportResumeWrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (2 nodes): `TeleportStash.tsx`, `TeleportStash()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (2 nodes): `TextInput.tsx`, `TextInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (2 nodes): `ThemePicker.tsx`, `ThemePicker()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (2 nodes): `ToolUseLoader.tsx`, `ToolUseLoader()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (2 nodes): `AgentDetail.tsx`, `AgentDetail()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (2 nodes): `AgentEditor.tsx`, `AgentEditor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (2 nodes): `AgentNavigationFooter.tsx`, `AgentNavigationFooter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (2 nodes): `AgentsList.tsx`, `AgentsList()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (2 nodes): `ModelSelector.tsx`, `ModelSelector()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (2 nodes): `generateAgent.ts`, `generateAgent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (2 nodes): `CreateAgentWizard.tsx`, `CreateAgentWizard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (2 nodes): `ColorStep.tsx`, `ColorStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (2 nodes): `ConfirmStepWrapper.tsx`, `ConfirmStepWrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (2 nodes): `DescriptionStep.tsx`, `DescriptionStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (2 nodes): `GenerateStep.tsx`, `handleGenerate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (2 nodes): `LocationStep.tsx`, `LocationStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (2 nodes): `MemoryStep.tsx`, `MemoryStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (2 nodes): `MethodStep.tsx`, `MethodStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (2 nodes): `ModelStep.tsx`, `ModelStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (2 nodes): `PromptStep.tsx`, `PromptStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (2 nodes): `ToolsStep.tsx`, `ToolsStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (2 nodes): `TypeStep.tsx`, `TypeStep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (2 nodes): `Divider.tsx`, `Divider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (2 nodes): `KeyboardShortcutHint.tsx`, `let()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (2 nodes): `ListItem.tsx`, `ListItem()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (2 nodes): `LoadingState.tsx`, `LoadingState()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (2 nodes): `Pane.tsx`, `Pane()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (2 nodes): `ProgressBar.tsx`, `ProgressBar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (2 nodes): `Ratchet.tsx`, `Ratchet()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (2 nodes): `StatusIcon.tsx`, `StatusIcon()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 288`** (2 nodes): `color.ts`, `color()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 289`** (2 nodes): `DiffDetailView.tsx`, `DiffDetailView()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 290`** (2 nodes): `SelectEventMode.tsx`, `SelectEventMode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (2 nodes): `CapabilitiesSection.tsx`, `CapabilitiesSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 292`** (2 nodes): `MCPAgentServerMenu.tsx`, `MCPAgentServerMenu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (2 nodes): `MCPReconnect.tsx`, `MCPReconnect()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (2 nodes): `MCPStdioServerMenu.tsx`, `MCPStdioServerMenu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (2 nodes): `McpParsingWarnings.tsx`, `McpConfigErrorSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 296`** (2 nodes): `AdvisorMessage.tsx`, `let()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 297`** (2 nodes): `AssistantRedactedThinkingMessage.tsx`, `AssistantRedactedThinkingMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (2 nodes): `AssistantTextMessage.tsx`, `InvalidApiKeyMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 299`** (2 nodes): `AssistantThinkingMessage.tsx`, `AssistantThinkingMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 300`** (2 nodes): `CollapsedReadSearchContent.tsx`, `VerboseToolUse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 301`** (2 nodes): `CompactBoundaryMessage.tsx`, `CompactBoundaryMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 302`** (2 nodes): `GroupedToolUseContent.tsx`, `GroupedToolUseContent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 303`** (2 nodes): `HookProgressMessage.tsx`, `HookProgressMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 304`** (2 nodes): `SystemTextMessage.tsx`, `SystemTextMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (2 nodes): `UserBashInputMessage.tsx`, `UserBashInputMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 306`** (2 nodes): `UserBashOutputMessage.tsx`, `UserBashOutputMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 307`** (2 nodes): `UserCommandMessage.tsx`, `UserCommandMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 308`** (2 nodes): `UserImageMessage.tsx`, `UserImageMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 309`** (2 nodes): `UserPlanMessage.tsx`, `UserPlanMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 310`** (2 nodes): `UserPromptMessage.tsx`, `UserPromptMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 311`** (2 nodes): `RejectedPlanMessage.tsx`, `RejectedPlanMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 312`** (2 nodes): `RejectedToolUseMessage.tsx`, `RejectedToolUseMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 313`** (2 nodes): `UserToolCanceledMessage.tsx`, `UserToolCanceledMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 314`** (2 nodes): `UserToolErrorMessage.tsx`, `UserToolErrorMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 315`** (2 nodes): `UserToolRejectMessage.tsx`, `UserToolRejectMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (2 nodes): `UserToolResultMessage.tsx`, `UserToolResultMessage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 317`** (2 nodes): `nullRenderingAttachments.ts`, `isNullRenderingAttachment()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 318`** (2 nodes): `teamMemSaved.ts`, `teamMemSavedPart()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 319`** (2 nodes): `PreviewQuestionView.tsx`, `PreviewQuestionView()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (2 nodes): `QuestionNavigationBar.tsx`, `QuestionNavigationBar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 321`** (2 nodes): `QuestionView.tsx`, `QuestionView()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 322`** (2 nodes): `SubmitQuestionsView.tsx`, `SubmitQuestionsView()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (2 nodes): `FilePermissionDialog.tsx`, `FilePermissionDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 324`** (2 nodes): `ideDiffConfig.ts`, `createSingleEditDiffConfig()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 325`** (2 nodes): `useFilePermissionDialog.ts`, `useFilePermissionDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 326`** (2 nodes): `FileWriteToolDiff.tsx`, `FileWriteToolDiff()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 327`** (2 nodes): `PermissionDialog.tsx`, `PermissionDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 328`** (2 nodes): `PermissionRequestTitle.tsx`, `PermissionRequestTitle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 329`** (2 nodes): `PermissionRuleExplanation.tsx`, `stringsForDecisionReason()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 330`** (2 nodes): `powershellToolUseOptions.tsx`, `powershellToolUseOptions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 331`** (2 nodes): `SandboxPermissionRequest.tsx`, `SandboxPermissionRequest()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 332`** (2 nodes): `WorkerBadge.tsx`, `WorkerBadge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 333`** (2 nodes): `WorkerPendingPermission.tsx`, `WorkerPendingPermission()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 334`** (2 nodes): `PermissionRuleDescription.tsx`, `PermissionRuleDescription()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 335`** (2 nodes): `PermissionRuleInput.tsx`, `PermissionRuleInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 336`** (2 nodes): `RemoveWorkspaceDirectory.tsx`, `RemoveWorkspaceDirectory()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 337`** (2 nodes): `useShellPermissionFeedback.ts`, `useShellPermissionFeedback()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 338`** (2 nodes): `SandboxDoctorSection.tsx`, `SandboxDoctorSection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 339`** (2 nodes): `SandboxSettings.tsx`, `getCurrentMode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 340`** (2 nodes): `ShellTimeDisplay.tsx`, `ShellTimeDisplay()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 341`** (2 nodes): `AsyncAgentDetailDialog.tsx`, `AsyncAgentDetailDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 342`** (2 nodes): `BackgroundTask.tsx`, `BackgroundTask()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 343`** (2 nodes): `InProcessTeammateDetailDialog.tsx`, `InProcessTeammateDetailDialog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 344`** (2 nodes): `renderToolActivity.tsx`, `renderToolActivity()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 345`** (2 nodes): `OrderedList.tsx`, `OrderedListComponent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 346`** (2 nodes): `OrderedListItem.tsx`, `OrderedListItem()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 347`** (2 nodes): `WizardDialogLayout.tsx`, `WizardDialogLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 348`** (2 nodes): `WizardNavigationFooter.tsx`, `WizardNavigationFooter()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 349`** (2 nodes): `useWizard.ts`, `useWizard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 350`** (1 nodes): `AgentProgressLine.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 351`** (1 nodes): `ApproveApiKey.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 352`** (1 nodes): `AutoModeOptInDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 353`** (1 nodes): `BashModeProgress.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 354`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 355`** (1 nodes): `select-input-option.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 356`** (1 nodes): `EffortCallout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 357`** (1 nodes): `Commands.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 358`** (1 nodes): `HighlightedCode.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 359`** (1 nodes): `ModelPicker.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 360`** (1 nodes): `HistorySearchInput.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 361`** (1 nodes): `ShimmeredInput.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 362`** (1 nodes): `QuickOpenDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 363`** (1 nodes): `SkillImprovementSurvey.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 364`** (1 nodes): `teammateSelectHint.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 365`** (1 nodes): `TeleportError.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 366`** (1 nodes): `ThinkingToggle.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 367`** (1 nodes): `TrustDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 368`** (1 nodes): `ColorPicker.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 369`** (1 nodes): `Dialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 370`** (1 nodes): `PromptDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (1 nodes): `MCPToolListView.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 372`** (1 nodes): `UserLocalCommandOutputMessage.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 373`** (1 nodes): `UserToolSuccessMessage.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 374`** (1 nodes): `FallbackPermissionRequest.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 375`** (1 nodes): `PermissionExplanation.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (1 nodes): `ShellProgressMessage.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 377`** (1 nodes): `DreamDetailDialog.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 5 inferred relationships involving `commitTextField()` (e.g. with `handleNavigation()` and `unsetField()`) actually correct?**
  _`commitTextField()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `formatDiff()` (e.g. with `StructuredDiffFallback()` and `transformLinesToObjects()`) actually correct?**
  _`formatDiff()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `getAgentDirectoryPath()` (e.g. with `getRelativeAgentDirectoryPath()` and `getNewAgentFilePath()`) actually correct?**
  _`getAgentDirectoryPath()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `saveAgentToFile()` (e.g. with `ensureAgentDirectoryExists()` and `getNewAgentFilePath()`) actually correct?**
  _`saveAgentToFile()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `handleNavigation()` (e.g. with `validateMultiSelect()` and `commitTextField()`) actually correct?**
  _`handleNavigation()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._