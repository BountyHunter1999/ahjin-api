# for khalti
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests

import os
my_env = os.environ

KHALTI_SECRET_KEY = my_env['KHALTI_SECRET_KEY']

@api_view(['POST'])
def khaltiPay(request):
    print("Request is:", request.data)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
    "token": str(request.data['token']),
    "amount": request.data['amount']
    }
    headers = {
    "Authorization": KHALTI_SECRET_KEY
    }

    response = requests.post(url, payload, headers = headers)
    print("RESPONSE IS ", response)
    return Response(response)