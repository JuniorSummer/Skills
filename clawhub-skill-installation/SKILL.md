---
name: clawhub-skill-installation
description: Install skills from ClawHub mirrors when standard hermes methods fail. Covers API discovery, fallback strategies, and manual skill installation.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [skills, installation, clawhub, mirror, troubleshooting]
  use_when:
    - Installing a skill from a ClawHub mirror URL fails
    - hermes skills install times out or can't find the skill
    - Standard tap additions don't work
---

# ClawHub Skill Installation

When installing skills from ClawHub mirrors (like cn.clawhub-mirror.com), the standard hermes commands may fail. This skill documents the troubleshooting process and fallback methods.

## Standard Method (Try First)

```bash
# Add the GitHub repo as a tap
hermes skills tap add owner/repo

# Then search/install
hermes skills search <keyword>
hermes skills install <identifier>
```

## Troubleshooting Steps

### 1. Check if the skill exists in hub

```bash
hermes skills search <skill-name>
```

### 2. Try adding tap from GitHub

```bash
hermes skills tap add waisimon/playwright-scraper-skill
hermes skills search <name>
```

### 3. Explore ClawHub API structure

Many ClawHub mirror endpoints return HTML (SPA), not JSON:

```python
import requests

# These typically return HTML, not useful data
endpoints = [
    "https://cn.clawhub-mirror.com/api/skill/{repo}",
    "https://cn.clawhub-mirror.com/skills/{repo}",
]

# Try sitemap for discovery
response = requests.get("https://cn.clawhub-mirror.com/sitemap-static.xml", timeout=30)
```

### 4. Manual Skill Installation (Fallback)

When API methods fail, manually create the skill:

```bash
# Create skill directory
mkdir -p ~/.hermes/skills/<category>/<skill-name>

# Create SKILL.md with proper YAML frontmatter
```

**YAML Frontmatter Template:**

```yaml
---
name: <skill-name>
description: <description>
version: 1.0.0
author: <author>
metadata:
  hermes:
    tags: [<tags>]
    homepage: <repo-url>
  prerequisites:
    commands: [<required-commands>]
    packages: [<required-pip-packages>]
  examples:
    - <example-use-case-1>
    - <example-use-case-2>
---

# Skill Title

Describe the skill purpose, installation, and usage...
```

### 5. Verify Installation

```bash
hermes skills list | grep -i <skill-name>
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Tap added but skill not found | Check if repo exists on GitHub |
| API returns HTML not JSON | ClawHub is SPA, use manual install |
| Git clone fails (timeout) | Create skill manually from docs |
| hermes skills install timeout | Use --force or try manual method |

## Example: Installing playwright-scraper

```bash
# Step 1: Try standard method
hermes skills tap add waisimon/playwright-scraper-skill
hermes skills search playwright

# Step 2: If fails, create manually
mkdir -p ~/.hermes/skills/productivity/playwright-scraper

# Step 3: Write SKILL.md with frontmatter + content
# See ~/.hermes/skills/productivity/playwright-scraper/SKILL.md for example

# Step 4: Verify
hermes skills list | grep playwright
```

## Key Insights

- ClawHub mirrors are SPAs - no simple REST API for skill content
- Network access to raw.githubusercontent.com may be blocked
- Manual installation bypasses network issues entirely
- YAML frontmatter is required for hermes to recognize the skill