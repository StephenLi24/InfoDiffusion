#!/bin/bash
export CUDA_VISIBLE_DEVICES=3
python run.py --model opt_diff --mode save_latent --is_bottleneck --a_dim 32 --mmd_weight 0.01 --epochs 40 --dataset celeba --sampling_number 16 --deterministic --prior regular --r_seed 64 --data_dir /data/CelebA/