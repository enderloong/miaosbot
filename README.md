# miaosbot

本仓库为喵沌老师TRPG骰子的源码。喵沌老师为Fate Atrous Grail TRPG规则的御用骰子，绑定了规则中常用的掷骰，便于玩家进行游戏。

## 如何使用喵沌老师

如果您只是希望使用喵沌老师进行游玩，那么可以无视本仓库的代码，从下述方式引入喵沌老师。

目前喵沌老师仍在开发过程中，功能并不稳定，很有可能会不定时中断。如果遇到了相关问题，请直接联系我。

### kook

喵沌老师目前仅支持kook(原开黑啦)。

您可以通过下列链接邀请喵沌老师进入您的服务器中：

https://www.kookapp.cn/app/oauth2/authorize?id=11545&permissions=22528&client_id=LsZdCmqgKsmFkxjz&redirect_uri=&scope=bot

## 喵沌老师的基本使用方式

调用喵沌老师的时候，需要使用“,”(半角逗号)作为前缀，并且与第一个命令之间无空格。

具体的投掷可以参见“,help dice”。

## 对喵沌老师进行开发

您可以使用miaos-core中的代码自由开发，本项目基于MIT协议，基本不存在使用限制(需要注明来源并包含LICENSE文件)。

代码比较简陋，不排除后续大修的可能(也可能就咕了)。

## 使用docker

docker文件夹中存放了喵沌老师的运行环境，可以使用Dockerfile构建镜像。

运行环境镜像也可以从dockerhub下载，命令为

```bash
docker pull enderloong/miaos_server_env:v0.1
```

## 联系方式

如果您对贡献本项目的代码感兴趣，或者使用时遇到了问题，欢迎直接联系我：

- QQ：121766186 (请注明喵沌老师相关或FAG相关)
- QQ群：893481833
- B站: https://space.bilibili.com/1550789
- 邮箱：lxlylz1001@qq.com (请注明喵沌老师相关或FAG相关)
