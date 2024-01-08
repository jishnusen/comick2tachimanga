#!/usr/bin/env python3

import sys

from comick import get_entries
from tachidb import TachiDb


def main(export, db_file) -> None:
    exp = get_entries(export)
    db = TachiDb(db_file)

    for e in exp:
        db.mark_read(e.title, e.read)
    db.commit()

if __name__ == "__main__":
    main(*sys.argv[1:])
