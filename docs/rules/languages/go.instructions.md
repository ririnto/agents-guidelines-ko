# Go 개발 가이드라인

이 문서는 Go 언어의 간결함과 Concurrency Model을 따르는 Backend 및 DevOps Tool 작성 규칙입니다.

## 1. 에러 처리

* **Explicit Error Check:** Function 호출 후 반환된 `error` 값을 절대 무시(`_`)하지 마십시오. 항상 `if err != nil` 패턴으로 즉시 처리하거나 Wrap하여 반환하십시오.
* **Panic 지양:** 일반적인 흐름 제어에 `panic`을 사용하지 마십시오. `error`를 반환하여 Caller가 처리하게 하십시오.

## 2. 고루틴 및 채널 (Concurrency)

* **Goroutine Leak 방지:** Goroutine을 시작할 때는 종료 조건이 명확한지, 또는 Parent Context가 취소될 때 함께 종료되는지 확인하십시오.
* **Channel:** Shared Memory를 통한 통신보다 Channel을 통한 통신을 선호하십시오.

## 3. 인터페이스

* **Small Interfaces:** Interface는 사용하는 곳(Consumer)에서 정의하며, 메서드 개수를 최소화(보통 1~2개)하여 유지하십시오.
