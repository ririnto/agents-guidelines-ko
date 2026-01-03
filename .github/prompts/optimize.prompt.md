---
name: optimize
description: Optimize code performance and readability.
argument-hint: 'Specify file or function to optimize (e.g., "processData function", "src/utils.ts")'
---

# Code Optimization

Improve code performance, readability, and maintainability.

## Optimization Areas

### 1. Performance Optimization

- Algorithm complexity improvement (O(n²) → O(n log n))
- Remove unnecessary operations
- Apply caching
- Lazy Loading
- Batch processing

### 2. Readability Optimization

- Clear naming
- Appropriate abstraction
- Consistent code style
- Remove unnecessary complexity

### 3. Memory Optimization

- Memory leak prevention
- Reduce unnecessary object creation
- Use streams/generators

### 4. Bundle Optimization (Web)

- Code splitting
- Tree shaking
- Image/asset optimization

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
