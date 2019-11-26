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
- pass
