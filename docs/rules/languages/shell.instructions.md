# Shell Script (Bash) 가이드라인

## 1. 안전성 (Safety)

* **Set Flags:** 스크립트 상단에 `set -euo pipefail`을 명시하여 오류 발생 시 즉시 중단되도록 하십시오.
* **Quoting:** 변수 사용 시 항상 Double Quote(`"$VAR"`)로 감싸서 공백 및 특수 문자로 인한 오류를 방지하십시오.

## 2. 도구 활용

* **ShellCheck:** 코드를 생성할 때 `shellcheck` 규칙을 준수하여 잠재적인 문제를 해결하십시오.
