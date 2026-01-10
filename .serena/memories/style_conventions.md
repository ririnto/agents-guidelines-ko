# Style and Conventions

## EditorConfig Settings

프로젝트 전체:
- **Charset**: UTF-8
- **Line ending**: LF
- **Indent**: 4 spaces
- **Max line length**: 120
- **Insert final newline**: Yes

Markdown 파일 (*.md):
- **Indent**: 2 spaces

## Language Rules

### Output Language
- 사용자 메시지가 한국어면 → 한국어로 응답
- 사용자 메시지가 영어면 → 영어로 응답

### Protected Terms (번역하지 않음)
- 프로그래밍 언어: JavaScript, TypeScript, Python, Go 등
- 프레임워크: React, Spring, Django 등
- 패턴: MVC, DDD, CQRS 등
- 에이전트: Claude, Copilot, MCP 등
- 코드 식별자, API 필드, 제품명

### Writing Guidelines
- 문서: `docs-writer-ko` / `docs-writer-en` 사용
- UI 텍스트: `ux-copywriter-ko` / `ux-copywriter-en` 사용
- 코드 주석: 영어 유지 (레포 규칙 없으면)
- 커밋 메시지: 영어 (팀 규칙 따름)

## Python Code Style

- Type hints 권장
- Docstrings (Google style 또는 reStructuredText)
- 함수/클래스에 설명 주석
- logging 사용 (print 대신)

## Markdown Style

- 들여쓰기 2칸
- 제목 후 빈 줄
- 코드 블록에 언어 지정
- 테이블 정렬

## Agent Routing

See `.claude/rules/agent-routing.md` for detailed agent selection rules:
- `scout`: 파일 찾기, 빠른 탐색
- `architect`: 설계, 아키텍처 결정
- `single-file-implementer`: 단일 파일 변경
- `implementer`: 다중 파일 구현
- `code-reviewer`: 코드 리뷰
- `security-auditor`: 보안 검토
