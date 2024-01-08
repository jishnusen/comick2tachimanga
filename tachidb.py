import dataclasses
import sqlite3
from typing import Dict

from comick import Manga, get_entries


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

    def mark_read(self, title: str, upto: float) -> None:
        cur = self.db.cursor()
        cur.execute(f"UPDATE Chapter SET read = 1 WHERE manga=? AND chapter_number<=?", (self.titles().get(title), upto))

    def titles(self) -> Dict[str, int]:
        cur = self.db.cursor()
        cur.execute("SELECT title, id FROM Manga")
        return dict(cur.fetchall())

    def commit(self) -> None:
        self.db.commit()

db = TachiDb("/home/jishnu/Downloads/backup/tachimanga.db")

titles = db.titles()
db.mark_read('The Knight King Who Returned with a God', 42.0)
db.commit()
