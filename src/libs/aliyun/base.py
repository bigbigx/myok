# -*- coding: utf-8 -*-
'''
通过aliyun的api连接阿里云的实现基类

'''

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import StsTokenCredential


class Base(object):
    def __init__(self,*args, **kwargs):
        sts_token_credential = StsTokenCredential('sts_access_key_id', 'sts_access_key_secret', 'sts_session_token')
        acs_client = AcsClient(region_id='cn-hangzhou', credential=sts_token_credential)
        return acs_client


