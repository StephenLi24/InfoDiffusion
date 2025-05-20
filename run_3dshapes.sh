#!/bin/bash
export CUDA_VISIBLE_DEVICES=2
python run.py --model diff --mode train --mmd_weight 0.01 --a_dim 32 --epochs 50 --dataset 3dshapes --batch_size 64 --save_epochs 2 --deterministic --prior regular --r_seed 64 --data_dir /data/3dshapes.npz
