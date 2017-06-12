# -*- coding: utf-8 -*-
import  xdrlib ,sys, csv
import xlrd
import sys
reload(sys)
import redis,MySQLdb
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
    tables = excel_table_byindex('C:\\auto.xls', 0, 2)
    f = open(r'C:/Users/csy/Desktop/result/validations.txt', 'w+')
    f.write('# -*- coding: utf-8 -*-')
    f.write('\n')
    f.write('from Page.page import homePage')
    f.write('\n')
    f.write('\n')
    r = open(r'C:/Users/csy/Desktop/result/run.txt', 'w+')
    r.write('# -*- coding: utf-8 -*-')
    r.write('\n')
    r.write('from Page import conf, testcase')
    r.write('\n')
    r.write('from model import executer')
    r.write('\n')
    r.write('import os, types, inspect, sys')
    r.write('\n')
    r.write('\n')
    r.write('def Case():')
    r.write('\n\t')

    for row in tables:
        print 'row',row,type(row)
        # car = row[u'品牌名'.decode('utf-8')] + " "+'一猫'
        car = row[u'关键词'] + " "+'一猫'
        i = row[u'页面'].split('com')[1].strip('/')
        page = row[u'页面'.decode('utf-8')]
        # print car,page
        r.write('executer.run(conf.Brush, testcase.brandvalidations.TestCase_'+i+')')
        r.write('\n\t')
        f.write('def TestCase_' + str(i) + '():')
        f.write('\n\t')
        f.write('env.KEYWORD = ' + "'" + car + "'")
        f.write('\n\t')
        f.write('env.TARGET = ' + "'" + "http://dealer.emao.com" + "'")
        f.write('\n\t')
        f.write("log.step_normal('>>>>>搜索关键词：[%s], >>>>>目标地址：[%s]' % (env.KEYWORD, env.TARGET))")
        f.write('\n\t')
        f.write("homePage.Brush.Serch.TypeIn(env.KEYWORD)")
        f.write('\n\t')
        f.write('homePage.Brush.Button.Click()')
        f.write('\n\t')
        f.write("homePage.Brush.Brush.Brush(env.TARGET)")
        f.write('\n')
        f.write('\n')
    r.write('\n')
    r.write('if __name__ == "__main__":')
    r.write('\n\t')
    r.write('Case()')
    r.close()
    f.close()




if __name__=="__main__":
     main()
    # file=open('C:/Users/csy/Desktop/sql/2016091310365742.csv', 'r')
    #
    # reader=csv.reader(file)
    #
    #
    # rows = []
    # next(reader,None)
    # for row in reader:
    #         rows.append(row[0].decode('gbk'))
    #
    #
    # try:
    #     # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
    #     conn = MySQLdb.connect(host='redis.lan', user='root', passwd='123456', port=3306, charset='utf8')
    #     cur = conn.cursor()  # 获取一个游标对象
    #
    #     cur.execute("USE brush")
    #
    #     cur.execute('select * from Cases')
    #     users = cur.fetchall()
    #
    #     cur.close()  # 关闭游标
    #     conn.commit()  # 向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    #     conn.close()  # 关闭到数据库的连接，释放数据库资源
    #
    #
    # except Exception as e:
    #     print("数据库操作发生异常 %s" % e)
    #
    # i = 1
    # for row in users:
    #     print '------>',row,row[1],row[2]
    #     f = open(r'C:/Users/csy/Desktop/result/exe.py', 'a')
    #     f.write('# -*- coding: utf-8 -*-')
    #     f.write('\n')
    #     f.write('from Page.page import homePage')
    #     f.write('\n')
    #     f.write('import random')
    #     f.write('\n')
    #     f.write('from model import webelement, env')
    #     f.write('\n')
    #     f.write('from model import common, log')
    #     f.write('\n')
    #     f.write('\n')
    #     f.write('def TestCase_'+str(i)+'():')
    #     f.write('\n\t')
    #     f.write('env.KEYWORD = {}'.format(row[1]))
    #     f.write('\n\t')
    #     f.write('env.TARGET = {}'.format(row[2]))
    #     f.write('\n\t')
    #     f.write("log.step_normal('>>>>>搜索关键词：[%s], >>>>>目标地址：[%s]' % (env.KEYWORD, env.TARGET))")
    #     f.write('\n\t')
    #     f.write("homePage.Brush.Serch.TypeIn(env.KEYWORD)")
    #     f.write('\n\t')
    #     f.write('homePage.Brush.Button.Click()')
    #     f.write('\n\t')
    #     f.write("webelement.WebElement.clicktarget(env.TARGET)")
    #     f.write('\n')
    #     f.write('\n')
    #     """
    #     f.write('executer.run(conf.Brush, testcase.validations.TestCase_'+str(i)+')')
    #     f.write('\n')
    #     """
    #     i = i + 1
    # f.close()
