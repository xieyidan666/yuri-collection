# data.py
import requests
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Work:
    id: int
    title: str
    category: str
    author: str
    rating: float
    tags: List[str]
    description: str
    cover_url: Optional[str] = None
    year: Optional[int] = None
    platforms: Optional[Dict[str, str]] = None


def fetch_yuri_anime() -> List[Work]:
    """从 AniList API 获取百合动漫"""
    query = """
    query {
      Page(page: 1, perPage: 30) {
        media(type: ANIME, tag_in: ["Yuri", "Girls Love"], sort: SCORE_DESC) {
          id
          title { chinese native romaji }
          averageScore
          startDate { year }
          genres
          description(asHtml: false)
          coverImage { large }
          tags { name }
          siteUrl
        }
      }
    }
    """
    try:
        resp = requests.post(
            "https://graphql.anilist.co",
            json={"query": query},
            timeout=10
        )
        resp.raise_for_status()
        items = resp.json()["data"]["Page"]["media"]
        works = []
        for i, item in enumerate(items):
            title = (item["title"].get("chinese") or
                     item["title"].get("native") or
                     item["title"].get("romaji") or "未知")
            rating = round((item.get("averageScore") or 0) / 10, 1)
            year = item.get("startDate", {}).get("year")
            desc = item.get("description") or "暂无简介"
            desc = desc[:300]
            tags = [t["name"] for t in (item.get("tags") or [])[:6]]
            cover = (item.get("coverImage") or {}).get("large")
            site = item.get("siteUrl", "https://anilist.co")
            works.append(Work(
                id=i + 100,
                title=title,
                category="动漫",
                author="AniList",
                rating=rating,
                tags=tags,
                description=desc,
                cover_url=cover,
                year=year,
                platforms={"AniList": site, "Bilibili": "https://www.bilibili.com/"}
            ))
        return works
    except Exception as e:
        return []


def fetch_yuri_manga() -> List[Work]:
    """从 AniList API 获取百合漫画/文学"""
    query = """
    query {
      Page(page: 1, perPage: 20) {
        media(type: MANGA, tag_in: ["Yuri", "Girls Love"], sort: SCORE_DESC) {
          id
          title { chinese native romaji }
          averageScore
          startDate { year }
          description(asHtml: false)
          coverImage { large }
          tags { name }
          siteUrl
          staff { edges { node { name { full } } role } }
        }
      }
    }
    """
    try:
        resp = requests.post(
            "https://graphql.anilist.co",
            json={"query": query},
            timeout=10
        )
        resp.raise_for_status()
        items = resp.json()["data"]["Page"]["media"]
        works = []
        for i, item in enumerate(items):
            title = (item["title"].get("chinese") or
                     item["title"].get("native") or
                     item["title"].get("romaji") or "未知")
            rating = round((item.get("averageScore") or 0) / 10, 1)
            year = item.get("startDate", {}).get("year")
            desc = item.get("description") or "暂无简介"
            desc = desc[:300]
            tags = [t["name"] for t in (item.get("tags") or [])[:6]]
            cover = (item.get("coverImage") or {}).get("large")
            site = item.get("siteUrl", "https://anilist.co")
            # 获取作者
            author = "未知"
            for edge in (item.get("staff", {}).get("edges") or []):
                if "Story" in edge.get("role", "") or "Art" in edge.get("role", ""):
                    author = edge["node"]["name"]["full"]
                    break
            works.append(Work(
                id=i + 200,
                title=title,
                category="文学",
                author=author,
                rating=rating,
                tags=tags,
                description=desc,
                cover_url=cover,
                year=year,
                platforms={"AniList": site}
            ))
        return works
    except Exception as e:
        return []


# 静态影视数据（API暂无免费影视源）
MOVIE_WORKS = [
    Work(
        id=301, title="《燃烧女子的肖像》", category="影视", author="瑟琳·席安玛",
        rating=9.3, tags=["历史", "艺术", "法国", "HE"],
        description="1760年的法国，女画家玛莉安受托为即将出嫁的富家小姐艾洛伊兹绘制肖像。在孤岛般的城堡中，两人点燃了禁忌的爱火。",
        year=2019, platforms={"Bilibili": "https://www.bilibili.com/", "腾讯视频": "https://v.qq.com/"}
    ),
    Work(
        id=302, title="《阿黛尔的生活》", category="影视", author="阿布戴·柯西胥",
        rating=8.5, tags=["法国", "现实", "虐心", "成长"],
        description="女孩阿黛尔在街头偶遇蓝发女孩艾玛，经历热恋、同居，也遭遇现实冲击。关于成长与失去的残酷青春物语。",
        year=2013, platforms={"Bilibili": "https://www.bilibili.com/"}
    ),
    Work(
        id=303, title="《指匠情挑》", category="影视", author="莎拉·沃特斯",
        rating=9.1, tags=["英国", "犯罪", "反转", "虐心"],
        description="BBC出品，维多利亚时代伦敦，一场针对富家女的骗局背后，阴谋与真情交织，多重反转令人叫绝。",
        year=2005, platforms={"Bilibili": "https://www.bilibili.com/"}
    ),
    Work(
        id=304, title="《请回答1988》", category="影视", author="申源浩",
        rating=9.7, tags=["韩国", "青春", "治愈", "友情"],
        description="1988年首尔双门洞，五个家庭的温情故事，那个年代的青春与爱情。",
        year=2015, platforms={"Netflix": "https://www.netflix.com/", "腾讯视频": "https://v.qq.com/"}
    ),
    Work(
        id=305, title="《橘子不是唯一的水果》", category="影视", author="BBC",
        rating=8.3, tags=["英国", "成长", "宗教", "HE"],
        description="少女珍妮特在宗教家庭中成长，发现自己爱上同性，与家庭和信仰的挣扎。BBC经典作品。",
        year=1990, platforms={"Bilibili": "https://www.bilibili.com/"}
    ),
]


def get_all_works() -> List[Work]:
    """获取所有作品（API + 静态）"""
    anime = fetch_yuri_anime()
    manga = fetch_yuri_manga()
    return manga + MOVIE_WORKS + anime


def get_work_by_id(work_id: int, all_works: List[Work] = None):
    if all_works is None:
        all_works = get_all_works()
    for w in all_works:
        if w.id == work_id:
            return w
    return None


def get_works_by_category(category: str, all_works: List[Work] = None) -> List[Work]:
    if all_works is None:
        all_works = get_all_works()
    return [w for w in all_works if w.category == category]


# 兼容旧代码
SAMPLE_WORKS = MOVIE_WORKS
