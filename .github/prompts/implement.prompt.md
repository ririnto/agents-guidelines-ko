---
name: implement
description: Implement features and write code following best practices.
argument-hint: 'Describe the feature to implement (e.g., "Add user login with OAuth2")'
---

# Implement Code

Implement requested features following language conventions.

## Implementation Rules

### Code Style

- Follow language-specific naming conventions
- Write self-documenting code
- No unnecessary comments

### When to Add Documentation

Add JSDoc or docstrings only when:

- Method name cannot fully express intent
- Complex algorithm needs explanation
- Public API requires usage examples

### Comment Policy

- Do NOT add comments unless explicitly requested
- Let code speak for itself through good naming
- Use documentation annotations for complex logic

## Process

1. **Understand** - Clarify requirements, ask if ambiguous
2. **Plan** - Design interface and structure
3. **Implement** - Write code following conventions
4. **Test** - Add or update tests
5. **Validate** - Run tests and lint checks

## Output Format

```markdown
## Implementation

### Files Changed

| File | Type  | Description |
| ---- | ----- | ----------- |
| path | Added | Description |

### Key Decisions

[Design choices made]

### Testing

[Tests added]

### Usage

(example code)
```

## Language Conventions Quick Reference

| Language   | Classes     | Functions    | Constants           |
| ---------- | ----------- | ------------ | ------------------- |
| Java       | PascalCase  | camelCase    | SCREAMING_SNAKE     |
| Python     | PascalCase  | snake_case   | SCREAMING_SNAKE     |
| JavaScript | PascalCase  | camelCase    | SCREAMING_SNAKE     |
| Go         | PascalCase  | camelCase    | PascalCase          |
| C++        | PascalCase  | snake_case   | SCREAMING_SNAKE     |

## Notes

- Implement only what is requested
- Match existing project style
- Write tests alongside implementation

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input above before proceeding.
If the input is empty, ask what feature to implement.
