from dataclasses import dataclass
from typing import List, Optional

import requests
import csv

@dataclass
class Entry:
    title: str
    read: int

@dataclass
class Manga:
    url: str
    title: str
    thumbnail_url: str

def search_title(title: str) -> Optional[Manga]:
    params = {
        "type": "comic",
        "page": 1,
        "limit": 1,
        "tachiyomi": "true",
        "showall": "false",
        "q": title,
        "t": "false",
    }
    headers = { "user-agent": "dummy" }
    res = requests.get("https://api.comick.cc/v1.0/search", params=params, headers=headers)
    if res.status_code != 200:
        return None
    if len(res.json()) != 1:
        return None
    raw = res.json()[0]

    ret = Manga(
        url="/comic/" + raw["hid"] + "#",
        title=raw["title"],
        thumbnail_url=raw["cover_url"]
    )

    print(ret)
    return ret

def get_entries(fname: str) -> List[Entry]:
    with open(fname) as f:
        rows = csv.DictReader(f)
        entries = [Entry(title=r['title'], read=float(r['read'] or '0')) for r in rows]

    return entries

def load_export(fname: str) -> List[Manga]:
    entries = get_entries(fname)

    return [m for e in entries if (m := search_title(e.title))]
