#!/bin/bash
export CUDA_VISIBLE_DEVICES=1

for model in opt_diff diff; do
    for img_id in {2..10}; do
        echo "Running ${model} model with img_id=${img_id}"
        python run.py --model $model \
                      --mode disentangle \
                      --img_id $img_id \
                      --mmd_weight 0.01 \
                      --a_dim 32 \
                      --epochs 40 \
                      --dataset celeba \
                      --deterministic \
                      --prior regular \
                      --r_seed 64 \
                      --data_dir /data/CelebA/
        echo "Completed ${model} @ ${img_id}"
        echo "------------------------------"
    done
done