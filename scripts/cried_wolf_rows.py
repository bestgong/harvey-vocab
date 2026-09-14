#!/usr/bin/env python3
"""The Boy Who Cried Wolf（第二套图书馆 L3-2）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-2 The Boy Who Cried Wolf"
DATE = "2026-09-14"

INTRO = "This story is about Sam, some sheep, the villagers and (maybe) a wolf."

# 从 id 2622 开始（The Magic Pear Tree 到 2621）
entries = [
    # ── Page 2-3 开场 ─────────────────────────────
    ("This story is about...", "句型", "这个故事是关于……",
     INTRO, "___Sam、一些绵羊、一群村民，也许还有一匹狼。",
     "介绍故事人物的常用开头。"),
    ("villager", "n.", "村民",
     INTRO, "这个故事讲的是 Sam、一些绵羊、___，也许还有一匹狼。",
     "village 村庄 + -r 变人。"),

    # ── Page 4-5 山村 ─────────────────────────────
    ("village", "n.", "村庄",
     "Sam lived in a little village in the mountains.", "Sam 住在高山上的一个小___里。",
     "country village 乡村；villager 村民。"),
    ("mountain", "n.", "山，高山",
     "Sam lived in a little village in the mountains.", "Sam 住在___上的一个小村庄里。",
     "mountain range 山脉。"),

    # ── Page 6-9 放羊日常 ─────────────────────────────
    ("from…to", "短语", "从……到……",
     "He took the sheep from the village to a grassy meadow.", "他带着羊，___村庄，来到那片草地。",
     "原文：from the village up the hill to a grassy meadow 从村庄上山到草地。"),
    ("hill", "n.", "山丘，小山",
     "Every day he took the sheep up the hill to a grassy meadow.", "他每天把羊带上___，来到一片草地。",
     "hill 比 mountain 矮；up the hill 上山。"),
    ("grassy meadow", "n. 短语", "长满草的草地",
     "Every day he took the sheep up the hill to a grassy meadow.", "他每天把羊带上小山，来到一片___。",
     "grass n. 草 → grassy adj. 长满草的。"),
    ("from morning until evening", "短语", "从早到晚",
     "He watched them from morning until evening.", "他___都守着这些羊。",
     "until 直到；同义：from morning to night。"),
    ("mutton brain", "n. 短语", "（俚语）笨蛋",
     "\"This way, mutton brain...\"", "\"往这边走，你这个___……\"",
     "mutton n. 羊肉；brain n. 脑。放羊娃骂羊的俏皮话。"),

    # ── Page 10-13 无聊日常 ─────────────────────────────
    ("the same", "短语", "同样地；一样",
     "Every day was the same.", "每一天都___。",
     "same adj. 相同的；the same old 老一套。"),
    ("lonely", "adj.", "孤单的",
     "Sam was lonely and he was SO bored.", "Sam 很___，而且无聊透了。",
     "lonely 孤单（情感）；alone 独自（状态）。"),
    ("bored", "adj.", "无聊的，厌倦的",
     "Sam was lonely and he was SO bored.", "Sam 很孤单，而且___透了。",
     "boring 令人无聊的；be bored with 厌倦。"),
    ("talk to", "v. 短语", "与……谈话",
     "He tried talking to the sheep.", "他试着和羊___。",
     "talk to sb. 对某人说话；talk with 交谈。"),
    ("moaned", "v.", "<非正式>抱怨，发牢骚（moan 的过去式）",
     "\"Nobody ever comes up here,\" moaned Sam.", "\"从没有人会上这儿来，\"Sam ___道。",
     "moan 呻吟、抱怨。"),
    ("had an idea", "v. 短语", "有一个想法（have 的过去式）",
     "One day, he had an idea.", "有一天，他突然___了。",
     "have-had；idea n. 主意、想法。"),

    # ── Page 16-21 第一次喊狼 ─────────────────────────────
    ("What's the matter?", "句型", "怎么了？",
     "\"What's the matter?\"", "\"___？\"村民问。",
     "询问状况的常用句；也可说 What's wrong?"),
    ("come out of", "v. 短语", "从……出来",
     "\"A wolf has come out of the forest!\"", "\"有一匹狼___森林！\"",
     "come out 出来；of 表示从……里面。"),
    ("run up the hill", "v. 短语", "跑上山",
     "Everyone ran up the hill with him.", "大家跟着他一起___。",
     "run-ran-run；反义：run down the hill 跑下山。"),
    ("puffing and panting", "adv. 短语", "气喘吁吁",
     "Puffing and panting, they reached the meadow.", "大家___地赶到了草地。",
     "puff 喘气；pant 气喘；……and…… 连用表状态。"),
    ("All that way for nothing.", "句型", "白跑了这么远。",
     "All that way for nothing.", "\"___！\"大家心想。",
     "for nothing 白白地、徒劳。"),
    ("quietly", "adv.", "轻轻地，安静地",
     "The sheep were quietly eating their grass.", "羊正在___吃草。",
     "quiet adj. → quietly adv.。"),
    ("angry", "adj.", "愤怒的，生气的",
     "The villagers were angry, but Sam just laughed.", "村民很___，但 Sam 只是笑。",
     "be angry with sb. 生某人的气；angrily adv.。"),

    # ── Page 24-29 第二次喊狼 ─────────────────────────────
    ("a few days later", "短语", "又过了几天，几天后",
     "A few days later, Sam was bored again.", "___，Sam 又觉得无聊了。",
     "a few 一些；later 之后。"),
    ("We'd better make sure.", "句型", "我们最好确认一下。",
     "\"We'd better make sure.\"", "\"哦，是吗？___。\"他们说。",
     "had better 最好；make sure 确保。"),
    ("grin at", "v. 短语", "咧嘴而笑（现在分词：grinning）",
     "\"What are you grinning at?\"", "\"你在___什么？\"",
     "grin 露齿笑；laugh 大笑；smile 微笑。"),

    # ── Page 30-33 第三次喊狼 ─────────────────────────────
    ("a week later", "短语", "一星期后",
     "A week later, Sam was bored again.", "___，Sam 又觉得无聊了。",
     "week 星期；上册学过 next week。"),
    ("this time", "短语", "这次",
     "Most people didn't believe him this time.", "___大多数人都不相信他。",
     "last time 上次；next time 下次（上册学过）。"),
    ("You think you're so clever…", "句型", "你以为你很聪明……",
     "\"You think you're so clever...\"", "\"___。\"村民说。",
     "clever 聪明的；讽刺语气。"),
    ("furious", "adj.", "狂怒的，暴怒的",
     "Now everyone was furious.", "这下所有人都___了。",
     "比 angry 更强烈；fury n. 狂怒。"),

    # ── Page 34-37 狼真的来了 ─────────────────────────────
    ("terrified", "adj.", "非常害怕的",
     "Sam was terrified.", "Sam ___极了。",
     "terrify v. 使害怕；terror n. 恐怖。"),
    ("as fast as he could", "短语", "尽可能快地",
     "He ran down to the village as fast as he could.", "他撒开腿___地往村里跑。",
     "as...as 尽可能……；上册 Oliver 学过 as...as。"),
    ("stupid", "adj.", "笨的，傻的",
     "\"Do you think we're so stupid?\"", "\"你觉得我们这么___吗？\"",
     "silly、foolish 同义。"),
    ("begged", "v.", "乞求，请求（beg 的过去式）",
     "Sam begged them to come with him.", "Sam ___大家跟他一起去。",
     "beg-begged；beg for sth. 乞求某物。"),
    ("come with him", "短语", "跟他来；跟他走",
     "Sam begged them to come with him.", "Sam 恳求他们___。",
     "come with sb. 跟某人一起来。"),

    # ── Page 38-43 教训 ─────────────────────────────
    ("in the end", "短语", "终于，最后",
     "In the end, Sam had to go back up the hill all alone.", "___，Sam 只好一个人回山上去。",
     "at the end of 在……末尾，注意区分。"),
    ("stay in", "v. 短语", "待着",
     "Sam stayed in the meadow until it was dark.", "Sam 在草地上___到天黑。",
     "stay 停留；stay home 待在家。"),
    ("finally", "adv.", "终于；总之",
     "Finally, the villagers came to find him.", "___，村民来找他了。",
     "同义词：at last、in the end。"),
    ("lies", "n.", "谎言，谎话（lie 的复数）",
     "\"You always told lies before,\" they said.", "\"你以前总是说___，\"他们说。",
     "tell lies 说谎；单数 lie；另义 v. 躺。"),
]

assert len(entries) == 38, f"expected 38 entries, got {len(entries)}"

start_id = 2622
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/cried_wolf_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 cried_wolf_rows.json")
