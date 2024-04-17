from data import Data

def main():
    data = Data(json_path = 'lemkin-json-from-html', pdf_path = 'lemkin-pdf')
    print(data.number_of_files())

if __name__ == '__main__':
    main()