from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.core.mail import send_mail
import random
import string
from rest_framework import status

from .models import Storage
from .serializers import *
from .permission import *
from django.conf import settings


# Create your views here.

class UploadFile(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post']

class ListUploadedFile(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]
    http_method_names = ['get']

class DownloadFile(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]

    @action(detail=True, methods=['GET'])
    def download_file(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        file_path = instance.file.path
        return FileResponse(open(file_path, 'rb'))

class Signup(APIView):

    def post(self, request):
        serializer = CustomerUserSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            random_string = ''.join(
                random.choices(
                    string.ascii_letters + string.digits, k=10
                    ))
            user = CustomUser(email = email,
                              username = username, 
                              is_active = False, 
                              random_string = random_string)
            user.set_password(password)
            user.save()
            url = f' {settings.BASE_URL}verification/{random_string}'
            subject = 'Account verification'
            message = f'Hi {username}, please click this url for account verification {url}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list)
            return Response({
                'detail': 'User registered successfully. Verification email sent.'
                }, 
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)

class verification(APIView):

    def get(self, request, random_string):
        custom_user_object = CustomUser.objects.filter(
            random_string = random_string)
        if custom_user_object.exists() and not custom_user_object.first().is_active:
            user_object = custom_user_object.first()
            user_object.is_active = True
            user_object.save()
            return Response({'detail': 'Account verified'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Already verified'}, status=status.HTTP_204_NO_CONTENT)
