import requests
import pandas as pd
import urllib.request
from io import StringIO
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

def transfer_date_string_to_int(cdate):
    cdates = cdate.split('-')
    return int(cdates[0]) * 10000 + int(cdates[1]) * 100 + int(cdates[2])

@app.route("/query", methods = ["POST"])
def get_k_data():
    #http://quotes.money.163.com/service/chddata.html?code=0601398&start=20000720&end=20150508
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    codes_str = request.form.get("codes_str")
    if start_date > end_date:
        return render_template("stock.html", msg="开始日期:{}晚于结束日期:{}".format(start_date, end_date))
    start_date = transfer_date_string_to_int(start_date)
    end_date = transfer_date_string_to_int(end_date)
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
        mcode = '0' + code if code.startswith('6') else '1' + code
        url = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}'.format(mcode, start_date, end_date)
        try:
            content = urllib.request.urlopen(url).read()
            content = content.decode("gbk").encode("utf-8")
            data = StringIO(str(content,'utf-8'))
        except Exception as e:
            return render_template("stock.html", msg="{}数据需要查询".format(code))
        tmp_df = pd.read_csv(data)
        tmp_df = tmp_df[["日期","股票代码","名称","开盘价","收盘价","最低价","最高价"]]
        tmp_df["股票代码"] = tmp_df["股票代码"].str.strip("'")
        df = df.append(tmp_df)
    return df.to_html()

if __name__ == '__main__':
    app.run(port = 54321)
