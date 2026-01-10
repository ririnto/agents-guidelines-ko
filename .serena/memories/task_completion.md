# Task Completion Checklist

작업 완료 시 수행해야 할 단계입니다.

## 1. Validation

### Python 코드 변경 시
```bash
# 테스트 실행
pytest test_setup_agents.py -v

# 설치 스크립트 테스트 (dry-run 없음, 실제 복사)
python3 setup-agents.py
```

### Markdown 파일 변경 시
- 링크 유효성 확인
- 코드 블록 언어 지정 확인
- 들여쓰기 2칸 확인

## 2. Code Review (자체 검토)

변경 사항 검토:
- [ ] 불필요한 변경 없음
- [ ] 기존 컨벤션 준수
- [ ] 에러 처리 적절
- [ ] 주석/문서 업데이트됨

## 3. Git Workflow

```bash
# 변경 사항 확인
git status
git diff

# 스테이징
git add <files>

# 커밋 (Conventional Commits)
git commit -m "type(scope): description"
```

### Commit Types
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 포맷팅 (코드 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 변경

## 4. Post-Edit Hook

`.claude/settings.local.json`에 정의된 훅이 `Write|Edit|MultiEdit|NotebookEdit` 후 자동 실행됩니다:
```
python3 .claude/hooks/post-tool-call.py
```

## 5. Documentation

변경에 따른 문서 업데이트:
- `README.md` (기능 추가/변경 시)
- 관련 에이전트/스킬 파일
- 인라인 주석/docstrings

## 6. Final Check

- [ ] 모든 테스트 통과
- [ ] 린트/포맷 규칙 준수
- [ ] 보안 민감 정보 없음
- [ ] 커밋 메시지 명확
