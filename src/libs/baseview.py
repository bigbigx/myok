from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny
)
from rest_framework.authentication import BasicAuthentication   #jianglb
from rest_framework.permissions import IsAuthenticated  #jianglb
from rest_framework.views import APIView

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
    #permission_classes = (IsAuthenticated,)

    def get(self, request, args: str = None):
        pass

    def post(self, request, args: str = None):
        pass

    def put(self, request, args: str = None):
        pass

    def delete(self, request, args: str = None):
        pass



#某些认证的模块管理者权限
class AuthenticatedUserpermissions(APIView):
    #authentication_classes = (
    #    BasicAuthentication,
        # SessionAuthentication,
        # TokenAuthentication,
    #)
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
