# CmdOven

本脚本用于提供快速的钉钉机器人发信功能，以及一个精简的钉钉 bot 发信 API。用于进行一些服务器上的事务回调。

可以考虑创建一个只有自己和 bot 的群聊来愉快地中断式监控服务器上的实验。

在做实验、配环境的过程中，考虑使用 CmdOven 脚本来让钉钉 bot 来告诉你跑完了！

享受指令“烘焙”完成时的“ding!”吧！

The scripts provide a way to send messages to DingTalk robot. It can be used to send messages to yourself when you are doing some time-consuming tasks.

Enjoy the "ding!" when the command is done!

## 使用 | Usage

```shell
alias ding = "python /path/to/cmd_oven.py"
ding echo "123"
```

## TODOs

- [ ] 更好的交互方式（目前在遇到 `;` 这种东西的时候会被阻隔）
- [ ] 更便捷的使用（`pip` 打包等）
- [ ] 更多的功能（?）