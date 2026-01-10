---
name: create-pr
description: Auto-generate PR descriptions.
argument-hint: 'Optionally specify PR scope or additional context'
---

# PR Description Generation

Analyze git changes and generate PR descriptions.

## Analysis Procedure

1. Gather changes:
   ```bash
   git diff main...HEAD --stat
   git log main..HEAD --oneline
   ```
2. Classify change types: feat, fix, refactor, docs, test, chore.
3. Assess impact: files/modules, dependencies, configs.

## Output Format

```markdown
## Overview

[One-line summary of changes]

## Changes

### Added

- [New features/files]

### Modified

- [Changed features/behavior]

### Removed

- [Removed features/files]

## Details

[Additional context or design decision rationale if needed]

## Testing

- [ ] Unit tests added/modified
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code style compliance
- [ ] Documentation updated
- [ ] No breaking changes

## Related Issues

Closes #issue-number
```

## PR Title Format

```text
<type>(<scope>): <description>
```

**Examples:**

- `feat(auth): add OAuth login functionality`
- `fix(api): fix null handling in user query`
- `refactor(core): improve data processing logic`

## Notes

- Describe changes clearly and concisely.
- Structure for easy reviewer comprehension.
- Link related issues or documentation.
- Explicitly mark breaking changes if present.

## User Input

```text
$ARGUMENTS
```

Consider any additional context from the user input above when generating the PR description.
