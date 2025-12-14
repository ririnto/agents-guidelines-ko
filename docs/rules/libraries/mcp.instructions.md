# Model Context Protocol (MCP) 가이드라인

이 문서는 AI Agent가 외부 시스템, 데이터, 도구와 상호작용하기 위한 표준 프로토콜인 MCP 사용 및 설정 규칙을 정의합니다.

## 1. 서버 구성 원칙 (Server Configuration)

* **Transport:** 기본적으로 **Stdio** (Standard Input/Output) 방식을 우선 사용하며, 원격 연결이 필요한 경우에만 **SSE** (Server-Sent Events)를 사용하십시오.
* **Execution:** Node.js 기반 서버는 `npx`, Python 기반 서버는 `uvx` 또는 `docker`를 사용하여 실행 환경 의존성을 최소화하십시오.

## 2. 클라이언트별 설정 (Client Setup)

### VS Code & Claude Desktop

설정 파일(`claude_desktop_config.json` 또는 VS Code `mcp.json`)은 JSON 포맷을 엄격히 준수해야 합니다.

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@scope/package-name"],
      "env": { "KEY": "VALUE" }
    }
  }
}
```

### JetBrains IDE (IntelliJ, PyCharm etc.)

JetBrains IDE(2025.1+ EAP)에서는 `Settings/Preferences` -> `Tools` -> `Model Context Protocol` 메뉴를 통해 관리합니다.

* **Definition:** JSON 설정 파일을 직접 수정하기보다 IDE UI를 통해 서버 정의를 추가하는 것을 권장합니다.
* **Environment:** Project-specific 설정보다는 IDE Global 설정으로 등록하여 여러 프로젝트에서 도구를 공유하십시오.

## 3. 추천 MCP 서버 스택 (Recommended Servers)

Agent 기능을 확장할 때 다음의 검증된 오픈소스 MCP 서버를 우선적으로 통합하십시오.

### 코딩 및 코드베이스 탐색 (Coding Agent)

* **Serena (`serena`):**
  * **Role:** Semantic Code Retrieval & Editing (LSP 기반).
  * **Use Case:** 단순 Grep 검색이 아닌, 심볼(Symbol) 단위의 참조 검색 및 구조적 코드 수정이 필요할 때.
  * **Command:** `uvx --from git+https://github.com/oraios/serena serena start-mcp-server`

### 추론 및 사고 과정 (Reasoning)

* **Sequential Thinking (`sequential-thinking`):**
  * **Role:** Dynamic & Reflective Problem Solving.
  * **Use Case:** 복잡한 문제를 단계별로 분해하고, 자신의 논리를 수정(Revision)하거나 분기(Branch)해야 할 때.
  * **Command:** `npx -y @modelcontextprotocol/server-sequential-thinking`

### 메모리 및 컨텍스트 (Memory & Context)

* **Knowledge Graph Memory (`memory`):**
  * **Role:** Persistent Knowledge Graph.
  * **Use Case:** 사용자와의 대화 내역에서 Entity와 Relation을 추출하여 장기 기억(Long-term Memory)으로 보존해야 할 때.
  * **Command:** `npx -y @modelcontextprotocol/server-memory` (또는 Docker 활용)

### 파일 시스템 및 기타

* **Filesystem:** `@modelcontextprotocol/server-filesystem` (로컬 파일 접근 제어)
* **PostgreSQL:** `@modelcontextprotocol/server-postgres` (DB 데이터 조회)
* **Git:** `@modelcontextprotocol/server-git` (Repository 조회)

## 4. 도구 개발 가이드

자체 MCP 서버를 개발할 때는 다음 SDK를 사용하십시오.

* **TypeScript:** `@modelcontextprotocol/sdk`
* **Python:** `mcp` (Official Python SDK)
