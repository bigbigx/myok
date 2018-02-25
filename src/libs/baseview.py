from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
    #DjangoModelPermissions
)
## 上面的权限分别用于指定权限, 所有人, 登录用户, 非登录用户只读，管理员


from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication   #jianglb
from rest_framework.views import APIView

### 审核人，超级管理员，工单提交人

##  jianglb
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

@method_decorator(api_view(['DELETE', 'GET', 'POST', 'PUT']), 'dispatch')
class BaseView(View):
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)

    def get(self, request, args: str = None):
        pass

    def post(self, request, args: str = None):
        pass

    def put(self, request, args: str = None):
        pass

    def delete(self, request, args: str = None):
        pass

#超级管理员权限
class SuperUserpermissions(APIView):
    
    permission_classes = (IsAdminUser,)

    def get(self, request, args: str = None):
        pass

    def post(self, request, args: str = None):
        pass

    def put(self, request, args: str = None):
        pass

    def delete(self, request, args: str = None):
        pass

# 审核人
class Approverpermissions(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, args: str = None):
        pass

    def post(self, request, args: str = None):
        pass

    def put(self, request, args: str = None):
        pass

    def delete(self, request, args: str = None):
        pass


class AnyLogin(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, args: str = None):
        pass

    def post(self, request, args: str = None):
        pass

    def put(self, request, args: str = None):
        pass

    def delete(self, request, args: str = None):
        pass
