# DictReader

This project is intended to help read JMdict and EDICT -- online dictionaries for Japanese. I planned to add ones of Chinese and CJK in the future.

## Operations

```python
from reader import japanese as jp
import json

edict = jp.edict()
print(json.dumps(edict.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
print(json.dumps(edict.get('２０００年問題対応'), indent=4, ensure_ascii=False))

jm_dict = jp.JMdict()
print(json.dumps(jm_dict.getRaw('２０００年問題対応'), indent=4, ensure_ascii=False))
print(json.dumps(jm_dict.get('２０００年問題対応'), indent=4, ensure_ascii=False))
```

## Resulting format

```
{
    'vocab': vocab,
    'kana': kana,
    'english': english,
    'type': type,
    'uses': uses,
    'see_also': see_also,
    'entry_id': entry_id
}
```

I have to plan to improve the resulting format from `get`. EDICT is quite hard, as the [specification](http://edrdg.org/jmdict/edict_doc.html) is quite old.

As for JMdict, there is quite a [clear spec](http://edrdg.org/jmdict/jmdict_dtd_h.html), but how to actually implement it is in my thought process in the Google Spreadsheet here: 
https://docs.google.com/spreadsheets/d/15SwRL96IHjyCwAm2PhGIMkkEwDBtFDuvxtLgUwIlmXc/edit?usp=sharing
