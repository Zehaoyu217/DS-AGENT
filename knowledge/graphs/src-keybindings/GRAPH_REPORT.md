# Graph Report - /Users/jay/Developer/claude-code-agent/src/keybindings  (2026-04-09)

## Corpus Check
- 14 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 80 nodes · 106 edges · 14 communities detected
- Extraction: 62% EXTRACTED · 38% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `loadKeybindings()` - 7 edges
2. `loadKeybindingsSyncWithWarnings()` - 7 edges
3. `validateBindings()` - 6 edges
4. `matchesKeystroke()` - 5 edges
5. `isKeybindingCustomizationEnabled()` - 4 edges
6. `getKeybindingsPath()` - 4 edges
7. `getDefaultParsedBindings()` - 4 edges
8. `resolveKeyWithChordState()` - 4 edges
9. `validateBlock()` - 4 edges
10. `logCustomBindingsLoadedOncePerDay()` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (11): getDefaultParsedBindings(), getKeybindingsPath(), handleChange(), handleDelete(), initializeKeybindingWatcher(), isKeybindingBlockArray(), isKeybindingCustomizationEnabled(), loadKeybindings() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.24
Nodes (11): checkDuplicates(), checkReservedShortcuts(), formatWarning(), formatWarnings(), getUserBindingsForValidation(), isKeybindingBlockArray(), isValidContext(), validateBindings() (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (6): keystrokeToDisplayString(), keystrokeToString(), keyToDisplayName(), parseBindings(), parseChord(), parseKeystroke()

### Community 3 - "Community 3"
Cohesion: 0.43
Nodes (5): buildKeystroke(), chordExactlyMatches(), chordPrefixMatches(), keystrokesEqual(), resolveKeyWithChordState()

### Community 4 - "Community 4"
Cohesion: 0.4
Nodes (2): useOptionalKeybindingContext(), useRegisterKeybindingContext()

### Community 5 - "Community 5"
Cohesion: 0.6
Nodes (5): getInkModifiers(), getKeyName(), matchesBinding(), matchesKeystroke(), modifiersMatch()

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (2): KeybindingSetup(), useKeybindingWarnings()

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): filterReservedShortcuts(), generateKeybindingsTemplate()

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 10`** (2 nodes): `shortcutFormat.ts`, `getShortcutDisplay()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `useShortcutDisplay.ts`, `useShortcutDisplay()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `defaultBindings.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `schema.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 6 inferred relationships involving `loadKeybindings()` (e.g. with `getDefaultParsedBindings()` and `isKeybindingCustomizationEnabled()`) actually correct?**
  _`loadKeybindings()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `loadKeybindingsSyncWithWarnings()` (e.g. with `loadKeybindingsSync()` and `getDefaultParsedBindings()`) actually correct?**
  _`loadKeybindingsSyncWithWarnings()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `validateBindings()` (e.g. with `validateUserConfig()` and `isKeybindingBlockArray()`) actually correct?**
  _`validateBindings()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `matchesKeystroke()` (e.g. with `getKeyName()` and `getInkModifiers()`) actually correct?**
  _`matchesKeystroke()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `isKeybindingCustomizationEnabled()` (e.g. with `loadKeybindings()` and `loadKeybindingsSyncWithWarnings()`) actually correct?**
  _`isKeybindingCustomizationEnabled()` has 3 INFERRED edges - model-reasoned connections that need verification._