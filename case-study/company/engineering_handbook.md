# Nebula Financial Engineering Handbook

## Engineering Philosophy

At Nebula, we believe that great software is built by empowered teams. We don't have a separate QA department or an Ops team that deploys your code.

**"You Build It, You Run It."**

This means developers are responsible for the entire lifecycle of their services: design, development, testing, deployment, and monitoring.

## Our Tech Stack

### Backend
- **Data Processing**: Python for data science pipelines, risk analysis, and ledger reconciliation.
- **Legacy**: A strict subset of Node.js services are being deprecated and migrated to Go.

### Frontend
- **Web**: React, TypeScript, Next.js.
- **Mobile**: React Native for iOS and Android.

### Infrastructure & DevOps
- **Cloud Provider**: AWS (exclusively).
- **Orchestration**: Kubernetes (EKS). Experience with Istio service mesh is highly valued.
- **IaC**: Terraform for everything. No ClickOps allowed.
- **CI/CD**: GitHub Actions.
- **Observability**: Datadog (APM, Logs), Prometheus/Grafana.

## Code Quality Standards

1. **Testing**: absolute minimum of 80% unit test coverage. Integration tests required for all API endpoints.
2. **Code Review**: All PRs need 2 approvals. "LGTM" is not a review.
3. **Documentation**: RFCs (Request for Comments) are required for any architectural change.

## On-Call

We practice a shared on-call rotation. Because you run what you build, you are incentivized to build stable, self-healing systems. We value sleep, so we invest heavily in automation to prevent paging at 3 AM.
