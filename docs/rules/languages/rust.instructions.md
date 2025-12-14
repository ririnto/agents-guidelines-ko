# Rust 개발 가이드라인

## 1. 에러 처리 및 안정성

* **No Unwrap:** `unwrap()`이나 `expect()` 사용을 지양하고, `match` 또는 `?` Operator를 통해 에러를 전파하십시오.
* **Borrowing:** 불필요한 `clone()`을 피하고 Reference(`&`)를 최대한 활용하십시오.

## 2. 구조화

* **Modularity:** 코드를 `mod`와 `crate`로 분리하고, Encapsulation을 위해 `pub` 사용 범위를 최소화하십시오.
