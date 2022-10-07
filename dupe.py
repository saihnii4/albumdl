#!/usr/bin/python
# removes duplicate album entries using le epic sets

import json

class KillMe():
    def __init__(self, kwargs, uniq):
        self.orig = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.__uniq = uniq

    def __hash__(self):
        print(hash(getattr(self, self.__uniq)))
        return hash(getattr(self, self.__uniq))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return getattr(self, self.__uniq)  == getattr(other, self.__uniq)

with open("/home/pur0/.config/mpd-discord-richpresence/config.json", "r") as config:
    data = json.load(config)
    data['covers'] = [cover.orig for cover in set([KillMe(cover, "value") for cover in data['covers']])]

    __import__("pprint").pprint(data)

    config.close()

    with open("/home/pur0/.config/mpd-discord-richpresence/config.json", "w") as config:
        json.dump(data, config)
