def delta_decoding(data: str):
    """Decode a delta-encoded string. / TODO: Fix this like encoding
    """
    result = []
    for item in data:
        if result:
            result.append(item + result[-1])
        else:
            result.append(item)
    return result


def delta_encoding(data):
    """Encode a string using delta encoding.
    """
    result = []
    last = 0
    for item in data:
        if result:
            result.append(int(ord(item) - ord(last)))
        else:
            result.append(item)
        last = item
    return result


def lz77_compressor(data):
    """LZ77 compressor.
    """


def get_probability_every_symbol_in_string(string):
    """Get the probability of every symbol in a string.
    """
    result = {}
    for char in string:
        if char in result:
            result[char] += 1
        else:
            result[char] = 1
    for char in result:
        result[char] /= len(string)
    return result


test = 'abehhilopsu'
delta = delta_encoding(test)
print(delta)
lz77 = lz77_compressor(delta)
print(lz77)
ans = get_probability_every_symbol_in_string(lz77)
print(ans)