from torch.utils.data import Dataset, DataLoader
from PIL import Image


"""

"""


class CustomImageDataset(Dataset):
    def __init__(self, image_paths, label_paths):
        self.image_paths = image_paths
        self.label_paths = label_paths

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx])
        label = Image.open(self.label_paths[idx])
        return image, label


image_paths = ['./data/img1.png', './data/img2.png', ...]
label_paths = ['./data/label1.png', './data/label2.png', ...]

dataset = CustomImageDataset(image_paths=image_paths, label_paths=label_paths)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)





