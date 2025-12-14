# Express.js 가이드라인

## 1. 아키텍처

* **Layer Separation:** Route, Controller, Service, Model을 분리하십시오.
* **Middleware:** 공통 로직(Auth, Logging, Error)은 Middleware로 구현하십시오.

## 2. 비동기 처리

* **Async Handler:** Async Route Handler 사용 시 Try-Catch로 감싸거나 `express-async-errors` 등을 사용하여 Unhandled Rejection을 방지하십시오.
