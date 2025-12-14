# Terraform 개발 가이드라인

이 문서는 DevOps Engineer가 Infrastructure as Code(IaC)를 작성할 때 따러야 할 규칙입니다.

## 1. 상태 관리 (State Management)

* **Remote State:** `local` State 사용을 금지합니다. S3, GCS, Terraform Cloud 등의 Backend를 사용하여 State File을 공유하고 Locking(`DynamoDB` 등)을 적용하십시오.

## 2. 모듈화 및 구조

* **Module 활용:** 반복되는 Resource 집합은 Module로 분리하십시오.
* **Standard Module Structure:** Module은 `main.tf`, `variables.tf`, `outputs.tf`로 명확히 분리하여 작성하십시오.

## 3. 변수 및 보안

* **Variables:** 모든 `variable`에는 `description`과 `type`을 반드시 명시하십시오.
* **Secrets:** Password, Access Key 등 Sensitive Data는 절대 Code에 하드코딩하지 말고, Environment Variable이나 Secret Manager를 통해 주입받으십시오.
