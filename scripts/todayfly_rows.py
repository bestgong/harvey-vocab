#!/usr/bin/env python3
"""Today I Will Fly!（小猪小象 1）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "Today I Will Fly!"
DATE = "2026-10-31"

S1 = "Today I will fly!"

# 从 id 2962 开始（The Three Little Pigs 到 2961）
entries = [
    # ── P31 词表 ─────────────────────────────
    ("today", "adv.", "今天，今日",
     S1, "___我要飞起来啦！",
     "today's news 今天的新闻。"),
    ("will", "v.", "将，将要",
     S1, "今天我___飞起来啦！",
     "will not 缩写 won't。"),
    ("fly", "v.", "飞，飞翔",
     S1, "今天我将要___啦！",
     "fly-flew-flown（不规则）。"),
    ("will not", "短语", "不会，肯定不会",
     "You will not fly today.", "你今天___飞起来。",
     "won't 为缩写形式。"),
    ("tomorrow", "adv.", "在明天",
     "You will not fly tomorrow.", "你___也飞不起来。",
     "the day after tomorrow 后天。"),
    ("next week", "短语", "下周，下星期",
     "You will not fly next week.", "你___更飞不起来。",
     "next 下一个 + week 星期。"),
    ("never", "adv.", "决不，永不",
     "YOU WILL NEVER FLY!", "你___飞不起来！",
     "never ever 强调：永远不。"),
    ("try", "v.", "试试",
     "I will try.", "我要___。",
     "try to do sth. 设法做某事。"),
    ("good-bye", "int.", "再见，拜拜",
     "Good-bye.", "___。",
     "亦作 goodbye / bye-bye。"),
    ("need", "v.", "需要",
     "You need help.", "你___帮助。",
     "need to do sth. 需要做某事。"),
    ("help", "v.", "帮助",
     "Will you help me?", "你愿意___我吗？",
     "help sb. do sth. 帮助某人做某事。"),
    ("thank you", "短语", "谢谢你",
     "Thank you. I do need help!", "___。我确实需要帮助！",
     "thanks 同义；many thanks 多谢。"),
    ("woof", "n.", "〈非正式〉（狗叫声）汪汪",
     "WOOF! WOOF! WOOF!", "___！狗叫了三声。",
     "拟声词；对应猫叫 meow。"),
    ("did", "v.", "做（do 的过去式）",
     "I did it! I flew!", "我___到了！我飞起来了！",
     "do-did-done（不规则）。"),
    ("flew", "v.", "飞，飞翔（fly 的过去式）",
     "I did it! I flew!", "我做到了！我___起来了！",
     "fly-flew-flown（不规则）。"),
    ("thank you for", "短语", "为……感谢",
     "Thank you for your help!", "___你的帮助！",
     "Thank you for doing sth. 感谢你做了某事。"),
    ("did not", "短语", "没有",
     "You did not fly.", "你___飞起来。",
     "did not = didn't；用于过去时否定。"),

    # ── P32 词表 ─────────────────────────────
    ("jumped", "v.", "跳跃（jump 的过去式）",
     "YOU JUMPED!", "你是___的！",
     "词表标注「过去分词」，实为过去式；jump-jumped-jumped。"),
    ("It was", "短语", "那是（过去），的确如此",
     "It was a big jump!", "___一个大跳跃！",
     "is 的过去式；It was... 那真是……。"),
    ("big", "adj.", "大的",
     "It was a big jump!", "这简直是___跳跃！",
     "big-bigger-biggest（双写 g）。"),
    ("again", "adv.", "再一次",
     "I will try again!", "我要___试试！",
     "again and again 一遍又一遍。"),
    ("eat", "v.", "吃，吃饭",
     "I will eat lunch.", "我要去___午饭。",
     "eat-ate-eaten（不规则）。"),
    ("lunch", "n.", "午餐，午饭",
     "I will eat lunch.", "我要去吃___。",
     "have lunch 吃午饭。"),
    ("oof", "int.", "哎呦",
     "Oof!", "___！",
     "感叹词，表示突然用力或不适。"),
    ("will you…", "句型", "会不会……？你是否愿意……？",
     "will you…", "___——用来礼貌地询问对方愿不愿意。",
     "Will you help me? 你愿意帮我吗？"),
    ("hello", "int.", "喂，你好（用于问候或打招呼）",
     "Hello!", "___！",
     "Hello? 接电话时用升调。"),
    ("friend", "n.", "朋友，友人",
     "My friend can fly!", "我的___能飞起来！",
     "friendly 友好的；friendship 友谊。"),
    ("can", "v.", "（表示有能力做或能够发生）能，会",
     "My friend can fly!", "我的朋友___飞起来！",
     "否定 cannot/can't；can-could（过去式）。"),
    ("get help", "v. 短语", "得到帮助",
     "I am getting help.", "我正在___。",
     "get + 名词：得到……。"),
    ("luck", "n.", "幸运，好运",
     "Good luck.", "祝你___。",
     "lucky 幸运的；Good luck! 祝你好运！"),
]

assert len(entries) == 30, f"expected 30 entries, got {len(entries)}"

start_id = 2962
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    rows.append([str(start_id + i), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条；id 范围: {rows[0][0]} - {rows[-1][0]}")
with open("/home/user/workspace/harvey-vocab/scripts/todayfly_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("已写入 todayfly_rows.json")
