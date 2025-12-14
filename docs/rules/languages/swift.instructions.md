# Swift 개발 가이드라인

이 문서는 iOS/macOS 개발 시 Swift 언어의 특징을 활용한 안전하고 명확한 Code 작성 규칙입니다.

## 1. 안전한 언래핑 (Safe Unwrapping)

* **Guard Statement:** Optional Binding 시 Nested If 구조(`if let`)보다는 `guard let`을 사용하여 Happy Path를 들여쓰기 없이 유지하고, 예외 상황을 조기에 Return하십시오.
* **Force Unwrapping 금지:** 개발 단계의 명백한 상황을 제외하고는 `!`(Force Unwrapping) 사용을 금지합니다.

## 2. 구조체와 클래스 (Struct vs Class)

* **Value Type 우선:** 기본적으로 `struct`(Value Type)를 사용하십시오. Identity가 필요하거나 Objective-C 상호 운용성이 필요한 경우에만 `class`(Reference Type)를 사용하십시오.
* **Protocol Oriented:** 상속(Inheritance)보다는 Protocol과 Extension을 활용한 Protocol Oriented Programming(POP)을 지향하십시오.

## 3. 메모리 관리

* **Weak Self:** Closure 내에서 `self`를 캡처할 때 Retain Cycle을 방지하기 위해 `[weak self]`를 명시하고, 내부에서 `guard let self = self else { return }` 패턴을 사용하십시오.
