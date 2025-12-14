# SwiftUI 개발 가이드라인

이 문서는 iOS UI 개발 시 SwiftUI의 선언형 문법과 State 관리 규칙입니다.

## 1. 뷰 구조 (View Structure)

* **Small Views:** `body` Property가 비대해지지 않도록, UI 부분을 작고 재사용 가능한 하위 View로 분리하십시오.
* **ViewModifier:** 공통된 Style이나 Logic은 Custom `ViewModifier`나 Extension으로 추출하십시오.

## 2. 상태 관리 (State Management)

* **Property Wrappers:**
  * `@State`: View 내부의 단순 로컬 상태.
  * `@Binding`: 부모 View와 양방향 데이터 공유.
  * `@StateObject`: View가 소유하는 Observable Object의 수명 주기 관리 (최초 생성).
  * `@ObservedObject`: 외부에서 주입받는 Observable Object (수명 주기 관리 안 함).
* 이 구분을 명확히 하여 Memory Leak이나 불필요한 Re-rendering을 방지하십시오.
