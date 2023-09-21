# 绘制普通词云图

import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = open("./data/去除停用词并分词（合并）.csv", encoding="gb18030").read()  # 标明文本路径，打开

# 生成对象
wc = WordCloud(font_path='C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc', width=500, height=400, mode="RGBA",
               background_color=None).generate(text)
# 显示词云图
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()

# 保存文件
wc.to_file("./result pictures/wordcloud.png")


# 绘制图形词云图

from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


mask = np.array(Image.open("./data/Alice.png"))

txt = open('./data/去除停用词并分词（合并）.csv', encoding='gb18030').read()
wordcloud = WordCloud(background_color="white",
                      font_path='C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc',
                      width=800,
                      height=600,
                      max_words=200,
                      max_font_size=80,
                      mask=mask,
                      contour_width=3,
                      contour_color='steelblue'
                      ).generate(txt)
wordcloud.to_file('./result pictures/wordcloud_Alice.png')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
