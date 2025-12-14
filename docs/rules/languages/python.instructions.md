# Python 개발 가이드라인

이 문서는 Python Code 작성 시 준수해야 할 Type Hinting 및 Style 규칙을 정의합니다.

## 1. 타입 힌트 및 안정성 (Type Hinting)

* **Strict Type Hints:** 모든 Function Signature(Arguments, Return Type)에 Type Hint를 명시하십시오. `typing` 모듈 또는 Built-in Collection Type(`list`, `dict` 등)을 사용하십시오.
* **Any 지양:** `Any` Type 사용을 피하고, 동적 Typing이 필요한 경우 `Union`이나 `TypeVar` (Generics)를 활용하십시오.
* **Pydantic 활용:** Data Class가 필요한 경우 표준 `dataclass`보다 Validation이 강력한 `Pydantic`의 `BaseModel`을 우선 고려하십시오.

## 2. 코드 스타일 및 관용구 (Pythonic Style)

* **List Comprehension:** 단순한 Loop를 통한 List 생성은 List Comprehension을 사용하되, 가독성을 해칠 정도로 복잡한 Logic은 일반 `for` Loop로 작성하십시오.
* **Context Manager:** File I/O, Network Connection, Lock 등 Resource 관리가 필요한 경우 반드시 `with` Statement를 사용하십시오.
* **Naming Convention:** Variable과 Function은 `snake_case`, Class는 `PascalCase`, Constant는 `UPPER_SNAKE_CASE`를 따르십시오.

## 3. 에러 처리

* **Specific Exception:** 막연한 `except Exception:`을 사용하지 말고, 구체적인 Exception Class(`ValueError`, `KeyError` 등)를 명시하여 Catch하십시오.
