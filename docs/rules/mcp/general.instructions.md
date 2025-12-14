# MCP 도구 사용 공통 가이드

이 문서는 AI Agent가 연결된 MCP(Model Context Protocol) 서버의 도구를 호출할 때의 공통 행동 수칙입니다.

## 1. 도구 감지 및 우선순위

* **Tool Discovery:** 작업을 시작하기 전에 현재 환경에 로드된 Tool 목록을 확인하십시오.
* **Override:** 동일한 기능(예: 파일 읽기)에 대해 내장 도구와 MCP 도구(예: `serena`, `filesystem`)가 동시에 존재할 경우, **특화된 MCP 도구**를 우선 사용하십시오.
  * 예: 단순 텍스트 검색보다 `serena`의 `find_symbol` 우선.

## 2. 오류 처리 (Error Handling)

* **Fallback:** MCP 도구 호출이 실패(예: Timeout, Connection Refused)하면, 즉시 사용자에게 보고하지 말고 내장 기능(Native Capabilities)을 사용하여 작업을 시도하십시오.
* **Argument Correction:** `Invalid Argument` 오류 발생 시, 에러 메시지를 분석하여 파라미터 형식을 수정한 후 1회 재시도하십시오.

## 3. 환각 방지 (No Hallucination)

* **Existence Check:** 존재하지 않는 Tool 함수를 추측하여 호출하지 마십시오. 반드시 제공된 Tool Schema와 Description에 기반해야 합니다.
