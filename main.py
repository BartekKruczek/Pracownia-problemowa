from data import Data
from utils import Utils

def main():
    data = Data(json_path='lemkin-json-from-html', pdf_path='lemkin-pdf')
    utils = Utils(json_path='lemkin-json-from-html')

    # how many files are there in both directories
    print("Detected {} .json and {} .pdf files".format(data.number_of_files()[0], data.number_of_files()[1]))

    # testing section
    print(utils.convert_pdf_to_png(data.yield_pdf_files()))


if __name__ == '__main__':
    main()
