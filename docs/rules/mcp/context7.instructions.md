# Context7 도구 사용 가이드

Agent는 학습 데이터(Training Data)에 의존하여 추측하지 말고, **Context7**을 통해 최신 라이브러리 정보를 조회해야 합니다.

## 1. 호출 시점 (When to use)

* **Unknown Libraries:** 학습 시점 이후에 출시되었거나, 잘 알려지지 않은 라이브러리를 사용해야 할 때.
* **Version Specifics:** 특정 버전(예: Next.js 13 vs 14)의 Breaking Change가 우려될 때.
* **Boilerplate:** 설정 파일(Config)이나 초기 세팅 코드가 필요할 때.

## 2. 사용 가능한 도구 (Available Tools)

### `resolve-library-id`

일반적인 라이브러리 이름으로 Context7 내부에서 사용하는 정확한 Library ID를 검색합니다.

* **Parameters:**
  * `libraryName` (string, required): 검색할 라이브러리의 이름 (예: "tanstack query", "supabase").
* **Usage:** 사용자가 `/owner/repo` 형태의 ID를 제공하지 않았을 때 가장 먼저 호출합니다.

### `get-library-docs`

Library ID를 기반으로 최신 문서 및 코드 예제를 조회합니다.

* **Parameters:**
  * `context7CompatibleLibraryID` (string, required): `resolve-library-id`를 통해 얻은 ID (예: `/vercel/next.js`).
  * `topic` (string, optional): 문서 내에서 검색할 특정 주제 (예: "routing", "server actions").
  * `page` (integer, optional): 문서의 페이지 번호 (Default: 1).
* **Usage:**
  * 구체적인 `topic`을 지정하여 필요한 정보를 필터링하십시오.
  * 정보가 잘렸거나 불충분하면 `page` 번호를 증가시켜 추가 호출하십시오.

## 3. 안티 패턴 (Anti-Patterns)

* **Guessing APIs:** Context7을 사용할 수 있는 환경에서, 문서를 조회하지 않고 가상의 API(Hallucinated API)를 작성하는 것은 엄격히 금지됩니다.
* **Ignoring Pagination:** 문서의 내용이 잘렸거나 부족해 보일 때 포기하지 말고 다음 페이지를 요청하십시오.
