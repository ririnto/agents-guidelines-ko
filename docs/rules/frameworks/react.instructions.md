# React 개발 가이드라인

이 문서는 React Ecosystem의 Best Practice와 추천 Library 조합을 정의합니다.

## 1. 핵심 프레임워크 및 구조

* **Framework:** 신규 프로젝트는 **Next.js** (App Router)를 기본으로 사용하십시오.
* **Language:** 반드시 **TypeScript**를 사용하십시오.
* **File Structure:** Feature-based Folder Structure를 지향하며, Business Logic과 UI View를 분리하십시오.

## 2. 추천 라이브러리 스택 (Preferred Stack)

에이전트는 아래의 **카테고리별 순위**를 참고하여 라이브러리를 선정하되, **1~2순위에 있는 무료/오픈소스**를 우선적으로 채택하십시오.

### 상태 관리 (State Management)

1. **Redux Toolkit** (Complex Global State)
2. **Zustand** (Simple/Medium Global State - Preferred)
3. Jotai
4. Recoil
5. MobX
6. XState
7. React Context API (For very simple prop-drilling prevention)

### 데이터 패칭 / 캐싱 / 서버 상태

1. **TanStack Query (React Query)**
2. SWR
3. Apollo Client (GraphQL)
4. RTK Query

### 라우팅 / 메타

1. **Next.js** (App Router)
2. React Router (Legacy or SPA only)
3. TanStack Router
4. Remix

### 폼 / 검증

1. **React Hook Form**
2. Formik
3. React Final Form
4. **Yup / Zod** (Validation Schema - Zod Preferred with TS)

### 유틸리티 / 컴포저블

1. Axios
2. clsx / tailwind-merge
3. date-fns
4. Lodash
5. React Use

### 애니메이션 / 인터랙션

1. **Framer Motion**
2. React Spring
3. GSAP (Check License for commercial use)
4. React Transition Group

### 차트 / 데이터 시각화

1. Recharts
2. Nivo
3. Chart.js (react-chartjs-2)
4. Victory
5. D3.js (For custom low-level visualization)

### 에디터 / 입력 컴포넌트

1. Draft.js
2. Slate.js
3. React Quill
4. Monaco Editor React

### 테스트

1. **React Testing Library**
2. **Vitest**
3. Jest
4. Cypress

### 빌드 / 개발 도구

1. **Vite** (SPA)
2. Turborepo
3. ESLint
4. Prettier
5. Storybook

### 머신러닝 / 데이터 (프론트엔드 연계)

1. TensorFlow.js
2. ml5.js
3. ONNX.js / ONNX Runtime Web
4. Brain.js

## 3. 컴포넌트 및 훅 패턴

* **Custom Hooks:** UI가 아닌 Logic은 반드시 Custom Hook으로 분리하십시오.
* **Composition:** Prop Drilling을 피하기 위해 Component Composition(Children Pattern)을 적극 활용하십시오.
