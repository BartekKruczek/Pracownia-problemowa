from data import Data
from utils import Utils

def main():
    data = Data(json_path='lemkin-json-from-html', pdf_path='lemkin-pdf')
    utils = Utils(json_path='lemkin-json-from-html')

    # how many files are there in both directories
    # print("Detected {} .json and {} .pdf files".format(data.number_of_files()[0], data.number_of_files()[1]))

    # converting pdf to png
    once_converted = False

    if once_converted:
        print(utils.convert_pdf_to_png(data.yield_pdf_files()))

    # extract text from png
    image_path = './lemkin-pdf/2014/WDU20140000600/O/_png/page_0.png'
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
    utils.json_text_debugger(iterator = utils.yield_json_files(), my_data = data)

    # perform LCS, only one pdf file (2014) and all 2014' json files
    # print(utils.find_max_lcs(json_iterator_paths = utils.yield_json_files(), pdf_text = combined))

if __name__ == '__main__':
    main()
