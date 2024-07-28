import os
import pypdfium2 as pdfium
import pandas as pd
import pylcs

class Utils():
    def __init__(self, json_path: str, pdf_path: str) -> None:
        self.base_json_path = json_path
        self.base_pdf_path = pdf_path

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

    def lcs_pylcs(self, a: list, b: str) -> list[int]:
        all_lcs: list = []

        for _ in a:
            if len(_) != 0:
                all_lcs.append(int(pylcs.lcs_sequence_length(a, b)))

        return max(all_lcs)


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

    def convert_pdf_to_png(self, pdf_path):
        try:
            pdf = pdfium.PdfDocument(pdf_path)
            n_pages = len(pdf)

            folder_path = pdf_path.rsplit('.', 1)[0] + '_png'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            for page_number in range(n_pages):
                page = pdf.get_page(page_number)
                pil_image = page.render(scale=5, rotation=0).to_pil()
                pil_image.save(f"{folder_path}/page_{page_number}.png")
        except pdfium.PdfiumError as e:
            print(f"Failed to load PDF document {pdf_path}: {e}")
        except Exception as e:
            print(f"An error occurred while converting {pdf_path} to PNG: {e}")


    def yield_json_files(self, year):
            json_path = os.path.join(self.base_json_path, str(year))
            for root, _, files in os.walk(json_path):
                for file in files:
                    if file.endswith('.json'):
                        yield os.path.join(root, file)

    def png_paths_creator(self, year) -> list[str]:
        pdf_path = os.path.join(self.base_pdf_path, str(year))
        pngs_0_list = []
        for root, _, files in os.walk(pdf_path):
            for file in files:
                if file.endswith('_0.png'):
                    pngs_0_list.append(os.path.join(root, file))
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
    
    # def find_max_lcs(self, json_iterator_paths: iter, png_list: list, my_data: classmethod) -> None:
    #     main_dict: dict = {}
    #     # number_of_iter = int(len(png_list))
    #     number_of_iter = int(5)

    #     # Convert iterator to list to allow multiple iterations
    #     json_paths_list = list(json_iterator_paths)

    #     # Initialize the main dictionary with empty dictionaries for each png_path
    #     for png_path in png_list[:number_of_iter]:
    #         main_dict[png_path] = {}

    #     # Populate the main dictionary with LCS values
    #     for png_path in png_list[:number_of_iter]:
    #         text = my_data.combine_text_to_one_string(my_data.clean_text(my_data.get_text_from_png(png_path)))
    #         print(f"Processing PNG: {png_path}")
    #         for file_path in json_paths_list:
    #             # lcs_value = self.longest_common_subsequence_dynamic(file_path, text)
    #             lcs_value = self.lcs_pylcs(file_path, text)
    #             if lcs_value is not None:  # Ensure the LCS value is valid
    #                 main_dict[png_path][file_path] = int(lcs_value)
    #                 print(f"Added LCS value {lcs_value} for JSON: {file_path} with PNG: {png_path}")
    #             else:
    #                 print(f"No LCS value found for JSON: {file_path} with PNG: {png_path}")

    #     # Convert the main_dict to a DataFrame and save it to an Excel file
    #     rows = []
    #     for png_path, lcs_dict in main_dict.items():
    #         for json_path, lcs_value in lcs_dict.items():
    #             rows.append([png_path, json_path, lcs_value])

    #     df = pd.DataFrame(rows, columns=['PNG Path', 'JSON Path', 'LCS Value'])
    #     df.to_excel('lcs_results.xlsx', index=False)
    #     print("Results saved to lcs_results.xlsx")

    #     # Iterate through the main dictionary and find the max LCS for each png_path
    #     for png_path, lcs_dict in main_dict.items():
    #         if lcs_dict:  # Check if the lcs_dict is not empty
    #             # Find the max value in the lcs_dict for the current png_path
    #             max_value = max(lcs_dict.values())
    #             # Find the json_path(s) with the max value
    #             for json_path, value in lcs_dict.items():
    #                 if value == max_value:
    #                     json_text = my_data.clean_text_from_json(my_data.get_text_from_json(my_data.read_json_data(json_path)))
    #                     if len(json_text) != 0:
    #                         print(f"{json_path} -> [{png_path}, {value}]")
    #                         print(f"PDF text: {text[:100]}")
    #                         print(f"JSON text: {json_text[:100]} \n")
    #         else:
    #             print(f"No LCS values found for {png_path}")

    # def json_text_debugger(self, iterator: iter, my_data: classmethod) -> None:
    #     print(f"Starting debugging...")

    #     for elem in iterator:
    #         json_text = my_data.clean_text_from_json(my_data.get_text_from_json(my_data.read_json_data(elem)))

    #         if len(json_text) != 0:
    #             print(f"{elem}")
    #             print(f"Json text first 100 characters: {json_text[:100]} \n")

    #     print(f"Debugging ended!")

    def find_max_lcs(self, json_iterator_paths, png_list, data_handler, year):
        main_dict = {}

        json_paths_list = list(json_iterator_paths)

        for png_path in png_list:
            main_dict[png_path] = {}

        for png_path in png_list:
            text = data_handler.get_text_from_png(png_path)
            for file_path in json_paths_list:
                json_data = data_handler.read_json_data(file_path)
                json_text = data_handler.get_text_from_json(json_data)
                lcs_value = self.longest_common_subsequence_dynamic(json_text, text)
                if lcs_value:
                    main_dict[png_path][file_path] = lcs_value

        rows = []
        for png_path, lcs_dict in main_dict.items():
            for json_path, lcs_value in lcs_dict.items():
                rows.append([png_path, json_path, lcs_value])

        df = pd.DataFrame(rows, columns=['PNG Path', 'JSON Path', 'LCS Value'])
        df.to_csv(f'lcs_results_{year}.csv', index=False)

        for png_path, lcs_dict in main_dict.items():
            if lcs_dict:
                max_value = max(lcs_dict.values())
                for json_path, value in lcs_dict.items():
                    if value == max_value:
                        json_data = data_handler.read_json_data(json_path)
                        json_text = data_handler.get_text_from_json(json_data)
                        print(f"{json_path} -> [{png_path}, {value}]")
                        print(f"PDF text: {text[:100]}")
                        print(f"JSON text: {json_text[:100]} \n")

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