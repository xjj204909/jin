# 生成测试集字典
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.utils import Bunch

bunch_path = './data/raw_Bunch_test'
train_tfid_path = './data/Bunch_train'
with open(bunch_path, 'rb') as file_obj:
    bunch = pickle.load(file_obj)
with open(train_tfid_path, 'rb') as file_obj1:
    trainbunch = pickle.load(file_obj1)
tfidf_space = Bunch( filenames = bunch.filenames,tfidf_weight_matrics = [],vocabulary = trainbunch.vocabulary)
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.13, min_df=0.001, vocabulary=trainbunch.vocabulary)
tfidf_space.tfidf_weight_matrics = vectorizer.fit_transform(bunch.contents)
#print (vectorizer.get_feature_names())
print(tfidf_space.tfidf_weight_matrics)
with open('./data/Bunch_test', 'wb') as file_obj2:
    pickle.dump(tfidf_space, file_obj2)
