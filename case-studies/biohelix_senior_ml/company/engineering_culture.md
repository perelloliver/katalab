# Engineering Culture & Standards

At BioHelix, we are building a **Science Factory**. A factory needs standard operating procedures, strict tolerances, and safety checks.

## 1. The "Three Stages of Maturity" Protocol
We don't expect research code to be perfect from day one. We follow a strict graduation process:

| Stage | Allowed Environment | Allowed Practices | Deployment Target |
| :--- | :--- | :--- | :--- |
| **Stage 1 (Sandbox)** | JupyterHub, Local Laptop | Hardcoded paths, no tests, `print()` debugging. | `paper_figures` folder. |
| **Stage 2 (Refinement)** | Dev Cluster | `.py` modules required. `poetry` for deps. Basic Unit Tests. | Internal Demo App. |
| **Stage 3 (Production)** | Prod Kubernetes | Fully Dockerized. CI/CD verified. 90% Code Coverage. Typed Python (`MyPy`). | **HelixServe** (Client Facing). |

**Your Job**: Move models from Stage 1 to Stage 3.

## 2. Our "Golden Path" Stack
We provide paved roads. If you go off-road, you are on your own.
- **Language**: Python 3.10+ (Type Hints Mandatory for Prod).
- **Dependency Mgmt**: Poetry (Conda is banned in CI/CD).
- **Linting**: `ruff` (we are strict). Pre-commit hooks are mandatory.
- **Containerization**: Distroless Docker images.
- **Orchestration**:
    - Training: Slurm (on-prem GPU cluster).
    - Inference: Kubernetes (EKS).

## 3. Rituals & Practices
- **RFCs (Request for Comments)**: No architectural change happens without a written document. "Talk is cheap, show me the design doc."
- **Blameless Post-Mortems**: When a model crashes in prod (and it will), we don't ask "Who broke it?", we ask "Why did the system allow it to break?".
- **The "Scout Rule"**: Leave the codebase cleaner than you found it. If you touch a legacy script, you add type hints to it.

## 4. The "Code Review" Bar
We are tough on code reviews.
- **Research Code**: Reviewed for *correctness* (does the math match the paper?).
- **Production Code**: Reviewed for *robustness* (error handling, types, logging, efficiency).
- **Blocking**: You cannot merge to `main` without 1 approval from a Domain Expert (Scientist) AND 1 approval from a Platform Engineer.
