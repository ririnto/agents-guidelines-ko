---
name: implement
description: Implement features and write code following best practices.
argument-hint: 'Describe the feature to implement (e.g., "Add user login with OAuth2")'
---

# Implement Code

Implement requested features following language conventions.

## Implementation Rules

### Code Style

- Follow language conventions; write self-documenting code
- Avoid unnecessary comments; add JSDoc/docstrings only when naming is insufficient, logic is complex, or public API needs examples

## Process

1. Understand: clarify requirements; ask if ambiguous.
2. Plan: design interface/structure.
3. Implement: write code following conventions.
4. Test: add/update tests.
5. Validate: run tests/lint.

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

| Language | Classes | Functions | Constants |
| --- | --- | --- | --- |
| Java | PascalCase | camelCase | SCREAMING_SNAKE |
| Python | PascalCase | snake_case | SCREAMING_SNAKE |
| JavaScript | PascalCase | camelCase | SCREAMING_SNAKE |
| Go | PascalCase | camelCase | PascalCase |
| C++ | PascalCase | snake_case | SCREAMING_SNAKE |

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
