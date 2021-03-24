import pandas as pd
import urllib.request
from stock import query
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def login():
    uname = request.form.get("username")
    pwd = request.form.get("pwd")
    if uname == "郝金星" and pwd == "123456":
        return render_template("stock.html")
    else:
        return render_template("login.html", msg="登陆失败")

@app.route("/query", methods = ["POST"])
def get_k_data():
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    codes_str = request.form.get("codes_str")
    if (not start_date) or (not end_date):
        return render_template("stock.html", msg="开始日期:{}或者结束:{}日期不能为空。".format(start_date, end_date))
    if start_date > end_date:
        return render_template("stock.html", msg="开始日期:{}晚于结束日期:{}".format(start_date, end_date))
    if not codes_str:
        return render_template("stock.html", msg="股票输入不能为空")
    codes = codes_str.strip().split(',')
    codes = [code.strip() for code in codes if code != '']
    if not all(_.isdigit() for _ in codes):
        return render_template("stock.html", msg="股票输入中包含非数字")
    if len(codes) == 0:
        return render_template("stock.html", msg="没有股票数据需要查询")
    df = pd.DataFrame()
    for code in codes:
        try:
            tmp_df = query(code, start_date, end_date)
            df = df.append(tmp_df)
        except Exception as e:
            print(e)
            return render_template("stock.html", msg="{}获取不到数据".format(code))
    return df.to_html()

if __name__ == '__main__':
    app.run(port = 54321, debug = True)
