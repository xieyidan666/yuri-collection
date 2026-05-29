# data.py
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Work:
    """作品数据类"""
    id: int
    title: str
    category: str  # "文学", "影视", "动漫"
    author: str
    rating: float
    tags: List[str]
    description: str
    cover_url: Optional[str] = None
    year: Optional[int] = None
    platforms: Optional[Dict[str, str]] = None  # 新增字段：观看渠道

# 样本数据（更新了platform字段）
SAMPLE_WORKS = [
    # --- 文学作品 ---
    Work(
        id=1, title="《她与她的秘密》", category="文学", author="佚名",
        rating=9.2, tags=["现代", "纯爱", "职场", "HE"],
        description="在繁华的都市中，两位职场女性因为一个偶然的项目相遇。她是雷厉风行的市场总监，她是温柔细腻的设计师。在一次次合作中，她们发现了彼此的秘密——那个只属于她们的、温暖而坚定的爱情。",
        year=2021,
        platforms={
            "豆瓣阅读": "https://read.douban.com/",
            "晋江文学城": "https://www.jjwxc.net/"
        }
    ),
    Work(
        id=2, title="《隔墙有耳》", category="文学", author="匿名者A",
        rating=8.8, tags=["悬疑", "虐心", "古风", "朝堂"],
        description="宫廷深处，两位女子因一场阴谋纠缠在一起。她是权倾朝野的女将军，她是深居简出的女医官。在权力的棋局中，她们是彼此的棋子，也是唯一的软肋。爱，在流言蜚语和刀光剑影中悄然生长。",
        year=2019,
        platforms={
            "晋江文学城": "https://www.jjwxc.net/"
        }
    ),
    Work(
        id=3, title="《夏日限定》", category="文学", author="小太阳",
        rating=9.5, tags=["校园", "青春", "治愈", "HE"],
        description="那个夏天，阳光正好，微风不燥。两位高中女孩，因为一次图书馆的偶遇，开启了属于她们的青春故事。一起看过的日落，一起写过的情书，都是夏日里最珍贵的限定记忆。",
        year=2022,
        platforms={
            "豆瓣阅读": "https://read.douban.com/",
            "微信读书": "https://weread.qq.com/"
        }
    ),
    # --- 影视作品 ---
    Work(
        id=4, title="《燃烧女子的肖像》", category="影视", author="瑟琳·席安玛",
        rating=9.3, tags=["历史", "艺术", "法国", "HE"],
        description="1760年的法国，女画家玛莉安受托为即将出嫁的富家小姐艾洛伊兹绘制肖像。在孤岛般的城堡中，两人在日复一日的相处中，从审视到吸引，最终点燃了那个时代禁忌的爱火。镜头如画，情感如诗。",
        year=2019,
        platforms={
            "Bilibili": "https://www.bilibili.com/",
            "腾讯视频": "https://v.qq.com/"
        }
    ),
    Work(
        id=5, title="《阿黛尔的生活》", category="影视", author="阿布戴·柯西胥",
        rating=8.5, tags=["法国", "现实", "虐心", "成长"],
        description="女孩阿黛尔，在一次街头偶遇中，被蓝发女孩艾玛深深吸引。她们经历了从热恋到同居的甜蜜，也遭遇了来自社会、家庭的现实冲击。爱是如何开始，又是如何消逝的？这是一部关于成长与失去的残酷青春物语。",
        year=2013,
        platforms={
            "Bilibili": "https://www.bilibili.com/",
            "爱奇艺": "https://www.iqiyi.com/"
        }
    ),
    Work(
        id=6, title="《指匠情挑》", category="影视", author="莎拉·沃特斯",
        rating=9.1, tags=["英国", "犯罪", "反转", "虐心"],
        description="BBC出品，必属精品。故事发生在维多利亚时代的伦敦，从小在犯罪集团长大的苏，被卷入一场针对富家女莫德的骗局。然而，在阴谋与欺骗的背后，一段跨越阶级与身份的复杂感情悄然展开。",
        year=2005,
        platforms={
            "Bilibili": "https://www.bilibili.com/",
            "腾讯视频": "https://v.qq.com/"
        }
    ),
    # --- 动漫作品 ---
    Work(
        id=7, title="《Citrus～柑橘味香气～》", category="动漫", author="サブロウタ",
        rating=7.8, tags=["校园", "傲娇", "姐妹", "纯爱"],
        description="因为父母再婚，原本是活泼辣妹的柚子，与冷静孤高的学霸女高中生芽衣成为了义理姐妹。从最初的处处针锋相对，到逐渐被对方吸引，两人之间酸酸甜甜的恋爱故事，就像柑橘的香气，清新又让人心动。",
        year=2018,
        platforms={
            "Bilibili": "https://www.bilibili.com/",
            "爱奇艺": "https://www.iqiyi.com/"
        }
    ),
    Work(
        id=8, title="《终将成为你》", category="动漫", author="仲谷鳰",
        rating=9.0, tags=["校园", "心理", "纯爱", "治愈"],
        description="不懂恋爱为何物的少女侑，遇见了学生会长七海灯子。灯子向侑坦白了自己无法喜欢上别人的烦恼，而侑也恰好无法对任何人产生心动。两人本以为找到了最合适的相处模式，却在日常的点点滴滴中，悄然改变了彼此。",
        year=2018,
        platforms={
            "Bilibili": "https://www.bilibili.com/",
            "腾讯视频": "https://v.qq.com/"
        }
    ),
    Work(
        id=9, title="《利兹与青鸟》", category="动漫", author="京都动画",
        rating=9.4, tags=["音乐", "治愈", "艺术", "青春"],
        description="《吹响吧！上低音号》的衍生作品，但独立成篇。讲述了负责双簧管的霙和负责长笛的希美之间细腻、纯粹又有些微妙的关系。一个想要紧紧抓住，一个想要展翅高飞。如同童话《利兹与青鸟》一般，爱是给予，也是放手。",
        year=2018,
        platforms={
            "Bilibili": "https://www.bilibili.com/",
            "腾讯视频": "https://v.qq.com/"
        }
    ),
    Work(
        id=10, title="《轻声密语》", category="动漫", author="池田学志",
        rating=8.0, tags=["校园", "日常", "喜剧", "纯爱"],
        description="性格内向的优等生利夏，其实一直暗恋着同班的活泼少女枫。她隐瞒着自己的心意，以朋友的身份陪伴在枫身边。然而，枫却对青梅竹马的男生抱有好感。一场关于暗恋、友情和成长的多角关系就此展开。",
        year=2009,
        platforms={
            "Bilibili": "https://www.bilibili.com/"
        }
    ),
]# 工具函数
def get_work_by_id(work_id: int) -> Optional[Work]:
    """根据ID获取作品"""
    for work in SAMPLE_WORKS:
        if work.id == work_id:
            return work
    return None

def get_works_by_category(category: str) -> List[Work]:
    """根据分类获取作品列表"""
    return [w for w in SAMPLE_WORKS if w.category == category]

def get_recommendations(count: int = 6) -> List[Work]:
    """获取推荐作品（这里简单返回评分最高的作品）"""
    sorted_works = sorted(SAMPLE_WORKS, key=lambda x: x.rating, reverse=True)
    return sorted_works[:count]