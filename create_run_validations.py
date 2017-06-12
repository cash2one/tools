# -*-coding:utf-8-*-
__author__ = 'csy'
import MySQLdb
import sys,os
reload(sys)
sys.setdefaultencoding("utf8")


def database():
    try:
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = MySQLdb.connect(host='', user='', passwd='', port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标对象

        cur.execute("USE brush")
        cur.execute('select count(*) from Cases')
        total = cur.fetchone()[0]

        cur.execute('select * from Cases')
        users = cur.fetchall()

        cur.execute('SELECT * FROM Cases WHERE Cases.created_time > DATE_SUB(NOW(), INTERVAL 30 MINUTE)')
        change = cur.fetchall()

        cur.close()  # 关闭游标
        conn.commit()  # 向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
        conn.close()  # 关闭到数据库的连接，释放数据库资源

        return total, users, change
    except Exception as e:
        print("数据库操作发生异常 %s" % e)

class Create(object):
    def __init__(self,path):
        self.path = path

    def create_validations(self, users):
        file = os.path.join(self.path, 'validations.py')
        i = 1
        f = open(file, 'w')
        f.write('# -*- coding: utf-8 -*-')
        f.write('\n')
        f.write('from Page.page import homePage')
        f.write('\n')
        f.write('import random')
        f.write('\n')
        f.write('from model import webelement, env')
        f.write('\n')
        f.write('from model import common, log')
        f.write('\n')
        f.write('\n')
        for row in users:
            f.write('def TestCase_' + str(i) + '():')
            f.write('\n\t')
            f.write('env.KEYWORD = ' + "'" + row[1] + "'")
            f.write('\n\t')
            if 'http' in row[2]:
                f.write('env.TARGET = ' + "'" + row[2] + "'")
            else:
                f.write('env.TARGET = ' + row[2])
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
            i = i + 1
        f.close()


    def create_run(self, total):
        file = os.path.join(self.path, 'run.py')
        run = open(file, 'w')
        run.write('# -*- coding: utf-8 -*-')
        run.write('\n')
        run.write('from Page import conf, testcase')
        run.write('\n')
        run.write('from model import executer,env')
        run.write('\n')
        run.write('\n')
        run.write('\n')
        run.write('def Case1():')

        for n in xrange(1, (int(total) + 1)):
            run.write('\n\t')
            run.write('executer.run(conf.Brush, testcase.validations.TestCase_' + str(n) + ')')

        run.write('\n')
        run.write('\n')
        run.write('if __name__ == "__main__":')
        run.write('\n\t')
        run.write('Case1()')
        run.close()

if __name__  == "__main__":
    total,users, change = database()
    if len(change) != 0:
        create = Create('C:/Users/csy/Desktop/result')
        create.create_run(total)
        create.create_validations(users)
        print '已重新生成！'
    print '执行完成！'
