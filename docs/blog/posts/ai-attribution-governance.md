---
date:
  created: 2026-07-06
readtime: 7
categories:
  - UPDATES
tags:
  - commit-check
  - ai
  - governance
  - compliance
authors:
  - shenxianpeng
---

# AI Attribution Governance: Enforcing AI Disclosure Policies at the CI Level

The open-source ecosystem is converging on a hard question: **when a commit is
written with AI assistance, how do we know — and how do we enforce the
disclosure policy?**

Python's discourse, Linux kernel's `Assisted-by` trailer, Fedora's AI policy,
Apache's disclosure guidelines — every major project is grappling with this.
But until now, there has been **no tool at the CI level** to enforce whatever
policy a project chooses.

Commit Check v2.11.0 introduces **AI Attribution Governance** — a
first-of-its-kind feature that detects known AI tool signatures in commit
messages and lets projects decide whether to forbid them outright.

<!-- more -->

## The industry need

The conversation around AI disclosure is no longer theoretical:

- The **Linux kernel** standardized on the `Assisted-by:` trailer format
- The **Python community** [is actively discussing](https://discuss.python.org/t/should-claude-codes-usage-be-described-in-the-code-docs-somewhere/107969) whether Claude Code usage should be documented
- **VS Code** [issue #313962](https://github.com/microsoft/vscode/issues/313962) proposes replacing `Co-authored-by` with `Assisted-by` for AI agents
- **Fedora, Apache, OpenTelemetry, Rocky Linux, QEMU, Gentoo** each have different AI contribution policies

But nobody had built a neutral enforcement layer that works in CI — until now.

## Configuration: a single toggle

Commit Check keeps it simple. One configuration value, three ways to set it:

=== "TOML (cchk.toml)"

    ```toml
    [commit]
    ai_attribution = "forbid"
    ```

=== "CLI"

    ```bash
    commit-check --message --ai-attribution=forbid
    ```

=== "Environment Variable"

    ```bash
    CCHK_AI_ATTRIBUTION=forbid commit-check --message
    ```

Two modes:

| Mode | Behavior |
|------|----------|
| `"ignore"` | No validation (default, backward compatible) |
| `"forbid"` | Rejects any commit containing known AI tool signatures |

There is no `require` mode or `ai_trailer_style` option — the signature
database recognizes all known formats automatically, and the policy is simply
whether you allow them or not.

## Detected AI tool signatures

Commit Check ships with a curated database of known AI tool markers. The
detection covers multiple signature formats per tool — `Co-authored-by`,
`Assisted-by`, body markers, and model names:

| AI Tool | What gets detected |
|---------|-------------------|
| **Claude Code** | `Co-authored-by: Claude`, `Assisted-by: Claude:<model>`, emoji markers, `Claude-Session:`, `Claude-Workflow:` |
| **GitHub Copilot** | `Co-authored-by: Copilot` |
| **OpenAI Codex** | `Co-authored-by: Codex` |
| **Gemini** | `Co-authored-by: Gemini` |
| **Cursor** | `Co-authored-by: Cursor` |
| **Devin** | `Co-authored-by: Devin` |
| **Aider** | `Co-authored-by: Aider`, `Co-authored-by: ... (aider)` |
| **Windsurf** | `Co-authored-by: Windsurf` |
| **Tabby** | `Co-authored-by: Tabby` |
| **Generic AI** | `Assisted-by: <tool>:<model> [tools]`, model names like `claude-sonnet-4`, `gpt-4-turbo` |

## Built-in false positive prevention

A `Co-authored-by: Claude` could theoretically be a human named Claude — but
in practice, AI tools use known noreply email addresses. Commit Check anchors
its detection to these, so:

✅ `Co-authored-by: Claude <noreply@anthropic.com>` — flagged  
✅ `Assisted-by: Claude:claude-sonnet-4-20250514 [tools]` — flagged  
❌ `Co-authored-by: Claude Monet <monet@impressionism.fr>` — **not flagged**  
❌ `Co-authored-by: Jane Doe <jane@example.com>` — **not flagged**

The kernel-style `Assisted-by:` format also handles optional trailing tool
lists correctly:

```text
Assisted-by: Claude:claude-sonnet-4-20250514 coccinelle sparse
```

Only the AI tool marker is matched — the tool list is preserved as-is.

## See it in action

With a config file containing `ai_attribution = "forbid"`:

```bash
# This commit message would be REJECTED
echo "fix: resolve race condition

Co-authored-by: Claude <noreply@anthropic.com>" | commit-check -m
```

```text
[FAIL] ai-attribution: Commit message contains known AI tool signature: Claude
```

```bash
# This commit message passes cleanly
echo "fix: resolve race condition

Co-authored-by: Jane Doe <jane@example.com>" | commit-check -m
```

```text
[PASS] commit message is valid
```

## Integration across the ecosystem

The feature is available across every surface of Commit Check:

- **CLI**: `--ai-attribution=forbid`
- **TOML config**: `[commit] ai_attribution = "forbid"`
- **Environment variables**: `CCHK_AI_ATTRIBUTION=forbid`
- **Python API**: `validate_message()` returns AI attribution results
- **`--format json`**: AI check status included in structured output
- **MCP Server** ([commit-check-mcp](https://github.com/commit-check/commit-check-mcp)): synced in v0.1.7
- **GitHub Action** ([commit-check-action](https://github.com/commit-check/commit-check-action)): available once the underlying dependency is updated

## What's next

AI attribution governance in v2.11.0 is the foundation. Future work includes:

1. **PR summaries** — show AI disclosure status per commit in pull requests
2. **MCP improvements** — AI agents query `describe_validation_rules` to
   auto-comply before writing a commit
3. **Richer JSON metadata** — structured AI signature data for SBOM and audit
   tooling

## Try it today

```bash
pip install commit-check==2.11.0
echo "feat: add streaming support" | commit-check -m --ai-attribution=forbid
```

Or add it to your `cchk.toml`:

```toml
[commit]
ai_attribution = "forbid"
```

And let CI enforce your AI disclosure policy — automatically, on every commit.

---

*Clean commits. Clear standards. Transparent AI contributions.*
