#mysql_5.7
#python_3.6 
#数据库调用函数，数据解释详见数据库说明手册

import mysql.connector

class DB(object):
    def __init__(self,server,username,password,dbname):
        self.__server = server
        self.__username = username
        self.__password = password
        self.__dbname = dbname
        self.__conn = mysql.connector.connect(self.__server,self.__username,self.__password,self.__dbname)






#增 
    def add_user(self,username,password,email):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("insert into user (username,password,email) values ({0},{1},{2})".format(username,password,email))
        id_user = cur._last_insert_id
        conn.commit()
        return id_user

    def add_blog(self,id_user,title,introduction,filename,time_launch):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("insert into blog id_blog,title,introduction,filename,time_launch values ({0},{1},{2},{3})".format(title,introduction,filename,time_launch))
        id_blog = cur._last_insert_id
        cur.execute("insert into relation_blog_user id_blog,id_user values ({0},{1})".format(id_blog,id_user))
        conn.commit()
        return id_blog

    def add_team(self,name,introduction,time_launch):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("insert into team id_team,name,introduction,time_launch values ({0},{1},{2})".format(name,introduction,time_launch))
        id_team = cur._last_insert_id
        conn.commit()
        return id_team

    def add_member(self,id_team,id_now_user,id_next_user):
        conn = self.__conn
        cur = conn.cursor()
        #cur.execute("insert into queue id_team,id_now_user,id_next_user valuse ({0},{1},{2})".format(id_team,id_now_user,id_next_user))
        cur.execute("insert into relation_team_user id_team,id_user values ({0},{1})".format(id_team,id_now_user))
        conn.commit()

    def add_task(self,id_team,name,time_begin,time_end,requirement):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("insert into task name,time_begin,time_end,requirement values ({0},{1},{2},{3})".format(name,time_begin,time_end,requirement))
        id_task = cur._last_insert_id
        cur.execute("insert relation_task_team id_task,id_team values ({0},{1})".format(id_task,id_team))
        conn.commit()
        return id_task

    def add_task_member(self,id_task,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("insert into relation_task_user id_task,id_user,isdone values ({0},{1},{2})".format(id_task,id_user,False))
        conn.commit()






#删
    def delete_task(self,id_task):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("delete from task where id={0}".format(id_task))
        cur.execute("delete from relation_task_user where id_task={0}".format(id_task))
        cur.execute("delete from relation_task_team where id_task={0}".format(id_task))
        conn.commit()

    def delete_member(self,id_team,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("delete from relation_team_user where id_team={0}&&id_user={1}".format(id_team,id_user))
        conn.commit()

    def delete_team(self,id_team):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("delete from relation_team_user where id_team={0}".format(id_team))
        cur.execute("delete from team where id_team={0}".format(id_team))
        conn.commit()

    def delete_blog(self,id_blog):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("delete from relation_blog_user where id_blog={0}".format(id_blog))
        cur.execute("delete from blog where id_blog={0}".format(id_blog))
        conn.commit()

    def delete_user(self,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("delete from relation_blog_user where id_user={0}".format(id_user))
        cur.execute("delete from relation_task_user where id_user={0}".format(id_user))
        cur.execute("delete from relation_team_user where id_user={0}".format(id_user))
        cur.execute("delete from user where id_user={0}".format(id_user))
        conn.commit()






#查—————函数命名遵循末尾项为查询目标，中间项为查询条件；对于blog-user,team-user和team-task这三种单一关系，仅返回一维数组
#       其他关系返回所有字段信息
    def search_user(self,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from user where id_user={0}".format(id_user))
        result = cur.fetchall()
        return result
    
    def search_blog(self,id_blog):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from blog where id_blog={0}".format(id_blog))
        result = cur.fetchall()
        return result

    def search_task(self,id_task):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from task where id_task={0}".format(id_task))
        result = cur.fetchall()
        return result

    def search_team(self,id_team):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from team where id_team={0}".format(id_team))
        result = cur.fetchall()
        return result

    def search_user_blog(self,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_blog_user where id_user={0}".format(id_user))
        result = cur.fetchall()
        arr = []
        for i in result:
            arr.append(i[0])
        return arr

    def search_blog_user(self,id_blog):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_blog_user where id_blog={0}".format(id_blog))
        result = cur.fetchall()
        arr = []
        for i in result:
            arr.append(i[1])
        return arr

    def search_user_team(self,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_team_user where id_user={0}".format(id_user))
        result = cur.fetchall()
        arr = []
        for i in result:
            arr.append(i[0])
        return arr

    def search_team_user(self,id_team):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_team_user where id_team={0}".format(id_team))
        result = cur.fetchall()
        arr = []
        for i in result:
            arr.append(i[1])
        return arr

    def search_task_user(self,id_task):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_task_user where id_task={0}".format(id_task))
        result = cur.fetchall()
        return result

    def search_user_task(self,id_user):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_task_user where = id_user={0}".format(id_user))
        result = cur.fetchall()
        return result

    def search_team_task(self,id_team):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_task_team where id_team={0}".format(id_team))
        result = cur.fetchall()
        arr=[]
        for i in result:
            arr.append(i[0])
        return arr
    
    def search_task_team(self,id_task):
        conn = self.__conn
        cur = conn.cursor()
        cur.execute("select * from relation_task_team where id_task={0}".format(id_task))
        result = cur.fetchall()
        arr=[]
        for i in result:
            arr.append(i[1])
        return arr
