# TF-IDF 建模
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.utils import Bunch
bunch_path = './data/raw_Bunch_train'
with open(bunch_path, 'rb') as file_obj:
    bunch = pickle.load(file_obj)
begintime = datetime.datetime.now()
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.15, min_df=0.001,max_features=2000)
tfidf_space = Bunch(filenames = bunch.filenames,tfidf_weight_matrics = [],vocabulary = {})
tfidf_space.tfidf_weight_matrics = vectorizer.fit_transform(bunch.contents)
#print (vectorizer.get_feature_names())
print(tfidf_space.tfidf_weight_matrics)
endtime = datetime.datetime.now()
print("执行完毕，用时为：" + str((endtime - begintime).seconds)+ "秒")
tfidf_space.vocabulary = vectorizer.vocabulary_
with open('./data/Bunch_train', 'wb') as file_obj1:
    pickle.dump(tfidf_space, file_obj1)
