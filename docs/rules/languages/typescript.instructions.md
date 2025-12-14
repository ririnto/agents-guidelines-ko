# TypeScript 개발 가이드라인

이 문서는 TypeScript Code 작성 시 AI Agent가 따라야 할 엄격한 Type Safety 및 Style 규칙을 정의합니다.

## 1. 타입 안정성 (Type Safety)

* `any` Type 사용을 엄격히 금지합니다. 불가피한 경우 `unknown`을 사용하고 Type Guard를 통해 Narrowing하십시오.
* Implicit `any`를 허용하지 않습니다 (`noImplicitAny`).
* 가능한 한 `interface`보다 `type` Alias를 사용하여 Consistency를 유지하되, Library Extension이 필요한 경우에만 `interface`를 사용하십시오.
* Function의 Return Type을 명시적으로 선언하십시오. Inference에 의존하지 마십시오.

## 2. 코드 스타일 및 모던 문법

* `const` Assertion(`as const`)을 사용하여 Literal Type을 최대한 활용하고 Immutability를 보장하십시오.
* Nullish Coalescing Operator(`??`)와 Optional Chaining(`?.`)을 적극 활용하여 Defensive Code를 간결하게 작성하십시오.
* `enum` 대신 `Union Type` 또는 `const object`를 사용하십시오 (Tree-shaking Optimization).
* Async 처리 시 `Promise.then` Chaining보다 `async/await` Syntax를 사용하십시오.

## 3. 에러 처리

* `try-catch` Block 내에서 Error를 잡을 때, Error Object를 `unknown`으로 Type 지정 후 Custom Error Type으로 변환하여 처리하십시오.
* Error를 무시(`// @ts-ignore`)하지 말고, Issue를 근본적으로 해결하십시오.
