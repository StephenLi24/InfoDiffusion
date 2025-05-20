#!/bin/bash
python eval_disentanglement.py --model opt_diff --a_dim 32 --mmd_weight 0.01 --epochs 30 --dataset celeba --sampling_number 16 --deterministic --prior regular --r_seed 64 --mode eval
