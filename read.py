from collections import namedtuple

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
nt


def read_file(path):
    with open(path, "r") as fp:
        # skip first two lines
        fp.readline()
        fp.readline()
        lines = fp.readlines()
        return lines


lines = read_file("data/acid.py")
nt._fields

tuples = {}

fields = []
for line in lines:
    start, *rest = line.split("=")
    if len(rest) > 0:
        # useful line
        key = rest[0].split(',')[0]
        if start.strip() in nt._fields:
            print(key)
            try:
                key = float(key)
            except ValueError:
                pass
            fields.append(key)

tuples["acid"] = nt(*fields)
print(tuples)
