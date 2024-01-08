from dataclasses import dataclass
from typing import List, Optional

import requests


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

def load_export(csv: str) -> List[Manga]:
    names = []
    with open(csv) as f:
        names = [l.split(",")[0] for l in f.readlines()]

    return [m for n in names if (m := search_title(n))]

