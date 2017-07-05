#coding:utf-8
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from fenci import Chinese_Segment
from ExcelHandle import ExcelHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TF_IDF:
    def __init__(self,file_list,stopwords_file):
        self.files = file_list
        self.stopwords = stopwords_file

    # 处理txt文档，中文分词、删除停用词、将结果放入字符串中并用空格隔开
    def get_content(self,filename,stopwords_file):
        file = open(filename,"r").read()
        file = file.decode('gbk','ignore').encode('utf-8')
        file = file.replace(" ","")
        stopwords = [line.strip() for line in open(stopwords_file,'r')]
        segs = Chinese_Segment.seg(file,stopwords)
        segs_del = segs.Del_stopwords()
        content = ""
        for i in segs_del:
             content = content + " " + i.encode('utf-8')
        return content

    #返回根据文件列表整合的符合CountVectorizer的列表形式
    def content_sum(self):
        str = []
        for i in range(len(self.files)):
            complete_content = self.get_content(self.files[i], self.stopwords)
            str.append(complete_content)
        return str

    #计算TF—IDF,str为字符串的列表
    def tfidf(self):
        str = self.content_sum()
        vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
        transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值  
        tfidf = transformer.fit_transform(vectorizer.fit_transform(str))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        print vectorizer.fit_transform(str)
        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语  
        weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        list = []
        for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重,这里weight是列表嵌套列表，一类文本为一个列表 
            dict = {}
            #print u"-------这里输出第", i+1, u"类文本的词语tf-idf权重------"
            for j in range(len(word)):
                if weight[i][j] > 0:
                    dict[word[j].decode('utf-8')] = weight[i][j]
            #按照TF_IDF逆序排序后输出
            dict = sorted(dict.items(),key = lambda item:item[1],reverse=True)
            # for i in dict:
            #     print i[0].encode('utf-8'),i[1]
            list.append(dict)
        return list


#库的使用格式
if __name__=='__main__':
    filename_list = [u"医学.txt",u"核弹.txt",u"计算机.txt",u"物理.txt",u"英语.txt"]
    stopwords_file = "stopwords.txt"
    #列表保存分词好、去停用词、加空格的数据，作为下一步TF-IDF的传入数据

    #保存所有文档的TF_IDF的字典的列表，因为进行排序后为元组，所以这是一个列表与列表的嵌套
    TF_IDF_list = TF_IDF(filename_list,stopwords_file).tfidf()
    filename_xls = "hello"
    Excel_handler = ExcelHandler.ExcelHandle(TF_IDF_list,filename_xls)
    Excel_handler.Excel_Write()
