# Graph Report - /Users/jay/Developer/claude-code-agent/src/ink  (2026-04-09)

## Corpus Check
- 97 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 628 nodes · 784 edges · 96 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `YogaLayoutNode` - 51 edges
2. `Ink` - 46 edges
3. `csi()` - 16 edges
4. `TerminalEvent` - 15 edges
5. `renderNodeToOutput()` - 13 edges
6. `FocusManager` - 12 edges
7. `Output` - 11 edges
8. `styles()` - 10 edges
9. `StylePool` - 9 edges
10. `markDirty()` - 8 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (1): YogaLayoutNode

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (3): drainStdin(), Ink, makeAltScreenParkPatch()

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (27): blitRegion(), cellAt(), cellAtCI(), cellAtIndex(), charInCellAt(), CharPool, clearRegion(), diff() (+19 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (17): applySelectionOverlay(), captureScrolledRows(), charClass(), clearSelection(), comparePoints(), extendSelection(), extractRowText(), findPlainTextUrlAt() (+9 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (15): applyPaddingToText(), applyStylesToWrappedText(), blitEscapingAbsoluteDescendants(), buildCharToSegmentMap(), clipsBothAxes(), drainAdaptive(), drainProportional(), dropSubtreeCache() (+7 more)

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (18): csi(), cursorBack(), cursorDown(), cursorForward(), cursorMove(), cursorPosition(), cursorTo(), cursorUp() (+10 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (11): fullResetSequence_CAUSES_FLICKER(), LogUpdate, moveCursorTo(), needsWidthCompensation(), readLine(), renderFrame(), renderFrameSlice(), transitionHyperlink() (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (8): flushBuffer(), intersectClip(), maxDefined(), minDefined(), Output, styledCharsWithGraphemeClustering(), stylesEqual(), writeLineToScreen()

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (12): appendChildNode(), collectRemovedRects(), createTextNode(), insertBeforeNode(), markDirty(), removeChildNode(), setAttribute(), setStyle() (+4 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (6): collectTabbable(), FocusManager, getFocusManager(), getRootNode(), isInTree(), walkTree()

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (1): TerminalEvent

### Community 11 - "Community 11"
Cohesion: 0.2
Nodes (11): copyNative(), link(), osc(), osc8Id(), parseOSC(), parseOscColor(), parseTabStatus(), setClipboard() (+3 more)

### Community 12 - "Community 12"
Cohesion: 0.24
Nodes (8): graphemeWidth(), hasMultipleCodepoints(), identifySequence(), isEastAsianWide(), isEmoji(), parseCSI(), parseCSIParams(), Parser

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (12): createNavKey(), createPasteKey(), decodeModifier(), inputToString(), isCtrlKey(), isShiftKey(), keycodeToName(), parseKeypress() (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (1): TerminalQuerier

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (2): applyProp(), setEventHandler()

### Community 16 - "Community 16"
Cohesion: 0.32
Nodes (11): applyBorderStyles(), applyDimensionStyles(), applyDisplayStyles(), applyFlexStyles(), applyGapStyles(), applyMarginStyles(), applyOverflowStyles(), applyPaddingStyles() (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (5): collectListeners(), Dispatcher, getEventPriority(), getHandler(), processDispatchQueue()

### Community 18 - "Community 18"
Cohesion: 0.36
Nodes (4): App, handleMouseEvent(), processKeysInBatch(), resumeHandler()

### Community 19 - "Community 19"
Cohesion: 0.25
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 0.25
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 0.52
Nodes (6): getBidi(), hasRTLCharacters(), needsBidi(), reorderBidi(), reverseRange(), reverseRangeNumbers()

### Community 22 - "Community 22"
Cohesion: 0.47
Nodes (3): applyColor(), applyTextStyles(), colorize()

### Community 23 - "Community 23"
Cohesion: 0.53
Nodes (4): getInstance(), getOptions(), renderSync(), wrappedRender()

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 0.7
Nodes (4): getClearTerminalSequence(), isMintty(), isModernWindowsTerminal(), isWindowsTerminal()

### Community 26 - "Community 26"
Cohesion: 0.4
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 0.7
Nodes (4): getEmojiWidth(), isZeroWidth(), needsSegmentation(), stringWidthJavaScript()

### Community 28 - "Community 28"
Cohesion: 0.5
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 0.67
Nodes (2): createClock(), _temp()

### Community 30 - "Community 30"
Cohesion: 0.83
Nodes (3): cleanupPath(), ErrorOverview(), getStackUtils()

### Community 31 - "Community 31"
Cohesion: 0.5
Nodes (1): EventEmitter

### Community 32 - "Community 32"
Cohesion: 0.5
Nodes (1): Event

### Community 33 - "Community 33"
Cohesion: 0.67
Nodes (2): InputEvent, parseKey()

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (2): KeyboardEvent, keyFromParsed()

### Community 35 - "Community 35"
Cohesion: 0.83
Nodes (3): dispatchClick(), dispatchHover(), hitTest()

### Community 36 - "Community 36"
Cohesion: 0.83
Nodes (3): embedTextInBorder(), renderBorder(), styleBorderLine()

### Community 37 - "Community 37"
Cohesion: 0.5
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 0.83
Nodes (3): applySGR(), parseExtendedColor(), parseParams()

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (2): colorsEqual(), stylesEqual()

### Community 40 - "Community 40"
Cohesion: 0.83
Nodes (3): sliceFit(), truncate(), wrapText()

### Community 41 - "Community 41"
Cohesion: 0.67
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 0.67
Nodes (1): ClickEvent

### Community 43 - "Community 43"
Cohesion: 0.67
Nodes (1): FocusEvent

### Community 44 - "Community 44"
Cohesion: 0.67
Nodes (1): TerminalFocusEvent

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
Cohesion: 0.67
Nodes (0): 

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
Cohesion: 1.0
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
Cohesion: 2.0
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

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 52`** (2 nodes): `AlternateScreen.tsx`, `AlternateScreen()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (2 nodes): `Box.tsx`, `Box()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (2 nodes): `Link.tsx`, `Link()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (2 nodes): `Newline.tsx`, `Newline()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (2 nodes): `NoSelect.tsx`, `NoSelect()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (2 nodes): `RawAnsi.tsx`, `RawAnsi()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (2 nodes): `ScrollBox.tsx`, `ScrollBox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (2 nodes): `Spacer.tsx`, `Spacer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (2 nodes): `TerminalFocusContext.tsx`, `TerminalFocusProvider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (2 nodes): `Text.tsx`, `Text()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (2 nodes): `get-max-width.ts`, `getMaxWidth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `use-animation-frame.ts`, `useAnimationFrame()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (2 nodes): `use-app.ts`, `useApp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (2 nodes): `use-declared-cursor.ts`, `useDeclaredCursor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (2 nodes): `use-input.ts`, `useInput()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (2 nodes): `use-search-highlight.ts`, `useSearchHighlight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (2 nodes): `use-stdin.ts`, `useStdin()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (2 nodes): `use-terminal-focus.ts`, `useTerminalFocus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (2 nodes): `use-terminal-title.ts`, `useTerminalTitle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (2 nodes): `use-terminal-viewport.ts`, `useTerminalViewport()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (2 nodes): `engine.ts`, `createLayoutNode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (2 nodes): `line-width-cache.ts`, `lineWidth()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (2 nodes): `measure-element.ts`, `measureElement()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (2 nodes): `measure-text.ts`, `measureText()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (2 nodes): `optimizer.ts`, `optimize()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (2 nodes): `renderer.ts`, `createRenderer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (2 nodes): `searchHighlight.ts`, `applySearchHighlight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (2 nodes): `supports-hyperlinks.ts`, `supportsHyperlinks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (2 nodes): `tabstops.ts`, `expandTabs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (2 nodes): `esc.ts`, `parseEsc()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (2 nodes): `useTerminalNotification.ts`, `useTerminalNotification()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (2 nodes): `warn.ts`, `ifNotInteger()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (2 nodes): `widest-line.ts`, `widestLine()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `AppContext.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `CursorDeclarationContext.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `StdinContext.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (1 nodes): `TerminalSizeContext.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `constants.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `event-handlers.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `global.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `instances.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `node.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `termio.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (1 nodes): `wrapAnsi.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 15 inferred relationships involving `csi()` (e.g. with `cursorUp()` and `cursorDown()`) actually correct?**
  _`csi()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `renderNodeToOutput()` (e.g. with `dropSubtreeCache()` and `blitEscapingAbsoluteDescendants()`) actually correct?**
  _`renderNodeToOutput()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `Community 10` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._