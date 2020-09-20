import stanza

# stanza.download('zh')

nlp = stanza.Pipeline(lang='zh', processors='tokenize,ner')

string = """2013.10-至今       广州银行                 营业部柜员"""
string1 = "2011.7-2013.9      广发银行                 营业部开户业务 "
string2 = "2010.10-2011.6     东亚银行（中国）有限公    营业部柜员 "
string3 = "2015.06  为南阳市桐柏县阳光半岛房地产项目制作“桐柏醉美啤酒节”主题微信宣传页面和抽奖活动程序；"
string4 = "2014.6-2015.5         中南财经政法大学财政税务学院学生会             学术部副部长"
string5 = "2014.9-2016.1         中南财经政法大学财政税务学院学生助教中心       助教兼负责人 "
string6 = "2016.12-2017.3        瑞华会计师事务所（特殊普通合伙）深圳分所       审计助理 "

doc = nlp(string6)
print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in doc.ents], sep='\n')
