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
