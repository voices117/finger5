import sys

from collections import Counter


SPECIAL_CHARS = [chr(x) for x in (range(1, 9) + range(11, 13) + range(14, 32) + range(127, 256))]


def most_common_words(text, num_words):
    words = (word for word in text.split())
    common_words = Counter(words).most_common(num_words)
    return [x[0] for x in common_words]


def escape(data, chars, esc_char='\x00'):
    for sc in SPECIAL_CHARS:
        data = data.replace(sc, '\x00' + sc)
    return data


def replace_words(text, encode_words):
    text = escape(text, SPECIAL_CHARS)
    for i, word in enumerate(encode_words):
        text = text.replace(word, SPECIAL_CHARS[i])
    return text


def encode(filename, outname=None):
    outname = outname or filename + '.encoded'
    with open(filename, 'r') as fp:
        data = fp.read()
    words = most_common_words(text=data, num_words=len(SPECIAL_CHARS))

    with open(outname, 'w') as fp:
        fp.write('\x00'.join(words))
        fp.write('\x00\x00')
        fp.write(replace_words(data, words))


#--------------------------------------------------------------------------------------------------

def decode(filename):
    with open(filename, 'r') as fp:
        data = fp.read()

    codemap, word, word_code, i = {}, '', 0, 0
    for c in data:
        i += 1
        if c == '\x00' and not word:
            # end of dict
            break
        elif c == '\x00':
            # new word
            codemap[SPECIAL_CHARS[word_code]] = word
            word = ''
            word_code += 1
        else:
            word += c

    assert len(codemap) == len(SPECIAL_CHARS), '%i != %i' % (len(codemap), len(SPECIAL_CHARS))

    data, output = data[i:], ''
    escape = False
    for c in data:
        if escape:
            output += c
            escape = False
        elif c == '\x00':
            escape = True
        elif c in SPECIAL_CHARS:
            output += codemap[c]
        else:
            output += c

    with open(filename + '.decoded', 'w') as fp:
        fp.write(output)


if __name__ == '__main__':
    assert 1 < len(sys.argv) < 3

    decode_mode = False
    if len(sys.argv) == 3:
        assert sys.argv[2] == '-d'
        decode_mode = True

    filename = sys.argv[1]

    if decode_mode:
        decode(filename)
    else:
        encode(filename)
