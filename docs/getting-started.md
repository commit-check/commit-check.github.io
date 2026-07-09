# Getting Started

Welcome to commit-check! This guide walks you from zero to enforcing commit
standards in your project — no prior configuration needed.

<!-- markdownlint-disable MD033 -->

---

## 1. Install

Choose the installation method that fits your stack:

=== "pip (recommended)"

    ```bash
    pip install commit-check
    ```

    Requires Python 3.10+. Works on Linux, macOS, and Windows.

    Verify the installation:

    ```bash
    commit-check --version
    # or its shorter alias
    cchk --version
    ```

=== "Homebrew (macOS)"

    ```bash
    brew install commit-check
    ```

=== "pre-commit"

    No direct install needed — add to your `.pre-commit-config.yaml`:

    ```yaml
    repos:
      - repo: https://github.com/commit-check/commit-check
        rev: v2.11.1
        hooks:
          - id: check-message
          - id: check-branch
    ```

    pre-commit will install commit-check automatically when you run
    `pre-commit install --hook-type commit-msg`.

=== "MCP Server (AI agents)"

    AI coding agents (Claude Code, Cursor, Copilot) can use commit-check
    without a direct Python install, via the MCP server:

    ```bash
    # Run with uvx — no install needed
    uvx commit-check-mcp
    ```

    See the [MCP Server docs](https://github.com/commit-check/commit-check-mcp)
    for client-specific configuration instructions.

---

## 2. Run Your First Check

Commit-check works **out of the box with zero configuration**. The default
rules enforce:

- [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
- [Conventional Branch](https://conventionalbranch.org/) for branch names

### Validate a commit message

```bash
# Pass a message via stdin
echo "feat: add user authentication" | commit-check --message
# Exit code: 0 (pass)

echo "bad commit message" | commit-check --message
# Exit code: 1 (fail) — shows error details and suggestion
```

### Validate from a file

```bash
# Pre-commit hooks pass the commit message file automatically
commit-check --message .git/COMMIT_EDITMSG
```

### Validate the current branch

```bash
commit-check --branch
```

### Validate everything at once

```bash
commit-check --message --branch --author-name --author-email
```

### Quiet output for CI

```bash
# Compact mode: one [FAIL] line per failure, no ASCII art
echo "bad message" | commit-check --message --compact
# Output: [FAIL] message: bad message

# Machine-readable JSON (great for automation and AI agents)
echo "feat: add feature" | commit-check --message --format json
```

---

## 3. Add a Configuration File

To customize the rules for your project, create a `cchk.toml` in your
repository root:

```toml
[commit]
# Require imperative mood in subject lines
subject_imperative = true

# Enforce a 72-character subject limit
subject_max_length = 72

# Restrict allowed commit types
allow_commit_types = ["feat", "fix", "docs", "refactor", "test", "chore"]

# Bypass checks for bot authors
ignore_authors = ["dependabot[bot]", "renovate[bot]"]

# AI attribution policy: "ignore" (default) or "forbid"
# "forbid" rejects commits co-authored by known AI coding agents
ai_attribution = "forbid"

[branch]
# Require rebase onto main
require_rebase_target = "main"
```

Run checks again — commit-check automatically discovers the config file:

```bash
commit-check --message --branch
```

> **Tip:** commit-check's TOML schema is published on
> [SchemaStore](https://www.schemastore.org/), so editors like VS Code
> (via the Even Better TOML extension) provide autocompletion and validation
> for `cchk.toml` out of the box.

### Configuration priority

```
CLI arguments  (highest priority)
      ↑
Environment variables  (CCHK_*)
      ↑
cchk.toml / commit-check.toml
      ↑
Built-in defaults  (lowest priority)
```

See the [configuration reference](https://commit-check.github.io/commit-check/configuration.html)
for a complete list of all options.

### Organization-wide config

Share a base policy across all repos in your organization:

```toml
# .github/cchk.toml
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # Override inherited value
```

---

## 4. Set Up Pre-commit Hooks

Commit-check provides five pre-commit hooks:

| Hook ID | Stage | What it checks |
|---------|-------|---------------|
| `check-message` | `commit-msg` | Commit message follows Conventional Commits |
| `check-branch` | `pre-commit` | Branch name follows Conventional Branch |
| `check-author-name` | `pre-commit` | Author name format |
| `check-author-email` | `pre-commit` | Author email format |
| `check-no-force-push` | `pre-push` | Prevents force pushes |

Add them to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.11.1
    hooks:
      - id: check-message
      - id: check-branch
      - id: check-author-name
      - id: check-author-email

  # Force push protection runs on pre-push (not pre-commit)
  - repo: https://github.com/commit-check/commit-check
    rev: v2.11.1
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

Install the hooks:

```bash
pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push
```

Now every commit, branch creation, and push is validated automatically.

---

## 5. Set Up CI/CD

### GitHub Actions

Add the [commit-check-action](https://github.com/commit-check/commit-check-action)
to your workflow:

```yaml
name: Commit Check
on: [push, pull_request]
jobs:
  commit-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write   # Required for PR comments
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0      # Required for merge-base checks
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
          job-summary: true
          pr-comments: ${{ github.event_name == 'pull_request' }}
```

### GitLab CI

```yaml
include:
  - remote: https://raw.githubusercontent.com/commit-check/commit-check/main/examples/gitlab-ci.yml
```

### Other CI platforms

commit-check is a standard Python CLI tool — it works anywhere Python runs.
Set environment variables (`CCHK_*`) or check in a config file, then run
`commit-check --message --branch` in your pipeline step.

---

## 6. Set Up for AI Coding Agents (MCP)

If your team uses AI coding agents (Claude Code, Cursor, Copilot, etc.),
commit-check helps enforce commit standards even on AI-generated commits.

### Claude Desktop

```json
{
  "mcpServers": {
    "commit-check": {
      "command": "uvx",
      "args": ["commit-check-mcp"]
    }
  }
}
```

### Claude Code CLI

Add to your project's `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "commit-check": {
      "command": "uvx",
      "args": ["commit-check-mcp"]
    }
  }
}
```

### AI Attribution Policy

Use the `ai_attribution` config option to control AI-assisted commits:

```toml
[commit]
# "ignore" (default) — AI co-authored commits are allowed
# "forbid"          — rejects commits with known AI tool signatures
ai_attribution = "forbid"
```

When set to `forbid`, commit-check detects signatures from 10+ AI coding
tools (Claude Code, GitHub Copilot, Cursor, Codex, and more) and rejects
commits that carry them.

See the [MCP Server README](https://github.com/commit-check/commit-check-mcp)
for all supported clients and configuration options.

---

## Next Steps

| Topic | Where to go |
|-------|-------------|
| Complete configuration reference | [Configuration docs](https://commit-check.github.io/commit-check/configuration.html) |
| In-depth examples | [Examples page](https://commit-check.github.io/commit-check/example.html) |
| Python API (for automation) | [API reference](commit_check.api) in the Python package |
| Migrate from v1 (YAML) to v2 (TOML) | [Migration guide](https://commit-check.github.io/commit-check/migration.html) |
| GitHub Action details | [commit-check-action](https://github.com/commit-check/commit-check-action) |
| AI agent integration | [commit-check-mcp](https://github.com/commit-check/commit-check-mcp) |
| Report a bug or request a feature | [GitHub Issues](https://github.com/commit-check/commit-check/issues) |
