#coding:utf-8
import jieba
import sys
reload(sys)  #重新加载sys
sys.setdefaultencoding('utf8')  ##调用setdefaultencoding函数


class seg:

    def __init__(self,Str,stopwords):
        self.str = Str
        self.stopwords = stopwords

    def Del_stopwords(self):

        segs = jieba.cut(self.str, cut_all=False)
        #final = ''
        seg_list = []
        for seg in segs:
            #print seg
            if seg not in self.stopwords:
                #final += seg
                seg_list.append(seg)
        return seg_list

#库的使用格式
if __name__ == "__main__":
    stopwords = [line.strip() for line in open('stopwords.txt','r')]
    Str = raw_input().replace(' ','')   #去掉空格
    content = seg(Str,stopwords)
    content.Del_stopwords()