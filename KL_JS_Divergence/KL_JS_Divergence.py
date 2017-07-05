#coding:utf-8
import scipy
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from fenci import Chinese_Segment

class KL:

    #传入两个文件，计算KL,两个文件都为字符串并且关键词用空格隔开
    def __init__(self,file_source,file_summary,stopfile):
        self.file_source = file_source
        self.file_summary = file_summary
        self.stopfile = stopfile
        #self.file_summary = file_summary

    def get_content(self,file_handled):
        file = open(file_handled, "r").read()
        file = file.decode('gbk', 'ignore').encode('utf-8')
        file = file.replace(" ", "")
        stopwords = [line.strip() for line in open(self.stopfile, 'r')]
        segs = Chinese_Segment.seg(file, stopwords)
        segs_del = segs.Del_stopwords()
        content = ""
        for i in segs_del:
            content = content + " " + i.encode('utf-8')
        return content

    #text和summary组成一个str列表[0]取出text的词频，[1]取出summary的词频
    def cal_p_q(self):
        str_source = self.get_content(self.file_source)
        str_summary = self.get_content(self.file_summary)
        str = []
        str.append(str_source)
        str.append(str_summary)
        vectorizer = CountVectorizer()
        #print str
        matrix_tf = vectorizer.fit_transform(str)
        words = vectorizer.get_feature_names()
        # for i in words:
        #     print i
        #某个词出现的概率
        matrix_be_added = matrix_tf.copy()
        array_be_added = matrix_be_added.toarray()
        array_be_added = array_be_added.astype("float32")  #此处不能直接修改.dtype，不然矩阵长度会改变。用astype()函数
        for i in range(len(array_be_added)):
            for j in range(len(array_be_added[i])):
                array_be_added[i][j] = 0.0005
        matrix_be_added = numpy.mat(array_be_added)
        # print matrix_be_added
        # print matrix_tf
        matrix_tf = matrix_be_added + matrix_tf
        # print matrix_tf
        ret_list = []
        ret_list.append(matrix_tf[0] / (str_source.count(" ") + 1 + 0.0005 * 1.5 * len(set(words))))
        ret_list.append(matrix_tf[1] / (str_summary.count(" ") + 1 + 0.0005 * 1.5 * len(set(words))))
        #返回text词频分布和summary词频分布的列表
        return ret_list

    #text和summary关键词概率都是存放在words（所有文本的关键词列表）中的
    def cal_KL(self):
        p = self.cal_p_q()[0].tolist()[0]
        q = self.cal_p_q()[1].tolist()[0]
        print (scipy.stats.entropy(p, q) + scipy.stats.entropy(q, p)) / 2

    def cal_JS(self):
        p = self.cal_p_q()[0].tolist()[0]
        q = self.cal_p_q()[1].tolist()[0]
        m = []
        for i,j in zip(p,q):
            m.append ((i+j)/2)
        print (scipy.stats.entropy(p,m) + scipy.stats.entropy(q,m)) / 2

#库的使用格式
if  __name__ == "__main__":
    kl = KL(u"text.txt", u"summary.txt", "stopwords.txt")
    kl.cal_KL()
    kl.cal_JS()




