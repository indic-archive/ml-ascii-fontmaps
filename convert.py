import csv
import json
import os
import re


class Convert():
    charmap = {}
    pre = ["േ", "െ", "ൈ", "ോ", "ൊ", "ൌ", "ൗ", "്ര"]
    post = ["്യ", "്വ"]

    def __init__(self, dirpath="maps"):
        self.dirpath = dirpath
        with open(os.path.join(dirpath, "index.json"), "r") as f:
            self.map_index = json.loads(f.read())

    def index(self):
        return self.map_index

    def load(self, fontname):
        if fontname not in self.map_index:
            raise Exception("'{}' not found in font maps".format(fontname))

        with open(os.path.join(self.dirpath, self.map_index[fontname]), "r") as f:
            self.charmap[fontname] = json.loads(f.read())

    def convert(self, txt, fontname):
        m = self.charmap[fontname]
        out = []
        txt = list(txt)
        n = 0
        while n < len(txt):
            c = txt[n]

            if c == " " or c == "\n" or c not in m:
                out.append(c)
                n += 1
                continue

            v = m[c]

            if v in self.pre:
                if n+2 < len(txt):
                    if m.get(txt[n+1]) == "്ര":
                        out.extend([m.get(txt[n+2], txt[n+2]),
                                    m.get(txt[n+1], txt[n+1]),
                                    v])
                        n += 3
                        continue

                    if m.get(txt[n+2]) in self.post:
                        out.extend([m.get(txt[n+1], txt[n+1]),
                                    m.get(txt[n+2], txt[n+2]),
                                    v])
                        n += 3
                        continue

                if n+1 < len(txt):
                    # Handle two consecutive "െ"s, eg: കൈ
                    if m.get(txt[n+1]) == "െ":
                        out.extend([m.get(txt[n+2], txt[n+2]),
                                   m.get(txt[n+1], txt[n+1]), v])
                        n += 3
                        continue

                    out.extend([m.get(txt[n+1], txt[n+1]), v])
                    n += 2
                    continue

            out.append(v)

            n += 1

        return "".join(out)


if __name__ == "__main__":
    c = Convert("./maps")

    # Load one or more fonts
    font = "ML-TTRevathi"
    c.load(font)

    print(c.convert("DÕmlw", font))
