# Zod 사용 가이드라인

이 문서는 Runtime Schema Validation Library인 Zod를 사용할 때의 Pattern과 규칙을 정의합니다.

## 1. 스키마 정의 및 타입 추론

* **Single Source of Truth:** Schema를 정의하고 `z.infer<typeof schema>`를 사용하여 TypeScript Type을 추출하십시오.
* **Optional & Default:** Field가 Optional인 경우 `.optional()`을, Default Value가 필요한 경우 `.default()`를 사용하십시오.

## 2. 유효성 검사 및 파싱

* **Safe Parse:** 신뢰할 수 없는 Data는 `safeParse`를 사용하여 Exception 발생 대신 Result Object(`success`, `data`, `error`)를 처리하십시오.
* **Transformation:** Data Sanitization이 필요한 경우 `.transform()`을 사용하여 Validation과 동시에 Data를 가공하십시오.

## 3. 에러 메시지

* **Custom Messages:** User에게 노출되는 경우 `z.string({ required_error: "..." })`와 같이 명확한 Error Message를 제공하십시오.
