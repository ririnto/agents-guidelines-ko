---
name: explain-code
description: 'Explain code operation, logic, and design clearly and systematically. Use when the user asks to explain code, understand how something works, what a function does, or requests logic analysis.'
compatibility: Requires code reading tools
allowed-tools:
  - Glob
  - Grep
  - Read
  - mcp__context7
  - mcp__fetch
  - mcp__jetbrains
  - mcp__markitdown
  - mcp__serena
---

# Code Explanation Skill

Explain code operation clearly and systematically.

## Explanation Process

### 1. Scope Identification

- Identify file, function, class, or code block
- Understand dependencies and call relationships

Use MCP tools for deeper analysis:

- `mcp__serena__find_symbol` - Find symbol definitions
- `mcp__serena__find_referencing_symbols` - Track usages
- `mcp__jetbrains__get_symbol_info` - Get documentation

### 2. Explanation Structure

#### Overview (2-3 sentences)

- What the code does
- Why it exists
- Its role in the system

#### Step-by-Step Operation

- Main logic flow
- Core algorithm explanation
- Important branch conditions

#### Input and Output

- Parameters and types
- Return values and types
- Side effects

#### Edge Cases and Limitations

- Exception handling approach
- Boundary conditions
- Known limitations

#### Usage Examples

- Basic invocation
- Common usage patterns
- Integration with other code

## Explanation Level Adjustment

### For Beginners

- Explain from basic concepts
- Include terminology definitions
- Detailed step-by-step explanations
- Use analogies and examples

### For Intermediate Developers (Default)

- Focus on core logic
- Mention patterns and conventions
- Appropriate abstraction level

### For Advanced Developers

- Design decision rationale
- Performance characteristics
- Alternative approaches
- Trade-offs

## Output Format

```markdown
## Overview

[Purpose and role of the code]

## How It Works

### Main Flow

1. [First step]
2. [Second step]
...

### Core Logic

(key code excerpt with comments)

[Logic explanation]

## Input/Output

| Parameter | Type | Description |
|-----------|------|-------------|
| param1    | Type | Description |

**Return**: `Type` - Description

## Caveats

- [Edge cases or limitations]

## Usage Example

(example code)
```

## Language-Specific Explanations

### JavaScript/TypeScript

- Closures and scope
- Async patterns (Promise, async/await)
- Prototype chain

### Python

- Decorators and context managers
- Generator patterns
- Magic methods

### Java/Kotlin

- Object-oriented design patterns
- Generics and type variance
- Stream API

### Go

- Goroutines and channels
- Interface implementation
- Error handling patterns

## Edge Cases

- **Complex code**: Break into smaller chunks
- **Library code**: Reference official documentation
- **Legacy code**: Provide historical context if available
- **Multi-language**: Explain language-specific idioms

## Tips

- MCP tools are optional; omit if unavailable or add others as needed
