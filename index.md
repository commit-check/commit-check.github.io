---
layout: default
title: Commit Check Documentation
---

# Commit Check Documentation

Welcome to the central documentation site for the Commit Check organization. Commit Check provides powerful tools for enforcing commit metadata standards across your development workflow.

## Available Tools

### [Commit Check Tool](commit-check/)
The main commit-check tool is a powerful command-line utility and pre-commit hook that enforces commit message formatting, branch naming, committer information, and more.

**Features:**
- Commit message validation (Conventional Commits support)
- Branch naming conventions
- Author name and email validation
- Commit signature verification
- Multiple integration options (CLI, pre-commit, Git hooks)

[View Documentation →](commit-check/)

### [Commit Check GitHub Action](commit-check-action/)
A GitHub Action that brings commit-check validation directly to your CI/CD pipeline, with support for pull request comments and job summaries.

**Features:**
- Seamless GitHub integration
- Pull request validation
- Workflow job summaries
- Custom configuration support
- Works with fork repositories

[View Documentation →](commit-check-action/)

## Quick Start

### Using as GitHub Action
```yaml
- uses: commit-check/commit-check-action@v1
  with:
    message: true
    branch: true
    author-name: true
    author-email: true
```

### Using as CLI Tool
```bash
pip install commit-check
commit-check --message --branch --author-name --author-email
```

### Using as Pre-commit Hook
```yaml
- repo: https://github.com/commit-check/commit-check
  rev: main
  hooks:
    - id: check-message
    - id: check-branch
```

## Getting Help

- **Issues & Feature Requests**: [GitHub Issues](https://github.com/commit-check/commit-check/issues)
- **Discussions**: [GitHub Discussions](https://github.com/commit-check/commit-check/discussions)
- **Source Code**: [GitHub Organization](https://github.com/commit-check)

## License

All Commit Check tools are released under the MIT License.