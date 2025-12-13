# BioHelix: Company Handbook

> **"Decoding Biology. Designing the Future."**

## 1. Who We Are
BioHelix is a Series B biotechnology company headquartered in Basel, Switzerland, with a compute hub in Boston, MA. We are pioneering the field of **Generative Biology**. Instead of discovering drugs by accident, we design them by intent, using massive-scale deep learning models trained on the largest proprietary protein dataset in the world.

## 2. Our 10-Year Vision
To cure 50 rare genetic diseases by 2035.
We believe that the future of medicine is programmable. By 2030, we aim to have the first end-to-end AI-designed biologic drug approved by the FDA, with zero human intervention in the design phase.

## 3. Our Products & Platform

### **HelixFold™ Engine**
Our core technology. A proprietary geometric deep learning model that predicts protein-ligand binding affinity with 99.8% accuracy, surpassing AlphaFold 2 benchmarks on our internal "hard targets" dataset.
- **Tech**: Custom PyTorch kernels, Equivariant GNNs, trained on 1024 A100 GPUs.
- **capabilities**: De novo protein hallucination, side-chain packing optimization.

### **LabOS**
The software that runs our robotic wet lab.
- **Function**: Automatically takes high-confidence candidates from HelixFold, instructs liquid handling robots to synthesize them, and pipes assay results back into the training set.
- **Closed Loop**: The "Active Learning" cycle allows our models to learn from their own failures in real-time.

## 4. Key Partnerships & Clients

### **Pharma Giants**
- **Novartis**: $50M strategic partnership to hunt for Alzheimer's targets using HelixFold.
- **Roche**: Multi-year collaboration to design novel antibody therapies for oncology.

### **Academic Alliances**
- **ETH Zurich & EPFL**: We fund 3 PhD positions annually and sponsor the "BioHelix Chair for Computational Biology".

## 5. Strategic Goals (FY 2026)

### **Goal 1: "The Great Un-Bottlenecking"**
- **Current State**: Our scientists can only run 5 experiments a week because they are blocked by manual infrastructure tasks.
- **Objective**: Automate the inference pipeline so scientists can run 100 experiments a week. 
- **Owner**: Platform Engineering Team.

### **Goal 2: Indication 001 to Clinical Trials**
- **Objective**: Get our lead candidate for Cystic Fibrosis (BHX-001) IND-approved for Phase I trials.
- **Requirement**: Full data lineage and audit trails for every line of code that touched BHX-001.

## 6. Investors
Backed by **Sequoia**, **Andreessen Horowitz (Bio + Health)**, and **GV**. Raised $85M to date.
