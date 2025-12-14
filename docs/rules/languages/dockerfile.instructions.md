# Dockerfile 작성 가이드라인

Build Performance 최적화와 Image Size 감소를 위한 규칙입니다.

## 1. BuildKit 및 Syntax

* **Enable BuildKit:** 파일 최상단에 `# syntax=docker/dockerfile:1`을 추가하여 최신 BuildKit 기능을 활성화하십시오.
* **Mounts:** Package Manager 캐시 등을 활용하기 위해 `RUN --mount=type=cache,target=...` 옵션을 적극 사용하십시오.

## 2. 레이어 캐싱 및 체이닝 (Layer Caching & Chaining)

* **Dependency First:** Source Code(`COPY . .`)를 복사하기 전에 Dependency Definition File(`package.json`, `go.mod`, `pom.xml`)을 먼저 복사하고 Install 명령을 실행하여 Layer Cache를 활용하십시오.
* **Selective Chaining:**
  * `apt-get update`와 `apt-get install`은 반드시 `&&`로 연결하여 동일한 Layer에서 실행해야 합니다 (Stale Repository 방지).
  * 하지만, 변경 빈도가 다른 Build Step이나 Debugging이 필요한 복잡한 설정은 `&&`로 무리하게 연결하지 말고 별도의 `RUN` 명령어로 분리하여 Cache Invalidation 범위를 좁히십시오.

## 3. 보안 및 최적화

* **Multi-stage Build:** Build 도구가 포함된 Image와 실행용 Image를 분리하여 Final Image Size를 줄이십시오.
* **User:** Root 권한 실행을 피하고 `USER` 지시어를 사용하십시오.
