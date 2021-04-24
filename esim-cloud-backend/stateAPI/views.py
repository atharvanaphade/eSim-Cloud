import uuid
from http.client import responses
from django.db.models.query import QuerySet
from django.http import response
from django.http.multipartparser import parse_header
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import *
from publishAPI.models import Circuit
from publishAPI.serializers import CircuitSerializer


# Create your views here.


class GetCircuit(APIView):
    
    parser_classes = [JSONParser, FormParser]
    serializer_class = CircuitSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses = {200: CircuitSerializer})
    def get(self, request, state):
        groups = self.request.user.groups.all()

        for g in groups:
            group = Groups.objects.get(group=g)
            for states in group.states.all():
                if(states == state):
                    try:
                        queryset = Circuit.objects.filter(state__title = state)
                        serializer = CircuitSerializer(queryset, many=True)
                        return Response(serializer.data)
                    except:
                        return Response({'error': 'Circuit not Found!'}, status = 404)
                else:
                    Response({'error': 'Unauthorized request!'}, status = 401)

class GetUserType(APIView):
    
    
    parse_classes = [JSONParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = self.request.groups.all()
        types = []
        for role in roles:
            types.append(role.name)
        serializer = UserSerializer(data = {'groups' : types})
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class CircuitView(APIView):


    parser_classes = [JSONParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer

    @swagger_auto_schema(responses={200: StatusSerializer})
    def get(self, request, cir_id):
        if isinstance(cir_id, uuid.UUID):
            saved = Circuit.objects.get(circuit_id=cir_id)
            if saved:
                state = saved.state
                serialized = StatusSerializer(state)
                return Response(serialized.data)
            else:
                return Response({'error': 'Circuit does not exist'}, status=404)
    
    @swagger_auto_schema(response={200: StatusSerializer}, request_body=StatusSerializer)
    def post(self, request, cir_id):
        if isinstance(cir_id, uuid.UUID):
            saved = Circuit.objects.get(circuit_id=cir_id)
            if saved:
                role = self.request.user.groups.all()
                if role:
                    delta = Delta.objects.get(init_state=saved.state, new_state=State.objects.get(title=request.data['name']))
                    roles = delta.user_type.all()
                    if delta.init_state != saved.state:
                        return Response({'error': 'Unauthorized request'}, status=401)
                    else:
                        roles_set = set(roles)
                        user_roles_set = set(role)
                        if user_roles_set & roles_set:
                            intersection = user_roles_set.intersection(roles_set)
                            for user_roles in intersection:
                                if role.groups.is_arduino is saved.is_arduino:
                                    if delta.creator is False and saved.author == request.user:
                                        return Response({'error': 'Unathorized request'}, status=401)
                                    else:
                                        history = DeltaMetadata(circuit_id=cir_id, author=request.user, init_state=saved.state, new_state=delta.new_state)
                                        history.save()
                                        saved.state = delta.new_state
                                        saved.save()
                                        state = saved.state
                                        serialized = StatusSerializer(state)
                                        return Response(serialized.data)
                else:
                    return Response(data={'error': 'No User Role'}, status=404)
            else:
                return Response({'error': 'Circuit does not Exist'}, status=404)
