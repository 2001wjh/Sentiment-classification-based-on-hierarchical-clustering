from jieba import analyse

comment_list = []
textrank = analyse.textrank
text = open("./data/评论去重（合并）.csv", encoding="gb18030", newline='')

for comment in text:
    keywords = textrank(comment)
    # print(type(keywords))
    if len(keywords) == 0:
        continue
    else:
        comment_list.append(keywords)

with open('./data/keywords.txt', 'a+', encoding='gb18030') as f:
    f.write(str(comment_list))
