## Nada

> The mind is like a serpent, forgetting all its unsteadiness by hearing the nada, it does not run away anywhere.

基于 Python 的多网站命令行音乐播放器, 目前包括 luoo 落网, echo 回声.

[![platform](https://img.shields.io/badge/python-2.7-blue.svg)]()
[![Software License](https://img.shields.io/packagist/l/doctrine/orm.svg)](https://github.com/ahonn/Nada/blob/master/LICENSE)
[![versions](https://img.shields.io/badge/pypi-v0.1.2-blue.svg)](https://pypi.python.org/pypi/nada)

[![nada](http://7xqvel.com1.z0.glb.clouddn.com/2.pic_hd.jpg?imageView/3/w/600/q/100)](https://pypi.python.org/pypi/nada)

## 安装 & 运行：
#### 通过 pip 安装
`$ sudo pip install nada`

OS X:  
`$ brew install mpg123`

Ubuntu:  
`$ sudo apt-get install mpg123`

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
  a   | 加入收藏
  r   | 移出收藏
  c   | 进入收藏
space | 播放/暂停

## To Do List
- ~~重构代码~~
- 添加曲名滚动
- 添加音量控制
- 添加下载功能
- 添加信息记录

## Change Log

#### 2016.02.18 
- [Add] 增加 common & database
- [Add] 增加收藏功能, 添加或删除收藏夹中的歌曲, 并将记录储存到本地

#### 2016.02.17
- [Release] 发布到 pypi
- [Add] 增加翻页, u 上一页, i 下一页
- [Fix] 修复播放下一曲时, 光标不跟随翻页的 Bug

#### 2016.02.14
- [Change] 重写逻辑, 调整函数命名等
- [Update] 调整 UI, 整个界面向左移  
- [Finish] 完成 echo 回声基本功能

#### 2016.02.13
- [Add] 添加 echo API, 用于获取分类频道, 及频道中的曲目信息
- [Add] 增加 echo 中的频道分类, 完成最热频道及最新频道
