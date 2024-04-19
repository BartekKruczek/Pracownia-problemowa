from data import Data

def main():
    data = Data(json_path = 'lemkin-json-from-html', pdf_path = 'lemkin-pdf')

    # how many files are there in both directories
    print("Detected {} .json and {} .pdf files".format(str(data.number_of_files()[0]), str(data.number_of_files()[1])))

    # read json data, for example for now
    # data.read_json_data()

    # load pdf as image
    data.load_pdf_as_image()

if __name__ == '__main__':
    main()