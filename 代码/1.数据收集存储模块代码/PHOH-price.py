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
    # 苯酚数据爬取
    baseurl1 = "https://www.buychemi.cn/hangqing/trend//30-608-zs/p"
    baseurl2 = "?ps=10&pn=3&accurateProductName=%E8%8B%AF%E9%85%9A&productId=608&state=0"

    # 1.爬取网页
    datalist = getData(baseurl1,baseurl2)
    # askURL(baseurl)

    # # 3.保存数据
    dbpath = "PHOH.db"
    saveData2DB(datalist,dbpath)  # 保存到数据库

    # savepath = ".\\PHOH.xls"  # .\\:表示保存在当前路径下；..\\：表示上一级路径
    # saveData(datalist, savepath)  # 保存到excel


# 正则表达式
findplace = re.compile(r'<div class="area"><p class="overflow-txt">(.*?)</p>') # 所在区域
findprice1 = re.compile(r'<div class="price-now"><p class="overflow-txt">.*?￥(\d*),(\d*).(\d*).*/吨</p></div>', re.S)  # 当日均价(注意：换行的地方除了需要re.S,还需要.*)
findprice2 = re.compile(r'<div class="last-price"><p class="overflow-txt">.*?￥(\d*),(\d*).(\d*).*/吨</p></div>', re.S) # 上次均价
findincrease = re.compile(r'<div class="price-type"><p class="overflow-txt">(.*?)</p>') # 涨跌
findextent1 = re.compile(r'<div class="price up">\n<p class="overflow-txt">(.*?\r\n%)</p></div>', re.S) # 涨跌幅度
findextent2 = re.compile(r'<div class="price flat">\n<p class="overflow-txt">(.*?\r\n%)</p></div>', re.S) # 涨跌幅度
findextent3 = re.compile(r'<div class="price down">\n<p class="overflow-txt">(.*?\r\n%)</p></div>', re.S) # 涨跌幅度
finddate = re.compile(r'<div class="time"><p class="overflow-txt">(.*?)</p>') # 报价日期


# 爬取网页
def getData(baseurl1,baseurl2):
    datalist = []
    for i in range(1,139):  # 注意页面数1-138，需要分批爬取，不然数据量太多，sqlite可能锁死
        url = baseurl1 + str(i) + baseurl2
        html = askURL(url)

        # 2.解析数据
        soup = BeautifulSoup(html, "html.parser")  # 解析html，用解析器parser
        for item in soup.find_all('li', class_="product-market-list-tr"):  # 查找符合要求的字符串，形成列表  class_:表示属性值
            data = []
            item = str(item)
            # print(item)  # 测试：item

            place = re.findall(findplace, item)[0]  # re库用来通过正则表达式查找指定字符串
            data.append(place)
            # print(place)

            price1 = re.findall(findprice1, item)[0]
            price = price1[0] + price1[1] + '.' + price1[2]  # 不需要将字符串转换为浮点数，因为输入数据库时会处理
            data.append(price)
            # print(price)

            price2 = re.findall(findprice2, item)[0]
            price = price2[0] + price2[1] + '.' + price2[2]  # 不需要将字符串转换为浮点数，因为输入数据库时会处理
            data.append(price)
            # print(price)

            increase = re.findall(findincrease, item)[0]     # 不需要将字符串转换为浮点数，因为输入数据库时会处理
            increase = increase.replace(',','')  # 可能存在12,000这种数字，需要去除逗号
            data.append(increase)
            # print(increase)

            if re.findall(findextent1, item):
                extent = re.findall(findextent1, item)[0]
            elif re.findall(findextent2, item):
                extent = re.findall(findextent2, item)[0]
            else:
                extent = re.findall(findextent3, item)[0]
            data.append(extent.replace('\r\n',''))
            # print(extent)

            date = re.findall(finddate, item)[0]
            data.append(date)
            # print(date)

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
    # init_db(dbpath)  # 如果table已经存在，则不需要创建
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index==1 or index==2 or index==3:
                continue
            data[index] = '"'+data[index]+'"'  # numeric类型不需要添加双引号，text类型需要添加双引号
        sql = '''
            insert into PHOH(
            place, pricenow, lastprice, increase, extent, date
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
        create table PHOH
            (id integer primary key autoincrement,
            place text,
            pricenow numeric,
            lastprice numeric,
            increase numeric,
            extent text,
            date text
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