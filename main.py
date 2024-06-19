from data import Data
from utils import Utils

def main():
    data = Data(json_path='lemkin-json-from-html', pdf_path='lemkin-pdf')
    utils = Utils(json_path='lemkin-json-from-html')

    # how many files are there in both directories
    print("Detected {} .json and {} .pdf files".format(data.number_of_files()[0], data.number_of_files()[1]))

    # converting pdf to png
    once_converted = False

    if once_converted:
        print(utils.convert_pdf_to_png(data.yield_pdf_files()))

    # extract text from png
    image_path = './lemkin-pdf/2014/WDU20140000596/O/_png/page_0.png'
    print(data.get_text_from_png(image_path))


if __name__ == '__main__':
    main()
