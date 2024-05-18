from torch.utils.data import Dataset, DataLoader

class OCRDataset(Dataset):
    def __init__(self, signs, binarized_signs, labels, transform=None):
        self.signs = signs
        self.binarized_signs = binarized_signs
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.signs)