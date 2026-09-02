#!/usr/bin/env python3
"""Happy Birthday, Danny and the Dinosaur!（汪培珽 L1-11）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-2 汪培珽L1-11 Happy Birthday, Danny and the Dinosaur"
DATE = "2026-09-02"

# 从 id 2509 开始（Danny and the Dinosaur 到 2508）
entries = [
    # ── Page 5 赶时间 ─────────────────────────────
    ("in a hurry", "adv. 短语", "赶时间，匆忙",
     "Danny was in a hurry.", "Danny ___。他得去见他的恐龙朋友。",
     "in a hurry to do sth. 赶着做某事；Sammy 和 Chester 里也出现过。"),

    # ── Page 6-7 生日宴会 + 高兴 ─────────────────────────────
    ("birthday party", "n. 短语", "生日宴会；生日聚会",
     "\"Will you come to my birthday party?\"", "\"你会来参加我的___吗？\"",
     "party=聚会；hold a party=举办聚会。"),
    ("delight", "v.", "高兴；以……为乐（过去分词：delighted）",
     "\"I would be delighted,\" said the dinosaur.", "\"我___极了，\"恐龙说。",
     "be delighted to do sth. 很乐意做某事。"),

    # ── Page 8-9 骑 + 博物馆 ─────────────────────────────
    ("ride", "v.", "骑；乘坐（过去式：rode）",
     "Danny rode the dinosaur out of the museum.", "Danny ___着恐龙走出了博物馆。",
     "rode 是 ride 的过去式；也可指坐车、骑车。"),
    ("museum", "n.", "博物馆",
     "Danny rode the dinosaur out of the museum.", "Danny 骑着恐龙走出了___。",
     "复数 museums；上册 Danny 就是在这里遇见恐龙的。"),

    # ── Page 10-11 接人 + 一亿 ─────────────────────────────
    ("pick up", "v. 短语", "接人；（开车）接载（过去式：picked）",
     "On the way they picked up Danny's friends.", "路上他们___了 Danny 的朋友们。",
     "picked 是 pick 的过去式；也可指捡起、拿起。"),
    ("a hundred million", "num. 短语", "一亿",
     "\"Today I'm a hundred million years and one day old,\" said the dinosaur.", "\"今天我___岁零一天了，\"恐龙说。",
     "100,000,000；上册恐龙已经\"一百亿岁\"了。"),

    # ── Page 12-13 挂气球 ─────────────────────────────
    ("hang up", "v. 短语", "挂起来（过去式：hung）",
     "The children helped Danny's father hang up balloons.", "孩子们帮 Danny 的爸爸把气球___。",
     "hung 是 hang 的过去式；也可指挂断电话。"),
    ("balloon", "n.", "气球（复数：balloons）",
     "The children helped Danny's father hang up balloons.", "孩子们帮 Danny 的爸爸把___挂起来。",
     "复数 balloons。"),

    # ── Page 14-15 分发 ─────────────────────────────
    ("give out", "v. 短语", "分发，发出（过去式：gave）",
     "Danny's mother gave out party hats.", "Danny 的妈妈在___派对帽子。",
     "gave 是 give 的过去式。"),

    # ── Page 16-17 拍手 ─────────────────────────────
    ("clap", "v.", "拍手，鼓掌（过去式：clapped）",
     "They sang, and everybody clapped their hands.", "他们唱完，大家都___了。",
     "clapped 双写 p 再加 -ed。"),

    # ── Page 18-19 覆盖 + 耳朵 ─────────────────────────────
    ("cover", "v.", "覆盖，遮盖（过去式：covered）",
     "He sang, and everybody covered their ears.", "他一唱，大家都___了耳朵。",
     "covered 是 cover 的过去式；上册学过 cover one's eyes。"),
    ("ear", "n.", "耳朵（复数：ears）",
     "He sang, and everybody covered their ears.", "他一唱，大家都捂住了___。",
     "复数 ears。"),

    # ── Page 20-21 钉 + 驴 ─────────────────────────────
    ("pin", "v.", "（用别针等）别上，钉上（过去式：pinned）",
     "\"Let's play pin the tail on the donkey,\" said Danny.", "\"我们来玩把尾巴___到驴身上的游戏吧，\"Danny 说。",
     "pinned 双写 n 再加 -ed；也作名词=别针。"),
    ("donkey", "n.", "驴",
     "\"Let's play pin the tail on the donkey,\" said Danny.", "\"我们来玩把尾巴别到___身上的游戏吧，\"Danny 说。",
     "复数 donkeys；pin the tail on the donkey=蒙眼贴驴尾游戏。"),

    # ── Page 22-23 坐下 + 休息 + 家具 + 窗 ─────────────────────────────
    ("sat down", "v. 短语", "坐下（sit 的过去式）",
     "The children sat down to rest.", "孩子们___休息。",
     "sat 是 sit 的过去式；词表原文即 sat down。"),
    ("rest", "v.", "休息，歇息",
     "The children sat down to rest.", "孩子们坐下来___。",
     "也可作名词=休息时间；have a rest=休息一下。"),
    ("furniture", "n.", "家具（总称，不可数）",
     "\"Please don't put your feet on the furniture,\" said Danny.", "\"请不要把脚放在___上，\"Danny 说。",
     "不可数名词；a piece of furniture=一件家具。"),
    ("window", "n.", "窗，窗玻璃",
     "The dinosaur put his feet out the window.", "恐龙把脚伸出了___。",
     "复数 windows；out the window=到窗外。"),

    # ── Page 24-25 每个 + 一盘 ─────────────────────────────
    ("each", "pron.", "每个",
     "Danny's mother and father gave each child a dish of ice cream.", "Danny 的爸爸妈妈给___孩子端来一盘冰淇淋。",
     "each child=每一个孩子；each other=互相。"),
    ("a dish of", "量词短语", "一盘",
     "Danny's mother and father gave each child a dish of ice cream.", "Danny 的爸爸妈妈给每个孩子端来___冰淇淋。",
     "dish=盘、碟；a dish of=一份/一盘。"),

    # ── Page 26-27 数数 + 蜡烛 ─────────────────────────────
    ("counted", "v.", "（按顺序）数数；计数（count 的过去式）",
     "They counted the candles.", "他们___了蜡烛。",
     "counted 是 count 的过去式；上册学过 circus man counted them。"),
    ("candle", "n.", "蜡烛（复数：candles）",
     "They counted the candles.", "他们数了___。",
     "复数 candles；生日蛋糕上按岁数插蜡烛。"),

    # ── Page 28-29 许愿 ─────────────────────────────
    ("make a wish", "v. 短语", "许愿",
     "\"First we have to make a wish!\"", "\"首先我们得___！\"",
     "吹蜡烛前先许愿，是生日聚会的传统。"),

    # ── Page 30-31 明年 + 吹灭 ─────────────────────────────
    ("next year", "n. 短语", "明年",
     "\"I wish we can all be together again next year,\" said Danny.", "\"我希望___我们还能都在一起，\"Danny 说。",
     "next week=下周；next month=下个月。"),
    ("blow out", "v. 短语", "吹灭，吹熄（过去式：blew）",
     "They blew out the candles.", "他们___了蜡烛。",
     "blew 是 blow 的过去式。"),

    # ── Page 32 最好的一次 ─────────────────────────────
    ("I have ever had", "句型", "（句尾）表示之前从未有过，最好的一次",
     "\"This is the best birthday party I have ever had,\" said Danny.", "\"这是我___最棒的生日聚会，\"Danny 说。",
     "ever 用于最高级之后，加强语气=迄今为止。"),
]

assert len(entries) == 27, f"expected 27 entries, got {len(entries)}"

start_id = 2509
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/happy_birthday_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 happy_birthday_rows.json")
