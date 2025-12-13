# Team Structure & Dynamics

BioHelix operates with a "Two-Team" model. The friction between these two groups is the primary bottleneck we are solving for.

## 1. The Discovery Team (Research)
**Mission**: "Publish or Perish (until it works)."
**Size**: 12 Researchers (10 PhDs).
**Key Personas**:
- **Prof. Elena Rossini (Head of Discovery)**: Brilliant visionary. Believes engineering constraints stifle creativity. Hates "processes".
- **Dr. Klaus Weber (Senior Biophysicist)**: World expert in protein folding. Writes 5,000-line Fortran scripts that no one else can read. Refuses to use Git ("Dropbox is fine").
- **Sarah Jenkins (Junior Researcher)**: Fresh PhD. Uses PyTorch Lightning. Wants to write better code but is pressured to "just get the plot" by next week.

**The Anti-Pattern**:
Discovery treats code as a "throwaway artifact" produced to generate a PDF figure. Once the paper is accepted, the code is abandoned.

## 2. The Platform Team (Engineering)
**Mission**: "Stability at Scale."
**Size**: 6 Engineers.
**Key Personas**:
- **Mark Chen (Head of Platform)**: Ex-Google SRE. Obsessed with uptime. Has a "Wall of Shame" for broken builds. Desperately trying to impose order.
- **Benji (DevOps Lead)**: The "Bus Factor" of 1. He is the only person who knows how the Slurm cluster actually talks to the Kubernetes cluster. If he gets hit by a bus, the company stops.
- **Priya (Data Eng)**: Spends 90% of her time cleaning up "CSV files with random columns" handed over by Discovery.

## 3. The "Missing Link" (Your Role)
We have a massive gap in the middle.
- **Discovery** throws "math" over the wall.
- **Platform** catches "fire".

We need a Senior MLE who can sit in the DMZ (Demilitarized Zone).
- You will translate Klaus's Fortran into CUDA.
- You will teach Sarah how to use Docker.
- You will negotiate with Elena to define a "Model Handover Contract" (input schemas, expected latency, artifact location).

## 4. Current Team Rituals
- **"The Clash" (Bi-weekly Sync)**: Research presents new models. Engineering points out why they won't scale. Usually ends in an argument about "premature optimization".
- **"Demo Day" (Fridays)**: The one time everyone gets along. Beer and demos of new protein visualizations.
