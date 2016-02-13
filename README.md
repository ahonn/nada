## Nada

> The mind is like a serpent, forgetting all its unsteadiness by hearing the nada, it does not run away anywhere.

命令行音乐播放器, 目前包括 luoo落网, echo 回声. 


基于 python2.7 , 需要 `BeautifulSoup`, `requests` 模块. 需要安装 mpg123 ( Linux 系统自带, OS X 需要安装).

## 安装：
`$ sudo python setup.py install`

## 运行
`$ nada`

## 基本操作:

键    | 功能
:----:|:--------
m     | 回到菜单
l     | 前进
h     | 后退
k     | 上移
j     | 下移
[     | 上一首
]     | 下一首
space | 播放/暂停

## To Do List
- 重构UI及逻辑代码
- 添加歌词及曲名滚动
- 添加音量控制
- 添加下载功能
- 添加信息记录

## Change Log
#### 2016.02.13 
- [Add] 添加 echo API, 用于获取分类频道, 及频道中的曲目信息
- [Add] 增加 echo 中的频道分类, 完成最热频道及最新频道