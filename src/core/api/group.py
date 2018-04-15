
import logging
from libs import baseview
from libs import util
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate
from core.models import (
    Account,
    AccountGroup
)
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class Group(baseview.SuperUserpermissions):
    def get(self, request, args=None):
        pass

    def put(self, request, args=None):
        if args == 'changemembers':
            pass

        elif args == 'b':
            pass
        else:
            pass

    def post(self, request, args=None):
        pass

    def delete(self, request, args=None):
        pass