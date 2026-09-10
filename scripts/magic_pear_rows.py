#!/usr/bin/env python3
"""The Magic Pear Tree（第二套图书馆 L3-1）词条 — 生成 Sheets 追加 JSON。

非泄漏原则：F 列例句翻译不能透露答案。挖空目标词后，翻译中不出现该词
的直接中文对应；同一句子被多个 id 共享时，各自定制不同的翻译，各锁定
各自的挖空词。
"""
import json

BOOK = "中级-3 第二套图书馆L3-1 The Magic Pear Tree"
DATE = "2026-09-10"

INTRO = ("This story is about selfish Shen, a hungry beggar, a kind woman, "
         "some YUMMY pears and a little bit of magic.")

# 从 id 2569 开始（Go to Camp 到 2568）
entries = [
    # ── Page 2-3 开场五连 ─────────────────────────────
    ("selfish", "adj.", "自私的，利己的",
     INTRO, "这个故事讲的是___的 Shen、一个饿肚子的叫花子、一位好心的大婶、一些好吃的梨，还有一点儿魔法。",
     "反义词：unselfish 大方的。"),
    ("beggar", "n.", "乞丐，叫花子",
     INTRO, "这个故事讲的是小气的 Shen、一个饥饿的___、一位好心的大婶、一些好吃的梨，还有一点儿魔法。",
     "动词 beg 乞讨，加 -r 变名词。"),
    ("kind woman", "n. 短语", "善良的女人",
     INTRO, "这个故事讲的是小气的 Shen、一个饿肚子的叫花子、一位___、一些好吃的梨，还有一点儿魔法。",
     "kind adj. 善良的；kindness n. 好心。"),
    ("yummy", "adj.", "<非正式>美味的，可口的",
     INTRO, "这个故事讲的是小气的 Shen、一个饿肚子的叫花子、一位好心的大婶、一些___的梨，还有一点儿魔法。",
     "儿语常用；同义词：delicious。"),
    ("a little bit of", "短语", "一点点的",
     INTRO, "这个故事讲的是小气的 Shen、一个饿肚子的叫花子、一位好心的大婶、一些好吃的梨，还有___魔法。",
     "a bit of 也可；修饰不可数名词。"),

    # ── Page 4-5 甜梨 ─────────────────────────────
    ("sweet", "adj.", "甜的",
     "The tree grew sweet, golden pears.", "这棵树结出了___的金色梨子。",
     "sweet-_-sweetly；sweetie 糖果。"),
    ("golden pears", "n. 短语", "金色的梨",
     "The tree grew sweet, golden pears.", "这棵树结出了甜甜的___。",
     "golden adj. 金色的；gold n. 金子。"),

    # ── Page 6-7 卖梨 ─────────────────────────────
    ("too many", "短语", "太多",
     "There were too many pears for Shen.", "梨___，Shen 一个人根本吃不完。",
     "too many + 可数复数；too much + 不可数。"),
    ("share", "v.", "分享",
     "But he didn't want to share them.", "但他不想把梨___给别人。",
     "share sth. with sb. 和某人分享某物。"),
    ("at the market", "短语", "在市场",
     "\"I'll sell them at the market,\" he thought.", "\"我要去___把它们卖掉，\"他想。",
     "go to the market 去市场；market n. 市场。"),
    ("make lots of money", "v. 短语", "赚很多钱",
     "I'll make lots of money.", "这下我就能___了。",
     "make money 赚钱；lots of 许多。"),

    # ── Page 8-9 乞丐讨梨 ─────────────────────────────
    ("for sale", "adj. 短语", "出售；待售",
     "\"Pears for sale!\"", "\"梨子___！\"",
     "on sale 特价出售，注意区分。"),
    ("stop to", "v. 短语", "停下做……",
     "A beggar stopped to look.", "一个乞丐___看了看。",
     "stop to do 停下来去做；stop doing 停止做。上册 Oliver 学过 stop to do sth.。"),
    ("May I have…", "句型", "我可以……吗？",
     "\"Please may I have a pear?\" he said.", "\"请问，___一个梨吗？\"他说。",
     "礼貌请求句型；回答常用 Yes, you may。"),

    # ── Page 10-11 付钱与刻薄 ─────────────────────────────
    ("pay", "v.", "支付，付钱",
     "\"Can you pay?\" asked Shen.", "\"你能___吗？\"Shen 问。",
     "pay for sth. 为某物付钱。"),
    ("go away", "v. 短语", "走开",
     "\"Then go away!\" shouted Shen.", "\"那就___！\"Shen 大喊。",
     "上册学过；反义词：come here。"),
    ("How mean!", "感叹句", "真刻薄！",
     "How mean!", "\"___！\"路人感叹道。",
     "How + 形容词，感叹句型。"),
    ("mean", "adj.", "吝啬的，刻薄的",
     "How mean!", "他这个人可真___！",
     "另义：意思是（What do you mean?）。"),

    # ── Page 14-17 赠梨 ─────────────────────────────
    ("give away", "v. 短语", "赠送",
     "\"Can't you give away one pear?\" she asked Shen.", "\"你就不能___一个梨吗？\"她问 Shen。",
     "away 表示送出去；上册 Happy Birthday 学过 give out 分发。"),
    ("enough to", "短语", "足以，足够",
     "\"That man is hungry and you have enough to share.\"", "\"那个人饿了，你的梨多到___分给他。\"",
     "enough + to do 足够做某事。"),
    ("That's kind of you.", "句型", "你真好。",
     "That's kind of you.", "\"谢谢，\"乞丐说，\"___。\"",
     "感谢用语；it is + adj. + of sb. 句型。"),

    # ── Page 18-21 吃梨 ─────────────────────────────
    ("quickly", "adv.", "快速地；很快",
     "He ate the pear quickly.", "他把这个梨吃得___。",
     "quick adj.；同义词：fast。"),
    ("spit out", "v. 短语", "吐出（过去式：spat）",
     "He spat out the seeds.", "他把梨籽___到地上。",
     "spit-spat-spat 不规则；反义词组：swallow down 吞下。"),
    ("happily", "adv.", "快乐地；幸运地",
     "\"Mmm, yummy,\" he said happily.", "\"嗯，真好吃，\"他___地说。",
     "happy adj. → happily adv.。"),
    ("my turn to", "短语", "轮到我……",
     "\"Now, it's my turn to give you a pear.\"", "\"现在，___送你一个梨了。\"",
     "turn n. 轮到的机会；one's turn to do。上册学过 one's turn。"),
    ("You Do have money!", "句型", "你其实有钱！",
     "\"You DO have money!\"", "\"啊哈！___\"Shen 叫道。",
     "DO 大写表示强调：确实、其实。"),

    # ── Page 22-27 种梨 ─────────────────────────────
    ("shake head", "v. 短语", "摇摇头（过去式：shook）",
     "The woman shook her head.", "那位女士___。",
     "shake-shook-shaken；shake one's head 摇头（表示否定）。"),
    ("crowd", "n.", "人群",
     "A crowd came to watch.", "___围拢过来看热闹。",
     "a crowd of 一群；crowded adj. 拥挤的。"),
    ("dig a hole", "v. 短语", "挖个坑（过去式：dug）",
     "The beggar dug a hole.", "乞丐在地上___。",
     "dig-dug-dug 不规则；hole n. 洞。"),
    ("dropped in", "v. 短语", "（使）落进（drop 的过去式）",
     "And dropped in the seeds.", "然后把种子___了坑里。",
     "drop v. 掉落；in 表示进去。"),
    ("hot water", "n. 短语", "热水",
     "\"May I have some hot water?\" he said.", "\"请问可以给我一些___吗？\"他说。",
     "ice water 冰水；warm water 温水。"),
    ("tea-seller", "n.", "卖茶的人",
     "A tea-seller gave him a teapot.", "一位___递给他一把茶壶。",
     "名词 + seller = 卖……的人；book-seller 卖书的。"),
    ("teapot", "n.", "茶壶",
     "A tea-seller gave him a teapot.", "一位卖茶人递给他一把___。",
     "词表原文标 v.，实为名词：tea + pot 合成词。"),
    ("pour into", "v. 短语", "倒入，灌注（过去式：poured）",
     "The beggar poured hot tea into the hole.", "乞丐把热茶___了坑里。",
     "pour 倒；pour out 倒出。"),
    ("gasped", "v.", "倒吸气（gasp 的过去式）",
     "The crowd gasped.", "围观的人都___了一口凉气。",
     "gasp 因惊讶而猛吸一口气。"),
    ("shoot", "n.", "嫩芽，新枝",
     "\"Look, a shoot!\"", "\"快看，一个___！\"",
     "另义 v. 射击（shoot-shot-shot）。"),
    ("grow and grow", "v. 短语", "长啊长（过去式：grew）",
     "The shoot grew and grew.", "小芽___，越长越高。",
     "grow-grew-grown；and 连接重复动词表示持续。"),

    # ── Page 28-33 分梨 ─────────────────────────────
    ("pick", "v.", "采，摘（花、果）（过去式：picked）",
     "The beggar picked a pear and gave it to the woman.", "乞丐从树上___了一个梨递给那位女士。",
     "上册 Happy Birthday 学过 pick up 捡起、接人。"),
    ("turned to", "v. 短语", "转身，转过头（turn 的过去式）",
     "The beggar turned to the crowd.", "乞丐___人群，大声问。",
     "turn to sb. 转向某人；turn-turned。"),
    ("anyone else", "代词短语", "还有谁，其他人",
     "\"Does anyone else want a pear?\"", "\"___还想要一个梨吗？\"",
     "else 别的；what else 还有什么。上册 Oliver 学过 someone else。"),
    ("pear after pear", "n. 短语", "一个又一个的梨",
     "The beggar picked pear after pear.", "乞丐___，摘个不停。",
     "名词 + after + 名词，表示一个接一个。"),

    # ── Page 34-39 树空了 ─────────────────────────────
    ("bare", "adj.", "光秃秃的",
     "Soon the tree was bare.", "很快，树就___了，一个果子也不剩。",
     "bare 光秃的；bear 熊，注意拼写。"),
    ("even", "adv.", "甚至",
     "Everyone got one - even selfish Shen.", "每个人都分到了一个——___小气的 Shen 也不例外。",
     "even 放在强调的部分前；另义 adj. 平的。"),

    # ── Page 40-43 砍树离开 ─────────────────────────────
    ("watch", "v.", "留意，关注",
     "Now no one was watching the beggar.", "这时大家的注意力都在梨上，没有人再___着乞丐。",
     "watch 注视；上册学过 watch out 小心。"),
    ("chop down", "v. 短语", "砍下（过去式：chopped）",
     "He chopped down the tree.", "他把树给___了。",
     "上册 Grizzwold 学过；chop v. 砍。"),
    ("stroll", "v.", "散步，闲逛（过去式：strolled）",
     "He chopped down the tree and strolled away.", "他把树砍倒，然后___走了。",
     "文中 stroll away 可理解为离开了。"),
    ("look around", "v. 短语", "环顾四周",
     "Suddenly, Shen looked around.", "突然，Shen ___了一下，四处张望。",
     "look around = look about。"),

    # ── Page 44-47 骗局与教训 ─────────────────────────────
    ("trick", "n.", "诡计，骗局",
     "\"It was a trick,\" he yelled.", "\"这是一个___！\"他大喊。",
     "play a trick on sb. 捉弄某人。"),
    ("turn … into", "v. 短语", "把……变成",
     "\"The beggar turned my box into a tree by magic.\"", "\"乞丐用魔法把我的箱子___了一棵树。\"",
     "turn A into B；by magic 用魔法。"),
    ("crafty", "adj.", "狡猾的",
     "That crafty beggar!", "那个___的叫花子！",
     "craft 手艺；crafty 狡猾的。"),
    ("next time", "短语", "下次",
     "\"Next time, perhaps you'll be less selfish,\" they said.", "\"___，说不定你会大方一点，\"大家说。",
     "上册学过 next year；this time 这次。"),
    ("perhaps", "adv.", "也许，可能",
     "\"Next time, perhaps you'll be less selfish,\" they said.", "\"下次，___你会大方一点，\"大家说。",
     "同义词：maybe、probably。"),
    ("less selfish", "adj. 短语", "少一些自私",
     "\"Next time, perhaps you'll be less selfish,\" they said.", "\"下次，也许你能比这次___一点，\"大家说。",
     "less + 形容词，更少地；反义组：more selfish。"),
]

assert len(entries) == 53, f"expected 53 entries, got {len(entries)}"

start_id = 2569
rows = []
for i, (word, pos, meaning, ex, ex_zh, note) in enumerate(entries):
    row_id = start_id + i
    rows.append([str(row_id), word, pos, meaning, ex, ex_zh, note, BOOK, "未掌握", "0", DATE])

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")

with open("/home/user/workspace/harvey-vocab/scripts/magic_pear_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print("已写入 magic_pear_rows.json")
