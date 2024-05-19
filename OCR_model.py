import torch
from torch.utils.data import DataLoader
from torchsummary import summary

class OCRModel(torch.nn.Module):
    def __init__(self) -> torch.nn.Module:
        super(OCRModel, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.maxpool1 = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.maxpool2 = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout1 = torch.nn.Dropout(p=0.5)
        self.conv3 = torch.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.maxpool3 = torch.nn.MaxPool2d(kernel_size=2, stride=2)
        self.flatten = torch.nn.Flatten()
        self.dense1 = torch.nn.Linear(in_features=128 * 4 * 4, out_features=256)
        self.dropout2 = torch.nn.Dropout(p=0.5)
        self.dense2 = torch.nn.Linear(in_features=256, out_features=128)
        self.dropout3 = torch.nn.Dropout(p=0.5)
        self.dense3 = torch.nn.Linear(in_features=128, out_features=89)

    def __repr__(self) -> str:
        return "OCRModel do treningu modelu OCR"
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.maxpool2(x)
        x = self.dropout1(x)
        x = self.conv3(x)
        x = self.maxpool3(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dropout2(x)
        x = self.dense2(x)
        x = self.dropout3(x)
        x = self.dense3(x)
        return x
    
    def train_model(self, train_loader: DataLoader, val_loader: DataLoader, criterion, optimizer, scheduler, device, epochs: int) -> None:
        self.to("cpu")

        summary_device = "cpu"
        summary(self, (1, 32, 32), device=str(summary_device))
        
        self.to(device)
        self.train()

        for epoch in range(epochs):
            running_loss = 0.0
            correct = 0
            total = 0

            # Training phase
            self.train()
            for images, labels in train_loader:
                images = images.unsqueeze(1).float().to(device)
                labels = labels.long().to(device)

                optimizer.zero_grad()
                outputs = self(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            epoch_loss = running_loss / len(train_loader)
            accuracy = 100 * correct / total
            current_lr = optimizer.param_groups[0]['lr']
            print(f"Epoch [{epoch + 1}/{epochs}], Train Loss: {epoch_loss:.4f}, Train Accuracy: {accuracy:.2f}%, LR: {current_lr:.6f}")

            # Validation phase
            self.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            with torch.no_grad():
                for images, labels in val_loader:
                    images = images.unsqueeze(1).float().to(device)
                    labels = labels.long().to(device)

                    outputs = self(images)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item()
                    
                    _, predicted = torch.max(outputs.data, 1)
                    val_total += labels.size(0)
                    val_correct += (predicted == labels).sum().item()

            val_epoch_loss = val_loss / len(val_loader)
            val_accuracy = 100 * val_correct / val_total
            print(f"Epoch [{epoch + 1}/{epochs}], Val Loss: {val_epoch_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%")
            scheduler.step()
    
    def test_model(self, test_loader: DataLoader, criterion, device) -> None:
        self.eval().to(device)
        test_loss = 0.0
        test_correct = 0
        test_total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images = images.unsqueeze(1).float().to(device)
                labels = labels.long().to(device)

                outputs = self(images)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                test_total += labels.size(0)
                test_correct += (predicted == labels).sum().item()

        test_epoch_loss = test_loss / len(test_loader)
        test_accuracy = 100 * test_correct / test_total
        print(f"Test Loss: {test_epoch_loss:.4f}, Test Accuracy: {test_accuracy:.2f}%")
