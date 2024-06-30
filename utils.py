import os
import pypdfium2 as pdfium
import os
import json

from data import Data

class Utils():
    def __init__(self, json_path: str) -> None:
        self.json_path = json_path

    def __repr__(self) -> str:
        return "Klasa do obsługi różnych narzędzi"
    
    # recursive
    def longest_common_subsequence_r(self, a, b):
        """
        Returns the longest common subsequence of two strings
        """
        if len(a) == 0 or len(b) == 0:
            return 0
        if a[-1] == b[-1]:
            return 1 + self.longest_common_subsequence_r(a[:-1], b[:-1])
        else:
            return max(self.longest_common_subsequence_r(a, b[:-1]), self.longest_common_subsequence_r(a[:-1], b))
        
    # dynamic
    def longest_common_subsequence_dynamic(self, a: list, b: str) -> int:
        all_lcs = []

        n = len(b)

        for _ in a:
            m = len(a)
            # deklaracja tablicy L[m+1][n+1] wypełnionej zerami
            L = [[None] * (n + 1) for i in range(m + 1)]

            # budowanie tablicy L[m+1][n+1] w sposób bottom-up
            for i in range(m + 1):
                for j in range(n + 1):
                    if i == 0 or j == 0:
                        L[i][j] = 0
                    elif a[i - 1] == b[j - 1]:
                        L[i][j] = L[i - 1][j - 1] + 1
                    else:
                        L[i][j] = max(L[i - 1][j], L[i][j - 1])
            all_lcs.append(L[m][n])

        return max(all_lcs)

        
    def json_folder_iterator(self):
        """
        Iterates over a directory with .json files
        """
        for root, dirs, files in os.walk(self.json_path):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    if file.endswith('.json'):
                        yield file

    def create_pdf_folder(dir: str) -> None:
        if not os.path.exists(dir):
            os.makedirs(dir)

    def create_png_folder(self, generator):
        # stripping last element from path
        for elem in generator:
            dir_without_last = elem.split('/')[:-1]
            dir_without_last = '/'.join(dir_without_last)
            
            # creating new directory with _png suffix
            new_dir = dir_without_last + '_png'
        
        yield new_dir

    def convert_pdf_to_png(self, iterator) -> None:
        """
        Converts pdf file to png and saves it in specified directory
        """
        for elem in iterator:
            new_elem = elem.split('/')
            new_elem = new_elem[0] + "/" + new_elem[1] + "/" + new_elem[2] + "/" + new_elem[3] + "/" + '_png'
            
            if not os.path.exists(new_elem):
                os.makedirs(new_elem)

            # convert pdf to image
            pdf = pdfium.PdfDocument(elem)
            n_pages = len(pdf)

            # save pages as separate images into new_elem directory
            for page_number in range(n_pages):
                page = pdf.get_page(page_number)
                pil_image = page.render(
                    scale=5,
                    rotation=0,
                )
                new_image = pil_image.to_pil()
                new_image.save(f"{new_elem}/page_{page_number}.png")

            print("Converted {} to png".format(elem))

    def yield_json_files(self):
        """
        Yields json files
        """
        for root, dirs, files in os.walk(self.json_path):
            for dir in dirs:
                # only 2014, for PP purpouse
                if dir == "2014":
                    for file in os.listdir(os.path.join(root, dir)):
                        if file.endswith('.json'):
                            yield os.path.join(root, dir, file)

    def list_of_json_paths(self) -> list[str]:
        my_list = []

        for root, dirs, files in os.walk(self.json_path):
            for dir in dirs:
                if dir == "2014":
                    for file in os.listdir(os.path.join(root, dir)):
                        if file.endswith('.json'):
                            my_list.append(os.path.join(root, dir, file))

        return my_list
        

    def delete_unwanted_dir(self, dir: str) -> None:
        """
        Deletes unwanted directory
        """
        for root, dirs, files in os.walk(dir):
            for di in dirs:
                if di.endswith('*_png'):
                    os.rmdir(dir)