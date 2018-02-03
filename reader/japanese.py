import os
import re
import json
import lxml.etree as etree
import html
import xmltodict
import collections


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

            result = {
                'kana': kana,
                'english': english,
                'type': type,
                'uses': uses,
                'see_also': see_also
            }
            if word not in self.data.keys():
                self.data[word] = [result]
            else:
                self.data[word] += [result]

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

    def generateRaw(self, word):
        for entry in self.entries:
            if word in html.unescape(etree.tostring(entry).decode('utf8')):
                yield xmltodict.parse(etree.tostring(entry))

    def getRaw(self, word):
        return list(self.generateRaw(word))

    def get(self, word):
        output = []
        for item in self.generateRaw(word):
            result = flatten(item)
            result.update({
                'kana': result.pop('entry_r_ele_reb'),
                'english': result.pop('entry_sense_gloss'),
                'type': result.pop('entry_sense_pos'),
                'uses': result.pop('entry_sense_field'),
                'see_also': result.pop('entry_sense_xref')
            })
            output += [result]
        return output


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


if __name__ == '__main__':
    os.chdir('..')

    d = edict()
    print(json.dumps(d.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
    print(json.dumps(d.get('２０００年問題対応'), indent=4, ensure_ascii=False))

    d = JMdict()
    print(json.dumps(d.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
    print(json.dumps(d.get('２０００年問題対応'), indent=4, ensure_ascii=False))
