---
name: optimize
description: Optimize code performance and readability.
argument-hint: 'Specify file or function to optimize (e.g., "processData function", "src/utils.ts")'
---

# Code Optimization

Improve code performance, readability, and maintainability.

## Optimization Areas

1. Performance: reduce complexity, remove needless work, caching, lazy loading, batching.
2. Readability: clear naming, right abstraction, consistent style, simplify.
3. Memory: prevent leaks, avoid extra objects, use streams/generators.
4. Bundle (web): code splitting, tree shaking, asset optimization.

## Output Format

```markdown
## Optimization Analysis

### Current State

- File: `path`
- Issues identified: N

### Optimization Suggestions

#### 1. [Optimization Type]: [Target]

**Problem:** [Current issue description]

**Before:** (current code)

**After:** (improved code)

**Effect:** [Performance improvement numbers or description]

### Verification Method

(Benchmark or test command)

### Notes

- [Trade-offs]
- [Compatibility considerations]
```

## Notes

- Don't optimize without measuring (avoid premature optimization)
- Consider balance between readability and performance
- Ensure identical behavior before and after optimization

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input above before proceeding.
If the input is empty, ask what code or function to optimize.
