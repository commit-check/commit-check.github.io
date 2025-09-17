---
layout: default
title: Troubleshooting - Commit Check Action
permalink: /commit-check-action/troubleshooting/
---

# Troubleshooting

Common issues and solutions for Commit Check GitHub Action.

## Common Issues

### Action Fails with "Permission denied"

**Problem**: The action fails with permission errors when trying to post PR comments.

**Solution**: Ensure you have the correct permissions in your workflow:

```yaml
permissions:
  contents: read
  pull-requests: write  # Required for PR comments
```

### Action Doesn't Work with Forked Repositories

**Problem**: PR comments feature doesn't work when the PR comes from a forked repository.

**Solution**: This is a known limitation. Forked repositories have restricted permissions for security reasons. Use `job-summary: true` instead:

```yaml
- uses: commit-check/commit-check-action@v1
  with:
    pr-comments: false
    job-summary: true
```

### merge-base Check Fails

**Problem**: The merge-base check fails unexpectedly.

**Solution**: Ensure you're fetching enough history:

```yaml
- uses: actions/checkout@v5
  with:
    fetch-depth: 0  # Fetch all history
```

### Custom Configuration Not Applied

**Problem**: Your `.commit-check.yml` file is not being used.

**Solution**: 
1. Ensure the file is in the repository root
2. Check the file syntax with a YAML validator
3. Verify the file is committed and available in the checked-out branch

### Action Times Out

**Problem**: The action takes too long and times out.

**Solution**: 
1. Use `fetch-depth: 1` if you don't need merge-base checking
2. Consider using `dry-run: true` for debugging
3. Check if your regex patterns are too complex

## Debug Mode

Enable debug mode by setting environment variables:

```yaml
- uses: commit-check/commit-check-action@v1
  env:
    ACTIONS_STEP_DEBUG: true
  with:
    dry-run: true
```

## Configuration Validation

Test your configuration locally:

```bash
# Install commit-check locally
pip install commit-check

# Test with your config
commit-check --config .commit-check.yml --dry-run --message --branch
```

## Getting Help

If you're still experiencing issues:

1. Check the [Issues](https://github.com/commit-check/commit-check/issues) page
2. Search for similar problems in [Discussions](https://github.com/commit-check/commit-check/discussions)
3. Create a new issue with:
   - Your workflow YAML
   - Error messages
   - Example commits that fail

[← Back to GitHub Action Documentation](../)