#!/usr/bin/env python3
"""Danny and the Dinosaur（汪培珽 L1-10）词条及 Sheets 追加数据。"""
import json

BOOK = "中级-2 汪培珽L1-10 Danny and The Dinosaur"
DATE = "2026-08-27"
START_ID = 2435

# (word, pos, meaning, example, non-leaking exampleZh, note)
entries = [
    ("museum", "n.", "博物馆", "One day Danny went to the museum.", "一天，Danny 去了___。", "复数 museums。"),
    ("Indians", "n.", "美洲原住民（旧称；复数）", "He saw Indians.", "他看见了___。", "故事原文用 Indians；现代英语更常用 Native Americans 或 Indigenous people。"),
    ("Eskimo", "n.", "爱斯基摩人（旧称）", "He saw Eskimos.", "他看见了___。", "故事原文为复数 Eskimos；在具体语境中现在常用 Inuit 等更准确称呼。"),
    ("gun", "n.", "枪", "He saw guns.", "他看见了___。", "复数 guns。"),
    ("sword", "n.", "剑；刀", "He saw swords.", "他看见了___。", "复数 swords。"),
    ("dinosaur", "n.", "恐龙", "Danny loved dinosaurs.", "Danny 喜爱___。", "复数 dinosaurs。"),
    ("play with", "v. 短语", "和……一起玩", "It would be nice to play with a dinosaur.", "要是能和恐龙___就太好了。", "play with sb./sth.。"),
    ("It would be nice to...", "句型", "做某事就太好了", "It would be nice to play with a dinosaur.", "___和恐龙一起玩。", "用于表达愿望；to 后接动词原形。"),
    ("for a ride", "adv. 短语", "去兜风；乘一趟", "I can take you for a ride.", "我可以带你___。", "take sb. for a ride=带某人兜风。"),
    ("get on", "v. 短语", "上车；骑上", "He put his head down so Danny could get on him.", "他低下头，好让 Danny ___。", "反义 get off。"),
    ("stare at", "v. 短语", "盯着看；凝视", "A policeman stared at them.", "一名警察___他们。", "stare at sb./sth.。"),
    ("red light", "n. 短语", "红灯", "He had never seen a dinosaur stop for a red light.", "他从没见过恐龙为___停下来。", "交通信号灯；反义 green light。"),
    ("hold up", "v. 短语", "举起；抬起（过去式：held）", "The dinosaur was so tall Danny had to hold up the ropes for him.", "恐龙太高了，Danny 只好替他___绳子。", "held 是 hold 的过去式。"),
    ("look out", "int. 短语", "当心；小心", "\"Look out!\" said Danny.", "“___！”Danny 说。", "同义表达：watch out。"),
    ("make a noise", "v. 短语", "发出声响；弄出声音", "I can make a noise like a car.", "我能像汽车一样___。", "noise=响声、噪声。"),
    ("honk", "int./n.", "嘟嘟声；汽车喇叭声", "\"Honk! Honk! Honk!\"", "“___！___！___！”", "也可作动词，表示按喇叭。"),
    ("rock", "n.", "岩石；石块", "\"What big rocks,\" said the dinosaur.", "“多么大的___啊，”恐龙说。", "复数 rocks。"),
    ("building", "n.", "建筑物；楼房", "\"They are buildings,\" said Danny.", "“它们是___，”Danny 说。", "复数 buildings。"),
    ("climb", "v.", "攀登；爬", "\"I love to climb,\" said the dinosaur.", "“我喜欢___，”恐龙说。", "climb a tree/mountain。"),
    ("careful", "adj.", "小心的；仔细的", "The dinosaur had to be very careful.", "恐龙必须非常___。", "be careful not to do=小心不要做……。"),
    ("knock over", "v. 短语", "撞倒；碰翻", "The dinosaur had to be very careful not to knock over houses or stores with his long tail.", "恐龙必须非常小心，不要用长尾巴把房屋或商店___。", "knock-knocked-knocked。"),
    ("tail", "n.", "尾巴", "The dinosaur had to be very careful not to knock over houses or stores with his long tail.", "恐龙必须非常小心，不要用长长的___撞倒房屋或商店。", "复数 tails。"),
    ("wait for", "v. 短语", "等待", "Some people were waiting for a bus.", "一些人正在___公共汽车。", "wait for sb./sth.。"),
    ("rode on", "v. 短语", "骑在……上面；乘坐（ride on 的过去式）", "They rode on the dinosaur's tail instead.", "他们___恐龙的尾巴。", "rode 是 ride 的过去式。"),
    ("instead", "adv.", "代替；反而；却", "They rode on the dinosaur's tail instead.", "他们___骑在恐龙的尾巴上。", "常放在句末。"),
    ("bundle", "n.", "包裹；捆", "It's very nice of you to help me with my bundles.", "你帮我拿这些___，真是太好了。", "复数 bundles。"),
    ("all over", "prep. 短语", "遍及；到处", "Danny and the dinosaur went all over town.", "Danny 和恐龙走遍了___小镇。", "all over town=全城各处。"),
    ("take an hour or two off", "v. 短语", "休息一两个小时", "It's good to take an hour or two off after a hundred million years.", "过了一亿年，___是件好事。", "take time off=抽时间休息。"),
    ("hour", "n.", "小时", "It's good to take an hour or two off after a hundred million years.", "过了一亿年，休息一两个___是件好事。", "an hour；h 不发音。"),
    ("a hundred million", "num. 短语", "一亿", "It's good to take an hour or two off after a hundred million years.", "过了___年，休息一两个小时是件好事。", "100,000,000。"),
    ("ball game", "n. 短语", "球赛", "They even looked at the ball game.", "他们甚至看了___。", "这里指棒球比赛。"),
    ("home run", "n. 短语", "本垒打", "\"Hit a home run,\" said the dinosaur.", "“打一个___，”恐龙说。", "棒球用语。"),
    ("boat", "n.", "小船；艇", "\"I wish we had a boat,\" said Danny.", "“真希望我们有一条___，”Danny 说。", "复数 boats。"),
    ("toot", "int./n.", "嘟嘟声；汽笛声", "\"Toot, toot!\" went the boats.", "船发出“___，___”的声音。", "也可作动词，表示鸣笛。"),
    ("any of that", "pron. 短语", "那些东西中的任何一点", "I haven't eaten any of that for a very long time.", "我已经很久没有吃过___了。", "that 在文中指绿草。"),
    ("please keep off", "祈使句", "请勿践踏；请勿进入", "The sign said, \"PLEASE KEEP OFF.\"", "牌子上写着：“___。”", "keep off=不接近、不踩踏。"),
    ("ice cream", "n. 短语", "冰淇淋", "They both had ice cream instead.", "他们俩改吃了___。", "通常作不可数名词。"),
    ("animal", "n.", "动物", "\"Let's go to the zoo and see the animals,\" said Danny.", "“我们去动物园看___吧，”Danny 说。", "复数 animals。"),
    ("stay", "v.", "留下；停留", "Nobody stayed to see the lions.", "没有人___看狮子。", "stay to do=留下来做某事。"),
    ("seal", "n.", "海豹", "Nobody stayed to see the seals, giraffes or hippos, either.", "也没有人留下来看___、长颈鹿或河马。", "复数 seals。"),
    ("giraffe", "n.", "长颈鹿", "Nobody stayed to see the seals, giraffes or hippos, either.", "也没有人留下来看海豹、___或河马。", "复数 giraffes。"),
    ("hippo", "n.", "河马", "Nobody stayed to see the seals, giraffes or hippos, either.", "也没有人留下来看海豹、长颈鹿或___。", "hippopotamus 的简称；复数 hippos。"),
    ("go away", "v. 短语", "走开；离开", "Please go away so the animals will get looked at.", "请___，这样人们就会去看动物了。", "go-went-gone。"),
    ("get looked at", "v. 短语", "被观看；受到关注", "Please go away so the animals will get looked at.", "请走开，这样动物们就会___了。", "get + 过去分词可构成被动含义。"),
    ("There they are", "句型", "他们在那里；他们来了", "\"There they are,\" said Danny.", "“___，”Danny 说。", "用于发现或指出一群人/物。"),
    ("ride on", "v. 短语", "骑在……上；乘坐", "\"Why, it's Danny riding on a dinosaur,\" said a child.", "“咦，是 Danny ___一只恐龙，”一个孩子说。", "ride-rode-ridden。"),
    ("I'd be delighted", "句型", "我很乐意", "\"I'd be delighted,\" said the dinosaur.", "“___，”恐龙说。", "I'd=I would；礼貌表达愿意。"),
    ("delight", "v./n.", "使高兴；愉快", "\"I'd be delighted,\" said the dinosaur.", "“我会非常___，”恐龙说。", "delighted adj.=高兴的、乐意的。"),
    ("hold on tight", "v. 短语", "抓紧；紧紧握住", "\"Hold on tight,\" said Danny.", "“___，”Danny 说。", "hold-held-held。"),
    ("better than", "比较短语", "比……更好", "\"This is better than a merry-go-round,\" the children said.", "“这___旋转木马，”孩子们说。", "better 是 good/well 的比较级。"),
    ("merry-go-round", "n.", "旋转木马", "\"This is better than a merry-go-round,\" the children said.", "“这比___还好玩，”孩子们说。", "也可写作 carousel。"),
    ("out of breath", "adj. 短语", "上气不接下气；喘不过气", "The dinosaur was out of breath.", "恐龙累得___。", "breath n. 呼吸。"),
    ("tricks", "n.", "把戏；技巧（复数）", "\"Teach him tricks,\" said the children.", "“教他一些___，”孩子们说。", "单数 trick。"),
    ("shake hands", "v. 短语", "握手", "Danny taught the dinosaur how to shake hands.", "Danny 教恐龙怎样___。", "shake-shook-shaken。"),
    ("roll over on your back", "v. 短语", "翻身仰躺", "\"Can you roll over on your back?\" asked the children.", "“你能___吗？”孩子们问。", "roll over=翻身。"),
    ("hide and seek", "n. 短语", "捉迷藏", "\"Let's play hide and seek,\" said the children.", "“我们来玩___吧，”孩子们说。", "play hide and seek=玩捉迷藏。"),
    ("smart", "adj.", "聪明的；机灵的", "\"He's smart,\" said Danny.", "“他很___，”Danny 说。", "同义词：clever。"),
    ("pat", "v.", "轻拍（过去式：patted）", "\"He's smart,\" said Danny, patting the dinosaur.", "“他真聪明，”Danny 说着，___恐龙。", "patting 双写 t 再加 -ing。"),
    ("cover", "v.", "遮住；覆盖（过去式：covered）", "The dinosaur covered his eyes.", "恐龙___了眼睛。", "cover one's eyes=遮住眼睛。"),
    ("hide", "v.", "躲藏；藏起来（过去式：hid）", "All the children ran to hide.", "所有孩子都跑去___。", "hide-hid-hidden。"),
    ("give up", "v. 短语", "放弃；认输", "\"I give up,\" he said.", "“我___，”他说。", "课后词表重复列出两次，本词库只保留一次。"),
    ("one's turn", "n. 短语", "轮到某人", "Now it was the dinosaur's turn to hide.", "现在___躲了。", "one's 可替换为 my/your/his/her 或名词所有格。"),
    ("behind", "prep.", "在……后面", "The dinosaur hid behind a house.", "恐龙躲在一座房子___。", "反义 in front of。"),
    ("sign", "n.", "标牌；指示牌", "He hid behind a sign.", "他躲在一块___后面。", "复数 signs。"),
    ("gas tank", "n. 短语", "储气罐；煤气罐", "He hid behind a big gas tank.", "他躲在一个大___后面。", "tank=大型容器。"),
    ("make believe", "v. 短语", "假装；装作", "\"Let's make believe we can't find him,\" Danny said.", "“我们___找不到他吧，”Danny 说。", "同义词：pretend。"),
    ("fool", "v.", "欺骗；愚弄（过去式：fooled）", "\"He fooled us,\" said the children.", "“他把我们___了，”孩子们说。", "也可作名词=傻瓜。"),
    ("hurrah", "int.", "好哇；万岁", "\"Hurrah for the dinosaur!\" the children cried.", "“___恐龙！”孩子们欢呼道。", "表示欢呼；也写作 hurray。"),
    ("late", "adj.", "晚的；迟的", "It got late and the other children left.", "天色___，其他孩子都走了。", "此处作形容词；get late=天色变晚。"),
    ("alone", "adj./adv.", "单独的；独自", "Danny and the dinosaur were alone.", "Danny 和恐龙___待在一起。", "强调没有其他人在场。"),
    ("have fun", "v. 短语", "玩得开心", "\"We could have fun,\" said Danny.", "“我们可以___，”Danny 说。", "have-had-had。"),
    ("get back", "v. 短语", "回去；返回", "But now I must get back to the museum.", "但现在我必须___博物馆。", "get back to a place=回到某地。"),
    ("out of sight", "adj. 短语", "看不见；在视线之外", "Danny watched until the long tail was out of sight.", "Danny 一直望着，直到长尾巴___。", "sight=视线、视野。"),
    ("wonderful", "adj.", "极好的；精彩的", "But we did have a wonderful day.", "但我们确实度过了___一天。", "did 在此加强语气。"),
]

assert len(entries) == 74, f"expected 74 entries, got {len(entries)}"

rows = [
    [str(START_ID + i), word, pos, meaning, example, example_zh, note,
     BOOK, "未掌握", "0", DATE]
    for i, (word, pos, meaning, example, example_zh, note) in enumerate(entries)
]

assert rows[-1][0] == "2508"
assert all(len(row) == 11 for row in rows)
assert all("___" in row[5] for row in rows)

out_path = "/home/user/workspace/harvey-vocab/scripts/danny_dinosaur_rows.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"共 {len(rows)} 条")
print(f"id 范围: {rows[0][0]} - {rows[-1][0]}")
print(f"首条：{rows[0][1]}  末条：{rows[-1][1]}")
print(f"已写入 {out_path}")
