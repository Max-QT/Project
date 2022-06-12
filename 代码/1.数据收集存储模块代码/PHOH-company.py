"""
作者：Max
日期：2021年08月12日
1.爬取网页,2.解析数据，3.保存在数据库中
"""

import urllib.request, urllib.error  # 制订URL，获取网页数据
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import sqlite3  # 进行SQLite数据库操作
import xlwt  # 进行excel操作
import time

def main():
    # 苯酚主要商家数据的爬取
    baseurl = "https://mall.buychemi.cn/product/3305"

    # 1.爬取网页
    datalist = getData(baseurl)
    # askURL(baseurl)

    # # 3.保存数据
    dbpath = "PHOH.db"
    saveData2DB(datalist,dbpath)  # 保存到数据库

    # savepath = ".\\PHOH.xls"  # .\\:表示保存在当前路径下；..\\：表示上一级路径
    # saveData(datalist, savepath)  # 保存到excel


# 正则表达式
findcompany = re.compile(r'<li.*?name="(.*?)".*?>',re.S)  # 公司
findplace = re.compile(r'<span class="shop-conteact-label">所在地区</span>\n<span class="shop-contact-val">\r\n(.*?)\r\n</span>',re.S)  # 地址
findpacking = re.compile(r'<td>包装规格</td>\n<td>(.*?)</td>',re.S)  # 包装规格
findpurity = re.compile(r'<li.*?purity="(.*?)".*?>',re.S)# 纯度
findbrand = re.compile(r'<td>品 牌</td>\n<td>(.*?)</td>',re.S)  # 品牌
findurl1 = re.compile(r'href="(.*?)" title="苯酚">苯酚</a>')  # 公司苯酚网址
findrank = re.compile(r'<td>等 级</td>\n<td>(.*?)</td>',re.S)  # 等级
findurl2 = re.compile(r'<a href="(.*?)" target="_blank">')  # 公司网址
findabstract = re.compile(r'<div class="shop-company-discription-p">(.*?)</div>',re.S) # 公司介绍


# 爬取网页
def getData(baseurl):
    datalist = []
    url = baseurl
    html = askURL(url)

    # 2.解析数据
    soup = BeautifulSoup(html, "html.parser")  # 解析html，用解析器parser
    for item in soup.find_all('li',class_=re.compile(r'clearfloat getData store')):  # 查找符合要求的字符串，形成列表  class_:下划线表示属性值
        data = []
        item = str(item)
        # print(item)  # 测试：item

        company = re.findall(findcompany,item)[0]
        data.append(company)
        # print(company)  # 公司

        brand = re.findall(findbrand, item)[0]
        if brand=='--':
            brand=''
        data.append(brand)
        # print(brand)  # 品牌

        purity = re.findall(findpurity, item)[0]
        data.append(purity)
        # print(purity)  # 纯度

        url1 = re.findall(findurl1, item)[0]
        data.append(url1)
        # print(url1)  # 公司苯酚网址

        html_item = askURL(url1)
        soup_item = BeautifulSoup(html_item, "html.parser")
        temp = str(soup_item.find_all('div',class_='goods-info')[0])
        rank = re.findall(findrank,temp)[0]
        data.append(rank)
        # print(rank)  # 等级

        packing = re.findall(findpacking, item)[0]
        data.append(packing)
        # print(packing)  # 包装规格

        url2 = re.findall(findurl2, item)[0]
        data.append(url2)
        # print(url2)  # 公司网址

        url3 = url2.rsplit('list')[0]  # 公司首地址
        url4 = url3 + 'contact'  # 公司地址信息url
        html_item = askURL(url4)
        soup_item = BeautifulSoup(html_item, "html.parser")
        temp = str(soup_item.find_all('div',class_='shop-contact-content')[0])
        place = re.findall(findplace,temp)[0]
        data.append(place)
        # print(place)  # 地址

        html_item = askURL(url3)
        soup_item = BeautifulSoup(html_item, "html.parser")
        temp2 = soup_item.find_all('div', class_='shop-company-discription-content clearfloat')
        if temp2:
            temp = str(temp2[0])
            abstract = re.findall(findabstract, temp)[0]
        else:
            abstract = ''
        data.append(abstract)
        # print(abstract)  # 公司介绍

        datalist.append(data)  # 把处理好的信息放入datalist
        # print(data)

    # print(datalist)  # 测试：输出
    return datalist


# 网页信息返回
def askURL(url):
    cookie = '''douban-fav-remind=1; _vwo_uuid_v2=D53A2251CC03F5E3402C7910D3B3261BB|643d82cfadc00490eec6ca452cdd9ba9; gr_user_id=f7e13b96-0f16-4f22-991c-abe756989e10; __yadk_uid=w8zXdq5JFpGRdnXBlQY9cc0uX9Orh6fM; viewed="1935929_19502270_1799271_1419667"; bid=90oVFCvm3-w; ll="108304"; _vwo_uuid_v2=D53A2251CC03F5E3402C7910D3B3261BB|643d82cfadc00490eec6ca452cdd9ba9; dbcl2="243976266:ZtuWYGEnMFY"; ck=AAev; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1628567615%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=c91c8aa5fd7807e0.1628567615.1.1628567615.1628567615.; _pk_ses.100001.4cf6=*; __utma=30149280.1644126318.1628567615.1628567615.1628567615.1; __utmb=30149280.0.10.1628567615; __utmc=30149280; __utmz=30149280.1628567615.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.828895523.1628567615.1628567615.1628567615.1; __utmb=223695111.0.10.1628567615; __utmc=223695111; __utmz=223695111.1628567615.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __gads=ID=88c888e7e3a02e87-22b9c8f2bcca002b:T=1628567615:RT=1628567615:S=ALNI_MbSCRo0DQ4PhBw1JbPnOoj38JtMCA; push_noty_num=0; push_doumail_num=0'''
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Cookie": cookie
    }
    request = urllib.request.Request(url, headers=head)  # 给请求封装头部
    time.sleep(1)  # 防止爬虫太快被封
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)  # 测试打印
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 数据库保存
def saveData2DB(datalist, dbpath):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'  # numeric类型不需要添加双引号，text类型需要添加双引号
        sql = '''
            insert into PHOH_sale(
            company, brand, purity, URL_PHOH, rank, packing, URL_company, place, abstract
            )
            values(%s);
        '''%",".join(data)
        # print(sql)  # 测试
        # %",".join(data):表示用逗号连接data里各元素（data是一个列表）
        # 再填充到字符串%s位置

        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


# 数据库初始化
def init_db(dbpath):
    sql = '''
        create table PHOH_sale
            (id integer primary key autoincrement,
            company text,
            brand text,
            purity text,
            URL_PHOH text,
            rank text,
            packing text,
            URL_company text,
            place text,
            abstract text
            );
    '''
    # text:文本格式,numeric:包括小数;最后的分号不能少;autoincrement:自动填充
    # print(sql)

    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# 用excel保存
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象,style_compression=0:样式可压缩
    sheet = book.add_sheet('IPA', cell_overwrite_ok=True)  # 创建工作表，cell_overwrite_ok=True：内容可覆盖
    col = ('品牌', '货号', '纯度规格', '包装', '库存', '价格')
    for i in range(0,6):
        sheet.write(0,i,col[i])  # 列名
    for i in range(0,45):
        # print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,6):
            sheet.write(i+1,j,data[j])

    book.save(savepath)  # 保存数据表


if __name__ == '__main__':
# 调用函数
    time_start=time.time()
    main()
    print('爬取完毕！')
    time_end=time.time()
    print('time cost',time_end-time_start,'s')