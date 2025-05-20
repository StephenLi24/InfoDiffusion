#!/bin/bash
export CUDA_VISIBLE_DEVICES=3
python run.py --model diff --mode train --mmd_weight 0.01 --a_dim 32 --epochs 50 --dataset dsprites --batch_size 32 --save_epochs 2 --deterministic --prior regular --r_seed 64 --data_dir /data/
