# Helm Chart 가이드라인

Kubernetes Resource Package 관리를 위한 규칙입니다.

## 1. Values 관리

* **values.yaml:** 모든 Configurable Value는 `values.yaml`에 정의하고, Template 내 하드코딩을 금지합니다.
* **Structure:** `values.yaml`의 구조는 Application Configuration 구조와 유사하게 Nested 형태로 구성하십시오 (예: `image.repository`, `image.tag`).

## 2. 템플릿 작성

* **Helpers:** 반복되는 Label, Resource Name 등은 `_helpers.tpl`에 Named Template으로 정의하여 재사용하십시오.
* **Checksum:** ConfigMap 변경 시 Pod 재시작을 유도하기 위해 Deployment Annotation에 Checksum function(`sha256sum`)을 사용하십시오.
