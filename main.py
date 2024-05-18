import torch
from data import Data
from utils import Utils
from OCR_model import OCRModel
from dataloader import OCRDataset
from torch.utils.data import DataLoader

def main():
    data = Data(json_path = 'lemkin-json-from-html', pdf_path = 'lemkin-pdf')
    my_utils = Utils(load_path = './zdekodowane')

    # how many files are there in both directories
    print("Detected {} .json and {} .pdf files".format(str(data.number_of_files()[0]), str(data.number_of_files()[1])))

    # read json data, for example for now
    # data.read_json_data()

    # load pdf as image
    data.load_pdf_as_image()

    # utils section
    signs, binarized_signs, labels, signs_dictionary = my_utils.load_files()
    decoded_image = my_utils.decode_image_from_binarized(binarized_signs[0])
    print("Decoded image: ", decoded_image)
    print("Labels: ", labels[0])

    # dataset section
    dataset = OCRDataset(signs, binarized_signs, labels)
    print("Dataset length: ", dataset.__len__())
    print("Dataset sample: ", dataset.__getitem__(0)[0].shape)

    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # model section
    model = OCRModel()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    model.train_model(model, dataloader, criterion, optimizer, epochs=10)

if __name__ == '__main__':
    main()