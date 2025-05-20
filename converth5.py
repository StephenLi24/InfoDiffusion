import os
import h5py
import numpy as np

# 路径设置
h5_file_path = "/data/3dshapes.h5"   # HDF5 数据集文件路径
output_file = "/data/3dshapes.npz"  # 输出文件路径

# 打开 HDF5 文件并读取数据
with h5py.File(h5_file_path, 'r') as h5_file:
    images = h5_file['images'][:]  # 假设图像数据存储在 "images" 键下
    labels = h5_file['labels'][:]  # 假设标签数据存储在 "labels" 键下

# 以字典形式保存数据
data_dict = {"images": images, "labels": labels}
np.savez_compressed(output_file, **data_dict)

print("图像和标签数据已以字典形式保存在一个文件中!")
