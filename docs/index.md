---
hide:
  - navigation
  - toc
template: home.html
title: Commit Check
---

<!-- markdownlint-disable MD041 MD033 MD036 MD025 -->

# Commit Check

## Everything you need for commit-check

<div class="grid cards" markdown>

- :material-chart-line: **Built in Open Source**

    ---

    Open-source and MIT-licensed. Bringing contributors together to empower impactful commit-check projects in open source and beyond.

- :material-cog: **Zero Configuration**

    ---

    Works out of the box with sensible defaults. Advanced users can customize every aspect to match their commit and branch standards.

- :material-devices: **Works Everywhere**

    ---

    GitHub Actions, Pre-commit, Command Line – integrate anywhere your code lives.

</div>

<div class="grid" markdown>

</div>

## Trusted by developers worldwide

<div class="trusted-by" markdown>

**Join thousands of developers and organizations using commit-check in production**

<div class="logo-grid">
  <div class="logo-item">
    <img src="https://github.com/apache.png" alt="Apache" title="Apache">
    <span>Apache</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/discovery-unicamp.png" alt="Discovery Unicamp" title="Discovery Unicamp">
    <span>Discovery Unicamp</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/TexasInstruments.png" alt="Texas Instruments" title="Texas Instruments">
    <span>Texas Instruments</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/opencadc.png" alt="OpenCADC" title="OpenCADC">
    <span>OpenCADC</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/extrawest.png" alt="Extrawest" title="Extrawest">
    <span>Extrawest</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/Chainlift.png" alt="Chainlift" title="Chainlift">
    <span>Chainlift</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/mila-iqia.png" alt="Mila" title="Mila">
    <span>Mila</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/RLinf.png" alt="RLinf" title="RLinf">
    <span>RLinf</span>
  </div>
</div>

<!-- <div class="stats-grid">
  <div class="stat">
    <strong>1,000+</strong>
    <span>GitHub Users</span>
  </div>
  <div class="stat">
    <strong>20K+</strong>
    <span>Downloads/Month</span>
  </div>
  <div class="stat">
    <strong>50+</strong>
    <span>Contributors</span>
  </div>
</div> -->

</div>

## Quick Start

=== "GitHub Actions"

    Add commit-check-action to your workflow in seconds:

    ```yaml
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # checkout PR HEAD commit
          fetch-depth: 0  # required for merge-base check
      - uses: commit-check/commit-check-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # use GITHUB_TOKEN because use of pr-comments
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
          job-summary: true
          pr-comments: ${{ github.event_name == 'pull_request' }}
    ```

=== "Pre-commit"

    Add to your `.pre-commit-config.yaml`:

    ```yaml
    repos:
      repo: https://github.com/commit-check/commit-check
      rev: the tag or revision
      hooks:
      -   id: check-message
      -   id: check-branch
      -   id: check-author-name
      -   id: check-author-email
    ```

=== "Command Line"

    Install and run locally:

    ```bash
    pip install commit-check

    # Validate message from STDIN
    echo "feat: new feature" | commit-check -m

    # Validate message from file
    commit-check -m commit_message.txt

    # Validate current git commit message (from git log)
    commit-check -m
    ```

---

<div class="community-section" markdown>

## Join Our Community

**Be part of a growing ecosystem of Commit Check developers who care about code quality.**

[GitHub Issue :fontawesome-brands-github:](https://github.com/commit-check/commit-check/issues){ .md-button }
[GitHub Pull Request :fontawesome-brands-github:](https://github.com/commit-check/commit-check/pulls){ .md-button }
<!-- [Discord Community :fontawesome-brands-discord:](https://discord.gg/commit-check){ .md-button }
[Stack Overflow :fontawesome-brands-stack-overflow:](https://stackoverflow.com/questions/tagged/commit-check){ .md-button } -->

</div>
