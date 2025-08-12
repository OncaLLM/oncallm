# OncallM Roadmap

Purpose

- Make OncallM a reliable on-call AI copilot that triages alerts, inspects Kubernetes signals (resources, events, logs, metrics), summarizes likely root cause, and proposes safe, auditable remediations. Optimized for a link-first workflow: Alertmanager (and other notifiers) include links to the OncallM web UI for each alert; optional ChatOps integrations can come later. Supports authenticated deep-links via SSO/SAML/OIDC. Emphasizes low-cost local LLM support for development and testing.

Versioning and planning

- Pre-GA milestones use 0.x versions (0.1 … 0.9). GA is 1.0 with semantic versioning.
- Each milestone lists goals and a concise definition of done (DoD) to keep PRs focused and reviewable.

Milestones

0.1 – MVP stabilization and clarity
Goals

- Solidify API endpoints and predictable error responses.
- Improve typing, docstrings, and error handling across services.
- Unify configuration via environment variables with sane defaults.
- Optional: streaming responses for LLM output.
- LLM provider abstraction with Local LLM dev mode (OpenAI-compatible endpoint) to enable low-cost development and testing.
DoD
- [ ] Endpoints return structured errors and consistent JSON.
- [ ] Type checks and lints pass in CI; essential unit tests added.
- [ ] A single configuration surface documented.

0.2 – Production readiness
Goals

- Retries, timeouts, and circuit breakers for external calls (K8s API, LLMs).
- Rate limiting and request size limits.
- PII scrubbing/redaction before LLM calls.
- Caching strategy for repeated context fetches.
- Observability: structured logging, metrics, health/readiness.
- Helm chart hardening: resources, security context, annotations.
DoD
- [ ] External calls have timeouts and retry policies.
- [ ] Basic redaction and request validation in place.
- [ ] Metrics and health endpoints exposed; Helm values for prod ready.

0.3 – Link-first workflow expansion
Goals

- Cloud LLM provider driver (e.g., OpenAI/Azure/Anthropic) added on top of the provider abstraction (local dev mode remains default for development).
- Link-first alert deep-links: canonical URL scheme `/alerts/{alert_id}` that renders triage status and results.
- Alertmanager template examples and a small helper to include the alert link in notifications.
- Optional signed links or per-alert tokens to protect access; config toggles for public vs. protected links.
- Basic SSO for the UI (SAML or OIDC), including minimal role mapping (viewer/admin) and per-alert access control options.
- Metrics providers: interface for Prometheus first.
DoD
- [ ] Cloud LLM provider works end-to-end via config toggle alongside local dev provider.
- [ ] Alert deep-link renders triage page end-to-end from a notification link.
- [ ] Alertmanager template snippet documented and covered by an example test.
- [ ] Signed link/token option implemented and tested.
- [ ] SSO login flow works with a sample IdP (metadata/issuer), with configuration docs and a smoke test.
- [ ] Metrics snapshot retrieval used in analysis flow.

0.4 – Intelligence and accuracy
Goals

- Modular analysis pipeline (context gatherer → reasoner → recommender).
- Runbook ingestion and light retrieval for grounding.
- Prompt templating/versioning with tests.
- Evaluation harness (golden cases to prevent regressions).
DoD
- [ ] Pipeline modules unit-tested and composable.
- [ ] Runbooks can be mounted/referenced; evaluated in prompts.
- [ ] Golden tests run in CI with pass/fail gates.

0.5 – UX and workflow
Goals

- Web UI polish: show status, inspected resources, recommendations + confidence; quick access to copy/share the alert link.
- Link-first flow: from Alertmanager message link to triage page with clear recommended actions.
- Incident timeline summaries and resolution notes.
DoD
- [ ] UI reflects analysis steps and outputs clearly; alert links are copyable from the UI.
- [ ] End-to-end link-first flow documented with setup steps.
- [ ] Slack interactions create/update an incident thread.

0.6 – Safety and controlled remediation
Goals

- Safe execution framework with whitelisted actions, dry-run by default.
- Policy layer per cluster/namespace/team.
- Audit trail of inputs, reasoning, recommendations, and approvals.
DoD
- [ ] Actions require explicit approval; audited with immutable logs.
- [ ] Policies enforced and test-covered.

0.7 – Performance and cost
Goals

- Batch/stream K8s data gathering.
- Cost-aware LLM usage (compression, tiered models, token accounting).
- Benchmarks for common scenarios.
DoD
- [ ] Benchmarks documented; CI job reports trends.

0.8 – Extensibility and plugin system
Goals

- Plugin interface for data sources, responders, and tools.
- Example community plugins to serve as templates.
DoD
- [ ] Plugins can be registered via config and discovered dynamically.

0.9 – Security and compliance
Goals

- Secrets management best practices; never log secrets.
- K8s RBAC least privilege examples.
- Supply chain hardening (pinned deps, SBOM, image scanning).
- Multi-tenant isolation considerations.
DoD
- [ ] Security checks run in CI; base images and deps pinned.

1.0 – GA readiness
Goals

- Stable APIs and documented migration path.
- Backward-compatible config; deprecation policy.
- Documentation and examples polished; reference architectures.
DoD
- [ ] Semantic versioning in place; release notes and upgrade guides.

Quality gates

- CI: lint, type-check, tests, security scans on PRs; build/publish images on tags.
- Test coverage report and status comment on PRs.
- Pre-commit hooks for formatting and static analysis.
- Nightly e2e against a kind cluster using example alerts.

Governance

- Code of Conduct and Maintainers guide (WIP).
- Triage rotations and SLA for issues/PRs.
- Roadmap tracked via milestones; changes proposed via RFC + issues.

How to propose roadmap changes

- Open an issue labeled roadmap with a concise problem statement, motivation, and acceptance criteria.
- For cross-cutting or security-impacting changes, start with an RFC and ping maintainers for async review.
