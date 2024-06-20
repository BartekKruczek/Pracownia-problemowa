import os
import json
import pdf2image
import pytesseract

from PIL import Image

class Data():
    def __init__(self, json_path = None, pdf_path = None):
        self.json_path = json_path
        self.pdf_path = pdf_path

    def __repr__(self) -> str:
        return 'Data handler'
    
    def dataframe_handler(self):
        pass
    
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
    
    def read_json_data(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def get_text_from_json(self, json_data: json) -> list[str]:
        extracted_text = []

        def recursive_search(node):
            if isinstance(node, dict):
                if 'text' in node and node['text']:
                    extracted_text.append(node['text'])
                for key in node:
                    recursive_search(node[key])
            elif isinstance(node, list):
                for item in node:
                    recursive_search(item)

        recursive_search(json_data)
        joined =  ''.join(extracted_text)

        return joined

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

    def yield_pdf_folders(self):
        """
        Converts pdf file to png, creates subfolder with pngs. Localization is the same as pdf file.
        """
        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                    for dir2 in dirs2:
                        yield os.path.join(root2, dir2)

    def yield_pdf_files(self):
        """
        Yields pdf files, string format path to file
        """
        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                if dir == "2014":
                    for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                        for file in files2:
                            if file.endswith('.pdf'):
                                yield os.path.join(root2, file)

    def get_text_from_png(self, image_path: str) -> str:
        # pytesseract.pytesseract.tesseract_cmd = "/net/people/plgrid/plgkruczek/.local/lib/python3.9/site-packages/tesseract"

        image_data = pytesseract.image_to_data(Image.open(image_path), output_type=pytesseract.Output.DICT)
        return ' '.join(image_data["text"])
    
    def clean_text(self, list: list) -> list[str]:
        # basicly iterate over the elements from list and remove blank spaces
        return [elem for elem in list if elem.strip()]
    
    def combine_text_to_one_string(self, list: list) -> str:
        return ''.join(list).lower()
    
    def clean_text_from_json(self, string: str) -> str:
        return ''.join(string.split()).lower()
    
    def find_max_lcs(self, json_iterator, text_from_png, utils):
        max_lcs = 0
        max_file = None
        for json_file in json_iterator:
            json_data = self.read_json_data(json_file)
            json_text = json.dumps(json_data)
            current_lcs = utils.longest_common_subsequence(text_from_png, json_text)
            if current_lcs > max_lcs:
                max_lcs = current_lcs
                max_file = json_file
        return max_file, max_lcs
