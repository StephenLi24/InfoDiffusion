#!/bin/bash
export CUDA_VISIBLE_DEVICES=2
python run.py --model diff --mode save_latent --a_dim 32 --mmd_weight 0.1 --epochs 50 --dataset 3dshapes --sampling_number 16 --deterministic --prior regular --r_seed 64 --data_dir /data/3dshapes.h5