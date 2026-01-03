---
name: code-review
description: 'Review code changes for quality, bugs, security, and performance issues. Use when the user asks to review code, check a PR, do a code quality check, security review, find bugs, or requests code inspection.'
compatibility: Requires Git repository and code reading tools
allowed-tools:
  - Bash(git:*, node:*, npm:*, npx:*, pnpm:*, yarn:*, python:*, pip:*, pytest:*, go:*, cargo:*, mvn:*, ./mvnw:*, gradle:*, ./gradlew:*, make:*, cmake:*, g++:*, gcc:*, clang:*)
  - Glob
  - Grep
  - Read
  - mcp__context7
  - mcp__fetch
  - mcp__git
  - mcp__jetbrains
  - mcp__markitdown
  - mcp__sequential-thinking
  - mcp__serena
---

# Code Review Skill

Systematically review code changes to identify quality, security,
and performance issues.

## Review Process

### 1. Gather Context

Check changed files:

```bash
git diff --name-only HEAD~1
git diff --cached --name-only
git status --short
```

Use MCP tools for deeper analysis:

- `mcp__git__git_diff` - View detailed changes
- `mcp__serena__find_referencing_symbols` - Track symbol usage
- `mcp__jetbrains__get_symbol_info` - Get symbol documentation

### 2. Analysis Areas

#### Code Quality

- Readability and clarity
- Consistent code style
- Appropriate abstraction level
- Code duplication
- Complexity (recommend ≤15 lines per function)

#### Potential Bugs

- Logic errors and edge cases
- Null/undefined handling
- Missing error handling
- Resource cleanup

#### Security Vulnerabilities

- SQL/Command Injection
- XSS (Cross-Site Scripting)
- Authentication/Authorization issues
- Sensitive data exposure
- Hardcoded secrets

#### Performance

- Unnecessary loops
- N+1 query problems
- Memory leak potential
- Inefficient algorithms

#### Test Coverage

- Test existence
- Edge case testing
- Mocking appropriateness

### 3. Output Format

```markdown
## Code Review Summary

[2-3 sentence overview of changes]

## Critical Issues (Must Fix)

- `file:line` - [Issue description] - [Fix approach]

## Major Issues (Should Fix)

- `file:line` - [Issue description] - [Improvement suggestion]

## Minor Suggestions (Optional)

- `file:line` - [Suggestion]

## Positive Observations

- [Good practices noted]

## Overall Assessment

[Final recommendations]
```

## Language-Specific Checkpoints

### JavaScript/TypeScript

- strict mode usage
- async/await error handling
- Type definition completeness
- ESLint rule compliance

### Python

- PEP 8 style
- Type hints usage
- Resource management with `with` statement
- Exception handling specificity

### Java/Kotlin

- Null safety
- Prefer immutable objects
- try-with-resources for resources
- Thread safety

### Go

- Error handling patterns
- defer usage
- goroutine leak prevention
- context propagation

## Edge Cases

- **No changes**: Notify that there is nothing to review
- **More than 20 issues**: Group by type, show top 10 by severity first
- **Unclear intent**: Specify ambiguous parts and request clarification
- **Config files only**: Analyze impact scope of configuration changes

## Notes

- MCP tools are optional; omit if unavailable or add others as needed
