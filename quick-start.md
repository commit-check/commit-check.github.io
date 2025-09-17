---
layout: default
title: Quick Start Guide
permalink: /quick-start/
---

# Quick Start Guide

Get up and running with Commit Check in minutes.

## For GitHub Actions

### 1. Create Workflow File

Create `.github/workflows/commit-check.yml` in your repository:

```yaml
name: Commit Check

on:
  push:
  pull_request:

jobs:
  commit-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - uses: commit-check/commit-check-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
          pr-comments: ${{ github.event_name == 'pull_request' }}
```

### 2. Commit and Push

The action will automatically run on your next commit or pull request.

## For Local Development

### 1. Install Commit Check

```bash
pip install commit-check
```

### 2. Run Manually

```bash
commit-check --message --branch --author-name --author-email
```

### 3. Set Up Pre-commit Hook

Install pre-commit:
```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: main
    hooks:
      - id: check-message
      - id: check-branch
      - id: check-author-name
      - id: check-author-email
```

Install the hooks:
```bash
pre-commit install
```

## For Git Hooks

### 1. Create Hook Script

Create `.git/hooks/pre-push`:

```bash
#!/bin/sh
commit-check --message --branch --author-name --author-email
```

### 2. Make Executable

```bash
chmod +x .git/hooks/pre-push
```

## Configuration (Optional)

Create `.commit-check.yml` for custom rules:

```yaml
checks:
  message:
    enabled: true
    regex: '^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'
    
  branch:
    enabled: true
    regex: '^(feature|bugfix|hotfix)\/[a-z0-9-]+$'
```

## Next Steps

- [View detailed documentation](commit-check/) for the CLI tool
- [Learn about GitHub Actions](commit-check-action/) integration
- [Customize configuration](commit-check/configuration/) for your needs
- [Get help with troubleshooting](commit-check-action/troubleshooting/)

## Need Help?

- 📖 [Full Documentation](/)
- 🐛 [Report Issues](https://github.com/commit-check/commit-check/issues)
- 💬 [Join Discussions](https://github.com/commit-check/commit-check/discussions)