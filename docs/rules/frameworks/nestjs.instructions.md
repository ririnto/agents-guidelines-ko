# Next.js 개발 가이드라인

이 문서는 Next.js(App Router 기준)를 사용한 Frontend 개발 시 Performance와 Architecture 규칙입니다.

## 1. 렌더링 전략 (Server vs Client)

* **Server Components Default:** 가능한 모든 Component를 Server Component로 작성하십시오.
* **Use Client:** Interactivity(onClick)나 Browser API(window)가 필요한 Leaf Component에만 최상단에 `'use client'`를 추가하십시오.

## 2. 데이터 페칭 (Data Fetching)

* **Fetch API:** Server Component 내부에서 `fetch`를 직접 사용하고, `revalidate` 옵션이나 `cache: 'no-store'`로 Caching을 제어하십시오.
* **Client Fetching:** Client Component에서 Data가 필요한 경우 SWR 또는 TanStack Query를 사용하십시오.

## 3. 최적화

* **Images & Fonts:** `next/image`와 `next/font`를 사용하여 Layout Shift를 방지하고 Loading 성능을 최적화하십시오.
