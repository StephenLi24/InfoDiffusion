#!/bin/bash
export CUDA_VISIBLE_DEVICES=1
python run.py --model opt_diff --mode disentangle --img_id 0 --mmd_weight 0.01 --a_dim 32 --epochs 40 --dataset celeba --deterministic --prior regular --r_seed 64 --data_dir /data/CelebA/
