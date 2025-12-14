# Vue 생태계 가이드라인

Vue 3, Nuxt 및 관련 Library 사용 시의 Standard Stack과 규칙입니다.

## 1. 핵심 프레임워크

* **Framework:** 신규 프로젝트는 **Nuxt**를 기본으로 사용하십시오.
* **Syntax:** `<script setup lang="ts">`와 **Composition API**를 필수적으로 사용하십시오.

## 2. 추천 라이브러리 스택 (Preferred Stack)

에이전트는 아래의 **카테고리별 순위**를 참고하여 라이브러리를 선정하되, **1~2순위에 있는 무료/오픈소스**를 우선적으로 채택하십시오.

### 상태 관리 (State Management)

1. **Pinia** (Preferred)
2. Vuex (Legacy)
3. TanStack Vue Query (Server State)
4. SWRV
5. vuex-orm

### 데이터 패칭 / 캐싱 / 서버 상태

1. **Axios** or **Nuxt useFetch**
2. TanStack Vue Query
3. Apollo Client
4. SWRV
5. urql

### 라우팅 / 메타

1. **Vue Router** (Nuxt Pages)
2. @vueuse/head
3. unhead
4. nuxt-seo-kit
5. vue-meta

### 폼 / 검증

1. **VeeValidate**
2. **Zod** (Schema)
3. Yup
4. Vuelidate
5. Vest

### 유틸리티 / 컴포저블

1. **VueUse** (Essential)
2. lodash-es
3. dayjs
4. mitt
5. nanoid

### 애니메이션 / 인터랙션

1. GSAP (Check License for commercial use)
2. **vueuse/motion**
3. anime.js
4. Velocity.js
5. Framer Motion Vue

### 차트 / 데이터 시각화

1. **ECharts**
2. Chart.js
3. D3.js
4. Plotly.js
5. Vega / Vega-Lite

### 에디터 / 입력 컴포넌트

1. Monaco Editor
2. TipTap
3. Quill
4. CodeMirror
5. Slate

### 테스트

1. **Vitest**
2. Cypress
3. Playwright
4. Vue Test Utils
5. Jest

### 빌드 / 개발 도구

1. **Vite**
2. unplugin-auto-import
3. unplugin-vue-components
4. ESLint (Vue Plugin)
5. Prettier

### 머신러닝 / 데이터 (프론트엔드 연계)

1. TensorFlow.js
2. ONNX Runtime Web
3. Brain.js
4. ml5.js
5. Comlink

## 3. Nuxt 및 컴포넌트 패턴

* **Auto Imports:** Nuxt의 Auto Import 기능을 활용하되, IDE 지원을 위해 `tsconfig.json` 설정이 올바른지 확인하십시오.
* **Global State:** Pinia Store는 Setup Store 문법(`defineStore(id, () => { ... })`)을 사용하십시오.
