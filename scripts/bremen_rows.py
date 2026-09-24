#!/usr/bin/env python3
"""The Musicians of Bremen（第二套图书馆 L3-4）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-4 The Musicians of Bremen"
DATE = "2026-09-24"

# 从 id 2694 开始（The Little Red Hen 到 2693）
entries = [
    # ── Page 3-5 刻薄的男主人 ─────────────────────────────
    ("musicians", "n.", "音乐家（musician 的复数）",
     "They never did become musicians.", "他们终究没能成为___。",
     "music 音乐 → musician 音乐家。"),
    ("mean man", "n. 短语", "刻薄的人",
     "Once upon a time, there was a very mean man.", "从前，有一个非常___。",
     "mean adj. 刻薄的；另义 v. 意味着。"),
    ("come on", "短语", "快点，赶快",
     "\"Come on!\" he shouted.", "\"___！\"他喊道。",
     "催促、打气常用语；Come on in! 快进来。"),
    ("supper", "n.", "晚餐",
     "\"Here's your supper.\"", "\"这是你的___。\"",
     "supper 晚餐；同义 dinner（上册学过 supper time）。"),
    ("rooster", "n.", "<美>公鸡",
     "He was very mean to his rooster.", "他对___也非常刻薄。",
     "美式英语；英式多说 cock。"),
    ("for lunch", "短语", "作为午餐",
     "We'll put him in the pot and eat him for lunch.", "我们要把它放进锅里，当___吃掉。",
     "for + 餐名；for breakfast 作为早餐。"),
    ("get too old", "v. 短语", "太老了（现在分词：getting）",
     "\"He's getting too old.\"", "\"它___了。\"",
     "get + adj. 变得……；get dark 变黑（上册学过）。"),

    # ── Page 6-8 公鸡的危机 ─────────────────────────────
    ("crow", "v.", "公鸡啼鸣（过去式：crowed）",
     "That evening, the rooster crowed as hard as he could.", "那天傍晚，公鸡拼命___。",
     "另义 n. 乌鸦。"),
    ("as hard as he could", "短语", "尽了最大努力",
     "That evening, the rooster crowed as hard as he could.", "那天傍晚，公鸡___地打鸣。",
     "同结构：as fast as he could 尽可能快（L3-2 学过）。"),
    ("the last time", "短语", "最后一次",
     "\"I'm crowing for the last time,\" said the rooster.", "\"这是我___打鸣了，\"公鸡说。",
     "last night 昨晚（上册学过）。"),
    ("rooster stew", "n. 短语", "炖鸡",
     "Tomorrow I'll be rooster stew.", "明天我就要变成___了。",
     "stew n. 炖菜；beef stew 炖牛肉。"),
    ("master", "n.", "主人",
     "\"The master is putting me in his cooking pot.\"", "\"___要把我放进炖锅里。\"",
     "旧时对主人的称呼；另义 n. 硕士。"),
    ("Bremen", "n.", "不来梅（德国地名）",
     "We can go to Bremen and join the town band.", "我们可以去___，加入市乐队。",
     "德国城市；格林童话《不来梅的音乐家》。"),
    ("town band", "n. 短语", "市乐队",
     "We can go to Bremen and join the town band.", "我们可以去不来梅，加入___。",
     "band 乐队；brass band 铜管乐队。"),
    ("violin", "n.", "小提琴",
     "\"I'll play the violin!\"", "\"我要拉___！\"",
     "乐器前加 the：play the violin。"),
    ("didgeridoo", "n.", "迪吉里杜管（澳大利亚土著乐器）",
     "\"I'll play the didgeridoo!\"", "\"我要吹___！\"",
     "澳大利亚土著吹奏的长管乐器。"),

    # ── Page 9-11 森林与小屋 ─────────────────────────────
    ("set off", "v. 短语", "出发；动身",
     "The four friends set off at once.", "四个好朋友立刻___。",
     "set off for + 地点，动身去……。"),
    ("scared", "adj.", "害怕的，惊恐的，恐惧的",
     "\"I'm scared.\"", "\"我___。\"",
     "scared of sth. 害怕某物；scary 吓人的。"),
    ("light", "n.", "光，光线",
     "\"Wait!\" called the rooster. \"I see a light.\"", "\"等等！\"公鸡叫道，\"我看见一点___。\"",
     "另义 v. 点亮（见本课 light candle）。"),
    ("cottage", "n.", "小屋",
     "\"It's coming from a cottage.\"", "它是从一座___里透出来的。",
     "乡间小屋；小而旧的房子。"),
    ("creep closer", "v. 短语", "蹑手蹑脚地靠近（过去式：crept）",
     "The four friends crept closer.", "四个好朋友___。",
     "creep-crept-crept（不规则动词）。"),
    ("a gang of robbers", "n. 短语", "一伙强盗",
     "\"And a gang of robbers.\"", "\"还有___。\"",
     "a gang of 一伙、一帮；robber 强盗。"),
    ("If only…", "句型", "只要……",
     "\"If only we could get inside,\" said the dog.", "\"___能进去就好了，\"小狗说。",
     "词表释义为“只要……”，语境中意为“要是……就好了”。"),

    # ── Page 12-15 叠罗汉吓强盗 ─────────────────────────────
    ("leap on", "v. 短语", "跃上（马）背",
     "The dog leaped on the donkey's back.", "小狗___驴子的背。",
     "leap 过去式 leaped/leapt 均可。"),
    ("climb on", "v. 短语", "爬到……上",
     "The cat climbed on top of the dog.", "小猫___小狗的背上。",
     "climb up 爬上（上册学过）；on top of 在……上面。"),
    ("burst into", "v. 短语", "闯入",
     "The donkey, the dog, the cat and the rooster BURST into the room.", "驴子、小狗、小猫和公鸡一起___房间。",
     "burst-burst-burst；burst into tears 突然大哭。"),
    ("Run for your lives.", "句型", "快逃命。",
     "\"Help!\" cried the robbers. \"Run for your lives.\"", "\"救命啊！\"强盗们喊道，\"___\"",
     "for one's life 拼命地；life 复数 lives。"),
    ("perfect", "adj.", "完美",
     "\"Perfect!\"", "\"___！\"驴子说。",
     "practice makes perfect 熟能生巧（上册学过）。"),

    # ── Page 18-19 强盗回来探查 ─────────────────────────────
    ("go out", "v. 短语", "熄灭",
     "The robbers saw the lights go out.", "强盗们看见灯___了。",
     "另义：外出；反义 come on（灯亮）。"),
    ("the robber chief", "n. 短语", "强盗首领",
     "\"We shouldn't have run away,\" said the robber chief.", "\"我们不该逃跑的，\"___说。",
     "chief n. 首领；另义 adj. 主要的。"),
    ("the shining eyes", "n. 短语", "闪闪发光的眼睛",
     "He saw the shining eyes of the cat.", "他看见了小猫那双___。",
     "shine v. 发光（上册学过）；shining 闪亮的。"),
    ("burning coals", "n. 短语", "炭火",
     "\"Burning coals!\" he thought.", "\"___！\"他想。",
     "burn v. 燃烧；coal 煤、炭。"),
    ("light candle", "v. 短语", "点亮蜡烛",
     "\"I'll use them to light my candle.\"", "我要用它们来___。",
     "light v. 点亮；lighter 打火机。"),

    # ── Page 20-24 惨遭反击 ─────────────────────────────
    ("leap at", "v. 短语", "向……扑去（过去式：leaped）",
     "...she leaped at his face.", "她朝他的脸___。",
     "词表“吐……扑去”系“向……扑去”之误。"),
    ("bite", "v.", "咬（过去式：bit）",
     "...where the dog bit his leg.", "……在那里小狗___了他的腿。",
     "bite-bit-bitten（不规则动词）。"),
    ("run across", "v. 短语", "跑着穿过",
     "The robber ran across the yard...", "强盗___院子……",
     "across 穿过（平面）。"),
    ("into", "prep.", "碰撞",
     "...and into the donkey.", "……一头___了驴子。",
     "此处表碰撞；into 通常表进入。"),
    ("screeched", "v.", "尖叫（screech 的过去式）",
     "\"Cock-a-doodle-doo!\" screeched the rooster, flying across the roof.", "\"喔喔喔！\"公鸡___着飞过屋顶。",
     "screech 刺耳的尖叫。"),
    ("screamed", "v.", "尖叫（scream 的过去式）",
     "\"Aaaargh!\" screamed the robber, running away as fast as he could.", "\"啊！\"强盗___着，拼命逃跑。",
     "scream 尖叫（比 screech 常用）。"),
    ("horrible witch", "n. 短语", "可怕的女巫",
     "\"There's a horrible witch in the house,\" he panted.", "\"屋子里有一个___，\"他喘着气说。",
     "horrible 可怕的；witch 女巫（上册学过）。"),
    ("panted", "v.", "喘息（pant 的过去式）",
     "\"There's a horrible witch in the house,\" he panted.", "\"屋里有一个可怕的女巫，\"他___。",
     "pant 气喘；L3-2 学过 puffing and panting。"),
    ("spat at", "v. 短语", "朝……吐唾沫（spit 的过去式）",
     "\"She spat at me and scratched me.\"", "她朝我___，还抓伤了我。",
     "词表“吐……吏唾沫”系“朝……吐唾沫”之误；spit-spat-spit。"),
    ("stabbed", "v.", "（用刀等锐器）刺，戳，捅（stab 的过去式）",
     "\"He stabbed me in the leg.\"", "\"他___我的腿。\"",
     "stab 刺、捅（利器）。"),
    ("club", "v.", "击棍",
     "\"He beat me with his club.\"", "\"他用___打了我。\"",
     "词表标 v.，例句中实为名词“棍棒”；另 v. 用棍打。"),

    # ── Page 25 结局 ─────────────────────────────
    ("as for", "短语", "至于",
     "As for the four friends... they never did go to Bremen.", "___那四个好朋友……他们终究没去不来梅。",
     "as for + 名词，用于转移话题。"),
    ("the rest of their lives", "短语", "他们的余生",
     "They liked the house so much they stayed there for the rest of their lives.", "他们太喜欢那座房子了，___都住在了那里。",
     "the rest of the day 今天剩下的时间。"),
]

assert len(entries) == 46, f"expected 46 entries, got {len(entries)}"

start_id = 2694
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/bremen_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 bremen_rows.json")
