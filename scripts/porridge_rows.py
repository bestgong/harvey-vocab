#!/usr/bin/env python3
"""The Magic Porridge Pot（第二套图书馆 L3-6）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-6 The Magic Porridge Pot"
DATE = "2026-10-10"

INTRO = "This story is about hungry Hannah, an old woman, a greedy boy, a magic pot and a LOT of porridge."

# 从 id 2780 开始（The King's Pudding 到 2779）
entries = [
    # ── 总词表第 1 页 ─────────────────────────────
    ("hungry", "adj.", "感到饿的，饥饿的",
     INTRO, "这个故事讲的是___的 Hannah、一位老婆婆、一个贪心的男孩、一口魔法锅和好多好多粥。",
     "hunger n. 饥饿；thirsty 口渴的。"),
    ("share", "v.", "分享",
     "But, when she had some food, she always shared it.", "可是，只要她有一点吃的，她总会___给别人。",
     "share sth. with sb. 与某人分享某物。"),
    ("greedy boy", "n. 短语", "贪婪的男孩",
     "One evening, a greedy boy smelled the porridge.", "一天傍晚，一个___闻到了粥的香味。",
     "greedy 贪心的；greed n. 贪婪。"),
    ("porridge", "n.", "麦片粥",
     INTRO, "这个故事讲的是饥饿的 Hannah、一位老婆婆、一个贪心的男孩、一口魔法锅和好多好多___。",
     "本课标题：The Magic Porridge Pot 魔法粥锅。"),
    ("sigh", "n.", "叹气（声），叹息",
     "Hannah never had enough to eat. \"Sigh!\"", "Hannah 总是吃不饱。\"___！\"",
     "也可作 v. 叹气：She sighed."),
    ("honey", "n.", "蜂蜜",
     "One day, Hannah found some honey in the forest.", "有一天，Hannah 在森林里找到了一些___。",
     "另义：亲爱的（称呼）；bee 蜜蜂。"),
    ("carrying", "v.", "携带，提（carry 的现在分词）",
     "The woman was carrying an empty pot.", "老婆婆___着一口空锅。",
     "carry-carried-carried；carrying 现在分词。"),
    ("Would you like…", "句型", "你想不想……，您是否希望……",
     "\"Would you like some honey?\" asked Hannah.", "\"___来点蜂蜜？\"Hannah 问。",
     "礼貌询问；回答 Yes, please. / No, thank you."),
    ("One good turn deserves another.", "句型", "善有善报；礼尚往来",
     "\"One good turn deserves another.\"", "\"___\"老婆婆说。",
     "turn n. 此处指“好事、帮助”；deserve v. 值得。"),
    ("empty", "adj.", "空的",
     "\"But your pot is empty.\"", "\"可是你的锅是___。\"",
     "反义词：full 满的。"),
    ("That doesn't matter.", "句型", "那不重要",
     "\"That doesn't matter.\"", "老婆婆笑了：\"___\"",
     "matter v. 要紧；It doesn't matter. 没关系。"),
    ("magic words", "n. 短语", "咒语",
     "\"You just need to know the magic words.\"", "你只需要知道___就行。",
     "magic 魔法的；L3-1 学过 magic pear tree。"),
    ("fill the pot", "v. 短语", "装满了罐子",
     "Hot porridge filled the pot.", "热粥___。",
     "fill 装满；pot 锅、罐。"),
    ("delicious meal", "n. 短语", "美味的一餐",
     "Hannah and the woman ate a delicious meal of porridge and honey.", "Hannah 和老婆婆吃了一顿有粥有蜂蜜的___。",
     "delicious 美味的；meal 一餐。"),
    ("keep", "v.", "保有，留下",
     "\"You can keep the pot,\" said the woman.", "\"这口锅你可以___，\"老婆婆说。",
     "keep-kept-kept（不规则动词）。"),
    ("never", "v.", "决不，永不，不会",
     "\"Remember the magic words and you will never be hungry again.\"", "记住咒语，你就___再挨饿了。",
     "词表标 v.，实为副词 adv.。"),
    ("from then on", "短语", "从那时起",
     "From then on, Hannah always had plenty to eat.", "___，Hannah 总有足够的东西吃。",
     "then 那时；from now on 从现在起。"),
    ("have plenty to eat", "v. 短语", "有足够的食物",
     "From then on, Hannah always had plenty to eat.", "从那以后，Hannah 总是___。",
     "plenty 大量、充足；plenty of 许多。"),
    ("stole", "v.", "偷（steal 的过去式）",
     "Then he crept in, stole the pot and ran home.", "然后他溜进屋，___走了锅，跑回了家。",
     "steal-stole-stolen（不规则动词）。"),

    # ── 总词表第 2 页 ─────────────────────────────
    ("start to", "v. 短语", "开始",
     "He saw the pot start to fill with porridge...", "他看见锅___冒出粥来……",
     "start to do = start doing。"),
    ("fill with", "v. 短语", "装满",
     "He saw the pot start to fill with porridge...", "他看见锅里开始___粥……",
     "be filled with 充满。"),
    ("creep in", "v. 短语", "悄悄进入",
     "Then he crept in, stole the pot and ran home.", "然后他___，偷走锅，跑回了家。",
     "creep-crept-crept（L3-4 学过 creep closer）。"),
    ("couldn't wait to", "v. 短语", "迫不及待地",
     "He couldn't wait to say the magic words...", "他___说出咒语……",
     "can't wait to do sth. 等不及要做某事。"),
    ("steaming porridge", "n. 短语", "热气腾腾的粥",
     "Steaming porridge filled the pot.", "___装满了锅。",
     "steam n. 蒸汽 → steaming 冒热气的。"),
    ("dripped over", "v. 短语", "滴在（drip 的过去式）",
     "Porridge dripped over the sides.", "粥从锅边___出来。",
     "drip-dripped（双写 p）。"),
    ("pour onto the floor", "v. 短语", "涌到了地板上",
     "Porridge poured onto the floor.", "粥___。",
     "pour 倾泻；onto 到……上面。"),
    ("fill the room", "v. 短语", "充满房间，满屋子都是",
     "Porridge filled the room.", "粥___。",
     "fill 装满；room 房间。"),
    ("run outside", "v. 短语", "跑了出去",
     "The boy ran outside.", "男孩___。",
     "run-ran-run；outside 外面。"),
    ("drown in", "v. 短语", "溺死在……之中",
     "\"I'll drown in porridge!\"", "我要___粥里了！",
     "drown 淹死；本课为夸张说法。"),
    ("sniff", "v.", "嗅，闻",
     "In her bedroom, Hannah sniffed.", "在卧室里，Hannah 用鼻子___了一下。",
     "sniff 用鼻子吸气闻；smell 闻到。"),
    ("pour down the street", "v. 短语", "涌向街道",
     "Porridge was pouring down the street.", "粥正___。",
     "down the street 沿着街道。"),
    ("at last", "短语", "最后；终于",
     "And at last, the pot stopped.", "___，锅停了下来。",
     "同义：finally、in the end（L3-2 学过）。"),
    ("touch", "v.", "吃，喝",
     "\"I'll never touch porridge again after this!\"", "\"从今以后我再也不___粥了！\"",
     "touch 本义触碰（L3-5 学过）；否定句中引申为“吃、喝”。"),
    ("steal", "v.", "偷窃，盗窃（过去式：stole）",
     "She got her pot back, and no one ever stole it again.", "她拿回了锅，再也没有人___过它。",
     "steal-stole-stolen；thief 小偷。"),
]

assert len(entries) == 34, f"expected 34 entries, got {len(entries)}"

start_id = 2780
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    rows.append([str(start_id + i), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条；id 范围: {rows[0][0]} - {rows[-1][0]}")
with open("/home/user/workspace/harvey-vocab/scripts/porridge_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("已写入 porridge_rows.json")
