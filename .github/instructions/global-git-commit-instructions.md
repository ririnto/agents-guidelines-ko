---
applyTo: "**"
description: Conventional Commits format rules
excludeAgent:
  - "coding-agent"
---

# Conventional Commit messages (Korean output)

## OUTPUT LANGUAGE (MANDATORY)

- Final commit message MUST be Korean for all natural-language parts (header, body, footer).
- English ONLY for protected identifiers, whitelist items, code keywords, paths, backticks, and code blocks.
- Output ONLY the final commit message text (no explanations or meta commentary).

## CLEAN OUTPUT (MANDATORY)

- Do not write internal tool traces, opaque placeholders, or assistant/meta notes into commits.

## FORMAT (MANDATORY)

- Structure: `<type>[optional scope]: <description>` → `[optional body]` → `[optional footer]` (keep exact order).
- Allowed `type`: `feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert`.
- Header pattern: `type(scope): description` or `type: description`; scope only if it adds clarity.
- Description: Korean, imperative, concise, no trailing period.
- Body/footer: if present, separate with blank lines.
- Breaking changes: mark with `!` in header and/or `BREAKING CHANGE:` footer (`BREAKING CHANGE:` stays in English).

## Examples

```text
feat(parser): 배열 파싱 기능 추가
fix(ui): 버튼 정렬 문제 수정
refactor: 데이터 처리 성능 개선
```

### Multi-line example

```text
feat(auth): OAuth 로그인 기능 구현

- Google OAuth 2.0 Provider 추가
- Login Callback Handler 구현
- Session 관리 Middleware 적용

Closes #123
```

## Validation checklist (must pass)

- Type is one of the allowed values.
- Header matches `type(scope): description` or `type: description`.
- Description is imperative, concise, and has no trailing period.
- Scope is used only when it improves clarity.
- Breaking changes are clearly marked (`!` and/or `BREAKING CHANGE:`).
- If body/footer exists, separate sections with blank lines
  in the final message.
- Korean output rules and preservation rules are respected.

## Context-aware commit messages

When writing commit messages, Claude will:

1. **Look at recent git history** to maintain consistent style and context
2. **Analyze the diff** to capture all meaningful changes
3. **Reference related issues/PRs** when applicable
   (e.g., `Closes #123`, `Fixes #456`)

## Instruction applicability fallback

- If custom instructions are not fully applied in the current Copilot surface,
  restate only the minimal relevant rules inline.

---

## Internationalization: Korean Output with Preserved Terms

### Pattern Rules

Do not translate:

- Code blocks and backtick-wrapped content
- CamelCase / PascalCase / snake_case / kebab-case identifiers
- Paths containing `.` `/` `[]`
- ALL_CAPS acronyms (API, SDK, JVM, etc.)
- Framework/library/service proper nouns
- Programming language reserved words

### Protected Terms (Compact)

**Core**: Git, commit, branch, merge, rebase, push, pull,
fetch, stash, cherry-pick, HEAD, origin

**Types**: feat, fix, docs, style, refactor, perf, test,
build, ci, chore, revert, BREAKING CHANGE

**Tech**: API, SDK, REST, GraphQL, Spring, JPA, Docker,
Kubernetes, AWS, transaction, cache, async, sync

### Output Rule

Protected terms → verbatim. All other content → fluent Korean.
