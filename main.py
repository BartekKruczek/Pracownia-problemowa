from data import Data
from utils import Utils

def main():
    data = Data(json_path='lemkin-json-from-html', pdf_path='lemkin-pdf')
    utils = Utils()

    # how many files are there in both directories
    print("Detected {} .json and {} .pdf files".format(data.number_of_files()[0], data.number_of_files()[1]))

    # testing the longest_common_subsequence method
    a = "abcde"
    b = "ace"
    print("The longest common subsequence of '{}' and '{}' is: {}".format(a, b, utils.longest_common_subsequence(a, b)))

if __name__ == '__main__':
    main()
