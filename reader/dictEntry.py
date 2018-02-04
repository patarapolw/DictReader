class dictResult:
    def __init__(self, **kwargs):
        self.result = dict()
        # {
        #     'kana': [],
        #     'english': [],
        #     'type': [],
        #     'uses': [],
        #     'see_also': []
        # }
        self.result.update(kwargs)

        # JMdict comvert
        for k in ('vocab', 'reading', 'english', 'type', 'uses', 'see_also', 'entry_id',
                  'sources (vocab)', 'sources (reading)', 'sense'):
            if k not in kwargs.keys():
                if k == 'vocab':
                    self.result[k] = self.result.pop('entry-k_ele-keb', []) \
                                     + self.result.pop('entry-k_ele', [])
                elif k == 'reading':
                    self.result[k] = self.result.pop('entry-r_ele-reb', []) \
                                     + self.result.pop('entry-r_ele', [])
                elif k == 'english':
                    self.result[k] = self.result.pop('entry-sense-gloss', []) \
                                     + self.result.pop('entry-sense', [])
                elif k == 'type':
                    self.result[k] = self.result.pop('entry-sense-pos', [])
                elif k == 'uses':
                    self.result[k] = self.result.pop('entry-sense-field', [])
                elif k == 'see_also':
                    self.result[k] = self.result.pop('entry-sense-xref', [])
                elif k == 'entry_id':
                    self.result[k] = ''.join(self.result.pop('entry-ent_seq', []))
                elif k == 'sources (vocab)':
                    self.result[k] = self.result.pop('entry-k_ele-ke_pri', [])
                elif k == 'sources (reading)':
                    self.result[k] = self.result.pop('entry-r_ele-re_pri', [])
                elif k == 'sense':
                    self.result[k] = self.result.pop('entry-sense-misc', []) \
                                     + self.result.pop('entry-sense', [])

        clean_dict = self.result.copy()
        for k, v in self.result.items():
            if v == [] or v == '':
                clean_dict.pop(k)
        self.result = clean_dict

    def __iter__(self):
        for k,v in self.result.items():
            yield k, v
