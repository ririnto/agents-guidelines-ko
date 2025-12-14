# Jetpack Compose 개발 가이드라인

이 문서는 Android UI 개발 시 Compose의 선언형 패턴과 성능 최적화 규칙입니다.

## 1. 컴포저블 함수 (Composable Functions)

* **Side Effects Free:** `@Composable` 함수는 원칙적으로 Side Effect가 없어야 합니다. Side Effect가 필요한 경우 `LaunchedEffect`, `DisposableEffect` 등의 Effect API를 사용하십시오.
* **State Hoisting:** State를 하위 Component 내부에 숨기지 말고, Caller가 제어할 수 있도록 Parameter로 끌어올리십시오(Hoisting).

## 2. 성능 최적화

* **Stability:** Composable의 Parameter가 Stable한지 확인하십시오. List 등을 전달할 때는 `ImmutableList`를 사용하거나 `@Stable` Annotation을 활용하여 불필요한 Recomposition을 건너뛰도록 하십시오.
* **Remember:** 계산 비용이 높은 작업이나 Object 생성은 `remember`를 사용하여 Recomposition 시에도 값을 보존하십시오.
