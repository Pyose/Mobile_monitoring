import torch
from PIL import Image
from torchvision.transforms import functional as F
import os

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, image_dir, label_data):
        self.image_dir = image_dir
        self.label_data = label_data
        self.image_paths = sorted(os.listdir(image_dir))

    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.image_paths[idx])
        boxes, labels = self.label_data[idx]
        return transform_image(image_path, boxes, labels)

    def __len__(self):
        return len(self.image_paths)

def transform_image(image_path, boxes, labels):
    image = Image.open(image_path).convert("RGB")
    image = F.to_tensor(image)
    target = {'boxes': torch.tensor(boxes, dtype=torch.float32), 'labels': torch.tensor(labels, dtype=torch.int64)}
    return image, target
