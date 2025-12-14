# 기술 스택 선정 기준 (Technology Stack Selection)

이 문서는 신규 프로젝트 착수, 리팩토링, 또는 새로운 기능을 도입할 때 **라이브러리 및 프레임워크를 선정하는 기준**을 정의합니다.

## 1. 기본 원칙 (Core Principles)

* **Standard Stack First:** AI 모델의 학습 데이터(Training Data)가 풍부하고 커뮤니티가 활성화된 대중적인 스택을 최우선으로 선택하십시오.
* **Opinionated Frameworks:** 단순 라이브러리 조합보다는 구조가 잡혀있는 프레임워크(Next.js, Nuxt, Spring Boot)를 선호합니다.

## 2. 라이선스 및 비용 (License & Cost)

* **Free & Open Source:** 비용이 발생하지 않는 **MIT**, **Apache-2.0** 라이선스 라이브러리를 최우선으로 사용하십시오.
* **Commercial Check:** 유료 라이선스나 사용량 기반 과금(SaaS)이 있는 도구는 사용자가 명시적으로 요청하지 않는 한 피하십시오.

## 3. AI 도구 및 확장 프로토콜 (AI Tools & Protocol)

외부 데이터나 도구를 연결할 때는 독자적인 API 연동보다 **MCP Standard**를 준수하는 서버 사용을 우선 고려하십시오.

* **Documentation:** 최신 라이브러리 문서는 Hallucination을 피하기 위해 **Context7** MCP를 활용하십시오.
* **Reasoning:** 복잡한 문제는 **Sequential Thinking** MCP를 통해 단계적으로 해결하십시오.
* **Coding:** 정밀한 코드 탐색 및 수정은 **Serena** MCP를, IDE 제어는 **JetBrains** MCP를 활용하십시오.
* **Memory:** 장기적인 프로젝트 정보 저장은 **Memory** MCP를 활용하십시오.

## 4. 카테고리별 선정 순위 (Selection Rankings)

에이전트는 특별한 사유가 없다면 각 카테고리의 **1순위** 기술을 Default로 사용하십시오.

### 패키지 매니저 (Package Managers - Frontend)

1. **pnpm** (Performance & Disk Efficiency preferred)
2. yarn
3. npm

### 빌드 도구 (Build Tools - Java/Kotlin)

1. **Gradle with Kotlin DSL** (`build.gradle.kts`)
2. Gradle with Groovy DSL
3. Maven

### 백엔드 프레임워크 (Backend Frameworks - Java/Kotlin)

1. **Spring Boot** (Standard)
2. Quarkus (Cloud Native / High Performance needs)

### 프론트엔드 프레임워크 (Frontend Frameworks)

1. **React (Next.js)** / **Vue (Nuxt)**
2. Vanilla React / Vue

### 상세 라이브러리 가이드

각 생태계별 상세 라이브러리 순위는 다음 파일을 참조하십시오:

* **React:** `docs/rules/frameworks/react.md`
* **Vue:** `docs/rules/frameworks/vue_ecosystem.md`
* **Spring Boot:** `docs/rules/frameworks/spring_boot.md`
