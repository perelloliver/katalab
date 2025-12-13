# Team Profile: Core Ledger Team

## Overview
The Core Ledger Team is the heart of Nebula Financial. We manage the systems of record that track every penny (and satoshi) of user funds. We are responsible for the consistency, durability, and availability of the financial ledger.

## Team Composition (Current: 5 Members)

### 1. Alex Vasiliev (Lead Engineer)
- **Role**: Tech Lead / Architect
- **Background**: Ex-HFT (High Frequency Trading). 15+ years exp.
- **Strengths**: Distributed systems, fierce code reviewer, system performance.
- **Weakness**: Currently the bottleneck for all architectural decisions. "Bus factor" of 1.

### 2. Priya Patel (Senior Backend)
- **Role**: Senior Engineer (Focus: Payment Rails)
- **Background**: 5 years at Nebula. Node.js expert.
- **Strengths**: Deep domain knowledge of banking APIs (SEPA, Swift).
- **Gaps**: Struggling to adapt to the new Go microservices patterns; prefers the old monolith.

### 3. Marcus Thorne (Backend Engineer)
- **Role**: Backend Engineer
- **Background**: 3 years exp. Hired 6 months ago.
- **Strengths**: Strong Go developer, very productive.
- **Gaps**: Lacks intuition for financial consistency (sometimes sacrifices safety for speed).

### 4. David Kim (Junior Engineer)
- **Role**: Junior Backend
- **Background**: Bootcamp grad, 1 year exp.
- **Strengths**: Eager learner, great at frontend/internal tools.
- **Gaps**: Needs significant mentoring on backend best practices and testing.

### 5. *OPEN ROLE* (Job Description: Senior Backend Engineer)
- **Target Profile**: Experienced engineer to take load off Alex and mentor David.

## Why We Are Hiring
The team is at a tipping point. The migration from our legacy Node.js monolith to the new Go distributed ledger is stalled.
- **Alex** is too busy fighting fires to drive the migration.
- **Priya** is hesitant to lead the Go transition.
- **Marcus** builds fast but breaks things.

We need a **Senior Engineer** who can:
1.  **Bridge the gap**: Bring strong consistency/database skills to stabilize the new system.
2.  **Unblock Alex**: Take ownership of the "Ledger v2" design.
3.  **Mentor**: Help David grow and model best practices for Marcus.

## Team Culture
- **High Pressure**: We move billions. Mistakes are expensive.
- **Direct Feedback**: Code reviews can be blunt.
- **Async First**: We try to minimize meetings, but currently, we are over-indexing on "War Room" syncs due to stability issues.
## Key Projects & Achievements
- **Ledger v2 Migration**: Spearheaded the migration from legacy Node.js monolith to a new Go-based distributed ledger system, enhancing scalability and fault tolerance.
- **Real-time Transaction Processing**: Developed and deployed a low-latency system for processing millions of transactions per second, ensuring immediate fund availability.
- **Multi-currency Support**: Implemented robust infrastructure to support various fiat and cryptocurrencies, including complex FX and settlement logic.
- **Audit & Compliance Reporting**: Built automated reporting tools to meet stringent financial regulations (e.g., SOC 2, GDPR), ensuring data integrity and traceability.

## Team Philosophy
Our philosophy is built on a foundation of **precision, resilience, and continuous improvement**.
- **Ownership & Accountability**: Every team member takes full ownership of their work, from design to deployment and monitoring. We are accountable for the financial integrity of our systems.
- **Security & Consistency First**: We prioritize security and data consistency above all else. Speed is important, but never at the expense of correctness or safety.
- **Proactive Problem Solving**: We anticipate potential issues and design systems to be fault-tolerant and self-healing. We learn from incidents and implement preventative measures.
- **Knowledge Sharing & Mentorship**: We foster an environment where knowledge is openly shared, and senior engineers actively mentor junior members, elevating the collective skill set.
- **Data-Driven Decisions**: We rely on metrics and data to inform our architectural choices and operational strategies, ensuring our solutions are effective and efficient.

## Software Development Best Practices
- **Test-Driven Development (TDD)**: Writing tests before code to ensure correctness and facilitate refactoring.
- **Continuous Integration/Continuous Deployment (CI/CD)**: Automating build, test, and deployment processes to ensure rapid and reliable releases.
- **Immutable Infrastructure**: Treating servers and deployments as disposable components that are rebuilt rather than modified in place.
- **Observability**: Implementing comprehensive logging, metrics, and tracing to understand system behavior in production.
- **Defensive Programming**: Writing code that anticipates and handles potential errors, invalid inputs, and edge cases gracefully.

