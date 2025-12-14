# Sequential Thinking 도구 사용 가이드

Agent는 복잡한 문제를 직면했을 때, 즉시 답변을 생성하는 대신 **Sequential Thinking** 도구를 사용하여 사고 과정을 명시적으로 전개해야 합니다.

## 1. 호출 시점 (When to use)

* **Complex Logic:** 다단계 추론이 필요한 알고리즘 문제나 아키텍처 설계.
* **Debugging:** 원인이 불분명한 버그의 근본 원인(Root Cause) 분석.
* **Planning:** 코드를 작성하기 전 전체적인 로드맵 수립.

## 2. 사용 가능한 도구 (Available Tool)

### `sequential_thinking`

문제를 단계별로 생각하고, 필요시 이전 생각을 수정하거나 분기하여 해결책을 도출합니다.

* **Parameters:**
  * `thought` (string, required): 현재 단계의 사고 내용.
  * `nextThoughtNeeded` (boolean, required): 다음 사고 단계가 필요한지 여부. `false`면 프로세스를 종료합니다.
  * `thoughtNumber` (integer, required): 현재 사고의 순번 (1부터 시작).
  * `totalThoughts` (integer, required): 해결을 위해 예상되는 총 단계 수. (진행하면서 동적으로 조정 가능).
  * `isRevision` (boolean, optional): 이 생각이 이전 단계를 수정하는 것이라면 `true`.
  * `revisesThought` (integer, optional): 수정 대상이 되는 이전 사고의 `thoughtNumber`.
  * `branchFromThought` (integer, optional): 새로운 사고의 가지(Branch)를 뻗어 나갈 기준이 되는 이전 사고 번호.
  * `branchId` (string, optional): 분기 식별자.
  * `needsMoreThoughts` (boolean, optional): `totalThoughts`를 늘려야 할 경우 `true`.

## 3. 도구 호출 전략 (Tool Calling Strategy)

이 도구는 단발성이 아닌 **Loop** 형태로 호출해야 합니다.

1. **초기 설정:** `thoughtNumber`: 1, `nextThoughtNeeded`: `true`로 시작하여 문제 정의 및 계획을 수립합니다.
2. **진행 및 수정 (Revision):** 논리적 오류 발견 시 `isRevision`: `true`를 사용하여 이전 단계를 바로잡습니다.
3. **분기 (Branching):** 여러 가설(Hypothesis)을 테스트해야 할 때 `branchFromThought`를 사용하여 사고 흐름을 분기합니다.
4. **종료:** 결론에 도달하면 `nextThoughtNeeded`: `false`로 호출하여 종료합니다.
