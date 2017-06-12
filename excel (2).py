# -*- coding: utf-8 -*-
import  xdrlib ,sys
import xlrd
import sys
import redis
reload(sys)
sys.setdefaultencoding( "utf-8" )

def open_excel(file= 'file.xls'):
    try:
         data = xlrd.open_workbook(file)
         return data
    except Exception,e:
         print str(e)
 #根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
     data = open_excel(file)
     table = data.sheets()[by_index]
     nrows = table.nrows #行数
     ncols = table.ncols #列数
     colnames =  table.row_values(colnameindex) #某一行数据
     list =[]
     for rownum in range(1,nrows):

          row = table.row_values(rownum)
          if row:
              app = {}
              for i in range(len(colnames)):
                 app[colnames[i]] = row[i]
              list.append(app)
     return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据

    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
                list.append(app)
    return list

def main():
    pool = redis.ConnectionPool(host='101.201.117.71', port=6379, db=1)
    r = redis.Redis(connection_pool=pool)
    """
    r.delete('page')
    tables = excel_table_byindex('C:\\test.xls', 0, 0)
    for row in tables:
        car = row['车系'.decode('utf-8')] + " "+'一猫'
        page = row['页面'.decode('utf-8')].split('com')[1].strip('/')

        r.lpush('page', page)
	
    for i in r.lrange('page', 0, -1):
	    print i
    
    print 'haha', len(r.lrange('page', 0, -1))
    """
    """
        f = open(r'C:/Users/csy/Desktop/result/exe.txt', 'a')
        f.write('executer.run(conf.Brush, testcase.validations.TestCase_'+page+')')
        f.write('\n')
        f.close()
    """



    """
    tables = excel_table_byname()
    for row in tables:
        print row



    #r.delete("陈仕洋")
    #r.set("陈仕洋".decode("utf-8"), 1)
    #r.expire('陈仕洋', 10)

    if r.exists("陈仕洋"):
        r.incr("陈仕洋", amount=1)
    else:
        r.set("陈仕洋".decode("utf-8"), 1)

    print r.get('陈仕洋')
"""

    pipe = r.pipeline()
    pipe_size = 100000


    len = 0
    key_list = []

    for key in r.scan_iter(match='陈仕洋',count=100000):

        key_list.append(key)
        pipe.get(key)
        if len < pipe_size:
            len += 1
        else:
            for (k, v) in zip(key_list, pipe.execute()):
                print k, v
            len = 0
            key_list = []

    for (k, v) in zip(key_list, pipe.execute()):
        print k, v







if __name__=="__main__":
     main()
