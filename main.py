import torch
import torch.optim.lr_scheduler as lr_scheduler
from torch.utils.data import DataLoader, random_split
from data import Data
from utils import Utils
from OCR_model import OCRModel
from dataloader import OCRDataset

def main():
    data = Data(json_path='lemkin-json-from-html', pdf_path='lemkin-pdf')
    my_utils = Utils(load_path='./zdekodowane')

    # how many files are there in both directories
    print("Detected {} .json and {} .pdf files".format(data.number_of_files()[0], data.number_of_files()[1]))

    # utils section
    signs, binarized_signs, labels, signs_dictionary = my_utils.load_files()
    decoded_image = my_utils.decode_image_from_binarized(binarized_signs[0])
    print("Decoded image: ", decoded_image)
    print("Labels: ", labels[0])

    # dataset section
    dataset = OCRDataset(signs, binarized_signs, labels)
    print("Dataset length: ", len(dataset))
    print("Dataset sample: ", dataset[0][0].shape)

    # Split the dataset
    train_size = int(0.8 * len(dataset))
    val_size = int(0.1 * len(dataset))
    test_size = len(dataset) - train_size - val_size

    train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # model section
    model = OCRModel()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

    model.train_model(train_loader, val_loader, criterion, optimizer, scheduler, epochs=10)
    model.test_model(test_loader, criterion)

if __name__ == '__main__':
    main()
