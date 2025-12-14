# Memory 도구 사용 가이드

Agent는 대화 맥락에서 **사용자의 정보, 선호도, 프로젝트 결정 사항**을 발견하면 즉시 Memory 도구를 통해 저장해야 합니다.

## 1. 호출 시점 (When to use)

* **User Facts:** 사용자 이름, 직업, 기술 스택 선호도, 작업 스타일 등.
* **Project Context:** 프로젝트의 핵심 설계 원칙, 주요 기술 결정, 금기 사항(Constraints).
* **Relationships:** 팀원 간의 관계나 모듈 간의 의존성 등 구조적 정보.

## 2. 사용 가능한 도구 (Available Tools)

### `create_entities`

새로운 개체(Entity)를 지식 그래프에 생성합니다.

* **Parameters:**
  * `entities` (array of objects):
    * `name` (string): 엔티티 고유 이름 (공백 대신 `_` 권장).
    * `entityType` (string): 엔티티 유형 (예: `Person`, `Organization`, `Concept`).
    * `observations` (string[]): 초기 관찰 정보 목록.

### `create_relations`

두 개체 간의 관계를 정의합니다.

* **Parameters:**
  * `relations` (array of objects):
    * `from` (string): 출발 엔티티 이름.
    * `to` (string): 도착 엔티티 이름.
    * `relationType` (string): 관계 유형 (능동태 권장, 예: `works_at`, `uses`).

### `add_observations`

기존 개체에 새로운 사실(Fact)을 추가합니다.

* **Parameters:**
  * `observations` (array of objects):
    * `entityName` (string): 대상 엔티티 이름.
    * `contents` (string[]): 추가할 관찰 내용 (문자열).

### `read_graph`

전체 지식 그래프를 조회합니다.

* **Parameters:** 없음.
* **Returns:** 모든 엔티티와 관계 구조.

### `search_nodes`

쿼리를 기반으로 엔티티 및 관련 정보를 검색합니다.

* **Parameters:**
  * `query` (string): 검색어 (이름, 타입, 관찰 내용 포함 검색).

### `open_nodes`

특정 이름을 가진 노드(엔티티)를 직접 조회합니다.

* **Parameters:**
  * `names` (string[]): 조회할 엔티티 이름 목록.

### `delete_entities`

엔티티와 연관된 관계를 삭제합니다.

* **Parameters:** `entityNames` (string[])

### `delete_relations`

특정 관계를 삭제합니다.

* **Parameters:** `relations` (array of objects: `from`, `to`, `relationType`)

### `delete_observations`

특정 관찰 내용을 삭제합니다.

* **Parameters:** `deletions` (array of objects: `entityName`, `observations`)

## 3. 전략적 사용법 (Strategy)

* **Naming:** 엔티티 이름은 고유해야 하므로 구체적으로 짓습니다 (예: `User` 대신 `User_JohnDoe`).
* **Active Voice:** 관계는 항상 능동태로 정의하여 방향성을 명확히 합니다 (`A -> owns -> B`).
* **Retrieval:** 세션 시작 시 `read_graph` 또는 `search_nodes`를 호출하여 컨텍스트를 로드하십시오.
