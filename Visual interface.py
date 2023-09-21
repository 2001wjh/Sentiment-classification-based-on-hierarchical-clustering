import keras
import re
import numpy as np
import wx


class Myframe(wx.Frame):
  def __init__(self, superior):
    wx.Frame.__init__(self, parent=superior, title='情感极性可视化界面', size=(400, 200))

    panel = wx.Panel(self, -1)
    label1 = wx.StaticText(panel, -1, '请输入您的评论:')
    label2 = wx.StaticText(panel, -1, '评论的情感极性:')
    self.comment = wx.TextCtrl(panel, -1, "", style=wx.TE_LEFT)
    self.emotion = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
    self.buttonCheck = wx.Button(parent=panel, label='判断')
    self.Bind(wx.EVT_BUTTON, self.predict_one, self.buttonCheck)

    sizer = wx.FlexGridSizer(3, 2, 10, 10)
    sizer.Add(label1)
    sizer.Add(self.comment)
    sizer.Add(label2)
    sizer.Add(self.emotion)
    sizer.Add(self.buttonCheck)
    panel.SetSizer(sizer)

  def predict_one(self, x):
    sentence = self.comment.GetValue()
    sentence = re.sub("[^\u4e00-\u9fa5]", "", str(sentence))  # 只保留中文
    # print(sentence)
    sentence = [word2Index[word] if word2Index.get(word) else 0 for word in sentence]
    sentence = sentence + [0] * (maxlen - len(sentence)) if len(sentence) < maxlen else sentence[0:300]
    # print(sentence)
    sentence = np.reshape(np.array(sentence), (-1, len(sentence)))
    pred_prob = new_model.predict(sentence)
    print(pred_prob[0][0])
    if pred_prob[0][0] > 0.0042:
      self.emotion.SetLabel('正面评论')
    elif pred_prob[0][0] < 0.0031:
      self.emotion.SetLabel('负面评论')
    else:
      self.emotion.SetLabel('待定')


def getWordIndex(vocabPath):
  """
  获取word2Index,index2Word
  :param vocabPath:词汇文件，使用的是data里的vocab.txt文件
  :return:
  """
  word2Index = {}
  with open(vocabPath, encoding="utf-8") as f:
    for line in f.readlines():
      word2Index[line.strip()] = len(word2Index)
  index2Word = dict(zip(word2Index.values(), word2Index.keys()))
  return word2Index, index2Word



if __name__=='__main__':
  maxlen = 100  # 最大样本长度，不足进行Padding，超过进行截取

  new_model = keras.models.load_model('./data/Emotional_classification_model.h5')  # 加载模型
  new_model.summary()

  vocabPath = "./data/vocab.txt"
  word2Index, index2Word = getWordIndex(vocabPath)

  app = wx.App()                # 创建应用程序对象
  frame = Myframe(None)         # 创建框架类对象
  frame.Show(True)              # 显示框架
  app.MainLoop()                # 事件循环等待与处理



