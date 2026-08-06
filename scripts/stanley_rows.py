#!/usr/bin/env python3
"""Stanley (汪培珽 L1-7) 55 條詞條 — 生成 add_rows JSON payload。
Non-leaking Chinese hint: F 列例句翻譯不洩漏目標詞中文意思，用 ___ 遮蔽。
"""
import json

BOOK = "中级-2 汪培珽L1-7 Stanley"
DATE = "2026-08-06"

# 序号从 2249 起（Chester 到 2248）
entries = [
    # (word, pos, meaning, example, exampleZh_non_leaking, note)
    # ── Pages 3-6 山洞里的日子 ─────────────────────────────
    ("a long time ago", "adv. 短语", "很久以前", "A long time ago there were no houses.",
     "___，那时还没有房子。", "常用于故事开头，交代时间背景。"),
    ("cave", "n.", "洞穴，山洞",
     "Stanley lived in a cave, but he did not like it.", "Stanley 住在___里，但他不喜欢。",
     "复数 caves；穴居人=caveman。"),
    ("cold", "adj.", "冷的，凉的",
     "The cave was cold. So Stanley was cold.", "山洞很___，所以 Stanley 也很___。",
     "反义词=hot；此处形容天气/身体感觉。"),
    ("hurt", "v.", "感到疼痛，受伤",
     "His head hurt because he had to sleep on a rock.", "他的头很___，因为他不得不睡在岩石上。",
     "hurt 现在式和过去式同形；hurt-hurt-hurt。"),
    ("had to", "v. 短语", "不得不做某事",
     "He had to sleep with it on a rock.", "他___把头枕在岩石上睡觉。",
     "have to 的过去式；表示不情愿的必须。"),
    ("rock", "n.", "岩石，礁石",
     "He had to sleep with his head on a rock.", "他不得不把头枕在一块___上睡觉。",
     "复数 rocks；花岗岩=granite rock。"),
    ("bat", "n.", "蝙蝠",
     "Bats flew around as though they owned the place.", "___在四周飞来飞去，仿佛这地方是它们的。",
     "同形词 bat=球棒；复数 bats。"),
    ("fly around", "v. 短语", "飞来飞去（过去式：flew）",
     "Bats flew around as though they owned the place.", "蝙蝠们___，仿佛这地方是它们的。",
     "flew 是 fly 的过去式；around=到处。"),
    ("as though", "conj.", "好像，仿佛",
     "Bats flew around as though they owned the place.", "蝙蝠们飞来飞去，___这地方是它们的。",
     "= as if，引导虚拟从句。"),
    ("own", "v.", "拥有，有（过去式：owned）",
     "Bats flew around as though they owned the place.", "蝙蝠们飞来飞去，仿佛___了这个地方。",
     "owned 是 own 的过去式；own 还可作 adj.=自己的。"),

    # ── Page 6 更好的方式 ─────────────────────────────
    ("better way", "n. 短语", "更好的方式",
     "Why can't we find a better way to live?", "为什么我们不能找到一种___来生活？",
     "better 是 good 的比较级。"),
    ("be good enough for", "v. 短语", "对……来说已经足够好",
     "This is good enough for us.", "这对我们来说___了。",
     "good enough=足够好；for + 对象。"),

    # ── Pages 7-9 硬汉与温柔 ─────────────────────────────
    ("carry", "v.", "提，扛，背（过去式：carried）",
     "The cavemen carried clubs.", "穴居人们___着棍棒。",
     "carried 是 carry 的过去式；y→ied。"),
    ("club", "n.", "棍棒",
     "The cavemen carried clubs.", "穴居人们扛着___。",
     "复数 clubs；另有\"俱乐部\"义。"),
    ("tough", "adj.", "吃苦耐劳的，坚韧不拔的",
     "They were very tough. Stanley was tough, too.", "他们非常___。Stanley 也很___。",
     "同时也有\"艰难的\"义，如 tough job。"),
    ("plant seeds", "v. 短语", "播种",
     "He liked to plant seeds in the ground and watch them grow.", "他喜欢在地里___，然后看着它们生长。",
     "plant=种植；seed=种子。"),
    ("paint pictures", "v. 短语", "画画",
     "He liked to paint pictures.", "他喜欢___。",
     "paint=用颜料画；picture=画作。"),
    ("be nice to", "v. 短语", "对……亲切，善待",
     "He liked to be nice to people.", "他喜欢___别人。",
     "be nice to sb=对某人友好。"),
    ("be kind to", "v. 短语", "友好对待",
     "He was kind to animals.", "他___小动物。",
     "was 是 is 的过去式；be kind to sb/sth。"),

    # ── Pages 10-11 冲突与坚持 ─────────────────────────
    ("act this way", "v. 短语", "照这样做，这样表现",
     "The other cavemen did not want Stanley to act this way.", "其他穴居人不希望 Stanley ___。",
     "act=表现，行为；this way=这样。"),
    ("act more like a caveman", "v. 短语", "表现得更像个穴居人",
     "Can't you act more like a caveman?", "你就不能___吗？",
     "more like=更像；caveman=穴居人。"),
    ("go on", "v. 短语", "继续（过去式：went）",
     "He went on planting seeds and painting pictures.", "他___播种和画画。",
     "went on 是 go on 的过去式；后接 doing。"),
    ("lovely day today", "句型", "今天天气真好",
     "Lovely day today, isn't it?", "___，是吧？",
     "英式寒暄；lovely=美好的。"),

    # ── Page 12 惹怒与驱逐 ─────────────────────────────
    ("make angry", "v. 短语", "惹怒（过去式：made）",
     "This made the other cavemen very angry.", "这___了其他穴居人。",
     "made 是 make 的过去式；make sb angry。"),
    ("chase away", "v. 短语", "驱逐，赶走",
     "They threw rocks at Stanley and chased him away.", "他们朝 Stanley 扔石头，把他___。",
     "chased 是 chase 的过去式。"),
    ("beat", "v.", "打，狠打",
     "Beat it!", "___吧！（滚开！）",
     "此处 \"Beat it!\" 是俚语=滚开、走开。"),

    # ── Pages 13-14 找地方住 ─────────────────────────────
    ("I don't care", "句型", "我不在乎",
     "I don't care. It was cold anyway.", "___，反正山洞很冷。",
     "care=在乎；用于表示无所谓。"),
    ("anyway", "adv.", "不管怎样，反正",
     "It was cold anyway.", "___山洞很冷。",
     "常放句末或句首，语气缓和。"),
    ("nest", "n.", "窝，巢",
     "You can't live in a nest, said the birds.", "鸟儿说：你不能住在___里。",
     "鸟窝=bird's nest。"),
    ("live in", "v. 短语", "居住在",
     "You can't live in the water, said the fish.", "鱼说：你不能___水里。",
     "live in + 地点；in the water=在水里。"),
    ("worm", "n.", "蠕虫",
     "You can't live in the ground, said a worm.", "一只___说：你不能住在地里。",
     "常见如 earthworm=蚯蚓。"),
    ("while", "conj.", "当……的时候",
     "Not while I'm up here, said an ape.", "___我在上面时不行，一只猿说。",
     "while + 从句，表示同时发生。"),
    ("ape", "n.", "猿，类人猿",
     "Not while I'm up here, said an ape.", "\"我在上面时你不能上来，\"一只___说。",
     "如 gorilla、chimpanzee 都是 ape。"),

    # ── Page 16 太空冒险 ─────────────────────────────
    ("space", "n.", "太空，空间",
     "Maybe I can live in space, said Stanley.", "Stanley 说：也许我可以住在___。",
     "outer space=外太空。"),
    ("jump off", "v. 短语", "跳下来（过去式：jumped）",
     "He jumped off a rock.", "他从一块岩石上___。",
     "jumped 是 jump 的过去式；jump off + 位置。"),
    ("ouch", "int.", "哎哟（突然疼痛时发出的声音）",
     "Ouch! said Stanley.", "\"___！\"Stanley 喊道。",
     "常用于被撞、被扎时的反应。"),

    # ── Pages 17-18 找草地 ─────────────────────────────
    ("Does anybody mind", "句型", "有人介意吗？",
     "Does anybody mind if I live here?", "如果我住在这里，___？",
     "mind=介意；后跟 if 引导条件。"),
    ("snore", "v.", "打鼾",
     "I don't mind if you don't snore.", "只要你不___，我就不介意。",
     "睡觉时发出鼾声。"),
    ("go to sleep", "v. 短语", "去睡觉（现在分词：going）",
     "Said an animal who was going to sleep.", "一只准备___的动物说道。",
     "fall asleep=入睡，稍有差别。"),
    ("take up too much room", "v. 短语", "占据太多空间",
     "I don't mind if you don't take up too much room.", "只要你不___，我就不介意。",
     "take up=占用；room=空间（不可数）。"),

    # ── Pages 19-20 造房子 ─────────────────────────────
    ("made himself at home", "v. 短语", "像在自己家里一样",
     "Stanley made himself at home.", "Stanley ___住了下来。",
     "住得舒适惬意；make oneself at home。"),
    ("suddenly", "adv.", "突然地，出乎意料地",
     "But suddenly the wind blew and Stanley was cold.", "但___起风了，Stanley 冷了起来。",
     "sudden=突然的；suddenly 修饰动词。"),
    ("the wind blow", "v. 短语", "起风（过去式：blew）",
     "Suddenly the wind blew.", "突然___了。",
     "blew 是 blow 的过去式；the wind blew=风吹起来。"),
    ("worse than", "adj. 短语", "比……更差",
     "This is worse than the cave.", "这比山洞___。",
     "worse 是 bad 的比较级；反义 better than。"),
    ("wall", "n.", "墙壁，围墙",
     "He made walls to keep out the wind.", "他砌了___来挡风。",
     "复数 walls；砌墙=build a wall。"),
    ("keep out", "v. 短语", "阻止进入，挡住",
     "He made walls to keep out the wind.", "他砌墙来___风。",
     "keep out sth=把某物挡在外面。"),
    ("roof", "n.", "屋顶",
     "He made a roof to keep out the rain.", "他做了一个___来挡雨。",
     "on the roof=在屋顶上。"),
    ("chimney", "n.", "烟囱，烟道",
     "He made a door, windows and chimney.", "他做了一扇门、几扇窗和一个___。",
     "壁炉的排烟管道。"),
    ("field mouse", "n. 短语", "田鼠",
     "That's the first house I ever saw, said a field mouse.", "一只___说：这是我见过的第一座房子。",
     "field=田野；mouse=老鼠（复数 mice）。"),

    # ── Page 22 田鼠回应 ─────────────────────────────
    ("belong in", "v. 短语", "属于……，适合在……",
     "I belong in the field.", "我___田野里。",
     "belong in + 地方；表示归属。"),
    ("from time to time", "adv. 短语", "不时，偶尔",
     "But I will come and visit you from time to time.", "但我会___来看你的。",
     "= occasionally；比 sometimes 更书面。"),

    # ── Pages 24 孤独 ─────────────────────────────
    ("lonesome", "adj.", "寂寞的，孤独的",
     "He loved his house. But he was lonesome.", "他喜欢他的房子，但他很___。",
     "= lonely；美式常用。"),
    ("wonder", "v.", "想知道，纳闷",
     "I wonder how my friends are, he said.", "他说：\"我___我的朋友们过得怎样。\"",
     "wonder + wh-从句；表示好奇。"),

    # ── Page 25 追赶穴居人 ─────────────────────────────
    ("out of here", "adv. 短语", "离开这里",
     "Let's chase them out of here.", "我们把他们赶___吧。",
     "out of + 场所；离开某处。"),

    # ── Page 26 救人 ─────────────────────────────
    ("be afraid", "v. 短语", "害怕",
     "Don't be afraid, he said.", "他说：\"不要___。\"",
     "be afraid of sth=害怕某物。"),
    ("go away", "v. 短语", "走开，离开",
     "He made the animals go away.", "他让动物们___。",
     "made sb do sth=使某人做某事（省 to）。"),
    ("save", "v.", "救助，搭救（过去式：saved）",
     "You saved us, Stanley, said the cavemen.", "穴居人们说：Stanley，你___了我们。",
     "saved 是 save 的过去式；save sb=拯救某人。"),

    # ── Page 28 房子不再是山洞 ─────────────────────────────
    ("old-fashioned", "adj.", "过时的，老式的",
     "Caves are old-fashioned, said Stanley.", "Stanley 说：山洞已经___了。",
     "带连字符；反义 modern=现代的。"),
    ("this is the way", "句型", "这就是……的方式",
     "This is the way we want to live.", "___我们想要的生活方式。",
     "the way + 从句，表示方式。"),
    ("people", "n.", "人，人们，人类",
     "A cave is for bears. A house is for people.", "山洞是熊住的，房子是给___住的。",
     "集合名词，作主语时用复数动词。"),

    # ── Page 30-31 教朋友 ─────────────────────────────
    ("showed", "v.", "展示，向……示范（show 的过去式）",
     "Stanley showed them how to paint pictures.", "Stanley ___他们怎么画画。",
     "show sb how to do sth=教某人做某事。"),
    ("each other", "pron. 短语", "彼此，互相",
     "He showed them how to be nice to each other.", "他教他们如何善待___。",
     "两人以上互相，作宾语；不作主语。"),
]

start_id = 2249
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/stanley_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 stanley_rows.json")
