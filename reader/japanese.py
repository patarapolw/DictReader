import os
import re
import json
import lxml.etree as etree
import xmltodict

from common import wrapper, common


class edict:
    def __init__(self):
        with open(os.path.join('database', 'edict2'), encoding='euc-jp') as f:
            self.raw = f.readlines()

        self.data = dict()
        self.rawdata = dict()
        for line in self.raw:
            matchObj = re.match('(.*) \[(.*)\] /(.*)/\n', line)
            if matchObj is None:
                continue
            word, kana, pre_english = matchObj.groups()

            type = None
            uses = None
            see_also = None
            try:
                type, pre_english = re.match('\(([^)]*)\) (.*)', pre_english).groups()
                uses, pre_english = re.match('{([^}]*)} (.*)', pre_english).groups()
                see_also, pre_english = re.match('\(See ([^)]*)\) (.*)', pre_english).groups()
            except AttributeError:
                pass

            english = pre_english.split('/')

            result = dictResult(**{
                'kana': kana,
                'english': english,
                'type': type,
                'uses': uses,
                'see_also': see_also
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
        self.raw = etree.parse(os.path.join('database', 'JMdict_e'))
        self.entries = self.raw.xpath('//entry')
        self.allWords = set()
        self.allWords.update(self.findWords(self.raw))

    @wrapper.iter2list
    def getRaw(self, word):
        for entry in self.entries:
            if word in self.findWords(entry):
                yield xmltodict.parse(etree.tostring(entry))

    @wrapper.iter2list
    def get(self, word):
        for item in self.getRaw(word):
            rawResult = common.flatten(item)
            result = dictResult(**rawResult)
            yield dict(result)

    @staticmethod
    @wrapper.iter2list
    def findWords(entry):
        for item in entry.findall('.//keb'):
            yield item.text
        for item in entry.findall('.//reb'):
            yield item.text


class dictResult:
    def __init__(self, **kwargs):
        self.result = dict()
        # {
        #     'kana': None,
        #     'english': None,
        #     'type': None,
        #     'uses': None,
        #     'see_also': None
        # }
        self.result.update(kwargs)

        for k in ('vocab', 'kana', 'english', 'type', 'uses', 'see_also', 'entry_id'):
            if k not in kwargs.keys():
                if k == 'vocab':
                    try:
                        self.result[k] = self.result.pop('entry_k_ele_keb')
                    except KeyError:
                        try:
                            self.result[k] = self.result.pop('entry_k_ele')
                        except KeyError:
                            pass
                elif k == 'kana':
                    try:
                        self.result[k] = self.result.pop('entry_r_ele_reb')
                    except KeyError:
                        try:
                            self.result[k] = self.result.pop('entry_r_ele')
                        except KeyError:
                            pass
                elif k == 'english':
                    try:
                        self.result[k] = self.result.pop('entry_sense_gloss')
                    except KeyError:
                        try:
                            self.result[k] = self.result.pop('entry_sense')
                        except KeyError:
                            pass
                elif k == 'type':
                    try:
                        self.result[k] = self.result.pop('entry_sense_pos')
                    except KeyError:
                        pass
                elif k == 'uses':
                    try:
                        self.result[k] = self.result.pop('entry_sense_field')
                    except KeyError:
                        pass
                elif k == 'see_also':
                    try:
                        self.result[k] = self.result.pop('entry_sense_xref')
                    except KeyError:
                        pass
                elif k == 'entry_id':
                    try:
                        self.result[k] = self.result.pop('entry_ent_seq')
                    except KeyError:
                        pass

    def __iter__(self):
        for k,v in self.result.items():
            yield k, v


if __name__ == '__main__':
    os.chdir('..')

    d = edict()
    print(json.dumps(d.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
    print(json.dumps(d.get('２０００年問題対応'), indent=4, ensure_ascii=False))

    d = JMdict()
    print(json.dumps(d.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
    print(json.dumps(d.get('２０００年問題対応'), indent=4, ensure_ascii=False))
    with common.speedTest('Checking all words'):
        allKeys = dict()
        for entry in d.entries:
            result = xmltodict.parse(etree.tostring(entry))
            keys = common.flatten(result).keys()
            for key in keys:
                if key not in allKeys.keys():
                    allKeys[key] = 1
                else:
                    allKeys[key] += 1

        d_view = [(v, k) for k, v in allKeys.items()]
        d_view.sort(reverse=True)  # natively sort tuples by first element
        for v, k in d_view:
            print("%s: %d" % (k, v))
