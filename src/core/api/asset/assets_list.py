from libs import util
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    ServerInfo,
    ServerConf,
    AssetBasic
)

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')
class assets_list(baseview.BaseView):
    '''
    获取资产清单
    '''
    def get(self, request, args=None):
        try:
            page = request.GET.get('page')
            username = request.GET.get('username')
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                pass

            except Exception as e:
                print(e)