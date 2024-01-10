#切词
import jieba
import jieba.posseg as pseg
import os
from sklearn.utils import Bunch
import pickle
types = ['地产','反腐','国际','金融','军事','科技','汽车','社会','体育','文娱']
R = {'地产':(0,2000),'反腐':(0,2000),'国际':(0,2000),'金融':(0,2000),'军事':(0,2000),'科技':(0,2000),'汽车':(0,2000),'社会':(0,2000),'体育':(0,2000),'文娱':(0,2000)}
def is_all_chinese(strs):
    for _char in strs:
        if (not '\u4e00' <= _char <= '\u9fa5'):
            return False
        return True
for t in types:
    dirpath = './data/news/' + t
    print(t, ' ', end='')
    cnt = 0
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            Path = os.path.join(root, f)
            file_obj = open(Path, 'rb')
            doc = file_obj.read()
            file_obj.close()
            l = len(doc)
            if l >= R[t][0] and l <= R[t][1]:
                cnt += 1
                words = pseg.cut(doc)
                word_str = ''
                first = True
                for word in words:
                    now_word = str(word.word)
                    if (('n' or 1) in word.flag and word.flag != 'nr' and is_all_chinese(now_word)):
                        if (first):
                            first = False
                        else:
                            word_str += ' '
                        word_str += word.word
                Path = os.path.join('./data/Data_Set/' + t, f)
                out = open(Path, 'w', encoding='UTF-8')
                out.write(word_str)
                out.close()
                print(cnt)
