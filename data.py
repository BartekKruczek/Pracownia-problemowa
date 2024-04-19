import os
import json
import pdf2image

class Data():
    def __init__(self, json_path = None, pdf_path = None):
        self.json_path = json_path
        self.pdf_path = pdf_path

    def __repr__(self) -> str:
        return 'Data handler'
    
    def number_of_files(self):
        files_counter_json = 0
        files_counter_pdf = 0

        # for json data
        for root, dirs, files in os.walk(self.json_path):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    files_counter_json += 1

        # for pdf data
        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    files_counter_pdf += 1

        return files_counter_json, files_counter_pdf
    
    def read_json_data(self):
        root = "lemkin-json-from-html/1918/1918_2.json"

        with open(root, encoding='utf-8') as f:
            data = json.load(f)
            print(data)

    def load_pdf_as_image(self):
        test_pdf_path = "lemkin-pdf/2014/WDU20140000596/O/D20140596.pdf"
        print(len(test_pdf_path))

        # convert pdf to image
        images = pdf2image.convert_from_path(test_pdf_path)

        # save pages as separate images
        for i in range(len(images)):
            images[i].save('page'+ str(i) +'.jpg', 'JPEG')
        