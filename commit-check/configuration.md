---
layout: default
title: Configuration - Commit Check Tool
permalink: /commit-check/configuration/
---

# Configuration

Commit Check can be configured using a `.commit-check.yml` file in your repository root.

## Default Configuration

If no configuration file is provided, Commit Check uses sensible defaults based on:
- [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
- [Conventional Branch](https://conventional-branch.github.io/) for branch naming

## Configuration File Structure

Create a `.commit-check.yml` file in your repository root:

```yaml
checks:
  # Commit message configuration
  message:
    enabled: true
    regex: '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)'
    error: "Commit message doesn't match Conventional Commits format"
    suggest: "Use format: <type>[optional scope]: <description>"

  # Branch naming configuration  
  branch:
    enabled: true
    regex: '^(bugfix|feature|release|hotfix|task|chore)\/.+|(master)|(main)|(HEAD)|(PR-.+)'
    error: "Branch name doesn't follow naming convention"
    suggest: "Use: feature/description, bugfix/description, etc."

  # Author name configuration
  author_name:
    enabled: true
    regex: '^.+$'
    error: "Author name is required"
    suggest: "Configure git user.name"

  # Author email configuration
  author_email:
    enabled: true
    regex: '^.+@.+\..+$'
    error: "Valid author email is required"
    suggest: "Configure git user.email with a valid email"

  # Commit signoff configuration
  commit_signoff:
    enabled: false
    regex: 'Signed-off-by:.*[A-Za-z0-9]\s+<.+@.+>'
    error: "Commit must be signed off"
    suggest: "Use 'git commit --signoff'"

  # Imperative mood configuration
  imperative:
    enabled: false
    error: "Commit message should use imperative mood"
    suggest: "Use imperative mood like 'Add', 'Fix', 'Update'"

  # Merge base configuration
  merge_base:
    enabled: false
    error: "Branch is not rebased onto target branch"
    suggest: "Rebase your branch onto the target branch"
```

## Configuration Options

### Global Settings

- `enabled`: Enable or disable the entire check
- `regex`: Regular expression pattern to match against
- `error`: Custom error message to display
- `suggest`: Suggestion text to help users fix the issue

### Message Check

Configure commit message validation:

```yaml
checks:
  message:
    enabled: true
    regex: '^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'
    error: "Invalid commit message format"
    suggest: "Use: type(scope): description (max 50 chars)"
```

### Branch Check

Configure branch naming validation:

```yaml
checks:
  branch:
    enabled: true
    regex: '^(feature|bugfix|hotfix|release)\/[a-z0-9-]+$'
    error: "Invalid branch name"
    suggest: "Use: feature/my-feature, bugfix/my-fix"
```

### Author Checks

Configure author name and email validation:

```yaml
checks:
  author_name:
    enabled: true
    regex: '^[A-Za-z ]+$'
    error: "Author name must contain only letters and spaces"
    
  author_email:
    enabled: true
    regex: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    error: "Author email must be a valid email address"
```

## Examples

### Strict Configuration

```yaml
checks:
  message:
    enabled: true
    regex: '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,72}$'
    error: "Commit message must follow Conventional Commits with max 72 chars"
    
  branch:
    enabled: true
    regex: '^(feature|bugfix|hotfix|release|support)\/[a-z0-9-]{3,50}$'
    error: "Branch must be: type/description (3-50 chars, lowercase, hyphens)"
    
  author_name:
    enabled: true
    regex: '^[A-Z][a-z]+ [A-Z][a-z]+$'
    error: "Author name must be First Last format"
    
  author_email:
    enabled: true
    regex: '^[a-zA-Z0-9._%+-]+@(company\.com|example\.org)$'
    error: "Author email must be from company.com or example.org domain"
    
  commit_signoff:
    enabled: true
    regex: 'Signed-off-by: .+ <.+@.+>'
    error: "All commits must be signed off"
    suggest: "Add '--signoff' to your git commit command"
```

### Relaxed Configuration

```yaml
checks:
  message:
    enabled: true
    regex: '^.{10,}$'
    error: "Commit message must be at least 10 characters"
    
  branch:
    enabled: false
    
  author_name:
    enabled: true
    regex: '^.+$'
    error: "Author name is required"
    
  author_email:
    enabled: true
    regex: '^.+@.+$'
    error: "Author email is required"
```

## Skip Patterns

You can configure patterns to skip validation:

```yaml
skip:
  message_patterns:
    - "^WIP:"
    - "^Merge "
    - "^Revert "
  
  commit_patterns:
    - "skip-check"
    - "no-verify"
```

## Environment Variables

Some settings can be overridden with environment variables:

- `COMMIT_CHECK_CONFIG`: Path to configuration file
- `COMMIT_CHECK_SKIP`: Skip all checks if set to "true"

## Testing Configuration

Test your configuration with dry-run mode:

```bash
commit-check --config .commit-check.yml --dry-run --message --branch
```

[← Back to Commit Check Documentation](../)