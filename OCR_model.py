import torch
from torch.utils.data import Dataset
from torchsummary import summary

class OCRModel(torch.nn.Module):
    def __init__(self) -> torch.nn.Module:
        super(OCRModel, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.maxpool1 = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.maxpool2 = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = torch.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.maxpool3 = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.flatten = torch.nn.Flatten()
        self.dense1 = torch.nn.Linear(in_features=128 * 4 * 4, out_features=256)
        self.dense2 = torch.nn.Linear(in_features=256, out_features=128)
        self.dense3 = torch.nn.Linear(in_features=128, out_features=89)

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
    
    def convert_data_to_tensor(self, data: list) -> torch.Tensor:
        return torch.tensor(data)
    
    def train_model(self, model: torch.nn.Module, dataloader: Dataset, criterion, optimizer, epochs) -> None:
        summary(model, (1, 32, 32))
        model.train()
        for epoch in range(epochs):
            running_loss = 0.0
            for images, labels in dataloader:
                images = images.unsqueeze(1).float()
                labels = labels.long()

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()

            epoch_loss = running_loss / len(dataloader)
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {epoch_loss:.4f}")