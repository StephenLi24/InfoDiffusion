import os
import torch
import torch.utils
import torch.utils.data
import torchvision
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
import h5py

class Crop:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __call__(self, img):
        return torchvision.transforms.crop(img, self.x1, self.y1, self.x2 - self.x1,
                                           self.y2 - self.y1)

    def __repr__(self):
        return self.__class__.__name__ + "(x1={}, x2={}, y1={}, y2={})".format(
            self.x1, self.x2, self.y1, self.y2)


def d2c_crop():
    # from D2C paper for CelebA dataset.
    cx = 89
    cy = 121
    x1 = cy - 64
    x2 = cy + 64
    y1 = cx - 64
    y2 = cx + 64
    return Crop(x1, x2, y1, y2)


class CustomTensorDataset(Dataset):
    def __init__(self, data, latents_values, latents_classes):
        self.data = data
        self.latents_values = latents_values
        self.latents_classes = latents_classes

    def __getitem__(self, index):
        return (torch.from_numpy(self.data[index]).float(), 
                torch.from_numpy(self.latents_values[index]).float(), 
                torch.from_numpy(self.latents_classes[index]).int())

    def __len__(self):
        return self.data.shape[0]

class Shapes3D(Dataset):
    """
    读取 h5py 格式的 3DShapes 数据集，同时返回图像和标签信息。
    假设 h5 文件中包含两个数据集：'images' 和 'labels'。
    """
    def __init__(self,
                 path,
                 transform = None,
                 original_resolution=64,
                 split=None,
                 as_tensor: bool = True,
                 do_normalize: bool = True,
                 **kwargs):
        self.original_resolution = original_resolution
        
        # 读取 h5 文件数据
        # h5_path = os.path.join(path, '3dshapes.h5')
        # self.h5_file = h5py.File(path, 'r')
        self.data_dict = np.load(path)
        self.data = self.data_dict['images']  # 假设数据集名称为 "images"
        self.labels = self.data_dict['labels']  # 假设标签名称为 "labels"
        self.length = self.data.shape[0]
        self.transform = transform
        if split is None:
            self.offset = 0
        else:
            raise NotImplementedError("Split other than None is not implemented yet.")

        transform = []
        if as_tensor:
            transform.append(torchvision.transforms.ToTensor())
        if do_normalize:
            transform.append(
                torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)))
        self.transform = torchvision.transforms.Compose(transform)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        assert index < self.length
        index = index + self.offset
        # 读取图像及标签（注意：h5py 数据集一般会返回 numpy 数组）
        img = self.data[index]
        label = self.labels[index]
        # 如果需要可以转换数据类型，如 uint8 -> float，取决于数据存储格式
        if self.transform is not None:
            # img = self.transform(img).permute(1, 2, 0)
            img = self.transform(img)
        return [img, label]
    
    
class CustomImageFolder(ImageFolder):
    def __init__(self, root, transform=None):
        super(CustomImageFolder, self).__init__(root, transform)

    def __getitem__(self, index):
        path = self.imgs[index][0]
        img = self.loader(path)
        if self.transform is not None:
            img = self.transform(img)

        return img


def get_dataset_config(args):
    if args.dataset == 'fmnist':
        args.input_channels = 1
        args.unets_channels = 32
        args.encoder_channels = 32
        args.input_size = 32
    elif args.dataset == 'mnist':
        args.input_channels = 1
        args.unets_channels = 32
        args.encoder_channels = 32
        args.input_size = 32
    elif args.dataset == 'dsprites':
        args.input_channels = 1
        args.unets_channels = 32
        args.encoder_channels = 32
        args.input_size = 64
    elif args.dataset == 'celeba':
        args.input_channels = 3
        args.unets_channels = 64
        args.encoder_channels = 64
        args.input_size = 64
    elif args.dataset == 'cifar10':
        args.input_channels = 3
        args.unets_channels = 64
        args.encoder_channels = 64
        args.input_size = 32
    elif args.dataset == 'chairs':
        args.input_channels = 3
        args.unets_channels = 32
        args.encoder_channels = 32
        args.input_size = 64
    elif args.dataset == 'ffhq':
        args.input_channels = 3
        args.unets_channels = 64
        args.encoder_channels = 64
        args.input_size = 64
    elif args.dataset == '3dshapes':
        args.input_channels = 3
        args.unets_channels = 64
        args.encoder_channels = 64
        args.input_size = 64
    shape = (args.input_channels, args.input_size, args.input_size)

    return shape


def get_dataset(args):
    if args.dataset == 'fmnist':
        return get_fmnist(args)
    elif args.dataset == 'mnist':
        return get_mnist(args)
    elif args.dataset == 'celeba':
        return get_celeba(args)
    elif args.dataset == 'cifar10':
        return get_cifar10(args)
    elif args.dataset == 'dsprites':
        return get_dsprites(args)
    elif args.dataset == 'chairs':
        return get_chairs(args)
    elif args.dataset == 'ffhq':
        return get_ffhq(args)
    elif args.dataset == '3dshapes':
        return get_3dshapes(args)


def get_mnist(args):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((args.input_size, args.input_size)),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Lambda(lambda t: (t * 2) - 1),
    ])

    dataset = torchvision.datasets.MNIST(root = args.data_dir, train=True, download=True, transform = transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size = args.batch_size, drop_last = True, num_workers = 4)

    return dataloader


def get_fmnist(args):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((args.input_size, args.input_size)),
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Lambda(lambda t: (t * 2) - 1),
    ])

    dataset = torchvision.datasets.FashionMNIST(root = args.data_dir, train=True, download=True, transform = transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size = args.batch_size, drop_last = True, num_workers = 4)

    return dataloader


def get_celeba(args,
               as_tensor: bool = True,
               do_augment: bool = True,
               do_normalize: bool = True,
               crop_d2c: bool = False):
    if crop_d2c:
        transform = [
            d2c_crop(),
            torchvision.transforms.Resize(args.input_size),
        ]
    else:
        transform = [
            torchvision.transforms.Resize(args.input_size),
            torchvision.transforms.CenterCrop(args.input_size),
        ]

    if do_augment:
        transform.append(torchvision.transforms.RandomHorizontalFlip())
    if as_tensor:
        transform.append(torchvision.transforms.ToTensor())
    if do_normalize:
        transform.append(
            torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)))
    transform = torchvision.transforms.Compose(transform)

    if args.mode in ['attr_classification', 'eval_fid', 'reconstruction']:
        train_set = torchvision.datasets.CelebA(root = args.data_dir, split = "train", download = True, transform = transform)
        valid_set = torchvision.datasets.CelebA(root = args.data_dir, split = "valid", download = True, transform = transform)
        test_set = torchvision.datasets.CelebA(root = args.data_dir, split = "test", download = True, transform = transform)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size = args.batch_size, drop_last = True, shuffle = True, num_workers = 4)
        valid_loader = torch.utils.data.DataLoader(valid_set, batch_size = args.batch_size, drop_last = True, shuffle = True, num_workers = 4)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size = args.batch_size, drop_last = True, shuffle = True, num_workers = 4)
        return (train_loader, valid_loader, test_loader)
    else:
        dataset = torchvision.datasets.CelebA(root = args.data_dir, split = "train", download = True, transform = transform)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size = args.batch_size, drop_last = True, shuffle = False, num_workers = 4)

        return dataloader


def get_cifar10(args):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    dataset = torchvision.datasets.CIFAR10(root = args.data_dir, train = True, download = True, transform = transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size = args.batch_size, drop_last = True, shuffle = True, num_workers = 4)
    return dataloader


def get_dsprites(args):
    root = os.path.join(args.data_dir+'/dsprites/dsprites_ndarray_co1sh3sc6or40x32y32_64x64.npz')
    file = np.load(root, encoding='latin1')
    data = file['imgs'][:, np.newaxis, :, :]
    latents_values = file['latents_values']
    latents_classes = file['latents_classes']
    train_kwargs = {'data':data, 'latents_values':latents_values, 'latents_classes':latents_classes}
    dset = CustomTensorDataset
    dataset = dset(**train_kwargs)

    dataloader = DataLoader(dataset,
                            batch_size=args.batch_size,
                            shuffle=True,
                            num_workers=4,
                            pin_memory=True,
                            drop_last=True)

    return dataloader


def get_chairs(args):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((args.input_size, args.input_size)),
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    dataset = CustomImageFolder(root = args.data_dir+'/3DChairs', transform = transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size = args.batch_size, drop_last = True, shuffle = True, num_workers = 4)
    return dataloader


def get_ffhq(args):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((args.input_size, args.input_size)),
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    dataset = CustomImageFolder(root = args.data_dir+'/ffhq', transform = transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size = args.batch_size, drop_last = True, shuffle = False, num_workers = 4)
    return dataloader

# def get_3dshapes(args):
#     h5_file_path = args.data_dir
#     # dataset = h5py.File(h5_file_path, 'r')
#      # 数据增强
#     transform = torchvision.transforms.Compose([
#         torchvision.transforms.Resize((args.input_size, args.input_size)),
#         torchvision.transforms.RandomHorizontalFlip(),
#         torchvision.transforms.ToTensor(),
#         torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
#     ])

#     # 创建 Dataset 和 DataLoader
#     dataset = Shapes3DDataset(h5_file_path, transform=transform)
#     dataloader = DataLoader(dataset, batch_size=args.batch_size, drop_last=True, shuffle=True, num_workers=4)
#     return dataloader

# # 定义 Dataset 类
# class Shapes3DDataset(Dataset):
#     def __init__(self, h5_file_path, transform=None):
#         self.dataset = h5py.File(h5_file_path, 'r')
#         self.images = self.dataset['images']  # (480000, 64, 64, 3)
#         self.labels = self.dataset['labels']  # (480000, 6)
#         # self.transform = transform

#         # 定义标签因子名称（与 CelebA 类似）
#         self.y_names = ['floor_hue', 'wall_hue', 'object_hue', 'scale', 'shape', 'orientation']

#     def __len__(self):
#         return self.labels.shape[0]  # 480,000

#     def __getitem__(self, idx):
#         # 读取图像并归一化
#         image = self.images[idx].astype(np.float32) / 255.0  # 归一化到 [0, 1]
#         image = torch.from_numpy(image).permute(2, 0, 1)     # (3, 64, 64)

#         # 保留原始标签，类型转换为 int64
#         labels = torch.tensor(self.labels[idx], dtype=torch.int64)  # (6,)
#         return image, labels


def get_3dshapes(args):
    file_path = args.data_dir
    # Data augmentation
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((args.input_size, args.input_size)),
        torchvision.transforms.RandomHorizontalFlip(),
        torchvision.transforms.ToTensor(),  # Handle ToTensor here
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    # dataset_1 = h5py.File('/data/3dshapes.npz', 'r')
    # images = dataset_1['images']  # array shape [480000,64,64,3], uint8 in range(256)
    # labels = dataset_1['labels']  # array shape [480000,6], float64
    # image_shape = images.shape[1:]  # [64,64,3]
    # Create Dataset and DataLoader
    dataset = Shapes3D(file_path,transform= transform)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, drop_last=True, shuffle=True, num_workers=4)
    return dataloader