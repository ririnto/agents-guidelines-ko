# 설정 및 데이터 포맷 가이드라인

Configuration 및 Data Serialization 포맷별 작성 규칙입니다.

## 1. YAML

* **Indentation:** Tab 문자를 금지합니다. 반드시 **2 Spaces**를 사용하십시오.
* **Strings:** Special Character가 포함되지 않은 경우 Quote를 생략해도 되지만, 확신이 없으면 Single Quote(`'`)를 사용하십시오.
* **Booleans:** `yes/no`, `on/off` 대신 명확한 `true/false`를 사용하십시오.

## 2. JSON & JSONC

* **Syntax:** Standard JSON 파일에는 Comment를 포함하지 마십시오. Comment가 필요한 경우 `.jsonc` Extension을 사용하거나 VS Code settings(`json.schemas`)를 활용하십시오.
* **Keys:** Property Key는 항상 Double Quote(`"`)로 감싸야 합니다.

## 3. TOML

* **Structure:** 관련 설정은 `[Section]` Header를 사용하여 그룹화하십시오.
* **Consistency:** Key와 Value 사이의 Equal Sign(`=`) 주변에 공백을 하나씩 두어 가독성을 높이십시오.

## 4. XML

* **Attributes vs Elements:** 구조적인 데이터는 Child Element로, 메타데이터나 식별자는 Attribute로 표현하십시오.
* **CDATA:** Special Character가 많이 포함된 Text Content는 `<![CDATA[ ... ]]>` 섹션을 사용하십시오.

## 5. Properties (Java/Spring)

* **Encoding:** 한글 사용 시 Unicode Escape(`\uXXXX`)가 필요한지 확인하거나, Editor가 UTF-8을 지원하는지 확인하십시오.
* **Grouping:** Dot Notation(`server.port`, `server.servlet.context-path`)을 사용하여 계층 구조를 명확히 하십시오.

## 6. CSV

* **Headers:** 첫 번째 Row에 반드시 Header를 포함하십시오.
* **Escaping:** Comma(`,`)나 Newline이 포함된 Field는 반드시 Double Quote(`"`)로 감싸십시오.

## 7. INI

* **Sections:** Global 설정은 파일 상단에 배치하고, 특정 모듈 설정은 `[Section]` 아래에 배치하십시오.
* **Comments:** Semicolon(`;`) 또는 Hash(`#`)를 사용하여 주석을 작성하십시오.

## 8. Env (.env)

* **Quoting:** Value에 Space나 Shell Special Character가 포함된 경우 Double Quote(`"`)로 감싸십시오.
* **Naming:** Variable Name은 `UPPER_SNAKE_CASE`를 따르십시오.
