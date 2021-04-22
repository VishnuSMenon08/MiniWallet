from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account,Transaction, CustAuthToken
from .serializer import TokenSerializer, AccountSerializer, TransactionSerializer
from .decorators import is_autheticated

import logging
import sys,decimal
from datetime import datetime

logging.basicConfig(level=logging.INFO,filename='apiLogs.log')

# Create your views here.
@api_view(['POST',])
def init_wallet(request):
    try:
        if request.method == 'POST':
            customer_xid = request.POST.get('customer_xid')
            account = Account(
                owned_by=customer_xid,
            )
            token = account.create()
            serialized_data = TokenSerializer(token)
            return Response({
                "data": serialized_data.data,
                "status": "success"
                },
                status=200)
    except Exception as ex:
        logging.error("Exception in init wallet : {}".format(str(ex)))
        return Response({"error":"Internal Server Error"},status=500)

@api_view(['POST','GET','PATCH'])
@is_autheticated
def enable_wallet(request):
    try:
        user_session = CustAuthToken.objects.get(token_id = request.headers.get('Authorization'))
        account = Account.objects.get(id = user_session.user.id)
        if request.method == "POST":
            if account.status == 'E':
                return Response({
                    "status" : "fail",
                    "data" : {"error" : "Already Enabled"}
                })
            account.status = 'E'
            account.changed_at = datetime.now().isoformat()
            account.save()
            serialized_acc_data = AccountSerializer(account)
            return Response({"status":"success","data":{"wallet":serialized_acc_data.data}})
        
        elif request.method == "GET":
            if account.status == 'D':
                 return Response({
                    "status" : "fail",
                    "data" : {"error" : "Account is Disabled"}
                })
            serialized_acc_data = AccountSerializer(account)
            return Response({"status":"success","data":{"wallet":serialized_acc_data.data}})  

        elif request.method == "PATCH":
            if "true" in request.POST.get('is_disabled'):
                if account.status == 'D':
                    return Response({
                    "status" : "fail",
                    "data" : {"error" : "Account already diabled"}
                    },status=200)
                account.status = 'D'
                account.save()
                serialized_acc_data = AccountSerializer(account)
                return Response({"status":"success","data":{"wallet":serialized_acc_data.data}})
            else:
                if account.status == 'D':
                    return Response({
                    "status" : "fail",
                    "data" : {"error" : "Invalid parameter value is_disabled"}
                    },status=200)

    except Exception as ex:
        logging.error("Exception in Enable wallet {}".format(str(ex)))
        return Response({"error":"Internal Server Error"},status=500)

@api_view(['POST',])
@is_autheticated
def deposit(request):
    user_session = CustAuthToken.objects.get(token_id = request.headers.get('Authorization'))
    account = Account.objects.get(id = user_session.user.id)
    reference_id = request.POST.get('reference_id')
    if request.method == "POST":
        if account.status == 'D':
            return Response({
                "status" : "fail",
                "data" : {"error" : "Account is Disabled"}
                },status=200)
        elif not check_reference_id(reference_id):
            return Response({
                "status" : "fail",
                "data" : {"error" : "referance_id not unique"}
                },status=200)
        
        tr = Transaction(
            transaction_by = account,
            transaction_type = "Deposit",
            transaction_time = datetime.now().isoformat(),
            amount = request.POST.get('amount'),
            reference_id = reference_id
        )
        account.balance += decimal.Decimal(request.POST.get('amount'))
        account.save()
        tr.save()
        serialized_tr = TransactionSerializer(tr)
        return Response({"status":"success","data":{"deposit":serialized_tr.data}})

@api_view(['POST',])
@is_autheticated
def withdraw(request):
    user_session = CustAuthToken.objects.get(token_id = request.headers.get('Authorization'))
    account = Account.objects.get(id = user_session.user.id)
    amount = decimal.Decimal(request.POST.get('amount'))
    reference_id = request.POST.get('reference_id')

    if account.status == 'D':
        return Response({
            "status" : "fail",
            "data" : {"error" : "Account is Disabled"}
            },status=200)
    
    elif not check_reference_id(reference_id):
        return Response({
            "status" : "fail",
            "data" : {"error" : "referance_id not unique"}
            },status=200) 

    elif amount > account.balance:
        return Response({"status":"failed","data":{"error":"Insufficient Funds"}},status=200)

    tr_wd = Transaction(
    transaction_by = account,
    transaction_type = "Withdrawal",
    transaction_time = datetime.now().isoformat(),
    amount = request.POST.get('amount'),
    reference_id = reference_id
    )
    account.balance = account.balance - amount
    account.save()
    tr_wd.save()
    serialized_tr = TransactionSerializer(tr_wd)
    return Response({"status":"success","data":{"withdrawal":serialized_tr.data}})


def check_reference_id(reference_id):
    try:
        tr = Transaction.objects.get(reference_id = reference_id)
        if tr:
            return False
        return True
    except:
        return True