import collections
from time import time
import xmltodict
import lxml.etree as etree
import re


def flatten(d, parent_key='', sep='-'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def xml2flatDict(xml, sep='-'):
    i = 0
    result = {}
    allKeys = flatten(xmltodict.parse(xml), sep=sep).keys()
    for key in allKeys:
        key = re.sub('{}?[@#][^/]*{}?'.format(sep, sep), '', key)
        xpath = '/{}'.format('/'.join(key.split(sep)))
        if '#' in xpath:
            print(xpath)
            i += 1
            continue
        if '@' in xpath:
            print(xpath)
            i += 1
            continue
        tree = etree.fromstring(xml)
        values = tree.xpath(xpath)
        try:
            if key not in result.keys():
                result[key] = [x.text.strip() for x in values]
            else:
                result[key] += [x.text.strip() for x in values]
        except AttributeError:
            pass

    if i != 0:
        print("Missed {} paths".format(i))
    return result


class speedTest:
    def __init__(self, testName):
        self.funcName = testName

    def __enter__(self):
        print('Started: {}'.format(self.funcName))
        self.init_time = time()
        return self

    def __exit__(self, type, value, tb):
        print('Finished: {} in: {} seconds'.format(self.funcName, time() - self.init_time))


if __name__ == '__main__':
    xml = '''
    <entry>
<ent_seq>2138230</ent_seq>
<k_ele>
<keb>２０００年問題対応</keb>
</k_ele>
<r_ele>
<reb>にせんねんもんだいたいおう</reb>
</r_ele>
<sense>
<pos>expressions (phrases, clauses, etc.)</pos>
<xref>２０００年対応・にせんねんたいおう</xref>
<field>computer terminology</field>
<gloss>Y2K compliant</gloss>
</sense>
</entry>
    '''
    result = xml2flatDict(xml)
    print(result)