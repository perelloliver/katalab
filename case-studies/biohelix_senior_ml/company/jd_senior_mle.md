# Senior Machine Learning Engineer (Platform & Inference)

**Location**: Boston, MA (Hybrid) or Remote (UTC +/- 3)
**Salary Range**: $180,000 - $240,000 + Equity + Benefits
**Department**: Platform Engineering

## The Opportunity

At BioHelix, we aren't just serving ads or recommending movies. We are designing proteins that will save lives.
Our Research team (mostly PhDs from DeepMind, Broad Institute, ETH) creates state-of-the-art models. But a model in a Jupyter Notebook is potential energy. We need you to turn it into kinetic energy.

We are looking for a **Senior Machine Learning Engineer** to join our Platform Team. You will be the architect who takes a 50GB model that requires 2 weeks to run on a cluster and turns it into a scalable, fault-tolerant inference service that completes in milliseconds.

## What You'll Build
- **HelixServe**: Our internal model serving platform. You will wrap complex PyTorch models (Transformers, Equivariant GNNs) into high-performance gRPC/HTTP APIs.
- **The "Model-to-Metal" Pipeline**: Automate the journey from a researcher's commit to a deployed model on our Kubernetes cluster, including automated quantization, TensorRT optimization, and regression testing.
- **Reproducibility Engine**: Build the system that guarantees every prediction can be traced back to the exact code, data commit (DVC), and random seed used to generate it.

## Who You Are
- **You are a Polyglot**: You speak "Research" (PyTorch, Einsums, Gradient Checkpointing) and "Production" (Docker, Kubernetes, Terraform, gRPC).
- **You hate "Works on my Machine"**: You obsess over deterministic builds, hermetic environments, and CI/CD.
- **You are an Optimizer**: You know how to profile a slow model, spot the bottleneck (CPU? GPU memory bandwidth? Python GIL?), and fix it (maybe writing a custom CUDA kernel or just optimizing the dataloader).

## Requirements
- 5+ years of software engineering experience, with at least 2 years in MLOps or MLE roles.
- Deep proficiency in **Python** (not just scripting, but building packages).
- Experience deploying ML models on **Kubernetes** (KServe, Seldon, or custom wrappers).
- Familiarity with **MLflow**, **Weights & Biases**, or similar experiment tracking tools.
- Understanding of distributed training (DDP, FSDP) is a huge plus.

## Creating the "Perfect" Team
You will be joining a team of 6 engineers and working directly with 15 researchers. 
- **The Gap we need to fill**: Our researchers write brilliant but "messy" code. We don't want to stop them from innovating, but we need you to build the guardrails that prevent that mess from breaking production.

## Benefits
- **Health**: 100% covered Medical, Dental, Vision.
- **Time**: Unlimited PTO (with a mandatory 3-week minimum).
- **Equity**: Significant early-stage stock options.
- **Gear**: Top-spec MacBook Pro + budget for your home office.
- **Science**: Weekly "Journal Clubs" where we discuss the latest papers in GenBio.
