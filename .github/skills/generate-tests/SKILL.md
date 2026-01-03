---
name: generate-tests
description: 'Generate comprehensive, maintainable test suites through code analysis. Use when the user asks to write tests, create unit tests, add test cases, test a function, or improve test coverage.'
compatibility: Requires test framework and code read/write tools
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
  - mcp__serena
---

# Test Generation Skill

Generate comprehensive, maintainable tests through code analysis.

## Test Generation Process

### 1. Code Analysis

- Understand function/method signatures
- Identify input/output contracts
- Map branch conditions and execution paths
- Check dependencies and side effects

Use MCP tools:

- `mcp__serena__find_symbol` - Get function signatures
- `mcp__context7__get-library-docs` - Get testing framework docs

### 2. Check Existing Test Patterns

```bash
# Find test files
find . -name "*.test.*" -o -name "*_test.*" -o -name "test_*"

# Check test framework
grep -r "describe\|it\|test\|expect" --include="*.test.*" | head -5
```

### 3. Design Test Cases

#### AAA Pattern (Arrange-Act-Assert)

```text
Arrange: Set up test data and environment
Act: Execute the test target
Assert: Verify results
```

#### Coverage Goals

- Happy Path: Normal input, expected output
- Edge Cases: Boundary values, empty, null
- Error Cases: Invalid input, exceptions
- Integration: Component interactions

## Framework Templates

### Jest (JavaScript/TypeScript)

```typescript
describe('[ModuleName]', () => {
  beforeEach(() => {
    // Test setup
  });

  afterEach(() => {
    // Cleanup
  });

  describe('[functionName]', () => {
    it('should return expected result for valid input', () => {
      // Arrange
      const input = /* test data */;

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });

    it('should return default value for empty input', () => {
      expect(functionUnderTest([])).toEqual(defaultValue);
    });

    it('should throw for invalid input', () => {
      expect(() => functionUnderTest(invalidInput))
        .toThrow(ExpectedError);
    });
  });
});
```

### pytest (Python)

```python
import pytest
from module import function_under_test

class TestFunctionName:
    @pytest.fixture
    def setup_data(self):
        """Test fixture"""
        return {"key": "value"}

    def test_valid_input_returns_expected(self, setup_data):
        # Arrange
        input_data = setup_data

        # Act
        result = function_under_test(input_data)

        # Assert
        assert result == expected_output

    def test_empty_input_returns_default(self):
        assert function_under_test([]) == default_value

    def test_invalid_input_raises_exception(self):
        with pytest.raises(ExpectedError):
            function_under_test(invalid_input)

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (0, 0),
    ])
    def test_parameterized(self, input, expected):
        assert function_under_test(input) == expected
```

### Go

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name     string
        input    InputType
        expected OutputType
        wantErr  bool
    }{
        {
            name:     "valid input returns expected",
            input:    validInput,
            expected: expectedOutput,
            wantErr:  false,
        },
        {
            name:     "empty input returns default",
            input:    emptyInput,
            expected: defaultValue,
            wantErr:  false,
        },
        {
            name:    "invalid input returns error",
            input:   invalidInput,
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := FunctionUnderTest(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if result != tt.expected {
                t.Errorf("got %v, want %v", result, tt.expected)
            }
        })
    }
}
```

## Test Naming Conventions

### Descriptive test names

- `should_return_expected_result_when_valid_input`
- `returns_empty_array_for_empty_input`
- `throws_error_for_negative_input`

## Mocking Guidelines

### What to Mock

- External API calls
- Database operations
- File system access
- Time-related functions
- Random functions

### Mocking Principles

- Use minimal mocking
- Configure to behave like real implementation
- Mock at interface boundaries
- Test behavior, not implementation details

## Output Format

```markdown
## Test Generation Result

### Target

- File: `path/to/file`
- Function: `functionName`

### Generated Tests

- Total N test cases
- Happy Path: N
- Edge Cases: N
- Error Cases: N

### Test File

`path/to/test/file`

### How to Run

```bash
npm test -- --testPathPattern="filename"
pytest path/to/test_file.py -v
go test ./... -run TestFunctionName
```

### Coverage Improvement Suggestions

- [Additional test case suggestions]

## Edge Cases

- **No test file exists**: Create new test file
- **Existing tests**: Maintain consistent style, add only new cases
- **Untestable code**: Suggest refactoring
- **Complex mocking required**: Offer integration test alternative

## Notes

- MCP tools are optional; omit if unavailable or add others as needed
