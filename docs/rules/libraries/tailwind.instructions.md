# Tailwind CSS 사용 가이드라인

이 문서는 Frontend Styling 시 Utility-first 접근 방식을 유지하기 위한 규칙입니다.

## 1. 클래스 정렬 및 가독성

* **Class Sorting:** `prettier-plugin-tailwindcss` 등을 사용하여 Class Name을 일관된 순서로 자동 정렬하십시오.
* **Arbitrary Values:** `w-[123px]`와 같은 Arbitrary Value 사용을 최소화하고, `tailwind.config.js`의 Theme을 확장하여 Design System Token을 사용하십시오.

## 2. 컴포넌트화

* **Apply 지양:** `@apply`를 사용하여 CSS File에 Custom Class를 만드는 것을 피하십시오. 대신 React/Vue Component로 UI 요소를 분리하여 재사용성을 확보하십시오.
* **Conditional Styles:** `clsx`나 `tailwind-merge` 라이브러리를 사용하여 조건부 Class 적용 및 충돌 문제를 해결하십시오.
