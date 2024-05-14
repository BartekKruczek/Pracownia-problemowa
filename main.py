from data import Data
from utils import Utils

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

if __name__ == '__main__':
    main()