from pathlib import Path
from collections import namedtuple

import polars as pl

nt = namedtuple(
    "cargo",
    [
        "id",
        "weight",
        "cargo_label",
        "penalty_lowerbound",
        "single_penalty_length",
        "price_factor",
    ],
)


def read_file(path):
    with open(path, "r") as fp:
        # skip first two lines
        fp.readline()
        fp.readline()
        lines = fp.readlines()
        fields = []
        for line in lines:
            start, *rest = line.split("=")
            if len(rest) > 0:
                # useful line
                key = rest[0].split(",")[0]
                if start.strip() in nt._fields:
                    # remove all quotes from the string
                    key = key.replace('"', "").replace("'", "").strip()
                    try:
                        key = float(key)
                    except ValueError:
                        pass
                    fields.append(key)
        return nt(*fields)


cargos = {}
for f in Path("data/").iterdir():
    cargo_name = f.stem
    if cargo_name.startswith("__"):
        continue
    fields = read_file(f)
    cargos[cargo_name] = fields

pl.DataFrame(list(cargos.values())).write_csv("cargo_stats.csv")
