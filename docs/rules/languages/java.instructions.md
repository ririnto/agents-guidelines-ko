# Java 개발 가이드라인

이 문서는 JDK 8, 11, 17, 21, 25(Preview) 버전을 아우르는 Java Code 작성 규칙입니다. Project의 Target Version에 맞는 기능을 우선 사용하십시오.

## 1. 빌드 도구 및 패키지 관리 (Build Tools)

* **Gradle Kotlin DSL:** 신규 프로젝트는 **Gradle**을 사용하며, 설정 스크립트는 **Kotlin DSL** (`build.gradle.kts`)을 사용하십시오.
  * Groovy DSL보다 Type Safety와 IDE Auto-completion 지원이 강력합니다.
* **Version Catalog:** Dependency Version 관리는 `libs.versions.toml` (Gradle Version Catalog)을 사용하여 프로젝트 전반의 일관성을 유지하십시오.
* **Maven:** Legacy 프로젝트나 명시적인 요청이 있는 경우에만 Maven(`pom.xml`)을 사용하십시오.

## 2. 버전별 핵심 기능 활용

* **JDK 8 (Baseline):**
  * Anonymous Class 대신 **Lambda Expression**을 사용하십시오.
  * `null` check 대신 `Optional`을 사용하되, Return Type으로만 제한하십시오.
  * Collection 처리 시 `Stream API`를 활용하십시오.
* **JDK 11 (LTS):**
  * Local Variable의 Type Inference를 위해 `var` 키워드를 사용하십시오 (가독성을 해치지 않는 선에서).
  * HTTP 요청 시 `HttpUrlConnection` 대신 `java.net.http.HttpClient`를 사용하십시오.
* **JDK 17 (LTS):**
  * DTO 작성 시 Class 대신 **Record**(`record`)를 사용하여 Immutability를 보장하고 Boilerplate를 제거하십시오.
  * `switch` Statement 대신 값을 반환하는 **Switch Expression**을 사용하십시오.
  * Text Block(`"""`)을 사용하여 JSON, SQL, HTML String을 가독성 있게 작성하십시오.
* **JDK 21 (LTS):**
  * Concurrency 처리 시 Platform Thread 대신 **Virtual Threads**를 사용하여 Throughput을 극대화하십시오.
  * **SequencedCollection** Interface를 사용하여 첫 번째/마지막 요소 접근을 표준화하십시오.

## 3. 코드 스타일 및 안전성

* **Null Safety (JSpecify):** Null 안정성을 위해 **JSpecify** 어노테이션(`org.jspecify.annotations.Nullable`)을 사용하십시오. 이는 Kotlin 및 다양한 IDE와의 상호운용성을 보장합니다.
* **Default Non-null:** 모든 Field와 Parameter는 기본적으로 Non-null로 간주합니다.
* **Exceptions:** Checked Exception 사용을 지양하고, 가능한 한 **Unchecked Exception**(Runtime Exception)을 사용하십시오.
