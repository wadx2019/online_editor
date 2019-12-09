# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 16:02:15 2019

@author: 27803
"""

from flask import session,Flask,request
import os
from db import dbOperation,generatorPno
import json
import datetime

app=Flask(__name__)
app.secret_key=os.urandom(24)
name_psd=set()

@app.route('/login',methods=['POST'])
def login():
    global dbop
    response={"state":0}
    if dbop.select_by_key('USERS',request.form):
        response['state']=1
        name_psd.add((request.form.get('uname'),request.form.get('upasswd')))
        session['name_psd']=(request.form.get('uname'),request.form.get('upasswd'))
    return json.dumps(response)
    
@app.route('/register',methods=['POST'])
def register():
    global dbop
    response={"state":0}
    key={'uname':request.form['uname']}
    if not dbop.select_by_key('USERS',key):
        if dbop.insert_by_key('USERS',request.form):
            response['state']=1
    return json.dumps(response)

@app.route('/createProject',methods=['POST'])
def createProject():
    global dbop
    response={"state":0}
    if session.get('name_psd') in name_psd:
        pname=request.form.get('pname')
        pno=generatorPno(pname)
        key={'pno':pno}
        while dbop.select_by_key('PROJECTS',key):
            pno=str((int(pno)+1)%int(1e8)).zfill(8)
            key['pno']=pno
        key={'pno':pno,'pname':pname,'createtime':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'pmaster':session['name_psd'][0]}
        attribute=[['fname','varchar(256)','primary key'],['fcontent','longtext'],['createtime','datetime'],['currentedit','varchar(256)']]
        if dbop.insert_by_key('PROJECTS',key) and dbop.insert_by_table(pname,attribute):
            response['state']=1
            response['pno']=pno
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/createFile',methods=['POST'])
def createFile():
    global dbop
    response={"state":0}
    if session.get('name_psd') in name_psd:
        pname=request.form.get('pname')
        fname=request.form.get('fname')
        key={'fname':fname}
        if not dbop.select_by_key(pname,key):
            key['createtime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if dbop.insert_by_key(pname,key):
                response['state']=1
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/modifyFile',methods=['POST'])
def modifyFile():
    global dbop
    response={"state":0}
    if session.get('name_psd') in name_psd:
        pname=request.form.get('pname')
        fname=request.form.get('fname')
        fcontent=request.form.get('fcontent')
        currentedit=session.get('name_psd')[0]
        key={'fname':fname}
        f=dbop.select_by_key(pname,key)
        print(f)
        if not f[0]['currentedit']:
            value={'fcontent':fcontent,'currentedit':currentedit}
            if dbop.update(pname,key,value):
                response['state']=1
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/query',methods=['POST'])
def query():
    global dbop
    response={"state":0}
    if session.get('name_psd') in name_psd:
        op=request.form.get('op')
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/removeProject',methods=['POST'])
def removeProject():
    global dbop
    response={"state":0}
    if session.get('name_psd') in name_psd:
        pname=request.form.get('pname')
        key={'pname':pname}
        tmp=dbop.select_by_key('PROJECTS',key)
        if tmp[0]['pmaster']==session.get("name_psd")[0]:
            if dbop.delete_by_table(pname) and dbop.delete_by_key('PROJECTS',key):
                response['state']=1
        else:
            response['state']=3
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/removeFile',methods=['POST'])
def removeFile():
    global dbop
    response={"state":0}
    if session.get('name_psd') in name_psd:
        pass
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/logout',methods=['POST'])
def logout():
    global dbop
    response={"state":0}
    name_psd.remove((request.form.get('uname'),request.form.get('upasswd')))
    return json.dumps(response)
@app.route('/modifyPasswd',methods=['POST'])
def modifyPasswd():
    global dbop
    response={"state":0}
    key={'uname':request.form['uname'],'upasswd':request.form['upasswd']}
    value={'upasswd':request.form['newpasswd']}
    if dbop.select_by_key('UESRS',key) and dbop.update('USERS',key,value):
        response['state']=1
        name_psd.remove((request.form.get('uname'),request.form.get('upasswd')))
    return json.dumps(response)
if __name__=='__main__':
    try:
        dbop=dbOperation(host='127.0.0.1',port=3306,user='root',passwd='',database='TEST')
        app.run(host='0.0.0.0',port=7000,debug=False)
    except Exception as e:
        print(e)
    finally:
        dbop.close()
