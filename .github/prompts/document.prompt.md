---
name: document
description: Auto-generate documentation for code.
argument-hint: 'Specify target to document (e.g., "UserService class", "API endpoints")'
---

# Documentation Generation

Generate documentation for code.

## Documentation Types

1. Code comments: JSDoc/TSDoc, Python docstrings, GoDoc, Javadoc
2. API docs: endpoints, request/response, auth, error codes
3. README: overview, install, usage, contributing
4. Architecture: system structure, components, data flow

## Output Format

### Function/Method Documentation

```typescript
/**
 * [Function description]
 *
 * @param {type} paramName - Description
 * @returns {type} Return value description
 * @throws {ErrorType} Condition that triggers error
 * @example
 * // Usage example
 * functionName(arg);
 */
```

### API Endpoint Documentation

```markdown
## [HTTP Method] /endpoint

[Description]

### Request

**Headers:**

| Name | Required | Description |
| --- | --- | --- |
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

**Body:**

(JSON schema)

### Response

**Success (200):** JSON response

**Errors:**

- 400: Bad request
- 401: Unauthorized
- 404: Not found
```

### README Template

```markdown
# Project Name

[One-line description]

## Installation

(installation commands)

## Usage

(example code)

## API

[Main API description]

## License

[License]
```

## Notes

- Follow existing documentation style
- Read the code and reflect accurate information
- Use working code for examples

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input above before proceeding.
If the input is empty, ask what to document.
