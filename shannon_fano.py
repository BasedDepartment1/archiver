from collections import Counter


def decode(encoded: str, coding_table: dict):
    decoded = bytearray()
    code = ""
    for char in encoded:
        code += char
        for char, char_code in coding_table.items():
            if code == char_code:
                decoded.append(char)
                code = ""
                break
    return decoded


class ShannonFano:
    def __init__(self, bytes):
        self.bytes = bytes
        self.alphabet = self.get_bytes_counter()
        self.probabilities = self.get_probabilities()
        self.codes = self.get_codes()

    def get_bytes_counter(self):
        return Counter(self.bytes)

    def get_probabilities(self):
        probabilities = {}
        for char, count in self.alphabet.items():
            probabilities[char] = count / len(self.bytes)
        return probabilities

    def get_codes(self):
        def get_codes_rec(probabilities, code=""):
            if len(probabilities) == 1:
                return {list(probabilities.keys())[0]: code}

            half = sum(probabilities.values()) / 2
            left = {}
            right = {}
            left_sum = 0
            right_sum = 0
            for char, prob in probabilities.items():
                if left_sum + prob <= half:
                    left[char] = prob
                    left_sum += prob
                else:
                    right[char] = prob
                    right_sum += prob

            return {
                **get_codes_rec(left, code + "0"),
                **get_codes_rec(right, code + "1"),
            }

        return get_codes_rec(self.probabilities)

    def encode(self):
        encoded = ""
        for char in self.bytes:
            encoded += self.codes[char]
        return encoded
