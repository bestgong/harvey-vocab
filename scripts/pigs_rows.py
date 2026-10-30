#!/usr/bin/env python3
"""The Three Little Pigs（第二套图书馆 L3-10）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-10 The Three Little Pigs"
DATE = "2026-10-30"

THREAT = "\"Then I'll huff and I'll puff and I'll blow your house in,\" said the wolf."

# 从 id 2935 开始（The Gingerbread Man 到 2934）
entries = [
    # ── P26 词表 ─────────────────────────────
    ("a pretty little house", "n. 短语", "漂亮的小房子",
     "They lived with their mother in a pretty little house.", "他们和妈妈住在___里。",
     "pretty 漂亮的（另义 adv. 相当）。"),
    ("of our own", "短语", "自己所有的，属于自己的",
     "\"We want homes of our own,\" they said.", "\"我们想要___的家，\"他们说。",
     "own 自己的；of one's own 属于某人自己的。"),
    ("packed their bags", "v. 短语", "收拾他们的行李（pack 的过去式）",
     "So they packed their bags and waved goodbye.", "于是他们___，挥手道别。",
     "pack 收拾（行李）；pack-packing 双写 k。"),
    ("waved goodbye", "v. 短语", "挥手道别（wave 的过去式）",
     "So they packed their bags and waved goodbye.", "于是他们收拾好行李，___。",
     "wave 挥（手）、波浪。"),
    ("watch out", "v. 短语", "小心，提防",
     "\"Watch out for the Big Bad Wolf,\" called Mother Pig.", "\"要___大灰狼，\"猪妈妈喊道。",
     "watch out for 提防……。"),
    ("trot along", "v. 短语", "沿着……小跑（过去式：trotted）",
     "The three little pigs trotted along until…", "三只小猪___，直到……",
     "trot （马）小跑；trot-trotted-trotted 双写 t。"),
    ("until", "conj.", "到……时",
     "The three little pigs trotted along until they met a man selling straw.", "三只小猪一路小跑，___遇见了一个卖稻草的人。",
     "直到……（= till）；not until 直到……才。"),
    ("straw", "n.", "（干燥的）麦秆，稻草",
     "\"Can I buy some straw?\" asked Pinky Pig.", "\"我能买些___吗？\"皮吉小猪问。",
     "a straw 一根稻草；strawberry 草莓。"),
    ("I’m going to do sth.", "句型", "我打算去做……",
     "I’m going to do sth.", "___——我心里已经想好了要做的事。",
     "sth. = something 某事；be going to 打算做……。"),
    ("put down a soft straw floor", "v. 短语", "铺上柔软的稻草地板",
     "Then he put down a soft straw floor.", "然后他___。",
     "put down 放下、铺上（put-put-put 不变）。"),
    ("grand", "adj.", "堂皇的；宏伟的",
     "\"Isn’t it grand?\"", "\"它难道不___吗？\"",
     "a grand house 宏伟的房子。"),
    ("shut the door", "v. 短语", "关上门",
     "Then he went inside and shut the door.", "然后他走进屋里，___。",
     "shut-shut-shut（不变）；shut up 闭嘴。"),
    ("trot on", "v. 短语", "快步走",
     "Percy and Poppy Pig trotted on until…", "珀西和波比小猪___，直到……",
     "on 表「继续」；与 trot along 近义。"),
    ("stick", "n.", "枝条，木棍",
     "\"Can I buy some sticks?\" asked Percy Pig.", "\"我能买些___吗？\"珀西小猪问。",
     "复数 sticks；carrot stick 胡萝卜条。"),
    ("better than", "短语", "好于……，比……好",
     "\"Sticks are better than straw.\"", "木棍___稻草。",
     "good/well-better-best（不规则）。"),
    ("brick", "n.", "砖，砖块",
     "\"Can I buy some bricks?\" asked Poppy Pig.", "\"我能买些___吗？\"波比小猪问。",
     "brick house 砖房。"),
    ("work hard", "v. 短语", "辛勤工作",
     "Poppy Pig worked hard.", "波比小猪___。",
     "hard 努力地；hard-working 勤奋的。"),
    ("so heavy", "短语", "太重了",
     "\"But they’re so heavy.\"", "\"可是它们___。",
     "so + 形容词：如此……；heavy 重的。"),
    ("the best of all", "短语", "最好的",
     "\"My house is the best of all!\"", "\"我的房子是___！\"",
     "of all 在所有……当中。"),
    ("Not by the hair on my chinny-chin-chin.", "句型", "字面：我的下巴上没有长头发；实际：那是不可能的",
     "\"Not by the hair on my chinny-chin-chin.\"", "\"___，\"小猪们喊道。",
     "词表原印「丌可能」，径改为「不可能」；chinny-chin-chin 为 chin（下巴）的儿语叠词，童话固定句。"),

    # ── P27 词表 ─────────────────────────────
    ("huff", "v.", "把……吹胀，吹气",
     THREAT, "\"那我就要___、还要吹气，把你的房子吹倒，\"狼说。",
     "huff and puff 固定搭配：又吹又喘。"),
    ("puff", "v.", "吹",
     THREAT, "\"那我就要鼓足了气、___，把你的房子吹倒，\"狼说。",
     "puff 噗地吹；（烟）一缕。"),
    ("blow your house in", "v. 短语", "把你的房子吹倒",
     THREAT, "\"那我就要吹啊鼓啊，___，\"狼说。",
     "blow-blew-blown（不规则）；blow in 吹塌。"),
    ("as fast as he could", "短语", "以最快的速度",
     "Pinky ran as fast as he could to the stick house.", "皮吉___跑向木棍房子。",
     "as fast as sb. can/could 尽某人最快的速度。"),
    ("ran out of puff", "v. 短语", "气喘吁吁（run 的过去式）",
     "…he ran out of puff.", "……他___，再也吹不动了。",
     "run out of 用完……；原形 run out of puff。"),
    ("jump onto", "v. 短语", "跳上去；跳到……上",
     "He jumped onto the roof.", "他___屋顶。",
     "onto 到……上面（on + to）。"),
    ("slammed on the lid", "v. 短语", "用力盖上盖子（slam 的过去式）",
     "The three little pigs slammed on the lid.", "三只小猪___。",
     "slam 猛地关上/盖上；slammed 双写 m。"),
]

assert len(entries) == 27, f"expected 27 entries, got {len(entries)}"

start_id = 2935
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    rows.append([str(start_id + i), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条；id 范围: {rows[0][0]} - {rows[-1][0]}")
with open("/home/user/workspace/harvey-vocab/scripts/pigs_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("已写入 pigs_rows.json")
