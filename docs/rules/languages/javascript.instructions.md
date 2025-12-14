# JavaScript 개발 가이드라인

이 문서는 TypeScript를 사용하지 않는 순수 JS 환경(Legacy 또는 Script)에서의 규칙입니다.

## 1. 모던 문법 (ES6+)

* **Const & Let:** `var` 사용을 금지합니다.
* **Arrow Function:** 익명 함수 사용 시 Arrow Function을 우선하여 `this` 바인딩 문제를 방지하십시오.
* **Async/Await:** Callback 지옥을 피하고 `async/await` 패턴을 사용하십시오.

## 2. 모듈 시스템

* **ES Modules:** 가능한 경우 CommonJS(`require`) 대신 ES Modules(`import/export`)를 사용하십시오.
