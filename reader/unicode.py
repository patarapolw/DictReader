import os
import re

class variant:
    def __init__(self):
        with open(os.path.join('database', 'unicode', 'Unihan', 'Unihan_Variants.txt'), encoding='ascii') as f:
            raw = f.readlines()

        self.data = dict()
        self.rawdata = dict()
        for line in raw:
            if line[0] == '#':
                continue

            matchObj = re.match('([^ ]*)\t([^ ]*)\t(.*)\n', line)
            if matchObj is None:
                continue
            pre_char, type, pre_variant = matchObj.groups()

            char = unicodePoint2char(pre_char[2:])
            variants_keys = pre_variant.split(' ')
            variants = []
            for i, variant_keys in enumerate(variants_keys):
                try:
                    variant, keys = variant_keys.split('<')
                except ValueError:
                    variant, keys = variant_keys, ''
                # print(pre_char, variant[2:])
                variants.append((unicodePoint2char(variant[2:])
                                 , keys.split(',')))

            result = {
                'type': type,
                'variants': variants
            }

            if char not in self.data.keys():
                self.data[char] = [dict(result)]
            else:
                self.data[char] += [dict(result)]

            if char not in self.rawdata.keys():
                self.rawdata[char] = [line]
            else:
                self.rawdata[char] += [line]

    def get(self, char):
        return self.data[char]

    def getRaw(self, char):
        return self.rawdata[char]


def unicodePoint2char(unicodePoint):
    if unicodePoint == '':
        return ''
    else:
        return chr(int(unicodePoint, 16))


if __name__ == '__main__':
    os.chdir('..')
    # print(unicodePoint2char('3400'))

    d = variant()
    print(d.get('一'))
