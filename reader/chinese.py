import re
import os

from reader import dictEntry

class cedict:
    def __init__(self):
        with open(os.path.join('database', 'chinese', 'cedict_ts.u8'), encoding='utf-8') as f:
            raw = f.readlines()

        self.data = dict()
        self.rawdata = dict()
        for line in raw:
            matchObj = re.match('(.*) (.*) \[(.*)\] /(.*)/\n', line)
            if matchObj is None:
                continue
            trad, simp, pinyin, pre_english = matchObj.groups()

            pre_result = {
                'traditional': trad,
                'simplified': simp,
                'reading': pinyin
            }

            english = []
            for item in pre_english.split('/'):
                if 'CL' in item:
                    pre_result['CL'] = item[3:]
                elif 'see also' in item:
                    pre_result['see also'] = item[9:]
                else:
                    english += [item]

            pre_result['english'] = english

            for word in (trad, simp):
                result = dictEntry.dictResult(**pre_result)
                if word not in self.data.keys():
                    self.data[word] = [dict(result)]
                else:
                    self.data[word] += [dict(result)]

                if word not in self.rawdata.keys():
                    self.rawdata[word] = [line]
                else:
                    self.rawdata[word] += [line]

    def getRaw(self, word):
        if word in self.rawdata:
            return self.rawdata[word]
        else:
            return []

    def get(self, word):
        if word in self.data:
            return self.data[word]
        else:
            return []


if __name__ == '__main__':
    os.chdir('..')

    d = cedict()
    print(d.get('汉字'))
