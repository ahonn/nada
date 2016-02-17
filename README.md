## Nada

> The mind is like a serpent, forgetting all its unsteadiness by hearing the nada, it does not run away anywhere.

基于 Python2.7 的命令行音乐播放器( Windows 平台不可用 ), 目前包括 luoo 落网, echo 回声.

需要 `BeautifulSoup`, `requests`, `lxml` 模块.

需要安装 mpg123 ( Linux 系统自带, OS X 需要安装).

## 安装 & 运行：
#### 通过 pip 安装
`pip install nada`

#### 通过源码安装
`$ git clone git@github.com:ahonn/Nada.git`

`$ cd Nada`

`$ sudo python setup.py install`

#### 运行
`$ nada`

## 基本操作:

  键  | 功能
:----:|:-------
  m   | 回到菜单
  l   | 前进
  h   | 后退
  k   | 上移
  j   | 下移
  u   | 上一页
  i   | 下一页
  [   | 上一首
  ]   | 下一首
space | 播放/暂停

## To Do List
- ~~重构代码~~
- 添加曲名滚动
- 添加音量控制
- 添加下载功能
- 添加信息记录

## Change Log

#### 2016.02.17
- [Add] 增加翻页, u 上一页, i 下一页

#### 2016.02.14
- [Change] 重写逻辑, 调整函数命名等
- [Update] 调整 UI, 整个界面向左移  
- [Finish] 完成 echo 回声基本功能

#### 2016.02.13
- [Add] 添加 echo API, 用于获取分类频道, 及频道中的曲目信息
- [Add] 增加 echo 中的频道分类, 完成最热频道及最新频道
