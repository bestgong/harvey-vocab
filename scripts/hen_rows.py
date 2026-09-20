#!/usr/bin/env python3
"""The Little Red Hen（第二套图书馆 L3-3）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-3 The Little Red Hen"
DATE = "2026-09-20"

# 从 id 2660 开始（The Boy Who Cried Wolf 到 2659）
entries = [
    # ── Page 2-3 开场：小红母鸡 ─────────────────────────────
    ("once upon a time", "短语", "从前",
     "Once upon a time, there was a little red hen.", "___，有一只红色的小母鸡。",
     "童话开头常用；后面常接 there was/there were。"),
    ("live on a farm", "v. 短语", "住在农场（过去式：lived）",
     "She lived on a farm in a little white hen house.", "她___，鸡舍是一栋带鲜红屋顶的小白屋。",
     "live on + 地点，住在某处。"),
    ("bright red", "adj. 短语", "鲜红的",
     "She lived on a farm in a little white hen house with a bright red roof.", "她的小白鸡舍有着___的屋顶。",
     "bright 明亮的；bright blue 蔚蓝。"),
    ("roof", "n.", "屋顶",
     "She lived on a farm in a little white hen house with a bright red roof.", "她的小白鸡舍有着鲜红色的___。",
     "复数 roofs。"),

    # ── Page 4-5 三位朋友 ─────────────────────────────
    ("glossy black", "adj. 短语", "乌黑发亮的",
     "A glossy black cat who lived in the farmhouse.", "一只___的猫住在农舍里。",
     "gloss 光泽 → glossy 有光泽的。"),
    ("farmhouse", "n.", "农舍",
     "A glossy black cat who lived in the farmhouse.", "一只乌黑发亮的猫住在___里。",
     "farm 农场 + house 房子。"),
    ("noisy", "adj.", "嗓门大的，聒噪的",
     "A big noisy duck who lived on the pond.", "一只大___的鸭子住在池塘上。",
     "noise 噪音（上册学过）；noisily adv.。"),
    ("quack", "n.", "（鸭子的）呱呱声",
     "\"Good morning noisy duck.\" \"Quack!\"", "\"早上好，大嗓门的鸭子。\"\"___！\"",
     "拟声词；moo 牛哞、oink 猪哼。"),
    ("barn", "n.", "谷仓",
     "And a fat brown rat who lived in the barn.", "还有一只住在___里的胖棕鼠。",
     "存放粮食的仓房。"),
    ("squeak", "n.", "吱吱声",
     "\"Good morning brown rat.\" \"Squeak!\"", "\"早上好，棕色的老鼠。\"\"___！\"",
     "老鼠叫声；squeaky 吱吱作响的。"),

    # ── Page 6-9 发现麦粒、种麦子 ─────────────────────────────
    ("juicy", "adj.", "多汁的，汁液丰富的",
     "She was looking for juicy worms to eat.", "她在找___的虫子当食物。",
     "juice 果汁 → juicy。"),
    ("worms", "n.", "虫子（worm 的复数）",
     "She was looking for juicy worms to eat.", "她在找多汁的___当食物。",
     "worm 蠕虫；bookworm 书虫。"),
    ("sharp toes", "n. 短语", "锋利的爪子",
     "She went \"scratch, scratch, scratch\" with her small sharp toes.", "她用小小的___刨土，咔嚓咔嚓响。",
     "sharp 锋利的（上册学过）；toe 脚趾。"),
    ("grains of wheat", "n. 短语", "麦粒",
     "She found some grains of wheat.", "她发现了几颗___。",
     "grain 谷粒；wheat 小麦。"),
    ("fluffed", "v.", "抖松，使松散（fluff 的过去式）",
     "\"Ooh!\" she cried. She fluffed her feathers.", "\"哦！\"她叫了起来，___自己的羽毛。",
     "fluff n. 绒毛。"),
    ("feathers", "n.", "羽毛（feather 的复数）",
     "\"Ooh!\" she cried. She fluffed her feathers.", "\"哦！\"她叫了起来，抖松自己的___。",
     "as light as a feather 轻如鸿毛。"),
    ("do it myself", "v. 短语", "自己动手做",
     "\"Fine!\" said the little red hen. \"Then I'll do it myself.\"", "\"好吧！\"小红母鸡说，\"那我就___。\"",
     "myself 我自己；DIY = do it yourself。"),
    ("pecked at", "v. 短语", "啄（peck 的过去式）",
     "The little red hen pecked at the ground and made a hole.", "小红母鸡___地面，刨出一个坑。",
     "peck 啄食；小鸟 peck at seeds。"),
    ("waste of time", "n. 短语", "浪费时间",
     "\"What a waste of time.\"", "\"真是___。\"",
     "waste v./n. 浪费；What a...! 感叹句。"),
    ("one by one", "adv. 短语", "一个接一个",
     "One by one, she dropped the grains in.", "她把麦粒___地丢进坑里。",
     "同结构：day by day 一天天。"),
    ("waited for", "v. 短语", "等待（wait 的过去式）",
     "The little red hen waited for her wheat to grow all through the winter.", "小红母鸡___她的麦子长大，熬过了一整个冬天。",
     "wait for sb./sth. 等待……。"),
    ("all through the winter", "短语", "整个冬天",
     "The little red hen waited for her wheat to grow all through the winter.", "___，小红母鸡都在守着她的麦子。",
     "all through 自始至终；同义 all winter long。"),

    # ── Page 10-13 麦子熟了、收割 ─────────────────────────────
    ("shoot", "n.", "嫩芽，新枝",
     "First, the shoots were small and green.", "起初，___又小又绿。",
     "shoot-shoots；另义 v. 射击。"),
    ("by spring", "短语", "到了春天",
     "By spring, the shoots were tall and strong.", "___，嫩芽长得又高又壮。",
     "by 到……时；by summer 到夏天。"),
    ("the wheat was ready.", "句型", "小麦熟了。",
     "At last, the wheat was ready.", "终于，___。",
     "be ready 准备好（上册学过 get ready）。"),
    ("cut down", "v. 短语", "砍倒（这里指收割小麦）",
     "\"Who will help me cut it down?\" said the little red hen.", "\"谁来帮我___？\"小红母鸡说。",
     "cut-cut-cut；down 表倒下。"),
    ("without any help at all", "短语", "没有任何帮助",
     "She cut down the wheat without any help at all.", "她把麦子割倒，___。",
     "not...at all 一点也不；书中重复出现三次。"),
    ("mill", "n.", "磨坊",
     "\"Who will help me take the wheat to the mill?\"", "\"谁来帮我把麦子送到___？\"",
     "windmill 风车；watermill 水磨。"),
    ("grind into", "v. 短语", "把……磨成……",
     "\"I want to grind it into flour.\"", "我想把它___面粉。",
     "grind-ground-ground（不规则动词）。"),
    ("flour", "n.", "面粉",
     "\"I want to grind it into flour.\"", "我想把它磨成___。",
     "与 flower 花 同音。"),
    ("ground it into flour", "v. 短语", "磨成了面粉",
     "She took the wheat to the mill and ground it into flour.", "她把麦子送去磨坊，___。",
     "ground 是 grind 的过去式。"),

    # ── Page 17-23 做面包、吃面包 ─────────────────────────────
    ("make the flour into bread", "v. 短语", "把面粉做成面包",
     "\"Who will help me make the flour into bread?\"", "\"谁来帮我___？\"小红母鸡问。",
     "make A into B 把 A 变成 B。"),
    ("bake the bread", "v. 短语", "烤面包",
     "She baked the bread without any help at all.", "她独自___，没让任何人插手。",
     "bake 烤（烤箱）；baker 面包师。"),
    ("jump up", "v. 短语", "跳起来",
     "The cat, the duck and the rat jumped up.", "猫、鸭子和老鼠都___。",
     "jump 跳（上册学过）；up 向上。"),
]

assert len(entries) == 34, f"expected 34 entries, got {len(entries)}"

start_id = 2660
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/hen_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 hen_rows.json")
