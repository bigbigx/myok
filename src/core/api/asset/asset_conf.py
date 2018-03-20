
assets_conf={
                                "disk_number":{
                                                        "name":"硬盘(个)",
                                                        "command":{
                                                                        "CentOS/RedHat5":"""mount -l|grep -Eo '^/dev/[a-zA-Z]+'|sort|uniq|wc -l""",
                                                                        "CentOS/RedHat6":"""mount -l|grep -Eo '^/dev/[a-zA-Z]+'|sort|uniq|wc -l""",
                                                                        "CentOS/RedHat7":"""mount -l|grep -Eo '^/dev/[a-zA-Z]+'|sort|uniq|wc -l""",
                                                                        "Ubuntu":"""mount -l|grep -Eo '^/dev/[a-zA-Z]+'|sort|uniq|wc -l""",
                                                                        "Aix":"""mount |grep   '/dev/'|sort|uniq|wc -l""",
                                                                        "Solaris":"""mount -l|grep -Eo '^/dev/[a-zA-Z]+'|sort|uniq|wc -l""",
                                                                },
                                                        "type":"number",
                                                        "show":True,
                                                },
                                "system_version":{
                                                        "name":"系统版本",
                                                        "command":{
                                                                "CentOS/RedHat5":"""echo  'import platform;print platform.dist()[1]'|python""",
                                                                "CentOS/RedHat6":"""echo  'import platform;print platform.dist()[1]'|python""",
                                                                "CentOS/RedHat7":"""echo  'import platform;print platform.dist()[1]'|python""",
                                                                "Ubuntu":"""echo  'import platform;print platform.dist()[1]'|python""",
                                                                "Aix":"""uname -a""",
                                                                "Solaris":""" """,
                                                        },
                                                        "type":"number",
                                                        "show":True,
                                                 },
                                "server":{
                                                        "name": "服务器",
                                                        "text":{
                                                                "pc-server": "PC服务器",
                                                                "blade-server":"刀片",
                                                                "min-machine":"小型机",
                                                            },
                                                },
                                "network":{
                                                        "name": "网络设备",
                                                        "text":{
                                                                "pc-server": "PC服务器",
                                                                "blade-server":"刀片",
                                                                "min-machine":"小型机",
                                                            },
                                                },
                                "safe-device": {
                                                        "name": "安全设备",
                                                        "text":{
                                                                   "firewall": "防火墙",
                                                                   "ids": "入侵检测设备",
                                                                   "dns": "互联网网关",
                                                                    "x-scan": "漏洞扫描设备",
                                                                    "digital-sign": "数字签名设备",
                                                                    "online-manager": "上网行为管理设备",
                                                                    "ops-audit": "运维审计系统",
                                                                    "encrypt-device": "加密机",

                                                               },

                                    "storage-device": {
                                                        "name": "存储设备",
                                                        "text": {
                                                            "raid": "磁盘阵列",
                                                            "NAS": "网络存储器",
                                                            "tape-lib": "磁带库",
                                                            "tape-machine": "磁带机",
                                                        },
                                                    },

                                    "room-device": {
                                                        "name": "机房设备",
                                                        "text": {
                                                            "UPS": "UPS",
                                                            "cabinet": "机柜",
                                                        },
                                                    },
    },


        }