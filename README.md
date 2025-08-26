# 干了兄弟们 #

功能：爬作业 爬答案 下文档

[sign已经支持自动解密](https://github.com/Tonyha7/msyk-invasion/pull/2)感谢贡献

[这个玩意儿是怎么做出来的](https://www.52pojie.cn/thread-1613563-1-1.html)（里面附带的代码有个脑瘫问题，题号都是1，原因是count=1的位置错了，当时复制的代码是改完没保存的。。。。。。）

### 使用

配置好python3环境，缺库的终端执行：

`pip install requests colorama`

首次运行请模拟pad登录获取信息

[![LfbpCR.png](https://s1.ax1x.com/2022/04/23/LfbpCR.png)](https://imgtu.com/i/LfbpCR)

对于已发布但未开始的作业可以通过**跑作业id.py（现已合并）**获取

*小心浏览器打开大量页面时卡死*

现在已经不需要用浏览器打开页面了，感谢[ljlVink](https://github.com/ljlVink)实现

### 欢迎大佬们前来改进程序，每次Push/Pull requests将会自动构建exe发布Release

——————————————————————————————————————

修复res返回空字符串时json.loads()无法解析的问题

修复阅读材料（作业类型5）类型作业无法获取材料链接的问题

在跑作业id和起始界面增加作业学科显示，便于识别

将起始界面的答题卡作业和阅读作业分开显示，便于识别

*25年了真的还在有人用这个东西（就是我）（我也是）*

*就是我也马上高三了，用的也很胆怯（第一次尝试更新程序，见谅）（加油，我也高三，争取持续贡献）*

*会持续维护，可能后续会提供教程或GUI*

*目前课件下载的API挂了，后续尝试恢复*

*更新内容见Updates.md*
