import json
import random

class WordBank:
    def __init__(self, size):
        self.size = size

        with open("src/wordBank.json", "r", encoding="utf-8") as file:
            self.bank = json.load(file)

    def get_categories(self):
        return [list(category.keys())[0] for category in self.bank["category"]]

    def get_subcategories(self, main_category):
        for category in self.bank["category"]:
            if main_category in category:
                return [list(sub.keys())[0] for sub in category[main_category]]
        return []

    def get_words(self, main_category, subcategory):
        for category in self.bank["category"]:
            if main_category in category:
                for sub in category[main_category]:
                    if subcategory in sub:
                        words = [w for w in sub[subcategory] if len(w) <= self.size]
                        random.shuffle(words)

                        num_words = min(len(words), self.size)

                        return words[:num_words]
        return []