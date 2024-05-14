import numpy as np
import json

class Utils:
    def __init__(self, dic_path, load_path) -> None:
        self.dic_path = dic_path
        self.load_path = load_path

    def __repr__(self) -> str:
        "Klasa do obsługi różnych narzędzi"

    def load_dictionary(self):
        with open(self.dic_path, 'r') as JSON:
            sign_dict = json.load(JSON)
        sign_dict = {int(number):sign for number, sign in sign_dict.items()}
        return sign_dict

    def load_files(self):
        signs = np.load(self.load_path + "\\" + "signs.npy")
        binarized_signs = np.load(self.load_path + "\\" + "binarized_signs.npy")
        labels = np.load(self.load_path + "\\" + "labels_int.npy")
        signs_dictionary = self.load_dictionary(self.load_path + "\\" + "dictionary.json")
        return signs, binarized_signs, labels, signs_dictionary