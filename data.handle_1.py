import pandas as pd
import jieba

# 查看数据的基本信息总结
# comment_data.info()

# def load_stop_words(file='./data/stopwords.txt'):  # 停用词检测
#     with open(file, 'r', encoding="utf-8") as f:
#         return f.read().split("\n")

def stopwordslist():  # 创建停用词表
    stopword_path = './data/stopwords.txt'
    stopwords = [
        line.strip()
        for line in open(stopword_path, encoding="UTF-8").readlines()
    ]
    return stopwords

def cut_words(commentSeries):
    stop_words = stopwordslist()
    result = []
    for words in commentSeries:  # 一行csv
        c_words = jieba.lcut(words)
        result.append([word for word in c_words if word not in stop_words and len(word)>1])   # 看看是不是在停用词里
    return result


def save_txt():
    com = pd.read_csv("./data/去除停用词并分词_1.csv", encoding='gb18030')
    for line in com.values:
        with open('./data/去除停用词并分词_1.txt', 'a+', encoding='gb18030') as f:
            f.write((str(line[0])))



if __name__ == '__main__':

    file_path = './data/comment_1.csv'
    comment_data = pd.read_csv(file_path, encoding='gb18030')

    # 去重，默认保留第一项
    data = comment_data.drop_duplicates()
    # 设置列名
    data.columns = ['评论']
    # 存储数据
    data.to_csv('./data/评论去重_1.csv', encoding='gb18030', index=False)

    # # 去除换行符
    # path = '评论去重_1.csv'
    # with open(path, encoding='gb18030', newline='') as fin:
    #     with open('评论去换行_1.csv', 'w', encoding='gb18030', newline='') as fon:
    #         r = csv.reader(fin)  # 读入文件
    #         w = csv.writer(fon)  # 写入文件
    #         for row in r:
    #             row = [col.replace('\\n', '').replace('\\r', '') for col in row]  # 将"\n"替换为无
    #             w.writerow(row)  # 写入新文件

    # 去除停用词并jieba分词
    data = pd.read_csv("./data/评论去重_1.csv", encoding='gb18030').astype(str)
    results = cut_words(data['评论'])
    rst = []
    for text in results:
        str_1 = ""
        for word in text:
            str_1 += word + " "
        rst.append(str_1)
    df = pd.DataFrame(columns=['评论'], data=rst)
    df.to_csv("./data/去除停用词并分词_1.csv", encoding='gb18030', index=False)

    # 去除空行
    find_line = pd.read_csv("./data/去除停用词并分词_1.csv", encoding='gb18030')
    find_line.dropna(axis=0, how='any', inplace=True)
    find_line.to_csv("./data/去除停用词并分词_1.csv", encoding='gb18030', index=False)

    # 将分词结果保存到txt文件中
    save_txt()

    print('数据处理并成功保存！')
