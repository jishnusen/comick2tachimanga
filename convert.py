#!/usr/bin/env python3

import sys

from comick import load_export
from tachidb import TachiDb


def main(export, db_file) -> None:
    exp = load_export(export)
    db = TachiDb(db_file)

    db.remove_comick_tracked()
    for m in exp:
        db.insert_manga(m)
    db.commit()

if __name__ == "__main__":
    main(*sys.argv[1:])
