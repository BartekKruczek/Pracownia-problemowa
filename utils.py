import os
import pypdfium2 as pdfium
import os

class Utils():
    def __init__(self, json_path: str, pdf_path: str) -> None:
        self.json_path = json_path
        self.pdf_path = pdf_path

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

        b = b[:100]
        n = len(b)

        for _ in a:
            if len(_) != 0:
                a = a[:100]
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
            else:
                continue

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

    def png_paths_creator(self) -> list[str]:
        """
        Creates list of png_0 paths
        """
        pngs_0_list: list = []

        for root, dirs, files in os.walk(self.pdf_path):
            for dir in dirs:
                # only 2014, for PP purpose
                if dir == "2014":
                    for root, dirs, files in os.walk(os.path.join(root, dir)):
                        for file in files:
                            if file.endswith('_0.png'):
                                full_path = os.path.join(root, file)
                                pngs_0_list.append(full_path)

        return pngs_0_list

    def list_of_json_paths(self) -> list[str]:
        my_list = []

        for root, dirs, files in os.walk(self.json_path):
            for dir in dirs:
                if dir == "2014":
                    for file in os.listdir(os.path.join(root, dir)):
                        if file.endswith('.json'):
                            my_list.append(os.path.join(root, dir, file))

        return my_list
    
    def find_max_lcs(self, json_iterator_paths: iter, png_list: list, my_data: classmethod) -> None:
        """
        max_lcs = {key: json_file_path, value: [png_path, max_lcs_value]}
        """
        max_lcs: dict = {}

        for png_path in png_list[:2]:
            text = my_data.combine_text_to_one_string(my_data.clean_text(my_data.get_text_from_png(png_path)))
            for file_path in json_iterator_paths:
                # file_path -> str
                max_lcs[f"{file_path}"] = [str(png_path), int(self.longest_common_subsequence_dynamic(file_path, text))]

            # Find the max value in max_lcs dictionary for the current png_path
            max_value = max(max_lcs.values(), key=lambda x: x[1])

            # Iterate through dict and find the key(s) with the max value
            for key, value in max_lcs.items():
                if value == max_value:
                    json_text = my_data.clean_text_from_json(my_data.get_text_from_json(my_data.read_json_data(key)))
                    if len(json_text) != 0:
                        print(f"{key} -> {value}")
                        print(f"PDF text: {text[:100]}")
                        print(f"JSON text: {json_text[:100]} \n")

    def json_text_debugger(self, iterator: iter, my_data: classmethod) -> None:
        print(f"Starting debugging...")

        for elem in iterator:
            json_text = my_data.clean_text_from_json(my_data.get_text_from_json(my_data.read_json_data(elem)))

            if len(json_text) != 0:
                print(f"{elem}")
                print(f"Json text first 100 characters: {json_text[:100]} \n")

        print(f"Debugging ended!")

    def pngs_list_debugger(self, my_list: list[str], my_data: classmethod) -> None:
        max_lcs = {}

        for elem in my_list[:1]:
            text = my_data.combine_text_to_one_string(my_data.clean_text(my_data.get_text_from_png(elem)))
            print(f"{elem} text: {text[:100]} \n")

            for file_path in elem:
                # file_path -> str
                max_lcs[f"{file_path}"] = self.longest_common_subsequence_dynamic(file_path, text)

            # max value
            max_value = max(max_lcs.values())
            print(f"Max lcs value {max_value}")