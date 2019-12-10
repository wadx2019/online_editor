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
import time
import threading
app=Flask(__name__)
app.secret_key=os.urandom(24)
name_psd={}
pf_editor={}

def main():
    global name_psd,pf_editor,dbop
    while True:
        time.sleep(300)
        try:
            curtime=time.time()
            name_psd_key=[]
            for item in name_psd.items():
                if curtime-item[1]>600:
                    name_psd_key.append(item[0])
            for item in name_psd_key: 
                name_psd.pop(item)
            
            curtime=time.time()
            pf_editor_key=[]
            for item in pf_editor.items():
                if curtime-item[1]>600:
                    pf_editor_key.append(item[0])
            for item in pf_editor_key:
                if dbop.update(item[0],{'fname':item[1]},{"currentedit":None}):
                    pf_editor.pop(item)
        except Exception as e:
            print(e)
    
@app.route('/login',methods=['POST'])
def login():
    global dbop
    response={"state":0}
    if dbop.select_by_key('USERS',request.form):
        response['state']=1
        name_psd[(request.form.get('uname'),request.form.get('upasswd'))]=time.time()
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
    response={"state":0,'pno':None}
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
        if not f[0]['currentedit'] or f[0]['currentedit']==session.get('name_psd')[0]:
            value={'fcontent':fcontent,'currentedit':currentedit}
            if dbop.update(pname,key,value):
                pf_editor[(pname,fname,currentedit)]=time.time()
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
        if op=='pro':
            pno=request.form.get('pno')
            key={'pno':pno}
            project=dbop.select_by_key('PROJECTS',key)[0]
            project['CREATETIME']=project['CREATETIME'].strftime("%Y-%m-%d %H:%M:%S")
            if project:
                pname=project['PNAME']
                files=dbop.select_by_table(pname)
                for i in range(len(files)):
                    files[i]={'fname':files[i]['fname'],'createtime':files[i]['createtime'].strftime("%Y-%m-%d %H:%M:%S"),'currentedit':files[i]['currentedit']}
                response['poject']=project
                response['files']=files
                response['state']=1
        elif op=='file':
            pname=request.form.get('pname')
            fname=request.form.get('fname')
            key={'fname':fname}
            data=dbop.select_by_key(pname,key)
            if data:
                file=data[0]
                file['createtime']=file['createtime'].strftime("%Y-%m-%d %H:%M:%S")
                response['file']=file
                response['state']=1
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
        if tmp[0]['PMASTER']==session.get("name_psd")[0]:
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
        pname=request.form.get('pname')
        key={'fname':request.form.get('fname')}
        if not dbop.select_by_key(pname,key)[0]['currentedit'] and dbop.delete_by_key(pname,key):
            response['state']=1
    else:
        response['state']=2
    return json.dumps(response)
@app.route('/finishFile',methods=['POST'])
def finishFile():
    global dbop
    response={'state':0}
    if session.get('name_psd') in name_psd:
        fname=request.form.get('fname')
        pname=request.form.get('pname')
        editor=session.get('name_psd')[0]
        key={'fname':fname,'currentedit':editor}
        value={'currentedit':None}
        if dbop.update(pname,key,value):
            try:
                pf_editor.pop(tuple([pname])+tuple(key.values()))
            except:
                pass
            response['state']=1
    return json.dumps(response)
@app.route('/logout',methods=['POST'])
def logout():
    global dbop
    response={"state":0}
    try:
        name_psd.pop((request.form.get('uname'),request.form.get('upasswd')))
        session.clear()
        response['state']=1
    except:
        pass
    return json.dumps(response)
@app.route('/modifyPasswd',methods=['POST'])
def modifyPasswd():
    global dbop
    response={"state":0}
    key={'uname':request.form['uname'],'upasswd':request.form['upasswd']}
    value={'upasswd':request.form['newpasswd']}
    if dbop.select_by_key('USERS',key) and dbop.update('USERS',key,value):
        response['state']=1
        try:
            name_psd.pop((request.form.get('uname'),request.form.get('upasswd')))
        except:
            pass
    return json.dumps(response)
if __name__=='__main__':
    try:
        main_t=threading.Thread(target=main)
        main_t.setDaemon(True)
        main_t.start()
        dbop=dbOperation(host='127.0.0.1',port=3306,user='root',passwd='',database='TEST')
        app.run(host='0.0.0.0',port=7000,debug=False,threaded=True)
    except Exception as e:
        print(e)
    finally:
        dbop.close()
