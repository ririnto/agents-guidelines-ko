# Markdown 작성 가이드라인

이 문서는 `markdownlint-cli2` 규칙 준수 및 문서 품질 향상을 위한 가이드입니다.

## 1. 헤더 (Headings)

* **MD001/heading-increment:** Header Level은 한 번에 한 단계씩만 증가해야 합니다 (h1 -> h2 (O), h1 -> h3 (X)).
* **MD003/heading-style:** Header Style은 ATX 스타일(`# Header`)만 사용하십시오.
* **MD025/single-title:** 문서 전체에서 H1 Header는 단 하나만 존재해야 하며, 파일 최상단에 위치해야 합니다.

## 2. 리스트 및 공백 (Lists & Spacing)

* **MD007/ul-indent:** Unordered List의 Indentation은 **2 Spaces**를 사용하십시오.
* **MD031/blanks-around-fences:** Code Block 위아래에는 반드시 빈 줄(Blank Line)이 있어야 합니다.
* **MD032/blanks-around-lists:** List 위아래에는 반드시 빈 줄이 있어야 합니다.

## 3. 라인 길이 및 코드 (Line Length & Code)

* **MD013/line-length:** 한 줄이 지나치게 길어지지 않도록 하십시오 (Soft Wrap 권장, 단 Table과 Code Block은 예외).
* **Language Syntax:** Code Block에는 항상 **Language Identifier**를 명시하십시오 (예: \`\`\`bash).
