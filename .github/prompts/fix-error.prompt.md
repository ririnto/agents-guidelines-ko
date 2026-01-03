---
name: fix-error
description: Analyze error messages and provide fix recommendations.
argument-hint: 'Paste the error message or describe the issue'
---

# Fix Error

Analyze given error messages and provide solutions.

## Analysis Procedure

1. **Identify Error Type**
   - Syntax Error
   - Runtime Error
   - Type Error
   - Reference Error
   - Network/External Service Error

2. **Stack Trace Analysis**
   - Error location (file:line)
   - Call path tracing
   - Related code review

3. **Identify Root Cause**
   - Interpret error message
   - Check related code context
   - Match common cause patterns

4. **Provide Solutions**
   - Immediately applicable fix
   - Alternative approaches
   - Preventive measures

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
