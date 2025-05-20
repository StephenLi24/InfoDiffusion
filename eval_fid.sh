#!/bin/bash
export CUDA_VISIBLE_DEVICES=1

# learned latent
# python run.py --model diff --mode train --mmd_weight 0.1 --a_dim 256 --epochs 50 --dataset celeba --batch_size 32 --save_epochs 5 --deterministic --prior regular --r_seed 64 

# python run.py --model diff --mode save_latent --mmd_weight 0.01 --a_dim 32 --epochs 50 --dataset celeba --deterministic --prior regular --r_seed 64 --data_dir /data/CelebA/

python run.py --model opt_diff --mode train_latent_ddim --a_dim 32 --epochs 40 --mmd_weight 0.01 --dataset celeba --deterministic --save_epoch 10 --prior regular --r_seed 64 --data_dir /data/CelebA/ --batch_size 32

python run.py --model opt_diff --mode eval_fid --split_step 500 --a_dim 32 --batch_size 32 --mmd_weight 0.01 --sampling_number 10000 --epochs 40 --dataset celeba --is_latent --prior regular --r_seed 64 --data_dir /data/CelebA/

# without learned latent
# python run.py --model diff --mode train --mmd_weight 0.1 --a_dim 256 --epochs 50 --dataset celeba --batch_size 32 --save_epochs 5 --deterministic --prior regular --r_seed 64 

# python run.py --model vanilla --mode train --a_dim 256 --epochs 50 --dataset celeba --batch_size 128 --save_epochs 10 --prior regular --r_seed 64

# python run.py --model diff --mode eval_fid --split_step 500 --a_dim 256 --batch_size 256 --mmd_weight 0.01 --sampling_number 10000 --epochs 50 --dataset celeba --prior regular --r_seed 64