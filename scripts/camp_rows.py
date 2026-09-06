#!/usr/bin/env python3
"""Danny and the Dinosaur Go to Camp（汪培珽 L1-12）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-2 汪培珽L1-12 Danny and the Dinosaur Go to Camp"
DATE = "2026-09-06"

# 从 id 2536 开始（Happy Birthday 到 2535）
entries = [
    # ── Page 5 露营 + 夏天 + 带上 ─────────────────────────────
    ("go to camp", "v. 短语", "去露营；去夏令营",
     "Danny went to camp for the summer.", "Danny 这个夏天去___了。",
     "camp n. 营地、夏令营。"),
    ("summer", "n.", "夏天，夏季",
     "Danny went to camp for the summer.", "整个___，Danny 都在营地里度过。",
     "summer camp=夏令营；summer vacation=暑假。"),
    ("take along", "v. 短语", "带上（过去式：took）",
     "He took along his friend the dinosaur.", "他___了他的恐龙朋友。",
     "took 是 take 的过去式；along 表示随身。"),

    # ── Page 6-7 享受 + 假期 + 主人 ─────────────────────────────
    ("enjoy", "v.", "享受，喜爱",
     "\"Camp is fun. You will enjoy it,\" said Danny.", "\"营地很好玩，你会___的，\"Danny 说。",
     "enjoy doing sth. 喜欢做某事。"),
    ("vacation", "n.", "假期",
     "\"Thanks. I needed a vacation,\" said the dinosaur.", "\"谢谢，我正好需要一个___，\"恐龙说。",
     "on vacation=在度假。"),
    ("owner", "n.", "所有者，主人",
     "\"Welcome,\" said the camp owner.", "\"欢迎光临，\"营地的___说。",
     "own v. 拥有；shop owner=店主。"),

    # ── Page 8-9 赛跑 + 迈一步 ─────────────────────────────
    ("race", "v.", "赛跑，速度竞赛",
     "Lana the leader said, \"Let's start with a race.\"", "领队 Lana 说：\"我们先来一场___。\"",
     "词表标 v.；文中作名词 a race，win a race=赢得比赛。"),
    ("take a step", "v. 短语", "迈出一步（过去式：took）",
     "The dinosaur took a step.", "恐龙只___，就赢定了。",
     "took 是 take 的过去式。"),

    # ── Page 10-11 橄榄球 + 达阵 ─────────────────────────────
    ("play football", "v. 短语", "打橄榄球（美式足球）",
     "The children played football.", "孩子们在___。",
     "美国的 football 指橄榄球；足球是 soccer。"),
    ("touchdown", "n.", "达阵得分",
     "\"Touchdown!\" shouted Danny.", "\"___！\"Danny 大喊。",
     "橄榄球术语：持球冲入对方端区得分。"),

    # ── Page 12-13 湖 + 划船 ─────────────────────────────
    ("lake", "n.", "湖，湖泊",
     "Lana took everybody to the lake.", "Lana 带大家去了___。",
     "复数 lakes。"),
    ("row boat", "v. 短语", "划船",
     "\"Here is where we row our boats,\" she said.", "\"我们就在这里___，\"她说。",
     "row v. 划（船）；boat n. 小船。"),

    # ── Page 14-15 番茄酱 + 当然 + 一…就… + 倒完 ─────────────────────────────
    ("ketchup", "n.", "番茄酱",
     "\"Please pass the ketchup,\" said Danny.", "\"请把___递给我，\"Danny 说。",
     "也可拼作 catsup。"),
    ("of course", "adv. 短语", "一定，当然",
     "\"Of course, just as soon as I finish this bottle,\" said the dinosaur.", "\"___，等我倒完这瓶就给你，\"恐龙说。",
     "上册 Oliver 里也学过。"),
    ("as soon as", "conj. 短语", "一……就……",
     "\"Of course, just as soon as I finish this bottle,\" said the dinosaur.", "\"当然，___我倒完这瓶就给你，\"恐龙说。",
     "引导时间状语从句。"),
    ("finish", "v.", "完成，做好（文中指“倒完”）",
     "\"Of course, just as soon as I finish this bottle,\" said the dinosaur.", "\"当然，我一___这瓶就给你，\"恐龙说。",
     "finish doing sth.；文中指把瓶里的番茄酱倒完。"),

    # ── Page 16-17 写信 + 信 + 披萨 ─────────────────────────────
    ("write", "v.", "写，写信（过去式：wrote）",
     "After lunch everybody wrote letters home.", "午饭后大家都在给家里___。",
     "wrote 是 write 的过去式。"),
    ("letter", "n.", "信，信函",
     "After lunch everybody wrote letters home.", "午饭后大家都往家里写___。",
     "复数 letters；另义“字母”。"),
    ("pizza", "n.", "披萨",
     "\"Send me a pizza,\" wrote the dinosaur.", "\"给我寄个___，\"恐龙写道。",
     "意大利式烤饼；复数 pizzas。"),

    # ── Page 18-21 远足 + 跟随 + 累了 + 抓紧 ─────────────────────────────
    ("hike", "n.", "徒步旅行，远足",
     "\"Now let's go on a hike,\" said Lana.", "\"现在我们去___吧，\"Lana 说。",
     "词表印作“进足”系“远足”之误；go on a hike=去远足。"),
    ("follow", "v.", "跟着，跟随（过去式：followed）",
     "And everybody followed her.", "大家都___在 Lana 身后。",
     "followed 是 follow 的过去式。"),
    ("get tired", "v. 短语", "疲倦；累了",
     "Then Danny got tired and climbed on the dinosaur.", "后来 Danny ___了，就爬到恐龙背上。",
     "get+形容词=变得；过去式 got。"),
    ("hold tight", "v. 短语", "抓紧了",
     "\"Hold tight,\" said the dinosaur.", "\"___，\"恐龙说。",
     "hold-held-held；tight=紧紧地。"),

    # ── Page 24-25 营火 + 烤棉花糖 ─────────────────────────────
    ("campfire", "n.", "营火；营火会",
     "Everybody sat around the campfire.", "大家围着___坐成一圈。",
     "camp+fire 合成词。"),
    ("toasted marshmallows", "n. 短语", "烤棉花糖",
     "Lana gave out toasted marshmallows.", "Lana 分发了___。",
     "toast v. 烤；marshmallow n. 棉花糖。"),

    # ── Page 26-27 胃口 ─────────────────────────────
    ("room", "n.", "空间，余地（文中指吃得下）",
     "\"Thanks, but I don't have room for more,\" said Danny.", "\"谢谢，不过我吃不下了，没有___再装了，\"Danny 说。",
     "room 此处指肚子里的空地方；上册 take up room 指占空间。"),

    # ── Page 28-29 就寝 + 被子 ─────────────────────────────
    ("time for bed", "n. 短语", "睡觉时间；就寝时间",
     "It was time for bed.", "到___了。",
     "It's time for bed.=该睡觉了。"),
    ("cover", "n.", "被子；覆盖物（复数 covers=被子）",
     "\"I can't wait to get under the covers,\" said Danny.", "\"我等不及要钻进___里了，\"Danny 说。",
     "复数 covers 常指被子；另义“封面”；上册学过动词 cover。"),

    # ── Page 30-31 铺位 + 枕头 ─────────────────────────────
    ("bunk", "n.", "铺位，床铺",
     "But the dinosaur's bunk was too small for him.", "可恐龙的___对他来说太小了。",
     "bunk bed=双层床。"),
    ("pillow", "n.", "枕头",
     "He took a pillow and went outside.", "他拿了___就到外面去了。",
     "复数 pillows。"),

    # ── Page 32 叫醒 + 早餐 + 睡着 ─────────────────────────────
    ("wake me up", "v. 短语", "叫醒我",
     "\"Wake me up for breakfast,\" said the dinosaur.", "\"吃早饭时___，\"恐龙说。",
     "wake-woke-woken；wake up=醒来、叫醒。"),
    ("breakfast", "n.", "早餐；吃早餐",
     "\"Wake me up for breakfast,\" said the dinosaur.", "\"___的时候记得叫醒我，\"恐龙说。",
     "词表标 v.；breakfast 也常作名词，have breakfast=吃早餐。"),
    ("fell asleep", "v. 短语", "睡着了（fall asleep 的过去式）",
     "He fell asleep on the ground.", "他在地上___了。",
     "fall-fell-fallen；asleep adj. 睡着的。"),
]

assert len(entries) == 33, f"expected 33 entries, got {len(entries)}"

start_id = 2536
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/camp_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 camp_rows.json")
