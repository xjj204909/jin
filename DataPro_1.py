#生成raw_Bunch_train和raw_Bunch_test
import sys
import jieba
import jieba.posseg as pseg
import os
from sklearn.utils import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
word_bag_filepath_train = './data/raw_Bunch_train'
word_bag_filepath_test = './data/raw_Bunch_test'
Bunch_train = Bunch(label=[], filenames=[], contents=[])
Bunch_test = Bunch(label=[], filenames=[], contents=[])
types = ['地产','反腐','国际','金融','军事','科技','汽车','社会','体育','文娱']
def is_all_chinese(strs):
    for _char in strs:
        if (not '\u4e00' <= _char <= '\u9fa5'):
            return False
        return True
for t in types:
    dirpath = './data/Data_Set/' + t
    print(dirpath)
    Train = True
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            Path = os.path.join(root, f)
            print(Path)
            file_obj = open(Path, 'r', encoding='UTF-8')
            doc = file_obj.read()
            file_obj.close()
            print(Train)
            if (Train):
                Bunch_train.filenames.append(str(f))
                Bunch_train.label.append(str(t))
                Bunch_train.contents.append(str(doc))
            else:
                Bunch_test.filenames.append(str(f))
                Bunch_test.label.append(str(t))
                Bunch_test.contents.append(str(doc))
            Train = not Train
with open(word_bag_filepath_train, 'wb') as file_obj1:
    pickle.dump(Bunch_train, file_obj1)
with open(word_bag_filepath_test, 'wb') as file_obj2:
    pickle.dump(Bunch_test, file_obj2)