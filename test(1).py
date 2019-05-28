import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np



def dictionary():
    dic = {}
    # requests.Session()
    # url = 'http://www.dianping.com/shop/14754041'
    # headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    # }
    # html = requests.get(url,headers = headers).text
    # obj = BeautifulSoup(html,'lxml')
    # print(obj)
    # item = obj.find(attrs={'class':'expand-info tel'})
    # css = obj.find_all(attrs={'rel':'stylesheet','type':'text/css'})[1]
    # css_url = 'http:' + css['href']
    # css_headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    #     'Referer':url
    # }
    # html1 = requests.get(css_url,headers=css_headers).text
    # doc = BeautifulSoup(html1,'lxml')
    # f = open('dic.txt','w')
    # f.write(html1)

    true_urls = []
    with open('dic.txt','r') as fp:
        line = fp.readline()
        if line :
            doc = ''.join(line)
        line = fp.readline()
    print(doc)
    url_pattern = '//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/(.*?).svg'
    urls = re.findall(url_pattern,doc)
    for_pattern = 'class\^="(.*?)"'
    tes = re.findall(for_pattern,doc)
    for url in urls:
        true_urls.append('https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/{}.svg'.format(url))

    for i in range(0,len(tes)):
        true_url = true_urls[i]
        te = tes[i]
        dic_new = make_single_dic(te,true_url,doc)
        dic = dict( dic_new, **dic )
    for item in dic.items():
        keys.append(item[0])
        values.append(item[1])

    css_values = pd.DataFrame(np.transpose([keys,values]),columns=['key','value'])
    css_values.to_excel('对照表.xlsx')

def make_single_dic(te,true_url,html1):
    dic = {}
    pattern = '(' + te + '\w+){background:(.+)px (.+)px;'
    list = re.findall(pattern, '\n'.join(html1.split('}')))
    url = true_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    html2 = requests.get(url,headers = headers) .text
    doc2 = BeautifulSoup(html2,'lxml')
    print('*'*40)
    texts = doc2.find_all('text')
    print(texts)
    if len(texts) != 1:
        y = []
        for text in texts:
            y.append(int(text['y']))
        print(y)
        for i in range(0,len(list)):
            y_index = -float(list[i][2])
            for j in range(0,len(y)):
                if y_index < y[j]:
                    y_index = j
                    break

            x_index = round((-float(list[i][1]) + 6)/14)
            if y_index <= y[-1]:
                value = texts[int(y_index)].text
                dic[list[i][0]] = value[x_index - 1]
        return dic
    else:
        paths  = doc2.find_all('path')
        texts = doc2.find_all('textpath')
        print(texts)
        y = []
        for path in paths:
            y.append(int(path['d'][3:-5]))
        for i in range(0,len(list)):
            y_index = -float(list[i][2])
            for j in range(0,len(y)):
                if y_index < y[j]:
                    y_index = j
                    break
        x_index = round((-float(list[i][1]) + 6) / 14)
        if y_index <= y[-1]:
            value = texts[int(y_index)].text
            dic[list[i][0]] = value[x_index - 1]
        return dic






        # if y_index< y[3]:
        #     y_index_new = 3
        #     if y_index< y[2]:
        #         y_index_new = 2
        #         if y_index< y[1]:
        #             y_index_new = 1
        #             if y_index < y[0]:
        #                 y_index_new = 0
        # x_index = -float(list[i][1])
        # x_index_new = round((x_index + 6)/14)
        # value = texts[y_index_new].text
        # dic[[i][0]] = value[x_index_new-1]
    #
    #
    #
    # words_list = re.findall('(pat\w+){background:(.+)px (.+)px;', '\n'.join(html1.split('}')))
    # words_dic = {}
    # words_url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/56183d6b772b01da10b2468285c3724b.svg'
    # html3 = requests.get(words_url,headers=headers)
    # doc3 = BeautifulSoup(html3.text,'lxml')
    # paths  = doc3.find_all('path')
    # texts = doc3.find_all('textpath')
    # print(texts)
    # y = []
    # for path in paths:
    #     y.append(int(path['d'][3:-5]))
    # for i in range(0,len(words_list)-1):
    #     y_index = -float(words_list[i][2])
    #     if y_index < y[7]:
    #         y_index_new = 7
    #         if y_index < y[6]:
    #             y_index_new = 6
    #             if y_index < y[5]:
    #                 y_index_new = 5
    #                 if y_index < y[4]:
    #                     y_index_new = 4
    #                     if y_index < y[3]:
    #                         y_index_new = 3
    #                         if y_index < y[2]:
    #                             y_index_new = 2
    #                             if y_index < y[1]:
    #                                 y_index_new = 1
    #                                 if y_index < y[0]:
    #                                     y_index_new = 0
    #     x_index = round(-float(words_list[i][1])/14)
    #     content = texts[y_index_new].text
    #     dic[words_list[i][0]] = content[x_index]
    #
    # print(dic)
    # keys = []
    # values = []
    # for item in dic.items():
    #     keys.append(item[0])
    #     values.append(item[1])
    #
    # css_values = pd.DataFrame(np.transpose([keys,values]),columns=['key','value'])
    # css_values.to_excel('对照表.xlsx')
def telephone_number(telephone):
    text = telephone
    excel = pd.read_excel('对照表.xlsx',index_col = 0)
    dic = {}

    for i in range(0,len(excel)):
        dic[excel['key'][i]] = excel['value'][i]

    strinfo = re.compile('<span (.*?)>')
    text = strinfo.sub('',text)
    strinfo = re.compile('</span>')
    text = strinfo.sub('',text)
    strinfo = re.compile('<d class=')
    text = strinfo.sub('',text)
    strinfo = re.compile('></d>')
    text = strinfo.sub('',text)
    strinfo = re.compile('"(.*?)"')
    ts = strinfo.findall(text)
    for t in ts:
        strinfo = re.compile('"' + t + '"')
        text = strinfo.sub(dic[t],text)
    return text


def location(location):
    text = '<e class="pat4pz"></e><e class="patmdp"></e><e class="patnmg"></e><e class="patkc8"></e>1<d class="pzcinw"></d><e class="pat9sb"></e><e class="patzk2"></e>侧<e class="patw1k"></e><e class="patlo5"></e>(<e class="pat4pz"></e><e class="patmdp"></e><e class="patnmg"></e><e class="patr0a"></e>对面)'
    excel = pd.read_excel('对照表.xlsx', index_col=0)
    dic = {}

    for i in range(0, len(excel)):
        dic[excel['key'][i]] = excel['value'][i]

    strinfo = re.compile('<e class=')
    text = strinfo.sub('', text)
    strinfo = re.compile('></e>')
    text = strinfo.sub('', text)
    strinfo = re.compile('<d class=')
    text = strinfo.sub('', text)
    strinfo = re.compile('></d>')
    text = strinfo.sub('', text)
    strinfo = re.compile('"(.*?)"')
    ts = strinfo.findall(text)
    for t in ts:
        strinfo = re.compile('"' + t + '"')
        text = strinfo.sub(dic[t], text)
    return text


if __name__ == '__main__':
    dictionary()