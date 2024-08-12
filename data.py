import os
import shutil
import json
import pdf2image
import pytesseract
import re

from PIL import Image
from datetime import datetime

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
    
    def get_text_from_json(self, json_data: json) -> str:
        print(f'Initializing {self.get_text_from_json.__name__}')
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
        
        if not extracted_text:
            return ""

        joined = ' '.join(extracted_text)
        return joined
    
    def get_text_from_pdf(self, pdf_path: str) -> str:
        """
        Ekstrahuje tekst z wszystkich stron dokumentu PDF.
        """
        try:
            images = pdf2image.convert_from_path(pdf_path)
            all_text = []

            for image in images:
                # Konwertowanie obrazu na tekst
                text = pytesseract.image_to_string(image)
                all_text.append(text)

            # Łączenie wszystkich tekstów w jedną całość
            combined_text = ' '.join(all_text)
            return combined_text

        except Exception as e:
            print(f"An error occurred while extracting text from {pdf_path}: {e}")
            return ""
    
    def load_pdf_as_image(self):
        print(f'Initializing {self.load_pdf_as_image.__name__}')
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
        print(f'Initializing {self.yield_pdf_folders.__name__}')
        """
        Converts pdf file to png, creates subfolder with pngs. Localization is the same as pdf file.
        """
        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                    for dir2 in dirs2:
                        yield os.path.join(root2, dir2)

    def yield_pdf_files(self, year):
        print(f'Initializing {self.yield_pdf_files.__name__}')
        """
        Yields pdf files, string format path to file
        """
        pdf_path = os.path.join(self.pdf_path, str(year))
        for root, dirs, files in os.walk(pdf_path):
            for dir in dirs:
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
        # return [elem for elem in list if elem.strip()]
        return [elem for elem in list]
    
    def combine_text_to_one_string(self, list: list) -> str:
        return ' '.join(list).lower()
        # return ' '.join(list)
    
    def clean_text_from_json(self, string: str) -> str:
        # string = ''.join(string.split()).lower()
        string = string.replace('\n', ' ').replace('\r', ' ')
        string = re.sub(r'\s+', ' ', string).strip().lower()
        return string
    
    def delete_unwanted_folders(self):
        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                if dir == '2015':
                    for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                        for dir2 in dirs2:
                            for root3, dirs3, files3 in os.walk(os.path.join(root2, dir2)):
                                for dir3 in dirs3:
                                    if dir3.endswith('_png') and len(dir3) >5:
                                        path = os.path.join(root3, dir3)
                                        # print(f"{path}")
                                        shutil.rmtree(path)

    def get_text_from_images(self, image_folder: str, first_png_only = bool) -> str:
        """
        Ekstrakcja tekstu z wszystkich obrazów w podanym folderze.
        """
        print(f"Initializing {self.get_text_from_images.__name__}")
        print(f"Starting processing {image_folder}...")
        all_text = []
        if first_png_only:
            try:
                image_files = sorted(os.listdir(image_folder))
                
                image_files = [file for file in image_files if file.endswith('.png')]
                
                if image_files:
                    first_image_path = os.path.join(image_folder, image_files[0])
                    print(f"Processing first image: {first_image_path}")
                    
                    image = Image.open(first_image_path)
                    text = pytesseract.image_to_string(image)
                    cleaned_text = text.replace("\n", " ").replace("\r", " ")
                    cleaned_text = cleaned_text = re.sub(r'\s+', ' ', text)
                    cleaned_text = cleaned_text.strip()
                    print(cleaned_text)
                    return cleaned_text
                else:
                    print(f"No images found in folder: {image_folder}")
                    return "No images found!"

            except Exception as e:
                print(f"An error occurred while extracting text from images in {image_folder}: {e}")
                return "Text not extracted!"
        else:
            try:
                num_pages = 0
                for filename in sorted(os.listdir(image_folder)):
                    if filename.endswith('.png'):
                        image_path = os.path.join(image_folder, filename)
                        image = Image.open(image_path)
                        text = pytesseract.image_to_string(image)
                        all_text.append(text)
                        print(f"Combined another page")
                        num_pages += 1

                combined_text = ''.join(all_text).lower()
                print(f"Processed {num_pages} pages.")
                # combined_text = self.clean_text(combined_text)
                # combined_text = self.combine_text_to_one_string(combined_text)

                text = text.replace("\n", " ").replace("\r", " ")
                text = re.sub(r'\s+', ' ', text)
                text = text.strip()

                print(text)
                return text
            except Exception as e:
                print(f"An error occurred while extracting text from images in {image_folder}: {e}")
                return "Text not extracted!"

    def get_text_data(text: str):
        miesiace = {
            "stycznia": 1,
            "lutego": 2,
            "marca": 3,
            "kwietnia": 4,
            "maja": 5,
            "czerwca": 6,
            "lipca": 7,
            "sierpnia": 8,
            "wrzesnia": 9,
            "września": 9,
            "pazdziernika": 10,
            "października": 10,
            "listopada": 11,
            "grudnia": 12,
            "01": 1, "1": 1,
            "02": 2, "2": 2,
            "03": 3, "3": 3,
            "04": 4, "4": 4,
            "05": 5, "5": 5,
            "06": 6, "6": 6,
            "07": 7, "7": 7,
            "08": 8, "8": 8,
            "09": 9, "9": 9,
            "10": 10,
            "11": 11,
            "12": 12
        }

        search_pattern = (
            r'\b(\d{1,2})(?:\s*[-/.\s]?\s*)'
            r'(stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|wrzesnia|września|pazdziernika|października|listopada|grudnia|\d{1,2})(?:\s*[-/.\s]?\s*)'
            r'(\d{4})\b'
            r'|'
            r'\b(\d{4})-(\d{2})-(\d{2})\b'
        )

        matches = re.findall(search_pattern, text, re.IGNORECASE)

        dates = []

        for match in matches:
            if match[0] and match[2]:
                day = int(match[0])
                month = miesiace.get(match[1].lower(), None)
                year = int(match[2])
            elif match[3] and match[4] and match[5]:
                year = int(match[3])
                month = int(match[4])
                day = int(match[5])
            else:
                continue

            try:
                dates.append(datetime(year, month, day))
            except ValueError:
                continue
        
        if len(dates) >= 2:
            return dates[1]
        elif len(dates) == 1:
            print("Only one date found, unable to find a second date.")
            return None
        else:
            print("No dates found in the text.")
            return None

    def get_data_json(self, path: str) -> str:
        pass