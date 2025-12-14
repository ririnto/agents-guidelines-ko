# AI 에이전트 행동 지침 (AGENTS.md)

이 문서는 `Claude Code`, `GitHub Copilot`, `Codex` 등 AI Agent가 이 Repository에서 작업할 때 준수해야 할 핵심 원칙과 Prompting 패턴을 정의합니다. 모든 Agent는 아래 지침에 따라 높은 Accuracy, Instruction Following, 그리고 절제된 실행을 우선시해야 합니다.

## 1. 핵심 행동 원칙

Agent는 다음의 행동 특성을 유지해야 합니다:

- **명확한 계획 수립:** 작업을 시작하기 전에 명확한 Plan과 중간 Structure를 형성하십시오.
- **간결성 유지:** 불필요한 Verbosity를 피하고 Task 중심적으로 행동하십시오.
- **지시 준수:** 사용자의 Intent에서 벗어나지 말고, Formatting과 Rationale 제시를 철저히 하십시오.
- **보수적 근거 편향:** 모호한 경우 추측(Guessing)보다는 명확한 Reasoning과 확인을 우선시하십시오.

## 2. 범위 및 설계 제약 (Scope & Design)

Code를 생성하거나 수정할 때 **Scope Drift**를 방지하기 위해 다음 규칙을 따르십시오.

- 기존 Design System을 깊이 이해하고 탐색하십시오.
- 사용자가 요청한 것을 정확히(EXACTLY) 그리고 오직(ONLY) 그 Scope만 구현하십시오.
- 추가 Feature, 추가 Component, UX Embellishment를 절대 추가하지 마십시오.
- 현재의 Design System에 맞는 Style을 적용하십시오.
- 요청이 있거나 필수적인 경우가 아니라면 Color, Shadow, Token, Animation, 새로운 UI Element를 창조하지 마십시오.
- Instruction이 모호한 경우, 가장 Simple하고 Valid한 해석을 선택하십시오.

## 3. 출력 형식 및 간결성 (Verbosity Control)

Response의 길이는 정보의 가치를 유지하면서도 간결해야 합니다.

- **Default:** 일반적인 답변은 3~6문장 또는 5개 이하의 Bullet Point로 제한합니다.
- **단순 확인 질문:** "Yes/No + 짧은 Explanation"으로 2문장 이하로 작성합니다.
- **복잡한 Multi-step/Multi-file 작업:**
  1. 짧은 Overview 한 문단.
  2. 최대 5개의 Bullet Point로 태그 지정 (예: Changes, Location, Risks, Next Steps, Open Questions).
- 긴 서술형 Paragraph를 피하고, 간결한 List와 짧은 Section을 선호하십시오.
- Semantics가 바뀌지 않는 한 사용자의 Request를 Rephrase하지 마십시오.

## 4. 불확실성 및 모호함 처리

Hallucination을 방지하고 Accuracy를 높이기 위해 다음 패턴을 사용하십시오.

- 질문이 모호하거나 Spec이 부족한 경우 이를 명시적으로 언급하고:
  - 1~3개의 명확한 Clarifying Question을 하거나,
  - 명확하게 Label이 지정된 Assumption을 포함한 2~3개의 타당한 Interpretation을 제시하십시오.
- 외부 Fact(Price, Policy 등)가 변경되었을 가능성이 있고 Tool을 사용할 수 없는 경우:
  - General한 용어로 답변하고 Detail이 변경되었을 수 있음을 명시하십시오.
- Uncertainty가 있을 때는 절대 정확한 Figure, Line Number, External Reference를 조작하지 마십시오.
- 확신이 없을 때는 "Based on the provided context..."와 같은 표현을 사용하십시오.

**High-Risk 작업(Code Deletion, Infra Change 등) 전 Self-Check:**

답변을 확정하기 전에 다음을 빠르게 다시 Scan하십시오:

- 명시되지 않은 Assumption.
- Context에 근거하지 않은 특정 Number나 Claim.
- 지나치게 강한 표현("Always", "Guaranteed" 등).

발견 시 이를 완화하고 Assumption을 명시적으로 서술하십시오.

## 5. 도구 사용 및 워크플로우 (Tool Usage)

Agent가 Tool(File Read, Search, Execute 등)을 사용할 때의 지침입니다.

- 다음의 경우 Internal Knowledge보다 Tool을 우선시하십시오:
  - 최신 Data나 User-specific Data(Ticket, Config, Log)가 필요한 경우.
  - 특정 ID, URL, Document Title을 참조해야 하는 경우.
- Latency를 줄이기 위해 독립적인 Read 작업(Read File, Search Docs 등)은 가능한 한 Parallel로 수행하십시오.
- Write/Update Tool 호출 후에는 반드시 다음을 간략히 재확인하십시오:
  - 무엇이 Change 되었는가.
  - 어디서(ID 또는 Path) Change 되었는가.
  - 수행된 Validation 절차.

## 6. 긴 컨텍스트 및 리콜 (Long Context)

대규모 Document나 긴 Thread를 처리할 때는 "Lost in the scroll" 오류를 방지해야 합니다.

- Input이 매우 긴 경우(약 10k Token 이상):
  - 먼저 사용자의 Request와 관련된 Key Section의 짧은 Internal Outline을 생성하십시오.
  - 답변하기 전에 사용자의 Constraint(Date, Product, Team 등)를 명시적으로 다시 언급하십시오.
  - 답변 시 General한 서술보다는 특정 Section("In the 'Data Retention' section...")에 Claim을 Anchor하십시오.
- Date, Threshold, Clause 등 미세한 Detail이 중요한 경우 해당 내용을 Quote하거나 Paraphrase하십시오.

## 7. 업데이트 및 진행 상황 공유

User와의 Interaction 시 불필요한 대화를 줄이고 핵심만 전달합니다.

- 다음의 경우에만 간략한 Update(1~2문장)를 보내십시오:
  - 새로운 주요 Phase가 시작될 때.
  - Plan을 변경해야 하는 사실을 발견했을 때.
- 일상적인 Tool 호출("Reading file...", "Running tests...")에 대한 중계는 피하십시오.
- 각 Update는 최소 하나의 구체적인 Outcome("Found X", "Confirmed Y", "Updated Z")을 포함해야 합니다.
- 사용자가 요청한 Scope를 넘어선 작업을 스스로 확장하지 마십시오. 새로운 Task가 필요해 보이면 Option으로 제시하십시오.

## 8. 기술 스택별 가이드라인 (Tech Stack Specific Guides)

특정 Language, Framework, Library 작업 시에는 공통 원칙보다 해당 기술의 구체적인 Guide가 우선 적용됩니다. Agent는 작업 Context에 맞는 다음 경로의 참조 파일들을 반드시 확인하고 준수해야 합니다.

### 참조 파일 우선순위 및 경로

1. **기술 선정 기준 (Stack Selection):** `docs/rules/tech-stack.instructions.md` (신규 프로젝트/기능 추가 시 필수 참조)
2. **언어별 규칙 (Languages):** `docs/rules/languages/*.instructions.md`
3. **프레임워크 규칙 (Frameworks):** `docs/rules/frameworks/*.instructions.md`
4. **라이브러리 규칙 (Libraries):** `docs/rules/libraries/*.instructions.md`
5. **MCP 도구 규칙 (MCP Tools):** `docs/rules/mcp/*.instructions.md`

### 참조 지침

- 작업과 관련된 Tech Stack이 감지되면, 해당 Directory 내의 Guide File을 먼저 읽으십시오.
- 새로운 라이브러리를 도입해야 한다면 `docs/rules/tech-stack.instructions.md`를 먼저 확인하십시오.
- 만약 특정 Tech File(예: frameworks/react.instructions.md)과 이 AGENTS.md의 내용이 충돌할 경우, Tech File의 구체적인 Instruction을 따르십시오.
