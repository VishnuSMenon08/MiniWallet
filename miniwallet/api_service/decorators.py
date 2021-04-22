import logging
import sys
from rest_framework.response import Response

from .models import Account,Transaction, CustAuthToken

def is_autheticated(fn):

    def authenticate(request,**kwargs):
        auth_token = request.headers.get('Authorization')
        try:
            if auth_token:
                user_session = CustAuthToken.objects.get(token_id = request.headers.get('Authorization'))
            else:
                return Response({"Data":"No Authorization token"},status=401)
        except:
            ex_type,ex_val,tr = sys.exc_info()
            if "DoesNotExist" in str(ex_type):
                return Response({"Data":"Authorization token Invalid"},status=401)
            else:
                logging.error("{0}: {1}".format(str(ex_type),str(ex_val)))
                return Response({"error":"Internal server Error"},status=500)
        return fn(request,**kwargs)

    return authenticate
        