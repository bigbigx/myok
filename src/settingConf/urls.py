'''
url table
'''
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from core.api.gensql import (
    addressing,
    gensql
)
from core.api.sqldic import (
    adminpremisson,
    exportdoc,
    dictionary,
    downloadFile
)
from core.api.user import (
    userinfo,
    generaluser,
    authgroup,
    ldapauth,
    login_auth
)

from core.api.group import (
    Group
)
from core.api.log.filecontent import (
    filecontent
)
from core.api.other import (
    maindata,
    messages,
    dingding
)
from core.api.managerdb import (
    managementdb,
    pushpermissions
)
from core.api.auditorder import (
    orderdetail,
    audit

)
from core.api.executeorder import (
    execute
)

from core.api.asset.host import (
    host
)
from core.api.authtoken import (
    authtoken
)

from core.api.exetoken import (
    exetoken
)
from core.api.asset.assets import (
    assets
)
from core.api.asset.yunassets import (
    yunassets
)
from core.api.record import recordorder
from core.api.sqlorder import sqlorder
from core.api.serachsql import serach

urlpatterns = [
    url(r'^api/v1/userinfo/(.*)', userinfo.as_view()),
    url(r'^api/v1/workorder/(.*)', addressing.as_view()),
    url(r'^api/v1/sqlorder/(.*)', gensql.as_view()),
    url(r'^api/v1/mamagement_sql/(.*)', managementdb.as_view()),
    url(r'^api/v1/audit_sql', audit.as_view()),
    url(r'^api/v1/execute_sql', execute.as_view()),
    url(r'^api/v1/sqldic/(.*)', dictionary.as_view()),
    url(r'^api/v1/auth_twice', authgroup.as_view()),
    url(r'^api/v1/sqlsyntax/(.*)', sqlorder.as_view()),
    url(r'^api/v1/adminsql/(.*)', adminpremisson.as_view()),
    url(r'^api/v1/record/(.*)', recordorder.as_view()),
    url(r'^api/v1/homedata/(.*)', maindata.as_view()),
    url(r'^api/v1/messages/(.*)', messages.as_view()),
    url(r'^api/v1/otheruser/(.*)', generaluser.as_view()),
    url(r'^api/v1/exportdocx/', exportdoc.as_view()),
    url(r'^api/v1/dingding', dingding.as_view()),
    url(r'^api/v1/detail', orderdetail.as_view()),
    url(r'^api/v1/search', serach.as_view()),
    url(r'^api/v1/ldapauth', ldapauth.as_view()),
    url(r'^api/v1/globalpermissions', pushpermissions.as_view()),
    url(r'^api/v1/download', downloadFile),
    url(r'^api-token-auth/', login_auth.as_view()),
    url(r'^api/v1/audit_token', authtoken.as_view()),
    url(r'^api/v1/exe_token', exetoken.as_view()),
    url(r'^api/v1/assets/(.*)', assets.as_view()),
    url(r'^api/v1/yunassets/(.*)', yunassets.as_view()),
    url(r'^api/v1/filemanager/(.*)', filecontent.as_view()),
    url(r'^api/v1/group/(.*)', Group.as_view()),
    url(r'^api/v1/host/(.*)', host.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
