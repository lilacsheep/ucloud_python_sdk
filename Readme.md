# UCloud SDK

## 初始化连接


```
from UCloud import UCloud

ucloud = UCloud('public_key', 'private_key')
```


## 切换zone

默认为GetRegion返回的IsDefault的域
```
ucloud.switch_zone('cn-bj2-03')
```


## 获取当前Zone下所有主机实例

```
ucloud.uhost.instances
```

## 通过UhostId获取实例

```
instance = ucloud.uhost.get(UhostId)
```


## UHost主机操作

### Uhost 监控概览
```
ucloud.uhost.mon_overview()
```


### UHost 信息
```
instance.private_ip #私有ip
instance.public_ips #公有ip
instance.eip #返回list, EIP实例
instance.id # UhostId
instance.tag # Uhost 业务组
instance.network_state # Uhost 网络状态
instance.cpu # Uhost CPU数量
instance.gpu # Uhost GPU数量
instance.memory # Uhost 内存大小

instance.name # Uhost 名称 默认：Uhost
instance.remark # Uhost 备注
instance.auto_renew # Uhost 是否自动续费
instance.create_time # Uhost 创建时间
instance.expire_time # Uhost 过期时间
instance.state # Uhost 状态： 初始化: Initializing; 启动中: Starting; 运行中: Running; 关机中: Stopping; 关机: Stopped 安装失败: Install Fail; 重启中: Rebooting
instance.storage_type # Uhost LocalDisk，本地磁盘; UDisk，云硬盘
```

### UHost 操作
```
instance.name = test # 修改Uhost Name字段
instance.tag = test # 修改Uhost 业务组
instance.remark = test # 修改Uhost 备注
instance.reboot() # 重启Uhost
instance.start() # 启动Uhost
instance.stop() # 停止Uhost
instance.make_snapshot() # 创建快照
instance.reload() # 重新加载Uhost信息
instance.mon(cpu=False, root_disk=False, data_disk=False, io_read=False, io_write=False, disk_ops=False,
            net_in=False, net_out=False, net_pack_in=False, net_pack_out=False, memory=False, alive_process=False,
            block_process=False, tcp_connect_num=False) # 获取监控信息，最多不能超过10个选项
```

