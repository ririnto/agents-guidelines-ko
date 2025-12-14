# Spring Boot 개발 가이드라인

이 문서는 Java/Kotlin 기반 Spring Boot Backend Application의 **Domain-Driven Design (DDD)** 및 의존성 선택 규칙입니다.

## 1. 도메인 중심 설계 및 아키텍처 (Domain-Driven Design)

모든 비즈니스 로직은 **Domain Model**을 중심으로 구현하며, **Anemic Domain Model** (빈약한 도메인 모델) 패턴을 지양합니다.

* **Layered Architecture:**
  * **Presentation Layer:** 사용자 요청 수신, 입력 유효성 검사, DTO <-> Domain 변환을 담당합니다.
  * **Application Layer:** 트랜잭션 관리, 도메인 객체 간의 흐름 제어(Orchestration)를 담당합니다. 비즈니스 로직을 직접 포함하지 않습니다.
  * **Domain Layer:** 핵심 비즈니스 로직, 상태 변경 규칙, 불변 조건(Invariant)을 포함합니다. 외부 의존성(DB, Web 등)을 가지지 않습니다.
  * **Infrastructure Layer:** Repository 구현체, 외부 API 호출, 메시징 등 기술적인 세부 사항을 담당합니다.
* **Entity & Value Object:**
  * 상태를 변경하는 로직은 Service가 아닌 **Entity** 내부에 메서드로 구현하여 응집도를 높이십시오.
  * 식별자가 필요 없는 데이터 묶음은 **Value Object (VO)**로 구현하고 불변성(Immutability)을 보장하십시오.

## 2. 의존성 주입 (Dependency Injection)

* **Constructor Injection:** Field Injection(`@Autowired` on field)을 금지합니다.
* **Explicit Injection:** `private final` 필드를 선언하고, **생성자(Constructor)**를 통해 명시적으로 의존성을 주입받아 테스트 용이성과 불변성을 확보하십시오.

## 3. 예외 처리

* **Custom Exception:** 도메인별 구체적인 예외(`UserNotFoundException` 등)를 정의하여 사용하십시오.
* **Global Exception Handler:** `@RestControllerAdvice`와 `@ExceptionHandler`를 사용하여 예외를 포착하고, 일관된 Error Response Format(Code, Message)으로 변환하여 반환하십시오.

## 4. 의존성 선택 가이드 (Dependency Ecosystem)

기능 추가 시 3rd Party Library를 직접 추가하기보다, 아래의 **Spring Boot Starter** 및 **Spring Cloud** 생태계에 포함된 의존성을 최우선으로 선택하십시오.

### 웹 / HTTP (Web & HTTP)

* **Standard (Servlet):**
  * **Web MVC:** `spring-boot-starter-web`
* **Reactive (WebFlux):**
  * **WebFlux:** `spring-boot-starter-webflux`
* **Others:**
  * **WebSocket:** `spring-boot-starter-websocket`
  * **RSocket:** `spring-boot-starter-rsocket`
  * **SOAP:** `spring-boot-starter-web-services`

### 데이터 / 영속성 (Data & Persistence)

* **SQL (RDBMS):**
  * **JPA:** `spring-boot-starter-data-jpa`
  * **JDBC:** `spring-boot-starter-data-jdbc`
  * **R2DBC (Reactive):** `spring-boot-starter-data-r2dbc`
* **NoSQL (Blocking):**
  * **Redis:** `spring-boot-starter-data-redis`
  * **MongoDB:** `spring-boot-starter-data-mongodb`
  * **Elasticsearch:** `spring-boot-starter-data-elasticsearch`
  * **Cassandra:** `spring-boot-starter-data-cassandra`
* **NoSQL (Reactive):**
  * **Redis:** `spring-boot-starter-data-redis-reactive`
  * **MongoDB:** `spring-boot-starter-data-mongodb-reactive`
  * **Cassandra:** `spring-boot-starter-data-cassandra-reactive`
* **Utilities:**
  * **REST (HAL):** `spring-boot-starter-data-rest`
  * **LDAP:** `spring-boot-starter-data-ldap`

### 유틸리티 및 개발 도구 (Utilities & Dev Tools)

* **Validation:**
  * **Standard:** `spring-boot-starter-validation` (Bean Validation)
* **Processors (Annotation):**
  * **Config Meta:** `spring-boot-configuration-processor` (@ConfigurationProperties)
  * **AutoConfig:** `spring-boot-autoconfigure-processor` (Custom Starter)
* **Development:**
  * **DevTools:** `spring-boot-devtools` (Hot Swap, Reload)

### 메시징 / 스트리밍 (Messaging & Streaming)

* **Message Brokers:**
  * **Kafka:** `spring-boot-starter-kafka`
  * **RabbitMQ:** `spring-boot-starter-amqp`
  * **Pulsar:** `spring-boot-starter-pulsar`
  * **ActiveMQ:** `spring-boot-starter-activemq`
  * **Artemis:** `spring-boot-starter-artemis`
* **Standard:**
  * **JMS:** `spring-boot-starter-jms`

### 배치 / 스케줄링 / 통합 (Batch & Integration)

* **Processing:**
  * **Batch:** `spring-boot-starter-batch`
  * **Quartz:** `spring-boot-starter-quartz`
* **Integration:**
  * **Spring Integration:** `spring-boot-starter-integration`

### 보안 (Security)

* **Core:**
  * **Security:** `spring-boot-starter-security`
* **OAuth2 / OIDC:**
  * **Client:** `spring-boot-starter-oauth2-client`
  * **Resource Server:** `spring-boot-starter-oauth2-resource-server`
  * **Auth Server:** `spring-boot-starter-oauth2-authorization-server`

### 템플릿 및 이메일 (Templates & Mail)

* **Templates:**
  * **Thymeleaf:** `spring-boot-starter-thymeleaf`
  * **Mustache:** `spring-boot-starter-mustache`
  * **FreeMarker:** `spring-boot-starter-freemarker`
* **Mail:**
  * **JavaMail:** `spring-boot-starter-mail`

### 운영 및 테스트 (Ops & Test)

* **Operations:**
  * **Actuator:** `spring-boot-starter-actuator`
* **Testing:**
  * **Core Test:** `spring-boot-starter-test`
  * **WebFlux Test:** `spring-boot-starter-webflux-test`
  * **Security Test:** `spring-boot-starter-security-test`
  * **JPA Test:** `spring-boot-starter-data-jpa-test`

### Spring Cloud (Cloud Native)

* **Gateway & Network:**
  * **Gateway:** `spring-cloud-starter-gateway`
  * **OpenFeign:** `spring-cloud-starter-openfeign`
  * **LoadBalancer:** `spring-cloud-starter-loadbalancer`
* **Discovery:**
  * **Eureka:** `spring-cloud-starter-netflix-eureka-client`
  * **Consul:** `spring-cloud-starter-consul-discovery`
  * **Zookeeper:** `spring-cloud-starter-zookeeper-discovery`
* **Config & Event:**
  * **Config:** `spring-cloud-starter-config`
  * **Bus:** `spring-cloud-starter-bus`
  * **Stream Kafka:** `spring-cloud-starter-stream-kafka`
  * **Stream Rabbit:** `spring-cloud-starter-stream-rabbit`

### Spring Cloud Kubernetes

* **Fabric8 기반:**
  * **통합:** `spring-cloud-starter-kubernetes-fabric8-all`
  * **Config:** `spring-cloud-starter-kubernetes-fabric8-config`
  * **Discovery:** `spring-cloud-starter-kubernetes-fabric8-discovery`
  * **LoadBalancer:** `spring-cloud-starter-kubernetes-fabric8-loadbalancer`
* **Java Client 기반:**
  * **통합:** `spring-cloud-starter-kubernetes-client-all`
  * **Config:** `spring-cloud-starter-kubernetes-client-config`
  * **Discovery:** `spring-cloud-starter-kubernetes-client-discovery`
  * **LoadBalancer:** `spring-cloud-starter-kubernetes-client-loadbalancer`
* **Common:**
  * **Core:** `spring-cloud-starter-kubernetes`
