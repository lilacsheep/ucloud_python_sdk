# UCloud SDK

## 安装
```
python setup.py install
```

## 初始化连接


```
from ucloud_sdk.UCloud import UCloud

ucloud = UCloud('public_key', 'private_key', 'project_id')
# project_id 为空时会默认使用默认项目
```

## 切换Project
```
ucloud.switch_project(project_id)
```

## 切换zone

默认为GetRegion返回的IsDefault的域
```
ucloud.switch_zone('cn-bj2-03')
```


## 发送短信
```
ucloud.send_sms('1111111,111111,111111,1111', '测试短信')
# 手机号码可以用逗号分隔, 也可以传入list
```


## UHost主机操作

### 获取当前Zone下所有主机实例

```
ucloud.uhost.instances
```


### Uhost 监控概览
```
ucloud.uhost.mon_overview()
```

### 通过UhostId获取实例

```
instance = ucloud.uhost.get(UhostId)
ucloud.uhost.get_many(ids) # 通过UHostId列表获取多个主机，返回一个由id为key的字典
```


### UHost 信息
```
instance.private_ip #私有ip
instance.public_ips #公有ip
instance.eip #返回list, EIP实例
instance.eip_ids #返回list, EIPId 列表
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
instance.terminate() # 销毁主机
instance.mon(cpu=False, root_disk=False, data_disk=False, io_read=False, io_write=False, disk_ops=False,
            net_in=False, net_out=False, net_pack_in=False, net_pack_out=False, memory=False, alive_process=False,
            block_process=False, tcp_connect_num=False) # 获取监控信息，最多不能超过10个选项
```


## EIP 查询与操作


### 获取当前Zone下EIP
```
ucloud.eip.instances # 所有EIP信息
ucloud.eip.unbind_eip # 所有未绑定EIP
ucloud.eip.get(EIPId) # 通过EIPId来获取EIP实例
ucloud.eip.share_bandwidth # 获取共享带宽
ucloud.eip.get_share_bandwidth(ShareBandwidthId) # 通过共享带宽id来获取 带宽实例
ucloud.eip.get_many(ids) # 通过EIPId列表获取多个主机，返回一个由EIPId为key的字典
```

### 创建EIP
```
ucloud.eip.create_eip(operator_name, bandwidth=2, charge_type='Month', name=None, tag=None, remark=None, share_bandwidth=None)

# operator_name EIP 属性, 一般传入BGP， 海外传International
# bandwidth 带宽值，取值2到100之间
# charge_type 付费类型默认：按月
# share_bandwidth 绑定的共享带宽ID

返回创建好的EIP实例
```

### EIP实例操作

#### EIP 实例信息
```
eip = ucloud.eip.get(EIPId) # 通过EIPId来获取EIP实例
eip.id #EIPId
eip.type # 类型
eip.name # 名称默认 EIP
eip.tag # 业务组
eip.remark # 备注
eip.charge_type #付费类型
eip.status # 状态 used: 已绑定, free: 未绑定, freeze: 已冻结
eip.create_time # 创建时间
eip.expire_time # 过期时间
eip.eip_address # EIP地址信息
eip.expire # 是否过期
eip.resource # 绑定的资源
```

#### EIP 实例操作
```
eip.name = test # 修改 EIP 名称
eip.tag = test # 修改 EIP 业务组
eip.remark = test # 修改 EIP 备注
eip.release() # EIP 释放
eip.unbind(resource) # EIP 解绑 传入Uhost实例或者ULB实例
eip.bind(resource) # EIP 绑定 传入Uhost实例或者ULB实例
```


### 共享带宽

#### 共享带宽信息
```
share = ucloud.eip.get_share_bandwidth(ShareBandwidthId)
share.id # 共享带宽ID
share.width # 带宽大小
share.charge_type # 付费类型
share.create_time #创建时间
share.expire_time # 过期时间
share.address # 带宽包含的IP信息，返回EIP实例
```

#### 共享带宽操作
```
share.add_eip() # 将EIP加入共享带宽 参数类型为list， 内容为EIPID
share.remove_eip() # 将EIP 从共享带宽中移除 参数类型为list， 内容为EIPID
share.new_eip() # 在该共享带宽中创建EIP
```


## ULB 查询和创建

### 获取当前Zone下ULB
```
ucloud.ulb.instances #获取所有ULB实例
ulb = ucloud.ulb.get(ulb_id) # 通过ULBId获取ULB实例
ucloud.ulb.mon_overview() # 获取所有ULB监控概览
```

### ULB 创建
```
ucloud.ulb.create(name, mode='OuterMode', tag=None, remark=None, eip_id=None, share_bandwidth=None, eip_type=None)
# mode 为ULB模式，默认外网模式
# eip_id 需要绑定到EIPId，需要配合eip_type 海外为: International 国内一般为：Bgp
# share_bandwidth 需要绑定到共享带宽ID，需要配合eip_type 海外为: International 国内一般为：Bgp
# 带宽默认为2MB, 暂时为开放调整接口
```

### ULB实例操作
暂时未接入SSL的信息和绑定

#### ULB 实例信息
```
ulb = ucloud.ulb.get(ulb_id)
ulb.id # ULBId
ulb.name # ULB name
ulb.remark
ulb.tag
ulb.create_time
ulb.ip_set # ULB IPSet 将来会返回EIP实例
ulb.vserver # 返回ULB下所有VServer实例
ulb.mon() # 监控信息
```


#### ULB 实例操作
##### ULB 实例删除
```
ulb.delete()
```

##### VServer 查询与操作
###### VServer 信息
```
vserver = ulb.get_vserver(vserver_id) # 通过VServerId 获取VServer实例
vserver.id #
vserver.name #
vserver.protocol #
vserver.port #
vserver.ssl #
vserver.status #
vserver.backends #
```


###### VServer 查询
```
vserver = ulb.get_vserver(vserver_id) # 通过VServerId 获取VServer实例
```

###### VServer 操作
```
vserver = ulb.create_vserver(name=None, mode=None, _type=None, port=None) #创建 返回VServer实例
vserver.delete() # 删除VServer
vserver.reload() # 重载VServer信息
```

##### Backends 查询与操作
###### Backends 信息
```
vserver = ulb.get_vserver(vserver_id)
backend = vserver.get_backend(backend_id)
backend.id # BackendId
backend.resource # Backend资源，返回Uhost实例和实例转发端口
backend.status #
backend.enabled #
```
###### Backends 查询
```
vserver = ulb.get_vserver(vserver_id) # 通过VServerId 获取VServer实例
vserver.backends # 当前VServer下所有Backends
```

###### Backends 操作
```
vserver = ulb.get_vserver(vserver_id) # 通过VServerId 获取VServer实例
backend = vserver.add_backend(self, resource, port, _type='UHost') # 添加Backend resource为Uhost 实例，返回Backend实例
backend.release() # 释放backend
```

# TODO: URedis, UDB等