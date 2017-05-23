#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pythonrouge.pythonrouge import Pythonrouge

#ROUGE-1.5.5.pl
ROUGE_path = "./lib/pythonrouge/pythonrouge/RELEASE-1.5.5/ROUGE-1.5.5.pl"
#data folder in RELEASE-1.5.5
data_path = "./lib/pythonrouge/pythonrouge/RELEASE-1.5.5/data"

# initialize setting of ROUGE, eval ROUGE-1, 2, SU4, L
rouge = Pythonrouge(n_gram=4, ROUGE_SU4=True, ROUGE_L=True, stemming=True, stopwords=True, word_level=True, length_limit=True, length=50, use_cf=False, cf=95, scoring_formula="average", resampling=True, samples=1000, favor=True, p=0.5)

"""
# summary: double list
summary = [[summaryA_sent1, summaryA_sent2], [summaryB_sent1, summaryB_sent2]]
# reference: triple list
reference = [[[summaryA_ref1_sent1, summaryA_ref1_sent2], [summaryA_ref2_sent1, summaryA_ref2_sent2]],
             [[summaryB_ref1_sent1, summaryB_ref1_sent2], [summaryB_ref2_sent1, summaryB_ref2_sent2]]
"""

# summary = [["我跟你讲，我真的想弄死她们的感觉，可能真的因为我现在在大学，但是我的班主任和辅导员都超级好，一对比，我真的不知道那个女生受了多少伤害，每科都是59分，该有多悲哀#北京电影学院性侵案# ​​​​","#北京电影学院性侵案##北京电影学院# 我毕业于北电 这个事件中 我唯一认识且了解的是朱老师 也是我唯一有资格去说出对其观点的人 我想大部分网民也许对于这个事件中的任何人都不认识 但却可以在网络中对其进行评论甚至语言攻击 所以作为认识朱老师的我来说 我有资格谈谈我的老师 她带我们去平遥布展 在 ​​​​...","#北京电影学院性侵案#卧槽，这个话题也太恶心了吧，就这样被压下去了？名校老师都这么可耻的吗 ​​"​​,"#北京电影学院性侵案#我真的是觉得有些人的思想恐怕都是跟朱姓教授靠齐，他们给你多少钱让你帮他们干这种伤天害理的事，老话说得好，不是不报，时候未到，你要真做了缺德的事，你还真别怕没人发现，这是迟早的事，你以为你一手遮天什么事都能干了，人不是你想的那么简单"]]
# reference = [[["【网曝北影学生遭老师父亲性侵】今日，有网友实名曝出，称其朋友在北影就读期间曾遭班主任朱某的父亲性侵，且发声后在校疑似遭排挤与打压。有媒体就此事联系该生老师，对方回应：“我也不是当事人，所以现在不好说什么，我觉得应该通过法律部门来解决。”随后，北京电影学院官微辟 ...","不管事实是什么，都希望这件事能够合法公正地解决，不能让一个人无缘无故地受到伤害。","#阿廖沙同学发文# 哇，话题一直在热搜榜前10，但是点进去却只有几条评论不得不说，现在学校简直太可怕了被爆出这种事后，不去调查事情的始末，反而一直在微博删评论，做公关，大家又不是瞎的。如果想洗白就应该把事情的真相找出来，还大家一个公道才对， ...","#不能说的夏天# 《不能说的夏天》郭采洁饰演的角色跟林奕含很像，被老师性侵，为了让自己好过，说服自己爱上老师。但其实，被迫害的阴影却一直阴魂不散。不过我实在不能理解的是，那些肆意揣测受害者，而为犯罪者开脱的人的心理，这无疑是人最大的恶意。文化人下作起来，超过屠狗辈。","#京城事#【网曝北影学生遭老师父亲性侵】今日，有网友实名曝出，称其朋友在北影就读期间曾遭班主任朱某的父亲性侵，且发声后在校疑似遭排挤与打压。有媒体就此事联系该生老师，对方回应：“我也不是当事人，所以现在不好说什么，我觉得应该通过法律部门来解决。”随后，北京 ..."]]]
# system summary & reference summary
summary = [["#大连15中车祸#  据@大连公安，5月10日17时51分许，崔某（男，67岁）驾驶车牌号为辽B3xxx2越野车，驶上秀月街南侧12路公交车站点人行步道，将多名放学学生及路人撞伤。事故发生后，交警及中山区委区政府等相关部门第一时间赶赴现场，联动120急救中心开展施救。目前，伤者已全部送往医院进行救治。截 ​​​​..."]]
reference = [[["#大连15中车祸# 【孩子走了…大连十五中车祸重伤男孩去世】11日晚间，重伤男孩传出脑死亡的消息，12日一早，男孩再次出了心脏骤停，医务人员及时抢救一度复苏成功，但终因伤势过重，男孩经抢救无效于今晨7点33分离世。经勘查，事故现场路面无肇事车辆刹车痕迹，驾驶员崔某未采取有效措施，直接导 ​​​​..."]]]
# If you evaluate ROUGE by sentence list as above, set files=False
setting_file = rouge.setting(files=False, summary=summary, reference=reference)

# If you need only recall of ROUGE metrics, set recall_only=True
result = rouge.eval_rouge(setting_file, recall_only=False, ROUGE_path=ROUGE_path, data_path=data_path)
print(result)