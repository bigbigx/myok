# -*- coding=utf-8 -*-

class assetobj(object):

        def getYunAssetsList(value):
            try:
                if value == 'ecs': # 获取ecs资产清单
                    with con_database.SQLgo(
                            ip='',
                            user='',
                            password='',
                            port=3306
                    ) as f:
                        data = f.execute(
                            sql=
                            '''
                            select *  from %s where opid_time =%s;
                            ''' % (backdb, opid))
                        return data

                elif value == 'rds':  # 获取rds资产清单
                    with con_database.SQLgo(
                            ip=conf.backupdb,
                            user=conf.backupuser,
                            password=conf.backuppassword,
                            port=conf.backupport
                    ) as f:
                        data = f.execute(
                            sql=
                            '''
                            select *  from %s where opid_time =%s;
                            ''' % (backdb, opid))
                        return data



            except Exception as e:
                print(e)
