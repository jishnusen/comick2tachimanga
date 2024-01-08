import dataclasses
import sqlite3
from typing import List

from comick import Manga


class TachiDb:
    def __init__(self, db) -> None:
        self.db = sqlite3.connect(db)
        self.comick_source = self.query_comick_source()

    def query_comick_source(self) -> str:
        cur = self.db.cursor()
        cur.execute("SELECT id FROM Source WHERE name=\"Comick\" AND lang=\"all\"")
        return cur.fetchone()[0]

    def remove_comick_tracked(self) -> None:
        cur = self.db.cursor()
        cur.execute("DELETE FROM Manga WHERE source=?", (self.comick_source,))

    def insert_manga(self, m: Manga) -> None:
        cols = [f.name for f in dataclasses.fields(m)]
        vals = [getattr(m, c) for c in cols]

        cols += ["in_library", "source"]
        vals += [1, self.comick_source]

        cur = self.db.cursor()
        params = ", ".join("?" * len(cols))
        cur.execute(f"INSERT INTO Manga ({', '.join(cols)}) VALUES({params})", vals)

    def titles(self) -> List[str]:
        cur = self.db.cursor()
        cur.execute("SELECT title FROM Manga")
        return cur.fetchall()

    def commit(self) -> None:
        self.db.commit()
