import os
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image


"""
Creates the data loader, which contains batches 
"""


class CustomImageDataset(Dataset):
    def __init__(self, image_paths, label_paths, transform=None):
        self.image_paths = image_paths
        self.label_paths = label_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx])
        label = Image.open(self.label_paths[idx])
        if self.transform:
            image = self.transform(image)
            label = self.transform(label)
        return image, label


def dataloader():
    img_base = "C:\\Users\\valai\\PycharmProjects\\plantDetection\\images\\images\\"
    lbl_base = "C:\\Users\\valai\\PycharmProjects\\plantDetection\\images\\labels\\"
    image_paths = [img_base + i for i in os.listdir(img_base)]
    label_paths = [lbl_base + i for i in os.listdir(lbl_base)]

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    dataset = CustomImageDataset(image_paths=image_paths, label_paths=label_paths, transform=transform)
    data_loader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=4)
    return data_loader



# for testing
def main():
    data = dataloader()
    for images, labels in data:
        print(images.size)
        print(labels.size)
        print("")


if __name__ == '__main__':
    main()

