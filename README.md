# defend_ssh

## 功能
保护 ssh ，用于将恶意登录 SSH的IP地址，加入 /etc/hosts.deny 黑名单。

## 条件
* 累计恶意登录ssh 超过10次(含) 的IP 地址。
* 不包括，信任的IP，白名单内的IP地址。

## 时间
* 惩罚时间拒绝链接，有效期为 1天。

## 使用方法
* 下载代码，保存到指定的路径，例如:
`/root/sh/`
* 使用 root 权限，添加 crontab 任务计划，例如:
`*/5 * * * * /root/sh/defend_ssh.py >> /root/sh/cron.log 2>&1`
