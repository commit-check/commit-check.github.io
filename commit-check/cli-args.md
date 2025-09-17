---
layout: default
title: CLI Arguments - Commit Check Tool
permalink: /commit-check/cli-args/
---

# CLI Arguments

## commit-check --help

```
usage: commit-check [-h] [-m] [-b] [-a] [-e] [-s] [-i] [-n] [-d]
                    [--message-skip-on MESSAGE_SKIP_ON] [--commit-skip-on COMMIT_SKIP_ON]
                    [--config CONFIG]

Checks commit message formatting, branch naming, commit author name, commit author email, commit signoff, 
and the commit is a merge base.

options:
  -h, --help            show this help message and exit
  -m, --message         check commit message formatting
  -b, --branch          check branch name
  -a, --author-name     check commit author name
  -e, --author-email    check commit author email  
  -s, --commit-signoff  check commit signoff
  -i, --imperative      check commit message is imperative mood
  -n, --merge-base      check current branch is rebased onto the target branch
  -d, --dry-run         dry run without fail
  --message-skip-on MESSAGE_SKIP_ON
                        skip checking message on given text
  --commit-skip-on COMMIT_SKIP_ON
                        skip checking commit on given text
  --config CONFIG       path to config file, default is .commit-check.yml
```

## Options Details

### `-m, --message`
Check commit message formatting against the configured rules. By default, this follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

### `-b, --branch`
Check branch naming conventions. By default, this follows [Conventional Branch](https://conventional-branch.github.io/) naming patterns.

### `-a, --author-name`
Validate the commit author name against configured patterns.

### `-e, --author-email`
Validate the commit author email against configured patterns.

### `-s, --commit-signoff`
Check that commits include a valid "Signed-off-by" line.

### `-i, --imperative`
Check that commit messages use imperative mood (e.g., "Add feature" not "Added feature").

### `-n, --merge-base`
Check that the current branch is properly rebased onto the target branch. This is useful for ensuring clean merge history.

### `-d, --dry-run`
Run all checks without failing. The exit code will be 0 regardless of check results, but violations will still be reported.

### `--message-skip-on TEXT`
Skip message checking when the commit message contains the specified text.

### `--commit-skip-on TEXT`
Skip all commit checking when the commit SHA or message contains the specified text.

### `--config PATH`
Specify a custom path to the configuration file. Defaults to `.commit-check.yml` in the repository root.

## Examples

### Basic Usage
```bash
# Check all common validations
commit-check --message --branch --author-name --author-email

# Check specific validations
commit-check -m -b  # Short form

# Include signoff and imperative checking
commit-check --message --branch --commit-signoff --imperative
```

### Advanced Usage
```bash
# Dry run to see what would fail without actually failing
commit-check --message --branch --dry-run

# Skip certain commits
commit-check --message --commit-skip-on "WIP"

# Use custom config file
commit-check --config /path/to/custom-config.yml --message --branch
```

### Integration Examples

**Git Hook**
```bash
#!/bin/sh
# .git/hooks/pre-push
commit-check --message --branch --author-name --author-email --commit-signoff
```

**CI/CD**
```bash
# Run in CI pipeline
commit-check --message --branch --author-name --author-email --merge-base
```

## Configuration

All CLI options can be customized via the `.commit-check.yml` configuration file. See the [main documentation](../) for configuration details.

[← Back to Commit Check Documentation](../)