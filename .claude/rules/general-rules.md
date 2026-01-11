# General Rules for Claude Agents

This file contains the master routing table and language guidelines for all Claude agents.

## Subagent Routing Rules

### Fast Discovery

- Use [`scout`](../agents/scout.md) to find files, entry points, and quick summaries.
- Use [`tech-researcher`](../agents/tech-researcher.md) to fetch and summarize external documentation.

### Deep Reasoning / Design

- Use [`architect`](../agents/architect.md) for hard debugging, architecture tradeoffs, and tricky performance issues.
- Use [`api-designer`](../agents/api-designer.md) for REST/GraphQL API design and consistency.
- Use [`refactor-coach`](../agents/refactor-coach.md) for incremental refactor plans.

### Implementation

- Use [`implementer`](../agents/implementer.md) for **all** implementation tasks (single-file or multi-file).
- Use [`test-runner`](../agents/test-runner.md) for failing tests.
- Use [`lint-fixer`](../agents/lint-fixer.md) for lint/format/typecheck fixes.

### Quality Gates

- Use [`code-reviewer`](../agents/code-reviewer.md) after significant diffs.

### Security

- Use [`security-auditor`](../agents/security-auditor.md) for threat modeling, security reviews, AND scan for secrets.
- Use [`compliance-auditor`](../agents/compliance-auditor.md) for regulatory compliance checks (GDPR/SOC2).
- Use [`red-team`](../agents/red-team.md) for adversarial security analysis.

### Ops

- Use [`incident-commander`](../agents/incident-commander.md) for incident coordination and stabilization.
- Use [`kubernetes-architect`](../agents/kubernetes-architect.md) for K8s manifests, Helm charts, and cluster design.
- Use [`runbook-writer`](../agents/runbook-writer.md) for operational runbooks.

### Writing

- Use [`release-comms`](../agents/release-comms.md) for PR descriptions, changelogs, commit messages, and release notes.
- Use [`ux-copywriter`](../agents/ux-copywriter.md) for UI microcopy (buttons, labels, error messages).

### Performance

- Use [`perf-profiler`](../agents/perf-profiler.md) for performance investigations and bottleneck analysis.
- Use [`flaky-test-hunter`](../agents/flaky-test-hunter.md) for flaky test isolation and fixes.

### Data & Analytics

- Use [`database-optimizer`](../agents/database-optimizer.md) for SQL query design and optimization.
- Use [`data-engineer`](../agents/data-engineer.md) for ETL pipelines and data modeling.
- Use [`analytics-instrumentation`](../agents/analytics-instrumentation.md) for adding analytics events safely.
- Use [`observability-engineer`](../agents/observability-engineer.md) for logs/metrics/traces improvements.

### CI/CD & Dependencies

- Use [`ci-fixer`](../agents/ci-fixer.md) for CI pipeline failures.
- Use [`dependency-manager`](../agents/dependency-manager.md) for dependency audits AND upgrades.
- Use [`feature-flag-manager`](../agents/feature-flag-manager.md) for feature flag integration.

### Documentation

- Use [`docs-writer`](../agents/docs-writer.md) for documentation (README/RFC/PRD) in English or Korean.
- Use [`adr-writer`](../agents/adr-writer.md) for Architecture Decision Records.
- Use [`onboarding-guide-writer`](../agents/onboarding-guide-writer.md) for onboarding documentation.
- Use [`architecture-diagrammer`](../agents/architecture-diagrammer.md) for Mermaid diagrams.

### Localization

- Use [`i18n-localization`](../agents/i18n-localization.md) for i18n/l10n tasks.
- Use [`translation-reviewer`](../agents/translation-reviewer.md) for translation quality review.

### Triage & Routing

- Use [`bug-triage`](../agents/bug-triage.md) for quick bug categorization.
- Use [`project-coordinator`](../agents/project-coordinator.md) for task tracking and status updates.

### Incident Communication

- Use [`incident-comms`](../agents/incident-comms.md) for incident status updates (Slack/StatusPage).

### Spring/Java/Kotlin

- Use [`spring-architect`](../agents/spring-architect.md) for Spring Boot/Cloud architecture design and microservices patterns.
- Use [`java-kotlin-expert`](../agents/java-kotlin-expert.md) for Java/Kotlin code implementation, best practices, and idioms.
- Use [`reactive-specialist`](../agents/reactive-specialist.md) for WebFlux/Reactor reactive programming and non-blocking patterns.
- Use [`spring-integration-expert`](../agents/spring-integration-expert.md) for Spring Integration, messaging patterns, and EIP.

### Frontend

- Use [`react-nextjs-expert`](../agents/react-nextjs-expert.md) for React/Next.js development, hooks, App Router, SSR/SSG, and RSC.
- Use [`vue-nuxt-expert`](../agents/vue-nuxt-expert.md) for Vue 3/Nuxt 3 development, Composition API, Pinia, and Nitro.
- Use [`typescript-expert`](../agents/typescript-expert.md) for TypeScript type design, generics, utility types, and strict mode.

---

## Language & Writing Rules

### Default Language

- If the user message is Korean, default to Korean outputs.
- If the user message is English, default to English outputs.

### When Writing User-Facing Text

- Use the language-specific writers when tone/grammar matters:
  - [`docs-writer`](../agents/docs-writer.md) for documentation (English/Korean)
  - [`ux-copywriter`](../agents/ux-copywriter.md) for UI microcopy (English/Korean)
- Product names / code identifiers / API fields must remain unchanged (keep them in English).

### When Writing Engineering Artifacts

- Code comments may remain in English unless the repo has a strict rule.
- Keep commit messages and PR descriptions in English unless your team explicitly uses Korean.

### If Uncertain

- Ask ONE clarifying question about the target audience and output language.
