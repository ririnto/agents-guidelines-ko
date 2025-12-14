# JetBrains IDE MCP 가이드라인

JetBrains IDE(2025.1+ EAP)는 자체적으로 MCP 서버 역할을 수행하여, 외부 에이전트가 **현재 열려 있는 에디터, 파일 시스템, 실행 구성(Run Configuration)**에 직접 접근할 수 있는 도구를 제공합니다.

## 1. 호출 시점 (When to use)

* **Active Context:** 사용자가 현재 보고 있는 파일이나 커서 위치에 즉각적인 코드를 작성해야 할 때.
* **Execution:** IDE에 이미 설정된 테스트나 빌드 설정을 실행해야 할 때.
* **Navigation:** 사용자의 IDE 화면을 특정 파일이나 심볼로 이동시키고 싶을 때.

## 2. 사용 가능한 도구 (Available Tools)

### 에디터 조작 (Editor Interaction)

* **`list_open_editors`**
  * **Description:** 현재 IDE 탭에 열려 있는 파일 목록을 가져옵니다.
  * **Usage:** 사용자의 현재 작업 컨텍스트(Active Context)를 파악할 때 가장 먼저 호출하십시오.

* **`read_editor_content`**
  * **Parameters:** `editor_id` (string, optional)
  * **Usage:** 특정 에디터의 텍스트 내용을 읽습니다. ID를 생략하면 현재 활성화된(Focused) 에디터 내용을 읽습니다.

* **`insert_content_at_cursor`**
  * **Parameters:** `content` (string, required)
  * **Usage:** 현재 커서 위치에 텍스트를 삽입합니다. 사용자가 "여기에 코드를 짜줘"라고 요청했을 때 가장 적합합니다.

* **`replace_selected_content`**
  * **Parameters:** `content` (string, required)
  * **Usage:** 사용자가 블록 지정한 코드를 리팩토링하거나 수정된 코드로 교체할 때 사용합니다.

### 탐색 및 파일 (Navigation & Files)

* **`open_file`**
  * **Parameters:** `path` (string, required)
  * **Usage:** 특정 파일을 IDE 에디터로 엽니다. 작업을 시작하기 전 해당 파일을 사용자에게 보여줄 때 유용합니다.

* **`search_everywhere`**
  * **Parameters:** `query` (string, required)
  * **Usage:** 파일명, 클래스명, 액션 등을 포괄적으로 검색합니다. (IDE의 Shift+Shift 기능)

### 실행 및 알림 (Execution & System)

* **`run_configuration`**
  * **Parameters:** `name` (string, required)
  * **Usage:** 프로젝트에 정의된 Run/Debug Configuration(예: "Run Tests", "Start Server")을 실행합니다. 쉘 명령어를 직접 구성하는 것보다 안전하고 정확합니다.

* **`show_notification`**
  * **Parameters:** `title` (string), `content` (string), `type` (string: "info"|"warning"|"error")
  * **Usage:** 작업 완료, 오류 발생 등 사용자의 주의가 필요한 메시지를 IDE 우측 하단 팝업으로 띄웁니다.

## 3. 전략적 사용법 (Strategy)

* **Context Priority:** 파일 내용을 읽을 때 `filesystem` 도구보다 `read_editor_content`를 사용하면, 디스크에 저장되지 않은(Unsaved) 변경 사항까지 포함된 최신 상태를 읽을 수 있습니다.
* **Cursor Awareness:** 코드를 작성할 때 라인 번호를 추측하기보다 `insert_content_at_cursor`를 사용하여 사용자가 의도한 정확한 위치에 삽입하십시오.
