# Docker Compose 가이드라인

Local Development Environment 구성을 위한 규칙입니다.

## 1. 서비스 정의

* **Version:** Compose Specification 최신 버전을 따르며, 최상단 `version` 속성은 생략합니다 (Compose V2 기준).
* **Container Name:** 명시적인 `container_name` 지정은 Scale-out 시 충돌을 유발하므로, Single Instance가 확실한 경우에만 사용하십시오.

## 2. 네트워크 및 볼륨

* **Networks:** Default Network에 의존하지 말고, Custom Bridge Network를 정의하여 Service 간 격리 및 통신을 제어하십시오.
* **Volumes:** Data Persistence가 필요한 Database 등은 반드시 Named Volume 또는 Host Bind Mount를 설정하십시오.

## 3. 환경 변수

* **Env Files:** Secret이나 환경별 설정은 `.env` 파일로 관리하고, `env_file` 속성을 통해 주입하십시오.
