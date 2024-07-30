import time

from data import Data
from utils import Utils

def main():
    start_time = time.time()

    data = Data(json_path='lemkin-json-from-html', pdf_path=  'lemkin-pdf')
    utils = Utils(json_path='lemkin-json-from-html', pdf_path = 'lemkin-pdf')

    # how many files are there in both directories
    # print("Detected {} .json and {} .pdf files".format(data.number_of_files()[0], data.number_of_files()[1]))

    # converting pdf to png
    once_converted = False

    if once_converted:
        print(utils.convert_pdf_to_png(data.yield_pdf_files()))

    years = [2014]

    # extract text from png
    image_path = './lemkin-pdf/2014/WDU20140001594/O/_png/page_0.png'
    text = data.get_text_from_png(image_path)

    # clean up text and combine it to one string, combined text is one string without spaces
    cleaned_text = data.clean_text(text)
    combined = data.combine_text_to_one_string(cleaned_text)
    # print(f"Pdf text \n{combined}")

    # yield json files
    # print(*utils.yield_json_files())

    # read json data
    json_data = data.read_json_data('lemkin-json-from-html/2014/2014_1594.json')
    json_text = data.clean_text_from_json(data.get_text_from_json(json_data))
    # print(f"Json text \n{json_text}")

    # perform LCS, only one pdf file and one json file
    # print(utils.longest_common_subsequence_dynamic(utils.list_of_json_paths(), combined))

    # json text debugger
    # utils.json_text_debugger(iterator = utils.yield_json_files(), my_data = data)

    # png_list_debugger
    # utils.pngs_list_debugger(pngs_list, data)

    # data.delete_unwanted_folders()

    do_iterate = False

    if do_iterate:
        for year in years:
            # for pdf_path in data.yield_pdf_files(year):
            #     print(f"{pdf_path}")
                # utils.convert_pdf_to_png(pdf_path)

            # list of all png_0 files
            pngs_list = utils.png_paths_creator(year)
            # print(pngs_list)
            # print(len(pngs_list))

            utils.find_max_lcs(json_iterator_paths = utils.yield_json_files(year = year), png_list = pngs_list, my_data = data, year = year)

    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print(f"Czas wykonania: {elapsed_time:.2f} minut")

if __name__ == '__main__':
    main()
