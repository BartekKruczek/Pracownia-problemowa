import numpy as np
import json

class Utils():
    def __init__(self, load_path = None) -> None:
        self.load_path = load_path

    def __repr__(self) -> str:
        return "Klasa do obsługi różnych narzędzi"

    def load_dictionary(self, path):
        with open(path, 'r', encoding='ISO-8859-1') as JSON:
            sign_dict = json.load(JSON)
        sign_dict = {int(number):sign for number, sign in sign_dict.items()}
        return sign_dict

    def load_files(self):
        signs = np.load(self.load_path + "/" + "signs.npy")
        binarized_signs = np.load(self.load_path + "/" + "binarized_signs.npy")
        labels = np.load(self.load_path + "/" + "labels_int.npy")
        signs_dictionary = self.load_dictionary(self.load_path + "/" + "dictionary.json")
        return signs, binarized_signs, labels, signs_dictionary
    
    @staticmethod
    def decode_image_from_binarized(binarized, idle_pixel = 0):    
        if (idle_pixel == 0):
            occupied_pixel = 255
        else:
            occupied_pixel = 0
        IMG_SIDE_LENGTH= 32
        bits_in_byte = 8
        img_arr = np.ones((IMG_SIDE_LENGTH*IMG_SIDE_LENGTH, 1))*idle_pixel
        for i, byte in enumerate(binarized):
            for j in range(bits_in_byte):
                if (byte >= 2**(bits_in_byte - j - 1)):
                    img_arr[i*bits_in_byte + j] = occupied_pixel
                    byte -= 2**(bits_in_byte - j - 1)
                else:
                    img_arr[i*bits_in_byte + j] = idle_pixel
        img_arr = img_arr.reshape((IMG_SIDE_LENGTH, IMG_SIDE_LENGTH))
        return img_arr