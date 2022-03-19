from tokenize import Token
from django.shortcuts import render
from rest_framework import viewsets

from .models import MobileUser, Card, Client, Process
from .serializers import MobileUserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import exceptions

import random
import requests
import time
import threading

from .generate import generate_client_id, generate_process

class Add_Card(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request, cc_number, client_id):
        if Card.objects.filter(cc_num = cc_number).exists():
            response = ('ALREADY_EXISTS')
        else:
            if Client.objects.filter(client_id = client_id).exists():
                Card.objects.create(cc_num = cc_number, client = client_id)
                response = ('SUCCESS')
            else:
                response = ('CLIENT_DOESNT_EXISTS')
    
        return Response( {"Response": response} )

class Check_Card(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, cc_number):
        if Card.objects.filter(cc_num = cc_number).exists():
            response = ('EXISTS')
        else:
            response = ('DOESNT_EXISTS')
        return Response( {'Response': response} )

class Receive_Payment(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, cc_number):
        if Card.objects.filter(cc_num = cc_number).exists():
            client = Client.objects.get(client_id = (Card.objects.get(cc_num = cc_number).client))
            
            if not client.is_busy:
                client.is_busy = True
                client.save()
                resp = {"response": "succesful"}
                
                process = generate_process(client)

                def setBusy(client, process):
                    print("siliyom ******************************************")
                    client.is_busy = False
                    client.save()
                    process.delete()

                set_busy_timer = threading.Timer( 60, setBusy, [client, process] )
                set_busy_timer.start()

            else:
                resp = {"response": "client_is_busy"}
        else:
            resp = {"response": "fail"}
        return Response(resp)
   
class MobileUserViewSet(viewsets.ModelViewSet):
    serializer_class = MobileUserSerializer
    queryset = MobileUser.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def MobileLogin(request, username, password, token):
    if token == "SUPERSECRETTOKEN":
        try:
            control = MobileUser.objects.filter(username = username)[0]
            exists = True
        except (IndexError):
            exists = False
        except:
            exists = None

        if exists == True:
            if password == control.password:
                response = 'ALL_TRUE'
            else:
                response = 'WRONG_PASSWORD'
        elif exists == False:
            response = 'USER_DOESNT_EXISTS'
        else:
            response = 'ERR'
    else:
        response = 'ACCESS_DENIED'
    
    if response == 'ALL_TRUE':
        response = {'response': response, 'client_id': control.client_id}
    else:
        response = {'response': response}

    return Response(response)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def MobileRegister(request, username, password, token):
    if token == 'SUPERSECRETTOKEN':
        try:
            doesnt_really_matter = MobileUser.objects.filter(username = username)[0]
            exists = True
        except (IndexError):
            exists = False
        except:
            exists = None
        if exists == True:
            response = 'USER_EXISTS'
        elif exists == False:
            client_id = generate_client_id()
            MobileUser.objects.create(username = username, password = password, client_id = client_id)
            Client.objects.create(client_id = client_id, is_busy = False)
            response = 'SUCCESSFUL'
        else:
            response = 'UNKONWN_ERR'
    else:
        response = 'ACCESS_DENIED'

    return Response(response)
