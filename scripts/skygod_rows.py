#!/usr/bin/env python3
"""The Leopard and The Sky God（第二套图书馆 L3-8）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-8 The Leopard and The Sky God"
DATE = "2026-10-20"

INTRO = "This story is about the Sky God, the leopard, his drum, the python, the elephant and the tortoise."

# 从 id 2857 开始（Chicken Licken 到 2856）
entries = [
    # ── 开场角色 ─────────────────────────────
    ("Sky God", "n. 短语", "天神",
     INTRO, "这个故事讲的是___、豹子、他的鼓、巨蟒、大象和陆龟。",
     "sky 天空 + god 神；非洲民间故事角色。"),
    ("leopard", "n.", "豹",
     INTRO, "这个故事讲的是天神、___、他的鼓、巨蟒、大象和陆龟。",
     "大型猫科动物，身上有斑点。"),
    ("drum", "n.", "鼓",
     INTRO, "这个故事讲的是天神、豹子、他的___、巨蟒、大象和陆龟。",
     "L3-5 学过 drum；本课故事主角之一。"),
    ("python", "n.", "巨蟒",
     INTRO, "这个故事讲的是天神、豹子、他的鼓、___、大象和陆龟。",
     "大蟒蛇；编程语言 Python 即以蟒蛇命名。"),
    ("tortoise", "n.", "陆龟",
     INTRO, "这个故事讲的是天神、豹子、他的鼓、巨蟒、大象和___。",
     "陆龟；turtle 多指海龟。"),

    # ── 天上的鼓声 ─────────────────────────────
    ("long ago", "短语", "很久以前",
     "Long ago, when the world was new, the animals lived in the forest.", "___，世界刚形成的时候，动物们住在森林里。",
     "long long ago 很久很久以前（童话开头）。"),
    ("high up above", "短语", "高空中",
     "High up above lived the Sky God.", "___住着天神。",
     "high up 高处；above 在……上方。"),
    ("wonderful", "adj.", "绝妙的，极好的",
     "One day, the Sky God heard a wonderful sound.", "有一天，天神听到一阵___的声音。",
     "wonder 奇迹 → wonderful。"),
    ("lean down", "v. 短语", "俯下身来（过去式：leaned）",
     "He leaned down and looked through the trees.", "他___，透过树木看下去。",
     "lean 斜靠、俯身。"),
    ("look through the tree", "v. 短语", "透过树看",
     "He leaned down and looked through the trees.", "他俯下身，___。",
     "look through 透过……看；through 穿过。"),
    ("play drum", "v. 短语", "打鼓",
     "There was the leopard, playing a great big drum.", "豹子正在那里___。",
     "play the drum 更常用。"),
    ("high and low", "短语", "时而高时而低",
     "He played high and low.", "他敲得___。",
     "search high and low 到处寻找。"),
    ("soft and loud", "短语", "时而轻时而响",
     "He played soft and loud!", "他敲得___！",
     "soft 轻柔（上册学过）；loud 响亮。"),
    ("May I try it?", "句型", "我可以试试吗？",
     "\"That's a fine drum. May I try it?\"", "\"这鼓真好。___？\"",
     "May I…? 礼貌请求。"),
    ("shake head", "v. 短语", "摇摇头（过去式：shook）",
     "\"Sorry,\" said the leopard. He shook his head.", "\"抱歉，\"豹子说着___。",
     "shake-shook-shaken（不规则动词）。"),
    ("careful", "adj.", "小心的；谨慎的",
     "\"I'll be very careful,\" said the Sky God.", "\"我会非常___的，\"天神说。",
     "be careful 小心；carefully adv.（上册学过）。"),

    # ── 豹子不肯借鼓 ─────────────────────────────
    ("borrow", "v.", "借用",
     "\"I'll borrow it when he goes hunting.\"", "等他去打猎时，我就把它___来。",
     "borrow 借入；lend 借出（上册学过）。"),
    ("go hunting", "v. 短语", "去打猎，去狩猎",
     "\"I'll borrow it when he goes hunting.\"", "等他___，我就把它借来。",
     "go + doing：go fishing 咽钓鱼、go shopping。"),
    ("keep his eye on", "v. 短语", "他密切关注……",
     "But the leopard kept his eye on the drum the whole time.", "可是豹子一直___那只鼓。",
     "keep an eye on 留意、照看。"),
    ("the whole time", "短语", "全部时间（自始至终）",
     "But the leopard kept his eye on the drum the whole time.", "可是豹子盯着那只鼓，___都没松懈过。",
     "whole 全部的；the whole day 一整天。"),
    ("walked away", "v. 短语", "走开，离开（walk 的过去式）",
     "The Sky God walked away.", "天神___。",
     "walk-walked-walked（规则动词）。"),
    ("as usual", "短语", "像往常一样",
     "He found the leopard, playing his drum as usual.", "他发现豹子___在打鼓。",
     "usual 通常的；as usual 固定搭配。"),
    ("May I…", "句型", "我可以……吗？",
     "\"May I look at your drum?\" asked the python.", "\"___看看你的鼓吗？\"巨蟒问。",
     "May I look at…? 我可以看看……吗？"),
    ("sharp claws", "n. 短语", "锋利的爪子",
     "...and he showed his long teeth and his sharp claws.", "他亮出长长的牙齿和___。",
     "claw 爪子；sharp 锋利的。"),
    ("slither away", "v. 短语", "滑走（过去式：slithered，（蛇等）蜿蜒地滑行）",
     "The python slithered away quickly.", "巨蟒飞快地___。",
     "slither 蜿蜒滑行（蛇的动作）。"),
    ("dangerous", "adj.", "危险的，有威胁的",
     "\"It's too dangerous.\"", "\"太___了。\"",
     "danger 危险（L3-5 学过 dangerous jungle）。"),
    ("up in a tree", "短语", "在树上",
     "There he was - up in a tree.", "他在那儿——___。",
     "in a tree 在树上（外物）。"),
    ("Leave me alone.", "句型", "不要打扰我；让我一个人呆会儿",
     "\"Leave me alone.\"", "\"___！\"豹子吼道。",
     "leave sb. alone 不打扰某人。"),
    ("roared", "v.", "咆哮（roar 的过去式）",
     "\"Leave me alone!\" roared the leopard.", "\"别打扰我！\"豹子___。",
     "roar 吼叫（L3-5 学过 roar）。"),
    ("shook and shook", "v. 短语", "摇啊摇（shake 的过去式）",
     "The elephant shook and shook the tree...", "大象把树___……",
     "动词叠用表反复：waited and waited 等啊等。"),
    ("difficult", "adj.", "困难的，难对付的",
     "\"Sorry,\" said the elephant. \"It's too difficult.\"", "\"抱歉，\"大象说，\"太___了。\"",
     "hard 同义；difficulty n. 困难。"),

    # ── 小乌龟的妙计 ─────────────────────────────
    ("now in those days", "短语", "在那个年代",
     "Now in those days the tortoise had no shell.", "___，陆龟还没有壳。",
     "in those days 在那些日子里。"),
    ("shell", "n.", "外壳",
     "Now in those days the tortoise had no shell, only a little soft body.", "在那个年代，陆龟还没有___，只有小小的软软的身体。",
     "egg shell 蛋壳；sea shell 贝壳。"),
    ("wait and see", "短语", "等着瞧",
     "But the tortoise said, \"Wait and see.\"", "陆龟却说：\"___。\"",
     "wait and see 拭目以待。"),
    ("enormous", "adj.", "巨大的，极大的",
     "\"It's enormous,\" said the tortoise.", "\"它___，\"陆龟说。",
     "huge、giant 同义。"),
    ("crawled inside", "v. 短语", "爬进去（crawl 的过去式）",
     "He rolled the drum along the ground and crawled inside.", "他把鼓顺着地面滚过去，___。",
     "crawl 爬行（L3-4 学过 crept）。"),
    ("Like this?", "句型", "像这样？",
     "\"Like this?\"", "\"___？\"豹子问。",
     "同义句：Is it like this? 是这样吗？"),
    ("right inside", "短语", "进去",
     "\"Right inside,\" said the tortoise.", "\"___，\"陆龟说。",
     "right 强调：完全、正好。"),
    ("looked around", "v. 短语", "环顾四周",
     "Then she looked around and spotted the leopard's cooking pot.", "然后她___，发现了豹子的锅。",
     "look around（L3-5 学过）；此处过去式。"),
    ("cooking pot", "n. 短语", "烹饪锅",
     "Then she looked around and spotted the leopard's cooking pot.", "然后她环顾四周，发现了豹子的___。",
     "cook 烹饪 + pot 锅。"),
    ("spot", "v.", "看见，注意到（过去式：spotted）",
     "Then she looked around and spotted the leopard's cooking pot.", "然后她环顾四周，___了豹子的烹饪锅。",
     "另义 n. 点、地点。"),
    ("clap the lid", "v. 短语", "（啪的一声）盖上盖子（过去式：clapped）",
     "Quickly, she clapped the lid over the end of the drum.", "她飞快地把盖子___鼓的一头。",
     "clap 拍手；clapped 双写 p。"),
    ("roll it along to", "v. 短语", "把它滚到……",
     "Then she rolled it along to the Sky God.", "然后她把它___天神那里。",
     "roll 滚（L3-4 学过）。"),
    ("pleased", "adj.", "高兴的",
     "The Sky God was very pleased.", "天神非常___。",
     "be pleased with 对……满意；pleasure n.。"),
    ("I don't want it any more.", "句型", "我不想要了。",
     "\"I don't want it any more. You can have it.\"", "\"___。你拿去吧。\"",
     "not...any more 不再。"),
    ("so that", "短语", "以便；为了",
     "\"I would like a shell on my body... so that nothing can hurt me.\"", "\"我想身上有个壳……___任何东西都伤不到我。\"",
     "so that + 目的从句。"),
    ("stormy", "adj.", "有暴风雨的，风暴的",
     "And, when the weather is stormy, you can still hear him...", "而且，每当天气___，你仍能听见他……",
     "storm 风暴 → stormy。"),
]

assert len(entries) == 47, f"expected 47 entries, got {len(entries)}"

start_id = 2857
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    rows.append([str(start_id + i), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条；id 范围: {rows[0][0]} - {rows[-1][0]}")
with open("/home/user/workspace/harvey-vocab/scripts/skygod_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("已写入 skygod_rows.json")
