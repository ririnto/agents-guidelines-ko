# Vue UI Library 가이드라인

Vuetify, PrimeVue, Quasar, NuxtUI 사용 규칙입니다.

## 1. Layout & Grid

* **Grid System:** CSS Flex/Grid를 직접 작성하는 것보다 Library의 **Grid System Components**(Row, Col)를 사용하여 Layout Consistency를 유지하십시오.
* **Spacing Utilities:** Margin, Padding 적용 시 Library의 **Utility Classes**(예: `pa-4`, `ma-2`)를 사용하십시오.

## 2. Components & Slots

* **Slots:** Complex Content를 전달할 때는 Props 대신 **Slots**(`template #name`) Mechanism을 적극 활용하십시오.
* **Global Config:** Default Props나 Theme Customization은 Component 별로 설정하지 말고 **Global Configuration** 레벨에서 처리하십시오.
