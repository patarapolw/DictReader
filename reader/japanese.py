import os
import re
import json
import lxml.etree as etree
import html

from common import wrapper, common
from reader import dictEntry


class edict2:
    def __init__(self):
        with open(os.path.join('database', 'japanese', 'edict2'), encoding='euc-jp') as f:
            raw = f.readlines()

        self.data = dict()
        self.rawdata = dict()
        for line in raw:
            matchObj = re.match('(.*) \[(.*)\] /(.*)/\n', line)
            if matchObj is None:
                continue
            words, kanas, pre_english = matchObj.groups()

            type = None
            uses = None
            see_also = None
            try:
                type, pre_english = re.match('\(([^)]*)\) (.*)', pre_english).groups()
                uses, pre_english = re.match('{([^}]*)} (.*)', pre_english).groups()
                see_also, pre_english = re.match('\(See ([^)]*)\) (.*)', pre_english).groups()
            except AttributeError:
                pass

            english_plus_entry_id = pre_english.split('/')

            for word in words.split(';'):
                result = dictEntry.dictResult(**{
                    'vocab': words.split(';'),
                    'reading': kanas.split(';'),
                    'english': english_plus_entry_id[:-1],
                    'type': [type], # No fix yet for multiple entries
                    'uses': [uses], # No fix yet for multiple entries
                    'see_also': [see_also], # No fix yet for multiple entries
                    'entry_id': english_plus_entry_id[-1]
                })
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


class JMdict:
    def __init__(self):
        self.raw = etree.parse(os.path.join('database', 'japanese', 'JMdict_e'))
        self.entries = self.raw.xpath('//entry')
        self.allWords = set()
        self.allWords.update(self.findWords(self.raw))

    @wrapper.iter2list
    def getRaw(self, word):
        for entry in self.entries:
            if word in self.findWords(entry):
                yield html.unescape(etree.tostring(entry).decode('utf8'))

    @wrapper.iter2list
    def get(self, word):
        for item in self.getRaw(word):
            rawResult = common.xml2flatDict(item)
            result = dictEntry.dictResult(**rawResult)
            yield dict(result)

    @staticmethod
    @wrapper.iter2list
    def findWords(entry):
        for item in entry.findall('.//keb'):
            yield item.text
        for item in entry.findall('.//reb'):
            yield item.text


if __name__ == '__main__':
    os.chdir('..')

    d = edict2()
    print(json.dumps(d.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
    print(json.dumps(d.get('２０００年問題対応'), indent=4, ensure_ascii=False))

    d = JMdict()
    # for word in d.allWords:
    #     print(d.get(word))
    print(json.dumps(d.get('２０００年問題対応'), indent=4, ensure_ascii=False))
    # with common.speedTest('Checking all words'):
    #     allKeys = dict()
    #     for entry in d.entries:
    #         to_convert = etree.tostring(entry)
    #         # print(to_convert)
    #         keys = common.xml2flatDict(to_convert).keys()
    #         for key in keys:
    #             if key not in allKeys.keys():
    #                 allKeys[key] = 1
    #             else:
    #                 allKeys[key] += 1
    #
    #     d_view = [(v, k) for k, v in allKeys.items()]
    #     d_view.sort(reverse=True)  # natively sort tuples by first element
    #     for v, k in d_view:
    #         print("%s: %d" % (k, v))
