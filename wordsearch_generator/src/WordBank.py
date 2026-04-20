import json
import random
from config import client

class WordBank:
    def __init__(self, size):
        self.size = size

        with open("src/resources/wordBank.json", "r", encoding="utf-8") as file:
            self.bank = json.load(file)

    def get_categories(self):
        return {
            i: list(category.keys())[0]
            for i, category in enumerate(self.bank["category"])
        }

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

    def validate_words(self, words):
        sanitized_words = []
        for word in words:
            word = word.strip()
            if len(word) <= self.size:
                sanitized_words.append(word)

        if len(sanitized_words) == 0:
            raise ValueError("There are no words that fit the size board chosen")
        elif len(sanitized_words) > 30:
            raise ValueError("List of words is too big")
        self.bank = sanitized_words
        return sanitized_words

    def save_to_word_bank(self, words, name):
        with open('src/resources/wordBank.json', 'r') as file:
            data = json.load(file)

        new_custom = {
            name: words
        }

        for item in data["category"]:
            if "custom" in item:
                item["custom"].append(new_custom)

        with open('src/resources/wordBank.json', 'w') as file:
            json.dump(data, file, indent=2)


    def generate_words(self, category, size):
        """
            generate_words() generates a list of words using openAI gpt model

            :param category: a String of user input for category
            :param size: size of the board which also determines the maximum length of a word
            :return: list of words that are generated
            """
        print("Generating...")
        messages = [
            {
                "role": "system",
                "content": "You are a JSON-only API. Return strictly valid JSON."
            },
            {
                "role": "user",
                "content": f"""
                    Category: "{category}"
                    Generate exactly {size} safe-for-work words of length {size} maximum.
                    
                    If the category is invalid or incomprehensible:
                    - Set "valid" to false
                    - Return an empty list
                
                    Return:
                    {{
                      "valid": boolean,
                      "words": string[]
                    }}
                    """
            }
        ]

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=messages,
            temperature=0
        )

        content = response.choices[0].message.content
        print("Content:", content)

        try:
            data = json.loads(content)
        except Exception:
            return None

        if not data.get("valid"):
            return None

        self.validate_words(data["words"])
        self.bank = data["words"]
        return data["words"]