import os
import json
import pdf2image

from utils import Utils

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

        # convert pdf to image
        images = pdf2image.convert_from_path(test_pdf_path)

        # save pages as separate images
        folder_path = 'pdf_images'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for i, image in enumerate(images):
            image.save(f'{folder_path}/page_{i}.jpg', 'JPEG')

    def read_pdf_data(self):
        pass

    def pdf_file_to_png(self):
        """
        Converts pdf file to png, creates subfolder with pngs. Localization is the same as pdf file.
        """
        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                    for dir2 in dirs2:
                        yield os.path.join(root2, dir2)
                        for file2 in os.listdir(os.path.join(root2, dir2)):
                            if file2.endswith('.pdf'):
                                continue