#!/usr/bin/env python3
"""Chicken Licken（第二套图书馆 L3-7）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-7 Chicken Licken"
DATE = "2026-10-15"

INTRO = "This is a story about Chicken Licken, Henny Penny, Cocky Locky, Ducky Lucky, Goosey Loosey, Turkey Lurkey and Foxy Loxy."

# 从 id 2814 开始（The Magic Porridge Pot 到 2813）
entries = [
    # ── 开场角色 ─────────────────────────────
    ("chicken", "n.", "小鸡",
     INTRO, "这个故事讲的是___、Henny Penny、Cocky Locky、Ducky Lucky、Goosey Loosey、Turkey Lurkey 和 Foxy Loxy。",
     "鸡肉也作 chicken；chick n. 小鸡。"),
    ("henny", "n.", "母鸡（通常为 hen，这里是为了押韵加了 y）",
     INTRO, "这个故事讲的是 Chicken Licken、___、Cocky Locky、Ducky Lucky、Goosey Loosey、Turkey Lurkey 和 Foxy Loxy。",
     "hen 母鸡 + 押韵 y；本课角色名。"),
    ("cocky", "n.", "公鸡（通常为 cock，这里是为了押韵加了 y）",
     INTRO, "这个故事讲的是 Chicken Licken、Henny Penny、___、Ducky Lucky、Goosey Loosey、Turkey Lurkey 和 Foxy Loxy。",
     "cock 公鸡 + 押韵 y；另义 adj. 自大的。"),
    ("ducky", "n.", "鸭子（通常为 duck，这里是为了押韵加了 y）",
     INTRO, "这个故事讲的是 Chicken Licken、Henny Penny、Cocky Locky、___、Goosey Loosey、Turkey Lurkey 和 Foxy Loxy。",
     "duck 鸭子 + 押韵 y。"),
    ("goosey", "n.", "鹅（通常为 goose，这里是为了押韵加了 y）",
     INTRO, "这个故事讲的是 Chicken Licken、Henny Penny、Cocky Locky、Ducky Lucky、___、Turkey Lurkey 和 Foxy Loxy。",
     "goose 复数 geese + 押韵 y。"),
    ("turkey", "n.", "火鸡",
     INTRO, "这个故事讲的是 Chicken Licken、Henny Penny、Cocky Locky、Ducky Lucky、Goosey Loosey、___ 和 Foxy Loxy。",
     "Turkey Lurkey 火鸡角色名；Turkey 土耳其。"),
    ("foxy loxy", "n. 短语", "狡猾狐狸",
     INTRO, "这个故事讲的是 Chicken Licken、Henny Penny、Cocky Locky、Ducky Lucky、Goosey Loosey、Turkey Lurkey 和___。",
     "fox 狐狸 → foxy 狡猾的；角色名。"),
    ("farmyard", "n.", "农场",
     "This is where they live: woods, farmyard, duck pond, King's palace, forest, field and old barn.",
     "他们住在这里：树林、___、鸭子池塘、王宫、森林、田地和旧谷仓。",
     "farm 农场 + yard 院子，指农家庭院。"),
    ("King's palace", "n. 短语", "王宫",
     "This is where they live: woods, farmyard, duck pond, King's palace, forest, field and old barn.",
     "他们住在这里：树林、农场、鸭子池塘、___、森林、田地和旧谷仓。",
     "king 国王；palace 宫殿。"),
    ("old barn", "n. 短语", "旧谷仓",
     "This is where they live: woods, farmyard, duck pond, King's palace, forest, field and old barn.",
     "他们住在这里：树林、农场、鸭子池塘、王宫、森林、田地和___。",
     "barn 谷仓（L3-4 学过）。"),

    # ── 天塌了 ─────────────────────────────
    ("most of", "短语", "大部分，大多数的",
     "Most of the animals on the farm were happy.", "农场里的动物___都很快乐。",
     "most of + 名词；most 最高。"),
    ("scared-of", "v. 短语", "对……害怕",
     "Chicken Licken was scared-of everything.", "Chicken Licken 对什么都___。",
     "词表原样保留连字符；= scared of（L3-5 学过 scared）。"),
    ("stop by", "v. 短语", "停在……近旁",
     "He stopped by an oak tree.", "他在一棵___树旁停了下来。",
     "stop by + 地点；另义：顺便拜访。"),
    ("oak tree", "n. 短语", "橡树",
     "He stopped by an oak tree.", "他在一棵___旁停了下来。",
     "oak 橡树；tree 树。"),
    ("tiny acorn", "n. 短语", "小橡子（橡树的果子）",
     "Suddenly, a tiny acorn dropped from the tree.", "突然，一颗___从树上掉了下来。",
     "acorn 橡子；tiny 极小的（上册学过）。"),
    ("drop from", "v. 短语", "从……落下",
     "Suddenly, a tiny acorn dropped from the tree.", "突然，一颗小橡子___树上。",
     "drop-dropped-dropped；drop n. 一滴（上册学过）。"),
    ("look up", "v. 短语", "仰望",
     "He looked up at the blue sky.", "他___蓝色的天空。",
     "look up 另义：查（字典）；反义 look down。"),
    ("rush back to", "v. 短语", "匆匆回到",
     "He rushed back to the farmyard.", "他___农场。",
     "rush 冲、奔；rush hour 高峰期。"),
    ("sitting by", "v. 短语", "坐在……旁边（sit 的现在分词）",
     "Henny Penny was sitting by the hen house.", "Henny Penny 正___鸡舍旁边。",
     "sit-sat-sat；by 在……旁边。"),
    ("out of my way", "句型", "别挡我的道（口语）",
     "\"Out of my way!\" yelled Chicken Licken.", "\"___！\"Chicken Licken 大喊。",
     "way 道路；让开路常用口语。"),

    # ── 逐个朋友加入 ─────────────────────────────
    ("What shall we do?", "句型", "我们该怎么做？",
     "\"Oh no!\" said Henny Penny. \"What shall we do?\"", "\"哦不！\"Henny Penny 说，\"___\"",
     "shall 用于提议；Let's... 同义。"),
    ("warn", "v.", "提醒，预先通知",
     "\"I'm going to warn the King,\" said Chicken Licken.", "\"我要去___国王，\"Chicken Licken 说。",
     "warn sb. of sth. 警告某人某事。"),
    ("past", "prep.", "经过，越过",
     "They ran past the hen house.", "他们___鸡舍跑过。",
     "介词；动词 pass 跑过。"),
    ("thump", "n.", "重击声，砰",
     "They ran past the hen house and... Thump!", "他们跑过鸡舍，然后……___！",
     "拟声词；L3-3 学过 SNAP 类拟声词。"),
    ("bump into", "v. 短语", "无意中遇到、碰到",
     "They bumped into Cocky Locky.", "他们___了 Cocky Locky。",
     "bump 碰撞；L3-4 学过 burst into。"),
    ("run out of the farmyard", "v. 短语", "跑出农场",
     "They ran out of the farmyard.", "他们___。",
     "run out of 另义：用完。"),
    ("run past", "v. 短语", "跑过……",
     "They ran past the duck pond.", "他们___鸭子池塘。",
     "past 经过；注意 run-ran-run。"),
    ("run across the bridge", "v. 短语", "跑（穿）过桥",
     "They ran across the bridge.", "他们___。",
     "across 穿过（L3-4 学过 run across）。"),
    ("sitting on her nest", "v. 短语", "坐在她的窝里（sit 的现在分词）",
     "Goosey Loosey was sitting on her nest.", "Goosey Loosey 正___。",
     "nest 鸟窝、巢。"),
    ("ran past the barn", "v. 短语", "跑出谷仓",
     "They ran past the barn.", "他们___。",
     "past 经过；barn 谷仓。"),
    ("peck", "v.", "啄，啄食（现在分词：pecking）",
     "Turkey Lurkey was pecking at the ground.", "Turkey Lurkey 正在地上___。",
     "peck at 啄食（L3-3 学过 pecked at）。"),
    ("ran through the field", "v. 短语", "穿过田地",
     "They ran through the field.", "他们___。",
     "through 穿过（立体）；field 田地。"),

    # ── 狐狸的捷径与结局 ─────────────────────────────
    ("shortcut", "n.", "近路；捷径",
     "\"I know a shortcut,\" said Foxy Loxy.", "\"我知道一条___，\"Foxy Loxy 说。",
     "short 短 + cut 切，抄近路。"),
    ("lead them into the forest", "v. 短语", "把他们引到森林（过去式：led）",
     "He led them into the forest...", "他把他们___……",
     "lead-led-led（不规则动词）。"),
    ("point to", "v. 短语", "指向（过去式：pointed）",
     "He pointed to a hole.", "他___一个洞。",
     "L3-5 学过 point to。"),
    ("down here", "短语", "从这里下去",
     "\"Down here,\" he said.", "\"___，\"他说。",
     "down 向下；here 这里。"),
    ("go down the hole", "v. 短语", "钻进洞里去（过去式：went）",
     "They all went down the hole.", "他们都___。",
     "go-went-gone（不规则动词）。"),
    ("gobble you all up", "v. 短语", "把你们都吞下去",
     "\"And it's where I'm going to gobble you all up!\"", "\"这正是我要___的地方！\"",
     "gobble up 狼吞虎咽地吃光。"),
    ("stupid", "adj.", "笨的，傻的",
     "\"Stupid bird,\" said Foxy Loxy.", "\"___的鸟，\"Foxy Loxy 说。",
     "L3-2 学过 stupid。"),
    ("just then", "短语", "就在那时",
     "Just then, an acorn hit Foxy Loxy on the head.", "___，一颗橡子砸中了 Foxy Loxy 的头。",
     "just 正；then 那时。"),
    ("ran down the tunnel", "v. 短语", "跑下隧道",
     "He ran down the tunnel and was never seen again.", "他___，从此再也没人见过他。",
     "tunnel 隧道；down 向下。"),
    ("fell on", "v. 短语", "落在（fall 的过去式）",
     "\"Are you sure the sky fell on your head?\" they said.", "\"你确定天___你的脑袋上了吗？\"他们说。",
     "fall-fell-fallen（不规则动词）。"),
    ("all the way home", "短语", "回家的路上",
     "And they chased him all the way home.", "他们一路追着他___。",
     "all the way 一路；home 作副词。"),
]

assert len(entries) == 43, f"expected 43 entries, got {len(entries)}"

start_id = 2814
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    rows.append([str(start_id + i), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条；id 范围: {rows[0][0]} - {rows[-1][0]}")
with open("/home/user/workspace/harvey-vocab/scripts/licken_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("已写入 liken_rows.json")
