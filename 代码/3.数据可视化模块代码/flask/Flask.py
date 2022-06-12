# -*- coding: UTF-8 -*-
"""
作者：Max
日期：2021年08月12日
"""

from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/product')
def PHOH_price():
    date1 = []
    price1 = []
    price2 = []
    price3 = []
    price4 = []
    datalist  = []
    con = sqlite3.connect("./PHOH.db")
    cur = con.cursor()

    sql = '''
          select pricenow,date from PHOH
          where place='华南地区'
          '''
    data = cur.execute(sql)
    for item in data:
        price1.append(item[0])
        date1.append(item[1])
    price1 = list(reversed(price1))  # 列表反转排序
    date1 = list(reversed(date1))   # 列表反转排序

    sql = '''
          select pricenow from PHOH
          where place='华北地区'
          '''
    data = cur.execute(sql)
    for item in data:
        price2.append(item[0])
    price2 = list(reversed(price2))  # 列表反转排序

    sql = '''
          select pricenow from PHOH
          where place='华东地区'
          '''
    data = cur.execute(sql)
    for item in data:
        price3.append(item[0])
    price3 = list(reversed(price3))  # 列表反转排序

    sql = '''
          select pricenow from PHOH
          where place='华中地区'
          '''
    data = cur.execute(sql)
    for item in data:
        price4.append(item[0])
    price4 = list(reversed(price4))  # 列表反转排序

    sql = '''
          select * from PHOH
          where place='华南地区'
          '''
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)

    cur.close()
    con.close()

    datalist2 = []
    con = sqlite3.connect("./PHOH.db")
    cur = con.cursor()
    sql = '''
        select * from PHOH_sale
        '''
    data = cur.execute(sql)
    for item in data:
        datalist2.append(item)
    cur.close()
    con.close()

    return render_template("product.html",date1=date1, price1=price1, price2=price2, price3=price3, price4=price4, datalist=datalist, datalist2=datalist2)

if __name__ == '__main__':
    app.run(debug=True)