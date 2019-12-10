# Online_Editor

## Client
- ### front
  - pyqt or qtcreator
  - 设计登录界面，登录完成后转为文本编辑界面
  - 实现文本显示高亮，多用户锁展示
  - 设计用户友好型界面，实现一键获取文本，保存文本
  
- ### back
  - python or c++
  - 遵守请求接收协议，获取相应文件的数据
  - 实现后台的定时刷新多用户使用情况

## Server
- ### language
  - python

- ### mode 
  - Socket or Flask

- ### flow
  - 有限状态机，当用户第一次发送请求时，建立数据库连接，之后根据请求报文和上一次的状态与数据库连接，并做出相应更改

## ER diagram
[获取ER图(密码：shujuku)](https://www.processon.com/view/link/5ddc8206e4b034050df1ec9f?pw=shujuku)

## Flow diagram
[获取控制流图(密码：shujuku)](https://www.processon.com/view/link/5dc6ce65e4b0fc314a096460)

## Division of labor
  - Shutong Ding:server
  - Hengquan Mei:back and resources
  - Huan Yang:front
  
## Protocol
- ### 登录注册部分:

- login:
   - 需要参数：’uname’ , ‘upasswd’
   - 是否需要cookie：no
   - 返回：’state’:{0:密码错误或账号不存在,1:登录成功}

- register：
   - 需要参数：’uname’ , ‘upasswd’
   - 是否需要cookie：no
   - 返回：’state’:{0:用户名已存在,1:注册成功}

- modifyPasswd:
   - 需要参数：’uname’ , ‘upasswd’ , ‘newpasswd’
   - 是否需要cookie：no
   - 返回: ‘state’:{0:账户不存在或原密码错误,1:修改密码成功}

- logout：
  - 需要参数：无
  - 是否需要cookie：yes
  - 返回：’state’:{0:该cookie不存在,1:登出成功}


- ### 编辑界面：

- createProject：
  - 需要参数：’pname’
  - 是否需要cookie：yes
  - 返回：’state’:{0:项目名已存在,1:创建成功,2:cookie失效}
  - ‘pno’:项目号 CHAR(8)

- createFile：
  - 需要参数：’pname’ , ‘fname’
  - 是否需要cookie：yes
  - 返回：’state’:{0:文件名已存在,1:创建成功,2:cookie失效}

- modifyFile:
  - 需要参数：’pname’ , ’fname’ , ‘fcontent’
  - 是否需要cookie：yes
  -返回：’state’:{0:有其他用户正在修改,1:修改成功,2:cookie失效}

- query：
  - 需要参数：’op’:{‘pro’:返回项目信息,’file’:返回文件信息}
  - ‘pro’情况下所需参数：‘pno’  
  - ‘file’情况下所需参数：’pname’ , ‘fname’
  - 是否需要cookie：yes
  - 返回：’state’:{0:项目名已存在,1:创建成功,2:cookie失效}
  - ‘pro’情况下：’project’={’pname’ , ‘createtime’ , ‘pmaster’} , ‘files’=[{‘fname’ , ’currentedit’ , ‘createtime’} for i in文件数]
  - ‘file’情况下：’file’:{‘fname’ , ’currentedit’ , ‘createtime’ , ‘fcontent’}

- finishFile：
  - 需要参数：’pname’ , ’fname’
  - 是否需要cookie：yes
  - 返回：’state’:{0:您不是当前修改者,1:结束成功,2:cookie失效}

- removeProject：
  - 需要参数：’pname’
  - 是否需要cookie：yes
  - 返回：’state’:{0:该项目正在被他人编辑,1:删除成功,2:cookie失效,3:您不是该项目所有者或不存在该项目}

- removeFile:
  - 需要参数：’pname’ , ’fname’ 
  - 是否需要cookie：yes
  - 返回：’state’:{0:该文件正在被他人编辑,,1:删除成功,2:cookie失效}



