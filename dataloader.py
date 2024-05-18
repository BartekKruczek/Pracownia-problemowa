from utils import Utils
from torch.utils.data import Dataset

class OCRDataset(Dataset):
    def __init__(self, signs, binarized_signs, labels, transform=None):
        self.signs = signs
        self.binarized_signs = binarized_signs
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.signs)
    
    def __repr__(self) -> str:
        return "Klasa stworzona do obsługi zbioru danych dla modelu OCR, własny dataset"
    
    def __getitem__(self, idx):
        sign = self.signs[idx]
        binarized_sign = self.binarized_signs[idx]
        label = self.labels[idx]

        # Dekodowanie obrazu
        image = Utils.decode_image_from_binarized(binarized_sign)

        # if transform implemented, default is None
        if self.transform:
            image = self.transform(image)

        return image, label