# React UI Library 가이드라인

MUI, Chakra UI, Ant Design, PrimeReact, NextUI 사용 규칙입니다.

## 1. Styling & Theming

* **Utility Props:** Margin, Padding, Color 등은 Library가 제공하는 **Utility Props**(`sx`, `p`, `m`, `color`)를 우선 사용하십시오.
* **Theme Tokens:** Hard-coded Hex Color나 Pixel Value 대신, **Theme Provider**에 정의된 Design Token(Primary Color, Spacing Scale 등)을 참조하십시오.

## 2. Components Usage

* **Composition:** Library Component를 직접 사용하기보다, Project 요구사항에 맞춰 Wrapper Component로 **Abstraction**하여 사용하십시오.
* **Icons:** Library 전용 Icon Package를 사용하고, `import` 시 Tree Shaking이 적용되도록 Path를 확인하십시오.
