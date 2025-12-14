# Jsonnet 작성 가이드라인

Configuration Template 언어인 Jsonnet 작성 시 Modularization과 Readability를 위한 규칙입니다.

## 1. 모듈화 및 임포트

* **Imports:** 공통 Library나 Template은 별도 파일로 분리하여 `import` 하십시오.
* **Path:** Import Path는 상대 경로(`./lib/utils.libsonnet`)를 명확히 사용하십시오.

## 2. 변수 및 스타일

* **Locals:** 복잡한 Expression이나 반복되는 값은 `local` Variable로 추출하여 가독성을 높이십시오.
* **Hidden Fields:** 최종 Output JSON에 포함되지 않아야 하는 중간 변수나 함수는 Hidden Field(`::`)를 사용하십시오.
* **Formatting:** `jsonnetfmt` 표준(2 Spaces Indentation, Double Quotes for Strings)을 따르십시오.

## 3. 함수 활용

* **Functions:** 반복되는 설정 패턴은 Function으로 정의하여 재사용성을 확보하십시오. Parameter에 Default Value를 제공하여 유연성을 높이십시오.
