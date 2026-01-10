# Suggested Commands

## Setup & Installation

```bash
# 모든 대상에 에이전트 설정 설치
python3 setup-agents.py

# 특정 대상만 설치
python3 setup-agents.py vscode
python3 setup-agents.py claude
python3 setup-agents.py codex
python3 setup-agents.py intellij

# 여러 대상 지정
python3 setup-agents.py vscode claude
```

## Testing

```bash
# 테스트 실행
pytest test_setup_agents.py

# 상세 출력
pytest -v test_setup_agents.py
```

## Git Operations

```bash
# 상태 확인
git status

# 변경 사항 확인
git diff

# 커밋 (Conventional Commits 형식)
git add .
git commit -m "feat: 새로운 기능 추가"
git commit -m "fix: 버그 수정"
git commit -m "docs: 문서 업데이트"
```

## File Operations (Darwin/macOS)

```bash
# 디렉토리 구조 확인
ls -la
find . -name "*.md" -type f

# 파일 검색
grep -r "pattern" .
rg "pattern"  # ripgrep 권장
```

## VS Code Tasks

VS Code에서 `Cmd+Shift+B`로 실행 가능한 작업:
- **Setup Agents (All)**: 모든 대상 설치 (기본)
- **Setup Agents (VS Code)**: VS Code만
- **Setup Agents (Claude)**: Claude만
- **Setup Agents (Codex)**: Codex만
- **Setup Agents (IntelliJ)**: IntelliJ만

## MCP Tool Usage

### Serena (심볼 탐색)
```
find_symbol, get_symbols_overview, search_for_pattern
```

### Context7 (문서)
```
resolve-library-id, get-library-docs
```

### ripgrep (텍스트 검색)
```
mcp__mcp-ripgrep__search, mcp__mcp-ripgrep__advanced-search
```
