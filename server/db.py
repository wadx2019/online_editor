# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:54:43 2019

@author: 27803
"""
import pymysql

def generatorPno(Pname):
    return str(hash(Pname)%int(1e8)).zfill(8)

class dbOperation:
    
    def __init__(self,host,port,user,passwd,database):
        self.conn=pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=database,charset='utf8')
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    
    def insert_by_key(self,table,key):
        if isinstance(key, dict):
            keys = ', '.join(key.keys())
            values = ', '.join(['%s'] * len(key))
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, keys, values)
            try:
                self.cursor.execute(sql, tuple(key.values()))
                self.conn.commit()
                return True
            except pymysql.MySQLError as e:
                print(sql)
                print(e.args)
                self.conn.rollback()
                return False
        elif isinstance(key,list):
            for i in range(len(key)):
                key[i]=' '.join(key[i])
            attribute=' , '.join(key)
            sql = 'CREATE TABLE `%s` ( %s ) ;' % (table,attribute)
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                return True
            except pymysql.MySQLError as e:
                print(e.args)
                self.conn.rollback()
                return False

    def insert_by_table(self,table,key):
        return self.insert_by_key(table,key)
        
    def select_by_key(self, table, key=None):
        sql = None
        if isinstance(key, dict):
            sql_where = ''
            for item in key.items():
                row_str = str(item[0]) + '=' + '%s' + ' and '
                sql_where += row_str
            sql_where = sql_where[:-4]
            sql = 'SELECT * FROM `%s` WHERE %s ;' % (table, sql_where)
        elif not key:
            sql = 'SELECT * FROM `%s`;' % (table)
        if sql:
            try:
                self.cursor.execute(sql,tuple(key.values()) if key else None)
                data = self.cursor.fetchall()
                if len(data) > 0:
                    return data
                return None
            except pymysql.MySQLError as e:
                print(sql)
                print(e.args)
        return None

    def select_by_table(self,table):
        return self.select_by_key(table)
    
    def delete_by_key(self,table,key=None):
        sql=None
        if isinstance(key, dict):
            sql_where = ''
            for item in key.items():
                row_str = str(item[0]) + '=' + '%s' + ' and '
                sql_where += row_str
            sql_where = sql_where[:-4]
            sql = 'DELETE FROM `%s` WHERE %s ;' % (table, sql_where)
        elif not key:
            sql = 'DROP TABLE `%s`;' % (table)
        if sql:
            try:
                self.cursor.execute(sql,tuple(key.values()) if key else None)
                self.conn.commit()
                return True
            except pymysql.MySQLError as e:
                print(e.args)
                self.conn.rollback()
                return False
                    
    def delete_by_table(self,table):
        return self.delete_by_key(table)
    
    def update(self,table,key,value):
        sql=None
        if isinstance(key,dict) and isinstance(value,dict):
            sql_where = ''
            for item in key.items():
                row_str = str(item[0]) + '=' + '%s' + ' and '
                sql_where += row_str
            sql_where = sql_where[:-4]
            sql_set = ''
            for item in value.items():
                row_str = str(item[0]) + '=' + '%s' + ' , '
                sql_set += row_str
            sql_set = sql_set[:-2]   
            sql = 'UPDATE `%s` SET %s  WHERE %s ;' % (table,sql_set,sql_where)
        if sql:
            try:
                print(sql)
                self.cursor.execute(sql,tuple(value.values())+tuple(key.values()))
                self.conn.commit()
                return True
            except pymysql.MySQLError as e:
                print(e.args)
                print(sql)
                self.conn.rollback()
                return False
            
        
    def close(self):
        self.cursor.close()
        self.conn.close()
