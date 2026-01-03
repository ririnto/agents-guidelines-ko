---
name: refactor
description: 'Improve code structure and readability while preserving behavior. Use when the user asks to refactor code, improve structure, clean up, reduce duplication, or apply design patterns.'
compatibility: Requires code read/write tools and test runner
allowed-tools:
  - Bash(node:*, npm:*, npx:*, pnpm:*, yarn:*, python:*, pip:*, pytest:*, go:*, cargo:*, mvn:*, ./mvnw:*, gradle:*, ./gradlew:*, make:*, cmake:*, g++:*, gcc:*, clang:*)
  - Glob
  - Grep
  - Read
  - Write
  - mcp__context7
  - mcp__fetch
  - mcp__jetbrains
  - mcp__markitdown
  - mcp__sequential-thinking
  - mcp__serena
---

# Refactoring Skill

Improve code structure and readability while preserving behavior.

## Refactoring Principles

### Core Rules

- **Preserve Behavior**: Improve structure without changing functionality
- **Small Steps**: One refactoring at a time, verify between steps
- **Test First**: Ensure test coverage before refactoring
- **Clear Intent**: Make code intent more obvious

### When to Refactor

- Code duplication discovered
- Function/class too long
- Hard to understand
- Before adding new features
- During code review

Use MCP tools:

- `mcp__serena__find_referencing_symbols` - Check all usages
- `mcp__jetbrains__rename_symbol` - Safe rename
- `mcp__serena__get_symbols_overview` - Understand structure

## Refactoring Techniques

### Extract Function

```text
// Before: Long function with multiple responsibilities
function processOrder(order) {
  // validate... 20 lines
  // calculate... 20 lines
  // save... 20 lines
}

// After: Small focused functions
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  saveOrder(order, total);
}
```

### Extract Variable

```text
// Before: Complex expression
if (user.age >= 18 && user.hasLicense && !user.isSuspended) {}

// After: Named condition
const canDrive = user.age >= 18 &&
  user.hasLicense &&
  !user.isSuspended;
if (canDrive) {}
```

### Extract Class

```text
// Before: Class with mixed responsibilities
class Order {
  calculateTotal() {}
  calculateTax() {}
  sendEmail() {}
  generatePdf() {}
}

// After: Separated responsibilities
class Order { calculateTotal() {} calculateTax() {} }
class OrderNotifier { sendEmail() {} }
class OrderExporter { generatePdf() {} }
```

### Inline Unnecessary Function

- When function body is as clear as its name
- When only called once

### Inline Unnecessary Variable

- When expression is clear enough
- When variable adds no meaning

### Move Field/Method

- Move to more appropriate class
- Follow Single Responsibility Principle

### Replace Conditional with Polymorphism

- Replace switch/if-else chains with subclasses
- Each case becomes a class

### Rename for Clarity

#### To Meaningful Names

- Abbreviation → Full word
- Generic name → Specific name
- Misleading name → Accurate name

#### Simplify Conditionals

- Nested conditions → Guard clauses
- Complex boolean → Named function

#### Loop → Pipeline

```javascript
// Before
let result = [];
for (let i = 0; i < items.length; i++) {
  if (items[i].active) {
    result.push(items[i].name);
  }
}

// After
const result = items
  .filter(item => item.active)
  .map(item => item.name);
```

## Refactoring Workflow

### 1. Analyze Current State

- Identify problem areas
- Check test coverage
- Understand dependencies

### 2. Plan

- Select refactoring technique
- Identify affected areas
- Prepare rollback strategy

### 3. Execute Stepwise

1. Run tests (ensure green)
2. Make one small change
3. Run tests again
4. Repeat until done

### 4. Verify

- All tests pass
- No behavior change
- Code quality improved

## Code Smell Catalog

- **Long Method**: Function > 20 lines
- **Large Class**: Class > 200 lines
- **Long Parameter List**: Function > 3 parameters
- **Duplicate Code**: Similar code in multiple places
- **Feature Envy**: Method uses another class's data heavily
- **Data Clumps**: Same data groups appear repeatedly
- **Primitive Obsession**: Overuse of primitives over objects
- **Switch Statements**: Complex switch that should be polymorphism

## Output Format

```markdown
## Refactoring Summary

### Problem

[What code smell or issue is being addressed]

### Technique

[Refactoring technique applied]

### Changes

#### Step 1: [First refactoring]

(before/after code)

#### Step 2: [Next refactoring]

...

### Risk Assessment

- [Potential risks]
- [Follow-up suggestions]

### Verification

(test commands)
```

## Edge Cases

- **No tests**: Add tests first, then refactor
- **Tight deadlines**: Document technical debt, defer
- **Shared code**: Coordinate with other teams
- **Breaking API**: Version the API, deprecate old

## Tips

- MCP tools are optional; omit if unavailable or add others as needed
