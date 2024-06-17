import os

class Utils():
    def __init__(self, json_path: str) -> None:
        self.json_path = json_path

    def __repr__(self) -> str:
        return "Klasa do obsługi różnych narzędzi"
    
    def longest_common_subsequence(self, a, b):
        """
        Returns the longest common subsequence of two strings
        """
        if len(a) == 0 or len(b) == 0:
            return 0
        if a[-1] == b[-1]:
            return 1 + self.longest_common_subsequence(a[:-1], b[:-1])
        else:
            return max(self.longest_common_subsequence(a, b[:-1]), self.longest_common_subsequence(a[:-1], b))
        
    def json_folder_iterator(self):
        """
        Iterates over a directory with .json files
        """
        for root, dirs, files in os.walk(self.json_path):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    if file.endswith('.json'):
                        yield file