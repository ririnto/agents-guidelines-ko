# Kotlin 개발 가이드라인

이 문서는 Android 및 Backend 개발 시 Kotlin Code의 Safety와 Coroutine 사용 규칙을 정의합니다.

## 1. 빌드 도구 (Build Tools)

* **Gradle Kotlin DSL:** Kotlin 프로젝트는 반드시 **Kotlin DSL** (`build.gradle.kts`)을 사용하십시오.
* **Version Catalog:** Dependency 관리는 `libs.versions.toml` (Version Catalog)을 사용하여 중앙에서 관리하십시오.

## 2. 불변성 및 Null 안전성 (Immutability & Null Safety)

* **Val over Var:** Variable 선언 시 가능한 한 `val`(Read-only)을 사용하고, 꼭 필요한 경우에만 `var`(Mutable)를 사용하십시오.
* **Null Safety:** `!!` Operator(Non-null Assertion) 사용을 엄격히 금지합니다. 대신 Safe Call(`?.`), Elvis Operator(`?:`), 또는 `let` Scope Function을 사용하십시오.

## 3. 비동기 처리 (Concurrency)

* **Coroutines:** Thread를 직접 관리하지 말고 Kotlin Coroutines를 사용하십시오.
* **Dispatcher:** Blocking I/O 작업은 `Dispatchers.IO`, CPU 연산은 `Dispatchers.Default`, UI 업데이트는 `Dispatchers.Main`을 명확히 구분하여 사용하십시오.

## 4. 데이터 구조

* **Data Class:** 데이터를 보유하는 Class는 `data class`로 선언하여 `toString()`, `copy()`, `equals()` 등의 Boilerplate를 줄이십시오.
* **Extension Function:** Utils Class를 만드는 대신, 특정 Type에 대한 Extension Function을 정의하여 가독성을 높이십시오.

## 5. 파일 및 클래스 구조 (File & Class Structure)

* **One Class Per File:** 원칙적으로 하나의 File(.kt)에는 하나의 **Top-level Class**, **Interface**, 또는 **Object**만 정의하십시오.
  * Kotlin은 여러 Class 정의를 허용하지만, Maintainability와 Navigation 편의성을 위해 Java 스타일의 파일 분리를 선호합니다.
* **Exceptions:** 파일 내에서만 사용되는 `private` Class나, 매우 작고 밀접하게 연관된 Data Class 집합(예: Sealed Class 계층)은 예외로 허용합니다.
