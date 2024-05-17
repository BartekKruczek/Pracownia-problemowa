import torch

class OCRModel(torch.nn.Module):
    def __init__(self) -> torch.nn.Module:
        super(OCRModel, self).__init__()
        self.conv1 = torch.nn.Conv2d(None, 26, 26, 32)
        self.maxpool1 = torch.nn.MaxPool2d(None, 13, 13, 32)
        self.conv2 = torch.nn.Conv2d(None, 13, 13, 64)
        self.maxpool2 = torch.nn.MaxPool2d(None, 6, 6, 64)
        self.conv3 = torch.nn.Conv2d(None, 6, 6, 128)
        self.maxpool3 = torch.nn.MaxPool2d(None, 3, 3, 128)
        self.flatten = torch.nn.Flatten(None, 1152)
        self.dense1 = torch.nn.Linear(None, 64)
        self.dense2 = torch.nn.Linear(None, 128)
        self.dense3 = torch.nn.Linear(None, 36)

    def __repr__(self) -> str:
        return "OCRModel do treningu modelu OCR"
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.maxpool2(x)
        x = self.conv3(x)
        x = self.maxpool3(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        return x