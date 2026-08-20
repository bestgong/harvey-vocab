#!/usr/bin/env python3
"""Oliver (汪培珽 L1-9) 词条 — 生成 add_rows JSON payload。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词的
直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定各自的
挖空词。
"""
import json

BOOK = "中级-2 汪培珽L1-9 Oliver"
DATE = "2026-08-20"

# 从 id 2365 开始（Captain Cat 到 2364）
entries = [
    # (word, pos, meaning, example, exampleZh_non_leaking, note)
    # ── Page 3 大象漂洋过海 ─────────────────────────────
    ("elephant", "n.", "大象（复数：elephants）",
     "Some elephants came across the ocean on a ship.", "一些___乘船漂洋过海而来。",
     "复数 elephants；本课主角 Oliver 就是一只 elephant。"),
    ("come across the ocean", "v. 短语", "漂洋过海（过去式：came）",
     "Some elephants came across the ocean on a ship.", "一些大象乘船___而来。",
     "came 是 come 的过去式；ocean=海洋。"),
    ("circus", "n.", "马戏团",
     "They were going to work in the circus.", "他们准备去___里工作。",
     "circus man=马戏团老板；circus parade=马戏团巡游。"),

    # ── Page 4 上岸清点 ─────────────────────────────
    ("land", "v.", "登陆，上岸（过去式：landed）",
     "When they landed the circus man counted them.", "他们___之后，马戏团老板清点数目。",
     "landed 是 land 的过去式；也可指飞机着陆。"),
    ("count", "v.", "（按顺序）数数；点数目（过去式：counted）",
     "When they landed the circus man counted them.", "他们上岸后，马戏团老板___。",
     "counted 是 count 的过去式。"),
    ("eleven", "num.", "十一",
     "\"And one makes eleven,\" said Oliver.", "\"再加一只就是___只，\"Oliver 说。",
     "ten 加 one = eleven。"),

    # ── Page 5 订错货 ─────────────────────────────
    ("mistake", "n.", "错误，过失",
     "\"There must be a mistake. I ordered only ten elephants.\"", "\"这里一定有___。我只订了十只大象。\"",
     "make a mistake=犯错。"),
    ("order", "v.", "订购（过去式：ordered）",
     "\"There must be a mistake. I ordered only ten elephants.\"", "\"一定弄错了。我只___了十只大象。\"",
     "ordered 是 order 的过去式；也可作\"命令\"。"),

    # ── Page 6 道别 ─────────────────────────────
    ("take up", "v. 短语", "占据（时间、地方）",
     "\"I won't take up much room,\" said Oliver.", "\"我不会___太多地方，\"Oliver 说。",
     "room 在此指空间；take up space=占空间。"),
    ("always", "adv.", "总是",
     "\"Elephants always do,\" said the circus man.", "\"大象___这样，\"马戏团老板说。",
     "反义 never。"),
    ("take good care of", "v. 短语", "照顾好，好好照看",
     "\"Take good care of yourself.\"", "\"要___你自己。\"",
     "= look after well。"),

    # ── Page 7 独自 + 老鼠 ─────────────────────────────
    ("all alone", "adv. 短语", "独自一人",
     "Oliver was all alone. He didn't know where to go.", "Oliver ___。他不知道该去哪里。",
     "= completely alone。"),
    ("come along", "v. 短语", "出现（过去式：came）",
     "A little mouse came along.", "一只小老鼠___了。",
     "came 是 come 的过去式；也可作\"跟着走\"。"),
    ("type", "n.", "类型，种类",
     "\"You look like the type they use there.\"", "\"你看起来像他们那里会用的那种___。\"",
     "= kind, sort。"),
    ("at once", "adv. 短语", "马上，立刻",
     "\"Thanks, I'll go at once,\" said Oliver.", "\"谢谢，我___就去，\"Oliver 说。",
     "= immediately, right away。"),

    # ── Page 8 出租车 + 搬运车 ─────────────────────────────
    ("taxi", "n.", "出租车，计程车",
     "\"Taxi!\" said Oliver.", "\"___！\"Oliver 喊道。",
     "= cab；打车常喊 Taxi!。"),
    ("moving van", "n. 短语", "家俱搬运车",
     "\"What you need is a moving van,\" said the taxi man.", "\"你需要的是一辆___，\"出租车司机说。",
     "van=厢式货车；moving=搬家的。"),
    ("follow", "v.", "跟着，跟随（过去式：followed）",
     "Oliver followed the cars.", "Oliver ___着那些车。",
     "followed 是 follow 的过去式。"),
    ("hold out", "v. 短语", "伸出（过去式：held）",
     "The drivers held out their hands when they made a turn.", "司机们转弯的时候___手臂。",
     "held 是 hold 的过去式；提示后车即将转弯。"),
    ("make a turn", "v. 短语", "转弯（过去式：made）",
     "The drivers held out their hands when they made a turn.", "司机们伸手示意他们要___。",
     "made 是 make 的过去式。"),

    # ── Page 9 象鼻 + 磅秤 ─────────────────────────────
    ("trunk", "n.", "象鼻",
     "When Oliver made a turn he held out his trunk.", "Oliver 转弯的时候伸出了他的___。",
     "此处指大象的鼻子；也可指树干、行李箱。"),
    ("weigh", "v.", "称重（现在分词：weighing）",
     "He saw a woman weighing herself.", "他看见一位女士在___。",
     "weighing 是 weigh 的现在分词。"),
    ("My goodness", "int.", "我的天啊（表吃惊）",
     "\"My goodness. I'm as heavy as an elephant,\" she said.", "\"___！我竟然像大象一样重，\"她说。",
     "= Oh my! 表惊讶。"),
    ("heavy", "adj.", "重的，沉的",
     "\"I'm as heavy as an elephant,\" she said.", "\"我像大象一样___，\"她说。",
     "反义 light。"),
    ("as...as", "conj.", "像……一样，同……一样",
     "\"I'm as heavy as an elephant,\" she said.", "\"我___大象一样重，\"她说。",
     "同级比较：as + 形容词 + as。"),

    # ── Page 10 磅秤 + 到达 + 主管 ─────────────────────────────
    ("scale", "n.", "磅秤",
     "Oliver got on the scale.", "Oliver 站上了___。",
     "复数 scales；用来称重的秤。"),
    ("reach", "v.", "到达，抵达（过去式：reached）",
     "At last Oliver reached the zoo.", "Oliver 终于___了动物园。",
     "reached 是 reach 的过去式。"),
    ("in charge", "adj. 短语", "负责，主管",
     "\"Who is in charge here?\" he asked.", "\"这里谁___？\"他问。",
     "in charge of=负责……。"),

    # ── Page 11 婉拒 ─────────────────────────────
    ("not right now", "adv. 短语", "现在不行",
     "\"I'm sorry, not right now,\" said the zoo man.", "\"抱歉，___，\"动物园管理员说。",
     "= not at this moment。"),
    ("Thanks anyway", "int. 短语", "还是要谢谢你",
     "\"Thanks anyway,\" Oliver said and walked away.", "\"___，\"Oliver 说着就走开了。",
     "被拒绝时的客气话。"),
    ("walk away", "v. 短语", "走开；离去（过去式：walked）",
     "\"Thanks anyway,\" Oliver said and walked away.", "\"还是要谢谢你，\"Oliver 说完就___了。",
     "walked 是 walk 的过去式。"),

    # ── Page 12 花生 + 诚实 ─────────────────────────────
    ("peanut", "n.", "花生，花生米（复数：peanuts）",
     "A man was selling peanuts.", "一个男人在卖___。",
     "复数 peanuts。"),
    ("May I help you", "int. 短语", "请问需要帮忙吗？请问您想买什么？",
     "\"May I help you sell them?\" asked Oliver.", "\"___我帮您卖它们？\"Oliver 问。",
     "商店/服务场景的礼貌用语。"),
    ("honest", "adj.", "诚实的，正直的",
     "The man gave him some peanuts for being honest.", "那人因为他很___，就给了他一些花生。",
     "honesty n. 诚实；反义 dishonest。"),

    # ── Page 13-14 宠物尝试 ─────────────────────────────
    ("pet", "n.", "宠物",
     "\"Would anyone like to have me for a pet?\" he asked.", "\"有人愿意把我当___吗？\"他问。",
     "常见 pets：dog、cat、bird 等。"),
    ("parakeet", "n.", "长尾小鹦鹉",
     "\"I have a parakeet,\" said one person.", "\"我已经有一只___了，\"一个人说。",
     "一种小型鹦鹉。"),
    ("person", "n.", "人",
     "\"I have a parakeet,\" said one person.", "\"我已经有一只鹦鹉了，\"一个___说。",
     "复数 people；another person=另一个人。"),
    ("goldfish", "n.", "金鱼",
     "\"I have goldfish,\" said another person.", "\"我已经有___了，\"另一个人说。",
     "单复数同形。"),

    # ── Page 15 其他人 + 狗 ─────────────────────────────
    ("someone else", "pron. 短语", "其他人",
     "\"I have a duck,\" said someone else.", "\"我有一只鸭子，\"___说。",
     "= another person。"),

    # ── Page 16 假扮 + 散步 ─────────────────────────────
    ("pretend", "v.", "伪装，假装；假扮",
     "\"I can pretend I'm a dog,\" said Oliver.", "\"我可以___是一只狗，\"Oliver 说。",
     "pretend to do sth. / pretend + 从句。"),
    ("go for a walk", "v. 短语", "散步（过去式：went）",
     "Oliver and the lady went for a walk.", "Oliver 和那位女士一起___。",
     "went 是 go 的过去式。"),

    # ── Page 17 干草 + 骨头 ─────────────────────────────
    ("hay", "n.", "（用作饲料的）干草",
     "\"Don't you have any hay?\" he asked.", "\"你没有___吗？\"他问。",
     "牛马大象的饲料。"),
    ("bone", "n.", "骨，骨头",
     "\"No, but I have a nice bone,\" said the lady.", "\"没有，但我有一根不错的___，\"那位女士说。",
     "复数 bones；狗爱啃 bone。"),

    # ── Page 18 毕竟 ─────────────────────────────
    ("after all", "adv. 短语", "毕竟；终究",
     "\"I guess I can't be your dog after all.\"", "\"看来我___当不了你的狗。\"",
     "常放句尾，表让步或补充。"),

    # ── Page 19 像 ─────────────────────────────
    ("like", "prep.", "像，如同",
     "\"You look like an elephant.\"", "\"你看起来___大象。\"",
     "此处为介词，注意与动词 like（喜欢）区分。"),

    # ── Page 20 骑马 + 跳栏 ─────────────────────────────
    ("giddyap", "int.", "驾（对马的吆喝声）",
     "\"Giddyap,\" he said.", "\"___，\"他吆喝道。",
     "催马快跑的口令。"),
    ("jump over", "v. 短语", "跳过（过去式：jumped）",
     "The horses jumped over the fence.", "马匹们___了栅栏。",
     "jumped 是 jump 的过去式。"),
    ("fence", "n.", "（赛马中的）障碍物；栅栏",
     "The horses jumped over the fence.", "马匹们跳过了___。",
     "赛马场里的跳栏，也泛指围栏。"),

    # ── Page 21 经过 + 荡秋千 ─────────────────────────────
    ("pass", "v.", "经过（过去式：passed）",
     "Oliver passed a playground.", "Oliver ___了一个游乐场。",
     "passed 是 pass 的过去式。"),
    ("swing", "v.", "（使）摆动，摇荡，荡秋千",
     "\"You may swing us,\" said the children.", "\"你可以帮我们___，\"孩子们说。",
     "swing 也作名词=秋千。"),

    # ── Page 22 不完全 + 跷跷板 ─────────────────────────────
    ("not quite", "adv. 短语", "不完全是",
     "\"Not quite,\" said the children.", "\"___，\"孩子们说。",
     "委婉否定；quite=完全。"),
    ("seesaw", "n.", "跷跷板",
     "\"It's a seesaw. We'll get on the other side.\"", "\"这是___。我们坐另一边。\"",
     "游乐场经典设施。"),

    # ── Page 23 滑梯 ─────────────────────────────
    ("slide", "n.", "滑滑梯",
     "The children rushed for the slide.", "孩子们冲向___。",
     "此处名词；slide 也可作动词=滑动。"),

    # ── Page 24 帮忙 + 谈论 + 长大 ─────────────────────────────
    ("help out", "v. 短语", "帮忙；帮助……摆脱困难（过去式：helped）",
     "Oliver helped out.", "Oliver 上前___。",
     "helped 是 help 的过去式。"),
    ("talk about", "v. 短语", "谈论某事（过去式：talked）",
     "The children talked about what they wanted to be when they grew up.", "孩子们___长大后想做什么。",
     "talked 是 talk 的过去式；单词表原文简写为 about。"),
    ("grow up", "v. 短语", "成长（过去式：grew）",
     "The children talked about what they wanted to be when they grew up.", "孩子们谈论他们___后想做什么。",
     "grew 是 grow 的过去式。"),

    # ── Page 25 想成为 + 护士 ─────────────────────────────
    ("want to be", "v. 短语", "想成为；想要成为",
     "\"I want to be a policeman,\" said Tommy.", "\"我___一名警察，\"Tommy 说。",
     "= would like to become。"),
    ("nurse", "n.", "护士",
     "\"I want to be a nurse,\" said Mary.", "\"我想成为一名___，\"Mary 说。",
     "复数 nurses。"),

    # ── Page 26 牛仔 ─────────────────────────────
    ("cowboy", "n.", "牧牛工，牛仔",
     "\"I want to be a cowboy,\" said Ben.", "\"我想成为一名___，\"Ben 说。",
     "美国西部形象；复数 cowboys。"),

    # ── Page 27 停下 + 巡游 ─────────────────────────────
    ("stop to do sth.", "v. 短语", "停下来去做某事（过去式：stopped）",
     "Everybody stopped to watch.", "大家都___看。",
     "stopped 是 stop 的过去式；对比 stop doing=停止正在做的事。"),
    ("circus parade", "n. 短语", "马戏团巡游",
     "They didn't see the circus parade coming.", "他们没看到___过来。",
     "parade=游行、巡游。"),

    # ── Page 28 杂技 + 玩杂耍 ─────────────────────────────
    ("acrobat", "n.", "杂技演员（复数：acrobats）",
     "They didn't see the acrobats.", "他们没看到那些___。",
     "复数 acrobats。"),
    ("juggler", "n.", "玩杂耍的人（复数：jugglers）",
     "They didn't see the jugglers.", "他们没看到那些___。",
     "juggle v. 抛接杂耍。"),

    # ── Page 29 小丑 + 训狮师 ─────────────────────────────
    ("clown", "n.", "小丑（复数：clowns）",
     "They didn't see the clowns!", "他们没看到那些___！",
     "复数 clowns。"),
    ("lion tamer", "n. 短语", "训狮师",
     "\"Are they looking at me?\" asked the lion tamer.", "\"他们在看我吗？\"___问。",
     "tame v. 驯服。"),

    # ── Page 30 跑过去 ─────────────────────────────
    ("run over to", "v. 短语", "跑过去（过去式：ran）",
     "He ran over to look.", "他___查看。",
     "ran 是 run 的过去式。"),

    # ── Page 31 犯错 ─────────────────────────────
    ("make a mistake", "v. 短语", "犯错（过去式：made）",
     "\"I made a big mistake. We do need you.\"", "\"我___了一个大错。我们确实需要你。\"",
     "made 是 make 的过去式。"),

    # ── Page 32 记得 + 当然 ─────────────────────────────
    ("remember", "v.", "记得；不忘记",
     "\"Will you remember us?\" asked the children.", "\"你会___我们吗？\"孩子们问。",
     "反义 forget。"),
    ("of course", "adv. 短语", "一定，当然",
     "\"Of course,\" said Oliver.", "\"___，\"Oliver 说。",
     "= certainly, sure。"),

    # ── Page 33 犀牛 ─────────────────────────────
    ("rhinoceros", "n.", "犀，犀牛",
     "\"And even a rhinoceros would remember the fun we had.\"", "\"就算是一头___也会记得我们一起的快乐。\"",
     "常缩写 rhino；复数 rhinoceroses。"),
]

start_id = 2365
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/oliver_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 oliver_rows.json")
