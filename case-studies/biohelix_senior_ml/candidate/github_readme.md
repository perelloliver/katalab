# ProteinGNN-v2

Implementation of "Equivariant Graph Networks for Molecular Docking" (NeurIPS 2023).

## Usage
To reproduce the results like in Table 2:

1. Download the PDBBind dataset and unzip it to `C:\Users\Sofia\Desktop\Data\pdbbind_v2020`.
2. Run the training script:
```bash
python3 main_v2_final_final.py --gpu 0 --epochs 500
```
3. To evaluate:
```bash
python3 evaluate.py --model_path ./checkpoints/best_model_run3_fixed.pt
```

## Dependencies
- torch==1.9.0 (PLEASE DO NOT UPDATE, it breaks the custom kernel)
- numpy
- pandas
- scipy
- rdkit

## Note
The custom CUDA kernel for the equivariant convolution is in the `clean_ops` folder. You might need to compile it manually using `nvcc`. I included a `compile.sh` but it is hardcoded for the ETH cluster paths.
