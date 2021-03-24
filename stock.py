import os
import peewee
import pandas as pd
db = peewee.SqliteDatabase(os.getcwd()+'/stock.db')
def get_table_name(model_class):
    return "s{}".format(model_class.__name__)

def class_generator(scode):
    value_dict = {}
    value_dict['date'] = peewee.CharField(max_length=14, primary_key=True, verbose_name="日期")
    value_dict['open'] = peewee.FloatField(verbose_name="开盘价")
    value_dict['close'] = peewee.FloatField(verbose_name="收盘价")
    value_dict['low']   = peewee.FloatField(verbose_name="最低价")
    value_dict['high']  = peewee.FloatField(verbose_name="最高价")
    value_dict['volume'] = peewee.BigIntegerField(verbose_name="成交量")
    value_dict['Meta'] = type('Meta', (object, ), {'database': db, 'table_function': get_table_name})
    return type(scode, (peewee.Model, ), value_dict)

def add(code, date, open_, close, low, high, volume):
    stock = class_generator(code)
    db.create_tables([stock])
    mdict = {'date':date, 'open':open_, 'close':close, 'low':low, 'high':high, 'volume':volume}
    return stock.insert(mdict).exexute()

def add_batch(code):
    stock = class_generator(code)
    db.create_tables([stock])
    df = pd.read_csv('data/{}.csv'.format(code))
    list_of_dicts = df.to_dict('records')
    return stock.insert_many(list_of_dicts).execute()

def query(code, start_date, end_date):
    stock = class_generator(code)
    mquery = stock.select(stock).where((stock.date > start_date) & (stock.date <= end_date))
    df = pd.DataFrame(list(mquery.dicts()))
    df_columns = df.columns.tolist()
    df['code'] = code
    code_list = ['code']
    code_list.extend(df_columns)
    df = df[code_list]
    return df

if __name__ == '__main__':
    #codes = ['600309','300750','600031','000963','600176','002352','000651','600276','600900','600585','300760','300015','002493','002415','000002','600887','002230','600570']
    #for code in codes: print(code, add_batch(code))
    df = query('600031', '2020-03-01', '2020-04-01')
    print(df)
