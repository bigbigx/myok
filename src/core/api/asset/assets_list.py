
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
                                        }

        }