# Graph Report - .  (2026-04-16)

## Corpus Check
- 652 files · ~703,660 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3435 nodes · 6026 edges · 287 communities detected
- Extraction: 55% EXTRACTED · 45% INFERRED · 0% AMBIGUOUS · INFERRED: 2710 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `ToolDispatcher` - 94 edges
2. `AgentLoop` - 88 edges
3. `SessionDB` - 70 edges
4. `Message` - 68 edges
5. `ModelClient` - 66 edges
6. `AgentTrace` - 61 edges
7. `TurnState` - 56 edges
8. `CompletionRequest` - 55 edges
9. `AnthropicClient` - 53 edges
10. `ModelProfile` - 50 edges

## Surprising Connections (you probably didn't know these)
- `MicroCompactor` --semantically_similar_to--> `SemanticCompactor`  [INFERRED] [semantically similar]
  progress.md → task_plan.md
- `register_all()` --calls--> `_build_spec()`  [INFERRED]
  backend/config/themes/altair_theme.py → config/themes/altair_theme.py
- `Read/write iteration log entries.` --uses--> `IterationLogEntry`  [INFERRED]
  backend/app/sop/log.py → backend/app/sop/types.py
- `Tests for app.storage.session_db — SessionDB CRUD + FTS5 + jitter retry.` --uses--> `SessionDB`  [INFERRED]
  backend/app/storage/tests/test_session_db.py → backend/app/storage/session_db.py
- `Verify jitter retry eventually succeeds after repeated OperationalError('locked'` --uses--> `SessionDB`  [INFERRED]
  backend/app/storage/tests/test_session_db.py → backend/app/storage/session_db.py

## Hyperedges (group relationships)
- **Statistical Analysis Workflow (validate gates findings)** — skill_statistical_analysis_hub, skill_correlation, skill_group_compare, skill_distribution_fit, skill_stat_validate, skill_statistical_gotchas [EXTRACTED 0.95]
- **Hermes Migration H1-H6** — task_plan_h1_ccagent_home, task_plan_h2_sessions_db, task_plan_h3_injection_parallel, task_plan_h4_compaction_cron, task_plan_h5_toolsets_batch, task_plan_h6_mcp_branding [EXTRACTED 1.00]
- **Reporting Output Assembly** — skill_reporting_hub, skill_dashboard_builder, skill_report_builder, skill_html_tables [EXTRACTED 0.90]
- **Plan Versioning Chain v1→v2→v3→v4** — progressive_plan_v1, progressive_plan_v2, progressive_plan_v3, progress_plan_v4 [EXTRACTED 1.00]
- **V3 Harness Wiring + Long-Session Phases** — phase_p15_wire_harness, phase_p17_microcompact, phase_p18_session_memory, phase_p21_token_budget, phase_p22_plan_mode [EXTRACTED 1.00]
- **Audit Findings → v0.1.0 Resolution** — audit_2026_04_16, deepdive_audit_2026_04_16, v0_1_0_milestone, changelog_log [EXTRACTED 1.00]
- **Foundations Plan Group (Restructure + Foundations + Harness)** — plan_project_restructure_and_harness, plan_foundations, plan_harness_and_prompt [INFERRED 0.85]
- **Eval Observability Stack (Eval Framework + SOP + Trace-Replay)** — plan_eval_framework, plan_eval_failure_sop, plan_trace_replay_infra [INFERRED 0.90]
- **Agent Capability Pillars (Foundations + Statistical + Harness + Composition)** — plan_foundations, plan_statistical_skills, plan_harness_and_prompt, plan_composition [INFERRED 0.85]
- **Sampling Biases Family** — gotcha_selection_bias, gotcha_survivorship_bias, gotcha_immortal_time_bias, gotcha_berksons_paradox [INFERRED 0.90]
- **Correlation Pitfalls Family** — gotcha_spurious_correlation, gotcha_multicollinearity, gotcha_confounding, gotcha_non_stationarity [INFERRED 0.85]
- **Three-File Invariant Implementation** — wiki_working, wiki_index, wiki_log, concept_three_file_invariant [EXTRACTED 1.00]

## Communities

### Community 0 - "SOP Analyzer / Suggestions"
Cohesion: 0.01
Nodes (207): _build_step_breakdown(), _build_suggestions(), _completion_status(), _extract_tables(), _infer_root_cause(), _parse_query_results(), Trace-based diagnostic analysis for the eval improvement loop.  TraceAnalyzer pr, Produces a TraceAnalysis from a raw AgentTrace — no LLM required. (+199 more)

### Community 1 - "Anthropic Client"
Cohesion: 0.01
Nodes (165): AnthropicClient, BatchResult, BatchSummary, Outcome of running a single prompt., Aggregate summary across all results., ModelProfile, get_compaction_diff(), get_context() (+157 more)

### Community 2 - "A2A Delegation"
Cohesion: 0.03
Nodes (185): Agent-to-Agent (A2A) delegation.  A parent agent calls ``delegate_subagent(task,, Register the ``delegate_subagent`` tool on *dispatcher*.      Must be called bef, Outcome of a delegated sub-agent run., Runs a child AgentLoop for A2A delegation.      Instantiate once per parent sess, Run a sub-agent synchronously and return its result.          Args:, register_delegate_tool(), SubagentDispatcher, SubagentResult (+177 more)

### Community 3 - "Frontend Sections (Agents)"
Cohesion: 0.01
Nodes (23): App(), useHashRoute(), fuzzyMatch(), score(), ErrorBoundary, FileNotFoundError, lifespan(), Start the cron engine on startup and shut it down gracefully on exit. (+15 more)

### Community 4 - "Skill Registry & Hierarchy"
Cohesion: 0.04
Nodes (68): Parsed metadata from SKILL.md frontmatter and skill.yaml.      ``level`` has bee, A node in the skill hierarchy tree.      Built by SkillRegistry.discover(). Not, SkillMetadata, SkillNode, InjectionAttemptError, Prompt-injection scanning for external content (wiki, skills, session notes).  A, Raised when an injection-like pattern is detected in external content., Scan *text* for prompt-injection patterns.      Raises :class:`InjectionAttemptE (+60 more)

### Community 5 - "ADRs (Architecture Decisions)"
Cohesion: 0.03
Nodes (109): ADR-000 Initial Vision Brainstorm, ADR-001 Python/FastAPI Backend, ADR-002 React+Vite Over Next.js, ADR Template, Berkson 1946 Biometrics, Pearl Simpson's Paradox Anatomy, Tyler Vigen Spurious Correlations, Wald 1943 WWII Bombers (+101 more)

### Community 6 - "Docs ADRs & Findings"
Cohesion: 0.03
Nodes (103): A2A Delegation, ADR-001: Wire harness first, ADR-002: Adopt SessionMemory template, ADR-003: Implement MicroCompact first, ADR-004: Token budget awareness, AgentLoop, Analytical-chatbot reference, Engineering Audit 2026-04-16 (+95 more)

### Community 7 - "Prompt Assembler"
Cohesion: 0.06
Nodes (52): assemble_prompt(), detect_conflicts(), _parse_range(), Prompt assembler: reads captured sections, detects byte-range conflicts., StepNotFoundError, CompactionEvent, _EventBase, EventBus (+44 more)

### Community 8 - "Config & Branding"
Cohesion: 0.05
Nodes (45): BaseSettings, get_branding(), Config API — expose runtime configuration to the frontend (H6)., Return the current branding configuration.      The frontend fetches this once o, AppConfig, BrandingConfig, _build_from_raw(), get_config() (+37 more)

### Community 9 - "Skill Error Templates"
Cohesion: 0.05
Nodes (28): Actionable error with template-based formatting.      Every error code maps to a, SkillError, Exception, FsTools, PathEscapeError, PathForbiddenError, Read-only filesystem tools for the agent (P25).  Gives the agent three tools to, Read-only filesystem access scoped to project_root. (+20 more)

### Community 10 - "A2A Tests"
Cohesion: 0.06
Nodes (30): _make_client(), test_delegate_tool_handler_round_trip(), test_delegate_tool_missing_task(), test_dispatch_creates_artifact(), test_dispatch_filters_tools_allowed(), test_register_delegate_tool(), _client(), test_inline_table_synthesis_uses_minimal_system_prompt() (+22 more)

### Community 11 - "Cron Jobs"
Cohesion: 0.08
Nodes (26): CronJobCreate, parse_schedule(), Pydantic models and schedule parsing for the cron scheduler (H4)., Return a valid 5-field cron expression from natural language or passthrough., Input model — accepts cron expression or natural language., create_job(), delete_job(), _get_db() (+18 more)

### Community 12 - "Altair Theme"
Cohesion: 0.07
Nodes (19): active_tokens(), _build_spec(), _DesignTokens, Design token provider for chart and report theming.  Implements the Swiss/Termin, Register Altair themes.  No-op in stub — charts use default theme., Switch active theme variant., Return the active design token set., Load tokens.yaml and register one Altair theme per variant as `gir_<variant>`. (+11 more)

### Community 13 - "Chat API Entrypoint"
Cohesion: 0.09
Nodes (24): _agent_loop_sync(), _build_dispatcher(), _build_system_prompt(), chat_endpoint(), chat_stream_endpoint(), _estimate_tokens(), filter_tools_for_plan_mode(), _get_system_prompt() (+16 more)

### Community 14 - "Conversations Persistence"
Cohesion: 0.11
Nodes (32): append_turn(), _conv_lock(), _conv_path(), Conversation, ConversationCreate, _conversations_dir(), ConversationSummary, ConversationTurn (+24 more)

### Community 15 - "Dashboard Builder"
Cohesion: 0.09
Nodes (25): build(), DashboardResult, DashboardSpec, Finding, FindingSection, KPICard, Methodology, ReportResult (+17 more)

### Community 16 - "Todo Store Tests"
Cohesion: 0.1
Nodes (17): _items(), Tests for the in-session todo store (P19)., test_store_clear_removes_session(), test_store_rejects_blank_id_or_content(), test_store_replace_overwrites_previous(), test_store_replace_stores_all(), test_store_scoped_per_session(), test_store_validates_status() (+9 more)

### Community 17 - "Session Notes Tests"
Cohesion: 0.09
Nodes (13): Tests for structured session notes (P18)., No tools called, turn_index=1 → notes must NOT be written., Tools called on turn 1 → notes SHOULD be written., turn_index=2 with no tools → notes SHOULD be written (turn threshold met)., Notes must be ≤ 3000 chars when written., Worklog section lists each tool call with step index and status., Worklog shows placeholder when no tools were called., test_notes_capped_at_3000_chars() (+5 more)

### Community 18 - "Hooks Tests"
Cohesion: 0.09
Nodes (11): Tests for HookRunner — P23 user-configurable hooks., Verify run_pre interface is correct — records tool_name., Hook command can read TOOL_NAME, TOOL_INPUT, SESSION_ID env vars., Commands that hang must be killed and not raise (10s timeout enforced)., Malformed JSON config is logged but doesn't raise., Empty hook lists don't execute anything., test_empty_hooks_list_is_noop(), test_env_vars_injected() (+3 more)

### Community 19 - "Skill Registry Tests"
Cohesion: 0.17
Nodes (19): _make_hierarchy(), hub/       SKILL.md       child_a/         SKILL.md         grandchild/, Any skill at any depth is accessible by name directly., pkg/ directory must never be discovered as a child skill., test_depth_is_computed_from_nesting(), test_generate_bootstrap_imports_includes_pkg_skills(), test_get_breadcrumb_nested(), test_get_breadcrumb_root() (+11 more)

### Community 20 - "Files API Tests"
Cohesion: 0.1
Nodes (2): Binary files return metadata only by default — avoids shipping     up to ~13 MB, test_read_binary_omits_content_by_default()

### Community 21 - "Batch Runner"
Cohesion: 0.18
Nodes (13): BatchRunner, _load_checkpoint(), main(), _parse_args(), _save_checkpoint(), _mock_loop_outcome(), _mock_session_db(), _patch_all() (+5 more)

### Community 22 - "Eval Framework Plans"
Cohesion: 0.13
Nodes (20): DevTools Panel (Judge Variance, Prompt Inspector, Compaction Timeline, SessionReplay), 5-Level Eval Framework, FailureReport, First National Bank dataset, Ladder (cost-ordered fix list), LLM Judge (Ollama-backed), TraceRecorder, TraceStore (+12 more)

### Community 23 - "Eval Data Seeding"
Cohesion: 0.15
Nodes (18): create_tables(), get_row_counts(), _plant_anomalies(), Generate ~400 accounts linked to customers., Plant 6 anomaly groups (3 true + 3 false positive) in Q3 2025.      Returns the, Generate ~5000 transactions for 2025 with planted anomalies., Generate 80 loans with credit-score-correlated rates and default patterns., Drop and recreate all 5 eval tables. (+10 more)

### Community 24 - "Home Path Resolution"
Cohesion: 0.16
Nodes (17): artifacts_db_path(), artifacts_disk_path(), config_path(), cron_path(), get_ccagent_home(), CCAGENT_HOME — single env var controls all runtime data paths.  Resolution order, Return the root data directory for this CCA instance.      Creates the directory, Path to the SQLite sessions database (added in H2). (+9 more)

### Community 25 - "Turn Wrap-Up"
Cohesion: 0.19
Nodes (9): _Bus, _extract_section(), _parse_findings(), Pull the body of `## <heading>` out of the scratchpad., Render a 9-section structured session notes markdown document.      Sections are, _render_session_notes(), _validate_passed(), _Wiki (+1 more)

### Community 26 - "Fallback Client"
Cohesion: 0.36
Nodes (14): _rate_limit(), _RecordingClient, _request(), test_all_rate_limited_raises_last_error(), test_exposes_primary_name_and_tier(), test_fallback_names_reflects_chain(), test_no_fallbacks_rate_limit_raises_immediately(), test_primary_success_skips_fallbacks() (+6 more)

### Community 27 - "Sandbox Bootstrap"
Cohesion: 0.12
Nodes (9): Unit tests for build_duckdb_globals in sandbox_bootstrap., _get_cached_preamble(None) must return the same string on every call., _get_cached_preamble(None) must populate _PREAMBLE_CACHE and reuse it., Registry-keyed cache: generate_bootstrap_imports must be called only once., Verify the generated preamble is valid Python that executes without error., test_build_duckdb_globals_runs_in_subprocess(), test_preamble_cache_hits_on_second_call(), test_preamble_cache_returns_same_string_on_repeat_calls() (+1 more)

### Community 28 - "Prompts API"
Cohesion: 0.18
Nodes (16): _approx_tokens(), _get_injector_template(), _get_system_prompt(), _get_tool_schemas(), _injector_prompt_path(), list_prompts(), PromptEntry, GET /api/prompts — expose the prompt catalog to the frontend. (+8 more)

### Community 29 - "SOP API"
Cohesion: 0.14
Nodes (3): _entry(), test_get_session_by_id(), test_list_sessions_returns_written_entries()

### Community 30 - "Community 30"
Cohesion: 0.2
Nodes (16): Look-ahead Bias, promote_finding tool guardrail, Simpson's Paradox, altair_charts Skill (20 templates), Charting Hub Skill, correlation Skill, dashboard_builder Skill, distribution_fit Skill (+8 more)

### Community 31 - "Test Context Manager"
Cohesion: 0.13
Nodes (2): Validate that information_loss_pct arithmetic is correct., test_session_registry_compaction_diff_loss_pct()

### Community 32 - "Test Recorder"
Cohesion: 0.27
Nodes (14): _feed(), _final_output(), _llm_call(), _session_end(), _session_start(), test_finalize_runs_judge_runner_when_provided(), test_finalize_skips_write_on_failure_mode_with_passing_grade(), test_finalize_swallows_write_errors() (+6 more)

### Community 33 - "Test Trace Api"
Cohesion: 0.14
Nodes (2): client(), _trace_doc()

### Community 34 - "Task Plan"
Cohesion: 0.14
Nodes (15): injection_guard, PARALLEL_SAFE_TOOLS frozenset, SessionDB (sessions.db + FTS5), Finding 18: Hermes Migration Candidates, Finding 19: sessions.db Schema Decisions, Finding 20: Prompt Cache Preservation, Finding 21: Parallel Tool Safety Rules, Gap Closure Phase 3 - Parallel Tool Dispatch (+7 more)

### Community 35 - "Distill"
Cohesion: 0.22
Nodes (9): distill_artifact(), _distill_chart(), _distill_generic(), _distill_profile(), _distill_table(), format_artifacts_for_compaction(), _round(), _TableParser (+1 more)

### Community 36 - "Files Api"
Cohesion: 0.27
Nodes (13): _build_node(), FileNode, FileReadResponse, _files_root(), FileTreeResponse, get_tree(), _posix_rel(), REST endpoints for sandboxed file tree browsing and reading.  All access is conf (+5 more)

### Community 37 - "Test Checks"
Cohesion: 0.14
Nodes (0): 

### Community 38 - "Test Artifact Store"
Cohesion: 0.14
Nodes (0): 

### Community 39 - "Test Skill Tool"
Cohesion: 0.33
Nodes (12): _build_dispatcher(), _call_skill(), test_direct_access_to_level3_skill(), test_hub_skill_appends_sub_skill_catalog(), test_hub_skill_body_and_metadata_returned(), test_leaf_skill_has_no_sub_skills_section(), test_level_1_skill_has_no_breadcrumb(), test_nested_skill_shows_breadcrumb() (+4 more)

### Community 40 - "Test Conversations Api"
Cohesion: 0.14
Nodes (2): Per-conversation lock serializes read-modify-write on /turns., test_concurrent_turn_appends_do_not_lose_writes()

### Community 41 - "Test Semantic Compactor"
Cohesion: 0.35
Nodes (9): _assistant(), _mock_client(), test_compact_client_failure_returns_original(), test_compact_preserves_head_and_tail(), test_compact_replaces_middle_with_summary_message(), test_compact_short_conversation_returns_unchanged(), test_estimate_tokens_approximates_correctly(), test_identify_turn_boundaries_groups_correctly() (+1 more)

### Community 42 - "Test Contracts"
Cohesion: 0.28
Nodes (10): _kpi(), _kpi_section(), _minimal_spec_with_kp_count(), _spec(), test_empty_dashboard_raises(), test_kpi_without_delta_raises(), test_research_memo_requires_three_key_points(), test_too_many_sections_raises() (+2 more)

### Community 43 - "Test Session Db"
Cohesion: 0.17
Nodes (3): Tests for app.storage.session_db — SessionDB CRUD + FTS5 + jitter retry., Verify jitter retry eventually succeeds after repeated OperationalError('locked', test_jitter_retry_on_lock()

### Community 44 - "Session Search Api"
Cohesion: 0.24
Nodes (11): dict, SearchResult, get_session(), list_sessions(), Session search API — full-text search across past sessions via FTS5., Thin wrapper — results are returned as plain dicts for forward compatibility., Full-text search across all past session messages.      Returns up to `limit` re, List recent sessions, newest first. (+3 more)

### Community 45 - "Fixtures"
Cohesion: 0.17
Nodes (0): 

### Community 46 - "Test Engine"
Cohesion: 0.45
Nodes (10): _make_engine(), _make_job(), test_add_job_disabled_does_not_schedule(), test_add_job_persists_to_db_and_schedules(), test_pause_job_updates_db_and_pauses_scheduler(), test_remove_job_deletes_from_db(), test_resume_job_updates_db(), test_sync_from_db_clears_existing_before_reload() (+2 more)

### Community 47 - "Result"
Cohesion: 0.22
Nodes (6): fit_one(), FitCandidate, _log_likelihood(), CompareResult, CorrelationResult, FitResult

### Community 48 - "Test Publishers"
Cohesion: 0.18
Nodes (0): 

### Community 49 - "Test Store"
Cohesion: 0.27
Nodes (6): _minimal_trace_yaml(), test_list_traces_returns_summaries_sorted_by_session_id(), test_list_traces_skips_corrupted_files(), test_list_traces_skips_non_yaml_files(), test_load_trace_returns_full_trace(), _write()

### Community 50 - "Test Triage"
Cohesion: 0.47
Nodes (10): _report(), _signals(), test_context_diff_branch_fires_on_token_count_growth(), test_picks_architecture_on_level5_with_no_subagents(), test_picks_context_when_compaction_high_and_no_scratchpad(), test_picks_harness_when_tool_errors_no_retries(), test_picks_routing_when_sonnet_absent_on_reasoning_level(), test_returns_none_when_no_signal_matches() (+2 more)

### Community 51 - "Test Home"
Cohesion: 0.2
Nodes (9): Tests for app.core.home — CCAGENT_HOME path helpers., When CCAGENT_HOME is not set, home resolves to ~/.ccagent., When CCAGENT_HOME is set, home resolves to that path., Every derived path helper returns a path inside get_ccagent_home()., get_ccagent_home() creates the directory if it does not exist yet., test_all_derived_paths_under_home(), test_default_home_is_dotccagent(), test_env_var_overrides_default() (+1 more)

### Community 52 - "Test Toolsets"
Cohesion: 0.33
Nodes (8): Unit tests for ToolsetResolver (H5.T1)., _resolver(), test_cycle_detection_raises(), test_names_returns_all_defined(), test_resolve_flat_toolset(), test_resolve_nested_deduplicates(), test_resolve_unknown_name_raises(), test_resolve_with_includes()

### Community 53 - "Test Methods"
Cohesion: 0.38
Nodes (9): _report(), test_explicit_method_wins(), test_three_group_nonnormal_picks_kruskal(), test_three_group_normal_homo_picks_anova(), test_two_group_nonnormal_picks_mann_whitney(), test_two_group_normal_hetero_picks_welch(), test_two_group_normal_homo_picks_student(), test_two_group_paired_nonnormal_picks_wilcoxon() (+1 more)

### Community 54 - "Test Micro Compact"
Cohesion: 0.31
Nodes (7): Tests for the proactive MicroCompact (P17)., test_compaction_dedups_artifact_refs(), test_compaction_drops_oldest_tool_results(), test_compaction_preserves_non_tool_messages(), test_no_compaction_below_budget(), test_no_compaction_when_not_enough_tool_results(), _tool_msg()

### Community 55 - "Test Eval Grading"
Cohesion: 0.2
Nodes (0): 

### Community 56 - "Test Events"
Cohesion: 0.29
Nodes (5): _llm_call_kwargs(), test_all_event_kinds_distinct(), test_llm_call_event_is_frozen(), test_llm_call_event_round_trip(), test_trace_full_round_trip()

### Community 57 - "Server"
Cohesion: 0.27
Nodes (5): dirExists(), getCommandList(), getToolList(), listDir(), validateSrcRoot()

### Community 58 - "Bus"
Cohesion: 0.22
Nodes (7): publish(), Sync in-process event bus for the trace subsystem.  Module-level singleton. Sync, Assign monotonic seq, then fan out to all subscribers., Remove a previously-subscribed callback. No-op if not registered., Clear subscribers and reset seq counter (test-only)., reset(), unsubscribe()

### Community 59 - "Autonomy"
Cohesion: 0.42
Nodes (8): AutonomyConfig, evaluate_graduation_readiness(), load_autonomy_config(), mark_autonomous(), Per-bucket autonomy config and graduation readiness check., True iff bucket meets all graduation criteria., revert_to_proposed(), _save()

### Community 60 - "Sop Api"
Cohesion: 0.28
Nodes (4): get_session(), list_sessions(), _log_dir(), REST endpoints for DevTools SOP views.

### Community 61 - "Test Mcp Sampling"
Cohesion: 0.33
Nodes (7): _make_app(), _mock_client(), Unit tests for POST /api/mcp/sample (H6.T2)., Endpoint should return the model's text output., The 6th request for the same session_id must return HTTP 429., test_rate_limit_returns_429_after_5_calls(), test_sample_endpoint_returns_text()

### Community 62 - "Plan"
Cohesion: 0.33
Nodes (6): from_template(), plan(), PlanResult, PlanStep, _render_working_md(), StepTemplate

### Community 63 - "Test Builder"
Cohesion: 0.22
Nodes (0): 

### Community 64 - "Test Table Css"
Cohesion: 0.22
Nodes (5): Table CSS contract tests.  ``render_table_css`` returns a ``<style>`` block for, Variant arg is accepted; output is identical for all values., Swiss/terminal aesthetic — monospace is non-negotiable for tables., test_uses_monospace_family_for_data_density(), test_variant_arg_accepted_but_ignored()

### Community 65 - "Test Judge Replay"
Cohesion: 0.36
Nodes (6): test_cached_path_returns_cached_variance(), test_cached_path_returns_empty_when_no_runs(), test_live_path_calls_runner(), test_live_path_raises_when_api_key_missing(), test_threshold_exceeded_is_empty_when_below_threshold(), _trace()

### Community 66 - "Test Timeline"
Cohesion: 0.61
Nodes (8): _base_events(), _llm(), test_build_timeline_counts_tool_calls_per_turn(), test_build_timeline_empty_trace_returns_empty_arrays(), test_build_timeline_groups_llm_calls_by_turn(), test_build_timeline_includes_compaction_events(), test_build_timeline_includes_scratchpad_events(), _trace()

### Community 67 - "Test Ladder Loader"
Cohesion: 0.22
Nodes (0): 

### Community 68 - "Test Log"
Cohesion: 0.33
Nodes (6): _entry(), test_entry_with_nullable_triage_and_fix(), test_list_entries_sorted(), test_next_session_id_increments(), test_next_session_id_skips_non_numeric_suffix(), test_write_and_read_roundtrip()

### Community 69 - "Gotchas"
Cohesion: 0.22
Nodes (9): Development Setup, Gotcha: Backend factory and CWD, Gotcha: models_api.py is user-owned, Gotcha: OpenRouter multi-turn tool_calls, Gotcha: reference/ is read-only, Gotcha: Sandbox subprocess sys.path, Gotcha: Skill evals are sealed, Gotcha: Tailwind opacity on CSS variable (+1 more)

### Community 70 - "Test Renderer"
Cohesion: 0.25
Nodes (0): 

### Community 71 - "Generators"
Cohesion: 0.25
Nodes (0): 

### Community 72 - "Test Generators"
Cohesion: 0.25
Nodes (0): 

### Community 73 - "Test Correlate"
Cohesion: 0.46
Nodes (7): _store(), test_correlate_handles_nans_and_reports(), test_correlate_insufficient_rows_raises(), test_correlate_linear_returns_high_coefficient(), test_correlate_nonlinear_flips_to_spearman(), test_correlate_partial_on_removes_confounder(), test_correlate_unknown_column_raises()

### Community 74 - "Db Init"
Cohesion: 0.29
Nodes (7): get_data_context(), initialize_db(), Initialize the shared DuckDB and load default datasets on startup.  On first lau, Return a rich schema description for the system prompt.      Works with any Duck, Create the DuckDB file and ingest default datasets if not already loaded., Return (min, max) for the first recognised date column, or None., _try_date_range()

### Community 75 - "Test Eval Judge"
Cohesion: 0.25
Nodes (0): 

### Community 76 - "Test Seed Eval"
Cohesion: 0.25
Nodes (0): 

### Community 77 - "Test Skill Base"
Cohesion: 0.25
Nodes (0): 

### Community 78 - "Test Assembler"
Cohesion: 0.32
Nodes (3): test_assemble_raises_for_missing_step(), test_assemble_returns_sections_for_step(), _trace()

### Community 79 - "Test Bus"
Cohesion: 0.43
Nodes (6): _event(), test_publish_assigns_monotonic_seq(), test_publish_fans_out_to_all_subscribers(), test_publish_with_no_subscribers_is_noop(), test_reset_clears_subscribers_and_counter(), test_seq_resets_with_reset()

### Community 80 - "Test Autonomy"
Cohesion: 0.39
Nodes (5): _entry(), test_graduation_fails_when_only_two_distinct_rungs(), test_graduation_fails_with_low_success_rate(), test_graduation_fails_without_five_sessions(), test_graduation_passes_with_five_sessions_80pct_success_three_rungs()

### Community 81 - "Test Baseline"
Cohesion: 0.29
Nodes (2): _sample(), test_roundtrip_update_and_load()

### Community 82 - "Test Runner"
Cohesion: 0.46
Nodes (7): _report(), test_empty_ladder_returns_advisory(), test_no_actionable_signal_returns_none_triage(), test_preflight_failure_short_circuits(), test_sop_result_is_json_serializable(), test_triage_returns_proposal_with_cheapest_rung(), test_unknown_bucket_returns_advisory()

### Community 83 - "Metrics"
Cohesion: 0.29
Nodes (2): _Noop, Prometheus metrics for the analytical agent backend.  Import this module early (

### Community 84 - "Retention"
Cohesion: 0.43
Nodes (5): delete_all(), delete_by_age(), delete_by_grade(), main(), Retention CLI: delete traces by --clear-all / --older-than / --grade.  Usage:

### Community 85 - "Log"
Cohesion: 0.38
Nodes (4): _entry_path(), Read/write iteration log entries., read_entry(), write_entry()

### Community 86 - "Test Router"
Cohesion: 0.52
Nodes (6): _cfg(), test_router_caches_clients_per_model(), test_router_escalate_on_gate_block_swaps_to_configured_model(), test_router_resolves_role_to_client(), test_router_unknown_role_raises(), test_router_warms_up_configured_models()

### Community 87 - "Test Config"
Cohesion: 0.29
Nodes (0): 

### Community 88 - "Test Build"
Cohesion: 0.43
Nodes (5): _spec(), _spec_minimal(), test_build_a2ui_returns_payload_no_path(), test_build_returns_paths_for_every_requested_format(), test_build_standalone_html_writes_file()

### Community 89 - "Test Method"
Cohesion: 0.29
Nodes (0): 

### Community 90 - "Community 90"
Cohesion: 0.38
Nodes (3): Check, Validation, Violation

### Community 91 - "Community 91"
Cohesion: 0.29
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 0.52
Nodes (6): _store(), test_compare_k_groups_eta_squared(), test_compare_nonnormal_falls_back_to_mann_whitney(), test_compare_paired_requires_paired_id(), test_compare_raises_on_small_group(), test_compare_two_groups_auto_picks_reasonable()

### Community 93 - "Community 93"
Cohesion: 0.48
Nodes (5): _as_array(), characterize(), _dominant_period(), _trend_slope(), TSCharacterization

### Community 94 - "Community 94"
Cohesion: 0.29
Nodes (1): Altair theme contract tests.  Tests pin the public API of the design-token modul

### Community 95 - "Community 95"
Cohesion: 0.29
Nodes (0): 

### Community 96 - "Community 96"
Cohesion: 0.67
Nodes (6): _level_result(), test_baseline_grade_propagated_to_diff(), test_build_failure_report_computes_diff(), test_build_failure_report_extracts_signals(), test_write_failure_report_yaml(), _trace()

### Community 97 - "Community 97"
Cohesion: 0.52
Nodes (6): _report(), test_all_pass_when_no_variance_no_drift(), test_data_quality_fails_on_seed_mismatch(), test_determinism_fails_on_rerun_grade_variance(), test_determinism_skipped_when_fewer_than_two_reruns(), test_evaluation_bias_fails_when_judge_variance_exceeds_threshold()

### Community 98 - "Community 98"
Cohesion: 0.6
Nodes (5): _finding(), test_advisory_fail_warns_only(), test_observatory_never_blocks_or_warns(), test_strict_fail_blocks(), test_strict_warn_does_not_block()

### Community 99 - "Community 99"
Cohesion: 0.6
Nodes (5): _res(), test_artifact_id_is_recorded(), test_event_emitted_for_each_artifact(), test_large_stdout_gets_trimmed_to_artifact_reference(), test_stat_validate_warning_surfaces_gotcha_refs()

### Community 100 - "Community 100"
Cohesion: 0.33
Nodes (0): 

### Community 101 - "Community 101"
Cohesion: 0.33
Nodes (4): liveness(), Kubernetes liveness probe — confirms the process is alive., Kubernetes readiness probe — confirms the app is ready to serve traffic., readiness()

### Community 102 - "Community 102"
Cohesion: 0.33
Nodes (4): ensure_theme_registered(), Call once at chart build time to guarantee themes exist., Return Altair mark kwargs for a named series role.      Data-driven role values, resolve_series_style()

### Community 103 - "Community 103"
Cohesion: 0.6
Nodes (5): _distribution_section(), _header(), render_html_report(), _risks_section(), _schema_section()

### Community 104 - "Community 104"
Cohesion: 0.33
Nodes (2): ProfileReport, Risk

### Community 105 - "Community 105"
Cohesion: 0.33
Nodes (2): cliffs_delta(), Cliff's delta: probability a > b minus probability a < b.

### Community 106 - "Community 106"
Cohesion: 0.33
Nodes (0): 

### Community 107 - "Community 107"
Cohesion: 0.53
Nodes (4): test_delete_all_removes_all_yaml_files(), test_delete_by_age_removes_old_files(), test_delete_by_grade_keeps_matching_grades(), _write_trace()

### Community 108 - "Community 108"
Cohesion: 0.4
Nodes (2): client(), _trace_doc()

### Community 109 - "Community 109"
Cohesion: 0.33
Nodes (0): 

### Community 110 - "Community 110"
Cohesion: 0.5
Nodes (4): build_duckdb_globals(), _get_cached_preamble(), Return the static import block for a given registry, building it once.      The, Build a Python preamble for the sandbox that wires up DuckDB access.      Connec

### Community 111 - "Community 111"
Cohesion: 0.7
Nodes (4): _extract_artifact_ids(), post_tool(), PostToolReport, _trim_stdout()

### Community 112 - "Community 112"
Cohesion: 0.7
Nodes (4): _characterized_non_stationary(), _mentions_df(), pre_tool_gate(), _validate_passed_in_trace()

### Community 113 - "Community 113"
Cohesion: 0.4
Nodes (0): 

### Community 114 - "Community 114"
Cohesion: 0.4
Nodes (0): 

### Community 115 - "Community 115"
Cohesion: 0.4
Nodes (0): 

### Community 116 - "Community 116"
Cohesion: 0.5
Nodes (2): GotchaIndex, load_index()

### Community 117 - "Community 117"
Cohesion: 0.4
Nodes (0): 

### Community 118 - "Community 118"
Cohesion: 0.7
Nodes (4): _fake_frame(), test_actual_vs_forecast_forecast_dashed(), test_actual_vs_forecast_has_three_layers_minimum(), test_actual_vs_forecast_raises_if_missing_actual()

### Community 119 - "Community 119"
Cohesion: 0.7
Nodes (4): groupby_counts(), quote(), select(), summary_stats()

### Community 120 - "Community 120"
Cohesion: 0.5
Nodes (2): partial_residuals(), _residuals()

### Community 121 - "Community 121"
Cohesion: 0.4
Nodes (0): 

### Community 122 - "Community 122"
Cohesion: 0.6
Nodes (3): _store(), test_fit_heavy_tail_detects_hill_alpha(), test_fit_normal_series_picks_norm_and_emits_artifacts()

### Community 123 - "Community 123"
Cohesion: 0.8
Nodes (4): _bootstrap_effect(), compare(), _effect(), _run_test()

### Community 124 - "Community 124"
Cohesion: 0.6
Nodes (3): AssumptionReport, check_assumptions(), _is_normal()

### Community 125 - "Community 125"
Cohesion: 0.4
Nodes (0): 

### Community 126 - "Community 126"
Cohesion: 0.8
Nodes (4): AnomalyResult, find_anomalies(), _robust_z(), _seasonal_esd()

### Community 127 - "Community 127"
Cohesion: 0.4
Nodes (0): 

### Community 128 - "Community 128"
Cohesion: 0.4
Nodes (0): 

### Community 129 - "Community 129"
Cohesion: 0.4
Nodes (0): 

### Community 130 - "Community 130"
Cohesion: 0.4
Nodes (2): Slash commands are dispatched client-side; the legacy execute endpoint     is go, test_execute_endpoint_removed()

### Community 131 - "Community 131"
Cohesion: 0.7
Nodes (4): _bar(), main(), _print_analysis(), run_level()

### Community 132 - "Community 132"
Cohesion: 0.6
Nodes (3): main(), startLegacySSE(), startStreamableHTTP()

### Community 133 - "Community 133"
Cohesion: 0.7
Nodes (4): _add_backend_to_path(), _backend_root(), main(), _run()

### Community 134 - "Community 134"
Cohesion: 0.4
Nodes (5): Changelog Policy (docs/log.md), Swiss/Terminal Aesthetic Direction, CLAUDE.md - Project Guide, Skills System Overview, Rationale: Density is a feature (power user UX)

### Community 135 - "Community 135"
Cohesion: 0.4
Nodes (5): Claude Code Explorer MCP Server, MCP Registry Publishing, MCP Legacy SSE Transport, MCP STDIO Transport, MCP Streamable HTTP Transport

### Community 136 - "Community 136"
Cohesion: 0.5
Nodes (3): Table CSS theme for HTML report rendering.  Returns a ``<style>`` block that mat, Return a ``<style>`` block for the requested variant., render_table_css()

### Community 137 - "Community 137"
Cohesion: 0.83
Nodes (3): _profile(), test_ollama_client_posts_and_parses_text_response(), test_ollama_client_surfaces_tool_calls()

### Community 138 - "Community 138"
Cohesion: 0.5
Nodes (0): 

### Community 139 - "Community 139"
Cohesion: 0.83
Nodes (3): end_of_turn(), _has_quantitative_shape(), _section_bodies()

### Community 140 - "Community 140"
Cohesion: 0.5
Nodes (0): 

### Community 141 - "Community 141"
Cohesion: 0.5
Nodes (3): data_info(), Data status endpoint — returns active database name and table list., Return active database name and table list for the UI status indicator.

### Community 142 - "Community 142"
Cohesion: 0.5
Nodes (3): get_hooks(), Read-only endpoint to inspect the current hook configuration (P23).  POST/PUT fo, Return the current hook configuration.

### Community 143 - "Community 143"
Cohesion: 0.5
Nodes (0): 

### Community 144 - "Community 144"
Cohesion: 0.83
Nodes (3): _spec_with_kpi_and_chart(), test_a2ui_chart_tile_references_artifact_id(), test_a2ui_has_version_and_tiles()

### Community 145 - "Community 145"
Cohesion: 0.5
Nodes (0): 

### Community 146 - "Community 146"
Cohesion: 0.83
Nodes (3): _is_missing(), _is_numeric(), render()

### Community 147 - "Community 147"
Cohesion: 0.83
Nodes (3): _spec(), test_render_analysis_brief_md_is_short(), test_render_research_memo_md_contains_key_sections()

### Community 148 - "Community 148"
Cohesion: 0.83
Nodes (3): _spec(), test_render_html_escapes_unsafe_body_markdown(), test_render_html_wraps_in_report_class()

### Community 149 - "Community 149"
Cohesion: 0.5
Nodes (0): 

### Community 150 - "Community 150"
Cohesion: 0.5
Nodes (0): 

### Community 151 - "Community 151"
Cohesion: 0.5
Nodes (0): 

### Community 152 - "Community 152"
Cohesion: 0.5
Nodes (0): 

### Community 153 - "Community 153"
Cohesion: 0.5
Nodes (0): 

### Community 154 - "Community 154"
Cohesion: 0.5
Nodes (0): 

### Community 155 - "Community 155"
Cohesion: 0.83
Nodes (3): correlate(), _p_value(), _point_estimate()

### Community 156 - "Community 156"
Cohesion: 0.5
Nodes (0): 

### Community 157 - "Community 157"
Cohesion: 0.5
Nodes (0): 

### Community 158 - "Community 158"
Cohesion: 0.83
Nodes (3): fit(), _outlier_indices(), _save_chart_artifact()

### Community 159 - "Community 159"
Cohesion: 0.5
Nodes (0): 

### Community 160 - "Community 160"
Cohesion: 0.83
Nodes (3): lag_correlate(), LagCorrelationResult, _shift()

### Community 161 - "Community 161"
Cohesion: 0.5
Nodes (0): 

### Community 162 - "Community 162"
Cohesion: 0.5
Nodes (0): 

### Community 163 - "Community 163"
Cohesion: 0.5
Nodes (0): 

### Community 164 - "Community 164"
Cohesion: 0.5
Nodes (4): Filesystem Tools (FsTools), User-configurable Hook System, Gap Fix & Capability Push Plan, Gap Fix + Capability Push Design

### Community 165 - "Community 165"
Cohesion: 0.5
Nodes (4): CCAGENT_HOME path unification, sessions.db (SQLite + FTS5), Rationale: sessions.db replaces YAML traces (single queryable source), Hermes Migration Design

### Community 166 - "Community 166"
Cohesion: 0.67
Nodes (0): 

### Community 167 - "Community 167"
Cohesion: 0.67
Nodes (1): Todo list read endpoint (P19).  The agent writes todos via the ``todo_write`` to

### Community 168 - "Community 168"
Cohesion: 1.0
Nodes (2): _spec(), test_render_pdf_produces_nonempty_bytes_or_skips()

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
Cohesion: 0.67
Nodes (0): 

### Community 180 - "Community 180"
Cohesion: 0.67
Nodes (0): 

### Community 181 - "Community 181"
Cohesion: 0.67
Nodes (2): Classic waterfall. `kind` values: 'total' (absolute bar) or 'delta' (stepped)., waterfall()

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
Nodes (2): _build_summary(), profile()

### Community 189 - "Community 189"
Cohesion: 1.0
Nodes (2): _is_date(), run()

### Community 190 - "Community 190"
Cohesion: 1.0
Nodes (2): bootstrap_ci(), _statistic()

### Community 191 - "Community 191"
Cohesion: 1.0
Nodes (2): detect_nonlinearity(), pick_method()

### Community 192 - "Community 192"
Cohesion: 0.67
Nodes (0): 

### Community 193 - "Community 193"
Cohesion: 1.0
Nodes (2): _series_for_stationarity(), validate()

### Community 194 - "Community 194"
Cohesion: 1.0
Nodes (2): check_stationarity_for_spurious(), _is_non_stationary()

### Community 195 - "Community 195"
Cohesion: 1.0
Nodes (2): check_leakage(), _parse()

### Community 196 - "Community 196"
Cohesion: 1.0
Nodes (2): check_confounder_risk(), _looks_causal()

### Community 197 - "Community 197"
Cohesion: 0.67
Nodes (0): 

### Community 198 - "Community 198"
Cohesion: 0.67
Nodes (0): 

### Community 199 - "Community 199"
Cohesion: 0.67
Nodes (0): 

### Community 200 - "Community 200"
Cohesion: 0.67
Nodes (0): 

### Community 201 - "Community 201"
Cohesion: 1.0
Nodes (2): ChangepointResult, find_changepoints()

### Community 202 - "Community 202"
Cohesion: 1.0
Nodes (2): decompose(), Decomposition

### Community 203 - "Community 203"
Cohesion: 0.67
Nodes (0): 

### Community 204 - "Community 204"
Cohesion: 0.67
Nodes (0): 

### Community 205 - "Community 205"
Cohesion: 0.67
Nodes (0): 

### Community 206 - "Community 206"
Cohesion: 0.67
Nodes (1): Smoke test for GET /api/hooks.

### Community 207 - "Community 207"
Cohesion: 0.67
Nodes (0): 

### Community 208 - "Community 208"
Cohesion: 0.67
Nodes (3): Batch Runner CLI, ToolsetResolver, H5 - Toolset Composition + Batch Runner

### Community 209 - "Community 209"
Cohesion: 0.67
Nodes (3): BrandingConfig (config/branding.yaml), MCP Sampling Endpoint, H6 - MCP Sampling + Theme System

### Community 210 - "Community 210"
Cohesion: 0.67
Nodes (3): analysis_plan Skill, data_profiler Skill, sql_builder Skill (DuckDB)

### Community 211 - "Community 211"
Cohesion: 0.67
Nodes (3): Project Restructure & Harness Plan, Rationale: Python/FastAPI over TypeScript backend, Project Restructure & Harness Design

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
Nodes (1): Storage helpers used by the REST routers.

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
Nodes (2): Inline Table Synthesis (P24), Gap Closure Phase 4 - Inline Table Synthesis

### Community 268 - "Community 268"
Cohesion: 1.0
Nodes (2): Gap Closure Phase 6 - Spec Drift Reconciliation, Rationale: Inline-collapse over separate component dirs

### Community 269 - "Community 269"
Cohesion: 1.0
Nodes (2): LiteLLM Proxy (Anthropic to Ollama translator), Ollama Integration README

### Community 270 - "Community 270"
Cohesion: 1.0
Nodes (2): ContextManager (L1/L2 layers), Finding 7: claude-code-agent ContextManager

### Community 271 - "Community 271"
Cohesion: 1.0
Nodes (2): Eval Scores Ledger (P27), Gap Closure Phase 5 - Eval Scores Ledger

### Community 272 - "Community 272"
Cohesion: 1.0
Nodes (2): Architecture Overview, Context Layer L1

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
Nodes (1): Load toolset definitions from *path* and return a resolver.

### Community 279 - "Community 279"
Cohesion: 1.0
Nodes (0): 

### Community 280 - "Community 280"
Cohesion: 1.0
Nodes (1): Gap Closure Phase 1 - Cleanup

### Community 281 - "Community 281"
Cohesion: 1.0
Nodes (1): v0.1.0 Release Cut

### Community 282 - "Community 282"
Cohesion: 1.0
Nodes (1): README - Analytical Agent

### Community 283 - "Community 283"
Cohesion: 1.0
Nodes (1): Finding 5: openfang OS-platform layout

### Community 284 - "Community 284"
Cohesion: 1.0
Nodes (1): Finding 6: Analytical-chatbot Progress Panel

### Community 285 - "Community 285"
Cohesion: 1.0
Nodes (1): Git Workflow

### Community 286 - "Community 286"
Cohesion: 1.0
Nodes (1): Testing Guide

## Knowledge Gaps
- **329 isolated node(s):** `A single variant's resolved tokens.`, `Shallow shape check for tokens.yaml. Raises ValueError with a clear message.`, `Storage helpers used by the REST routers.`, `Prometheus metrics for the analytical agent backend.  Import this module early (`, `Application configuration loaded from environment variables.      Runtime data p` (+324 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 212`** (2 nodes): `smoke.spec.ts`, `loadApp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 213`** (2 nodes): `FocusTrap.tsx`, `FocusTrap()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (2 nodes): `VisuallyHidden.tsx`, `VisuallyHidden()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (2 nodes): `LiveRegion.tsx`, `LiveRegion()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (2 nodes): `__init__.py`, `Storage helpers used by the REST routers.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (2 nodes): `test_anthropic_client.py`, `test_anthropic_client_maps_request_to_api()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (2 nodes): `tiers.py`, `apply_tier()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (2 nodes): `test_report_tool.py`, `test_report_build_tool_registered()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (2 nodes): `test_skill_tools.py`, `test_register_core_tools_wires_all_expected_names()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (2 nodes): `a2ui.py`, `to_a2ui()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (2 nodes): `layouts.py`, `resolve_spans()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (2 nodes): `render_md.py`, `render_md()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (2 nodes): `test_composition_smoke.py`, `test_plan_chart_report_dashboard_end_to_end()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (2 nodes): `test_violin.py`, `test_violin_faceted_by_group()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (2 nodes): `test_ecdf.py`, `test_ecdf_uses_window_cumulative_count()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (2 nodes): `test_dumbbell.py`, `test_dumbbell_has_two_points_and_connecting_rule()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 228`** (2 nodes): `test_range_band.py`, `test_range_band_has_area_and_line_layers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (2 nodes): `test_template_surface.py`, `test_all_twenty_templates_exported()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (2 nodes): `test_slope.py`, `test_slope_chart_has_line_segments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (2 nodes): `test_area_cumulative.py`, `test_area_cumulative_returns_area_with_window()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (2 nodes): `actual_vs_forecast.py`, `actual_vs_forecast()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (2 nodes): `boxplot.py`, `boxplot()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (2 nodes): `histogram.py`, `histogram()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (2 nodes): `correlation_heatmap.py`, `correlation_heatmap()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (2 nodes): `area_cumulative.py`, `area_cumulative()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (2 nodes): `range_band.py`, `range_band()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (2 nodes): `multi_line.py`, `multi_line()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (2 nodes): `stacked_bar.py`, `stacked_bar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (2 nodes): `slope.py`, `slope()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (2 nodes): `lollipop.py`, `lollipop()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (2 nodes): `kde.py`, `kde()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (2 nodes): `grouped_bar.py`, `grouped_bar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (2 nodes): `bar_with_reference.py`, `bar_with_reference()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (2 nodes): `bar.py`, `bar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (2 nodes): `ecdf.py`, `ecdf()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (2 nodes): `violin.py`, `violin()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (2 nodes): `scatter_trend.py`, `scatter_trend()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (2 nodes): `dumbbell.py`, `dumbbell()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (2 nodes): `small_multiples.py`, `small_multiples()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (2 nodes): `test_relationships.py`, `test_flags_collinear_pair()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (2 nodes): `duplicates.py`, `run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (2 nodes): `missingness.py`, `run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 254`** (2 nodes): `keys.py`, `run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 255`** (2 nodes): `distributions.py`, `run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (2 nodes): `outliers.py`, `run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (2 nodes): `relationships.py`, `run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (2 nodes): `sample_size.py`, `check_sample_size()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (2 nodes): `multiple_comparisons.py`, `check_multiple_comparisons()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (2 nodes): `simpsons.py`, `check_simpsons_paradox()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (2 nodes): `candidates.py`, `auto_candidates()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (2 nodes): `hill.py`, `hill_alpha()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (2 nodes): `rank.py`, `rank_candidates()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (2 nodes): `methods.py`, `pick_method()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (2 nodes): `test_cli.py`, `test_cli_prints_result_for_latest_report()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (2 nodes): `index.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (2 nodes): `Inline Table Synthesis (P24)`, `Gap Closure Phase 4 - Inline Table Synthesis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (2 nodes): `Gap Closure Phase 6 - Spec Drift Reconciliation`, `Rationale: Inline-collapse over separate component dirs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (2 nodes): `LiteLLM Proxy (Anthropic to Ollama translator)`, `Ollama Integration README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (2 nodes): `ContextManager (L1/L2 layers)`, `Finding 7: claude-code-agent ContextManager`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (2 nodes): `Eval Scores Ledger (P27)`, `Gap Closure Phase 5 - Eval Scores Ledger`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (2 nodes): `Architecture Overview`, `Context Layer L1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (1 nodes): `tailwind.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (1 nodes): `playwright.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `test-setup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (1 nodes): `Load toolset definitions from *path* and return a resolver.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (1 nodes): `vercelApp.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (1 nodes): `Gap Closure Phase 1 - Cleanup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `v0.1.0 Release Cut`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (1 nodes): `README - Analytical Agent`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (1 nodes): `Finding 5: openfang OS-platform layout`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (1 nodes): `Finding 6: Analytical-chatbot Progress Panel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (1 nodes): `Git Workflow`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (1 nodes): `Testing Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionDB` connect `Anthropic Client` to `SOP Analyzer / Suggestions`, `A2A Delegation`, `Test Session Db`, `Prompt Assembler`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `ArtifactStore` connect `Anthropic Client` to `A2A Delegation`, `Frontend Sections (Agents)`, `Prompt Assembler`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `ToolDispatcher` (e.g. with `ToolCall` and `SubagentResult`) actually correct?**
  _`ToolDispatcher` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Are the 79 inferred relationships involving `AgentLoop` (e.g. with `SubagentResult` and `SubagentDispatcher`) actually correct?**
  _`AgentLoop` has 79 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `SessionDB` (e.g. with `TraceRecorder` and `TraceRecorder — buffers events in-memory; finalizes to YAML + SessionDB.`) actually correct?**
  _`SessionDB` has 54 INFERRED edges - model-reasoned connections that need verification._
- **Are the 67 inferred relationships involving `Message` (e.g. with `CompactionReport` and `MicroCompactor`) actually correct?**
  _`Message` has 67 INFERRED edges - model-reasoned connections that need verification._
- **Are the 62 inferred relationships involving `ModelClient` (e.g. with `SubagentResult` and `SubagentDispatcher`) actually correct?**
  _`ModelClient` has 62 INFERRED edges - model-reasoned connections that need verification._