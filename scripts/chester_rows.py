#!/usr/bin/env python3
"""Chester (汪培珽 L1-6) 62 條詞條 — 生成 add_rows JSON payload。
Non-leaking Chinese hint principle: F 列例句翻譯不洩漏目標詞中文意思。
"""
import json

BOOK = "中级-2 汪培珽L1-6 Chester"
DATE = "2026-07-30"

# id 從 2193 起
entries = [
    # 序号, 单词, 词性, 中文释义, 英文例句, 例句翻译(不洩漏), 用法备注
    # ── Pages 3-6 野马登场 ─────────────────────────────────
    ("wild horse", "n. 短语", "野马", "Chester was a wild horse.", "Chester 曾是一匹___。", "wild=野生的；表示未被驯服的马。"),
    ("lived out", "v. 短语", "住在（live 过去式）", "He lived out West with other wild horses.", "他和其他野马一起在西部___。", "live out=住在（某处）；此处 lived 是过去式。"),
    ("west", "n.", "西部", "He lived out West with other wild horses.", "他和其他野马一起住在___。", "首字母大写 West 特指美国西部。"),
    ("take care of", "v. 短语", "照顾，抚养", "I wish someone took care of me.", "我希望有人来___我。", "took 是 take 的过去式；take care of sb=照顾某人。"),
    ("It is fun to be", "句型", "这（做某事）很有趣", "It is fun to be wild.", "___野生的（很有意思）。", "It is fun to be + adj/n。"),
    ("silly", "adj.", "傻傻的，愚蠢的", "You are silly.", "你真___。", "口语中带责备或调侃语气。"),

    # ── Pages 6-9 绳索、被带走 ───────────────────────────────
    ("rope", "n.", "粗绳，绳索", "One day men came with ropes.", "有一天，人们带着___来了。", "常见复数 ropes。"),
    ("be glad to", "v. 短语", "乐于……", "I am glad to see you.", "我___见到你。", "be glad to + do sth。"),
    ("cannot", "v.", "不能，无法", "That horse cannot run.", "那匹马___跑。", "cannot=can not 的连写形式。"),
    ("take", "v.", "带走（过去式：took）", "They took all the other horses.", "他们把其他所有的马都___了。", "took 是 take 的过去式。"),

    # ── Pages 10-11 臭鼬 ──────────────────────────────────
    ("either", "adv.", "也（不）", "No one wants me either.", "没有人想要我，___不想。", "either 用于否定句末，相当于\"也\"。"),
    ("skunk", "n.", "臭鼬", "He left in a hurry when the skunk came.", "当那只___过来时，他匆忙离开了。", "臭鼬受惊会喷出臭液。"),
    ("in a hurry", "adv. 短语", "立即，匆忙", "He left in a hurry.", "他___地离开了。", "in a hurry 修饰动作，表示仓促。"),

    # ── Pages 12-15 农场动物 ─────────────────────────────────
    ("maybe", "adv.", "大概，或许", "Maybe someone here wants me.", "___这里有人想要我。", "表示不确定的推测。"),
    ("lay egg", "v. 短语", "下蛋", "You can't lay eggs.", "你不会___。", "lay 在此为原形；单只蛋 lay an egg。"),
    ("pull the wagon", "v. 短语", "拉马车", "I pull the wagon around here.", "我在这里___。", "wagon=四轮运货马车；the 是定冠词。"),

    # ── Pages 16-19 公路、汽车 ─────────────────────────────────
    ("walk down", "v. 短语", "沿着……走（过去式：walked）", "He walked down the road.", "他___那条路。", "walk down + 路径。"),
    ("come by", "v. 短语", "经过", "A car came by.", "一辆汽车___。", "came 是 come 的过去式。"),
    ("horse power", "n. 短语", "马力（功率单位）", "This car has 250 horse power.", "这辆车有 250 ___。", "现代拼写常写作 horsepower。"),
    ("gas station", "n. 短语", "加油站", "The car stopped at a gas station.", "汽车在一个___停下了。", "美式英语；英式常用 petrol station。"),

    # ── Pages 20-22 加仑、指示牌 ─────────────────────────────
    ("gallon", "n.", "加仑（液量单位）", "I'll have ten gallons of gas.", "我要十___汽油。", "1 美加仑 ≈ 3.785 升。"),
    ("gas", "n.", "汽油", "I'll have ten gallons of gas.", "我要十加仑___。", "美式英语；英式为 petrol。"),
    ("sign", "n.", "指示牌，标志", "Chester saw a sign.", "Chester 看到了一块___。", "常见搭配 read a sign。"),
    ("oat", "n.", "燕麦", "The sign said OATS.", "指示牌上写着___。", "复数 oats 更常见；燕麦=马的主食。"),

    # ── Pages 22-25 水果店 ─────────────────────────────────
    ("fruit store", "n. 短语", "水果店", "Chester saw a fruit store.", "Chester 看到了一家___。", "美式；英式常用 fruit shop。"),
    ("a pound of", "n. 短语", "一磅", "I'll have a pound of apples.", "我要___苹果。", "1 磅 ≈ 0.454 千克。"),
    ("pay for", "v. 短语", "为……付钱", "Can you pay for them?", "你能___它们（付钱）吗？", "pay for + 商品。"),
    ("come back", "v. 短语", "回来", "Then come back when you can pay.", "那你能付钱时再___。", "come back 强调返回原地。"),

    # ── Page 26 食糖 ─────────────────────────────────────
    ("sugar", "n.", "食糖，方糖", "How much sugar do you want?", "你要多少___？", "不可数名词。"),
    ("as much as", "adv. 短语", "和……那样多", "As much as I can have.", "我能拿到的___。", "as much as + 从句/名词。"),

    # ── Pages 28-29 玩具店 ─────────────────────────────
    ("rocking horse", "n. 短语", "摇摆木马", "I wish I had a rocking horse.", "我希望有一匹___。", "儿童玩具；rock=前后摇动。"),

    # ── Pages 30-33 雕像、静止不动 ───────────────────────
    ("statue", "n.", "雕像", "Chester saw a statue of a horse.", "Chester 看到了一尊马的___。", "a statue of + 人/动物。"),
    ("still", "adj.", "静止的，不动的", "He stood very still.", "他站得非常___。", "此处形容词；另有副词义\"仍然\"。"),
    ("think", "v.", "认为，觉得（过去式：thought）", "All the people thought he was a statue.", "所有人都___他是一座雕像。", "thought 是 think 的过去式。"),

    # ── Pages 34-37 羽毛、打喷嚏 ─────────────────────
    ("feather", "n.", "羽毛", "Chester saw a lady with a feather in her hat.", "Chester 看到一位女士的帽子上有一根___。", "复数 feathers。"),
    ("sneeze", "v.", "打喷嚏", "I will sneeze if that feather touches my nose.", "如果那根羽毛碰到我的鼻子，我就会___。", "打喷嚏时也可作名词 a sneeze。"),
    ("touch", "v.", "接触，触及（过去式：touched）", "The feather touched his nose.", "那根羽毛___了他的鼻子。", "touched 是 touch 的过去式。"),
    ("walk away", "v. 短语", "走开，离去（过去式：walked）", "He walked away.", "他___了。", "walk away 强调离开现场。"),

    # ── Pages 40-45 消防车 ─────────────────────────────
    ("long ago", "adv. 短语", "在以前，很久以前", "Long ago horses pulled the fire engines.", "___马匹拉动消防车。", "位于句首常表时间背景。"),
    ("engine", "n.", "发动机，引擎", "They could not start the engine.", "他们发动不了___。", "消防车、汽车、火车的动力装置。"),
    ("start the engine", "v. 短语", "发动发动机", "They could not start the engine.", "他们无法___。", "start=启动；the engine=那台发动机。"),
    ("get you there", "v. 短语", "带你们到那里", "I will get you there in time.", "我会及时___。", "get sb somewhere=把某人送到某地。"),
    ("in time", "adv. 短语", "及时，适时", "I will get you there in time.", "我会___把你们带到那里。", "in time=不迟到；on time=准时。"),

    # ── Pages 46-49 消防车街头 ─────────────────────────
    ("clang", "n.", "叮当声，铿锵声", "Clang! Clang! Clang!", "___！___！___！", "金属碰撞声。"),
    ("the engine is running", "句型", "发动机运转了", "The engine is running again.", "___又转起来了。", "run 表示机器运转。"),

    # ── Pages 49-55 旋转木马 ─────────────────────────
    ("merry-go-round", "n.", "旋转木马", "He saw a merry-go-round.", "他看到了一个___。", "带连字符的复合名词；也叫 carousel。"),
    ("around and around", "adv. 短语", "一圈又一圈", "Around and around they went!", "他们转啊转，___！", "重复表示持续。"),
    ("ride", "n.", "游乐设施；乘骑", "The ride ended.", "那个___结束了。", "此处名词；rocking horse、merry-go-round 都是 ride。"),
    ("get off", "v. 短语", "从……下来（过去式：got）", "The children got off the horses.", "孩子们从马上___。", "get off + 交通工具；上车=get on。"),

    # ── Pages 56-57 争论、Giddyap ─────────────────────
    ("giddyap", "int.", "跑（对马的吆喝声）", "A real horse runs when you say 'Giddyap!'", "真马听到你喊\"___\"就会跑。", "美式牛仔用语；驾马疾行的口令。"),

    # ── Pages 58-59 Giddyap 时刻 ───────────────────────
    ("together", "adv.", "同时，一齐", "They all said it together.", "他们___喊了出来。", "表示动作齐发。"),

    # ── Pages 60-61 追回 ─────────────────────────────
    ("whoa", "int.", "吁（让马停下的口令）", "Whoa! they said.", "他们喊：\"___！\"", "对马发出的停止口令。"),

    # ── Pages 62-63 马厩 ─────────────────────────────
    ("stable", "n.", "马厩", "They took him to a bright, clean stable.", "他们把他带到了一间明亮、干净的___。", "养马的房屋。"),
    ("It is nice to be", "句型", "这样很好", "It is nice to be loved and cared for.", "被爱和被照顾___。", "It is nice to be + 过去分词/adj。"),

    # ── Page 64 结尾金句 ─────────────────────────────
    ("make sense", "v. 短语", "言之有理，有道理", "That makes sense.", "那___。", "常用短语；不合理=doesn't make sense。"),
    ("horse sense", "n. 短语", "常识", "Good horse sense.", "很好的___。", "字面\"马的判断力\"，引申为常识。"),
]

# 生成 rows: [id, word, pos, meaning, example, exampleZh, note, book, "未掌握", "0", DATE]
start_id = 2193
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"最后一条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/chester_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 chester_rows.json")
