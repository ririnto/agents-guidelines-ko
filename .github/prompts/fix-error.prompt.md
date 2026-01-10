---
name: fix-error
description: Analyze error messages and provide fix recommendations.
argument-hint: 'Paste the error message or describe the issue'
---

# Fix Error

Analyze given error messages and provide solutions.

## Analysis Procedure

1. Classify error: syntax, runtime, type, reference, network/external.
2. Stack trace: location(file:line), call path, related code.
3. Root cause: interpret message, inspect context, match common patterns.
4. Solutions: recommend fix, alternatives, preventive measures.

## Output Format

```markdown
## Error Analysis

### Error Type

[Error classification]

### Location

`filepath:linenumber`

### Cause

[Root cause explanation]

### Solutions

**Method 1 (Recommended):** (fix code)

**Method 2 (Alternative):** ...

### Preventive Measures

- [Suggestions for future prevention]
```

## Notes

- If the error message is incomplete, request additional information.
- Analyze related code files together if available.
- Search codebase for similar error patterns.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input above before proceeding.
If the input is empty, check for errors in the current file or ask for the error message.
