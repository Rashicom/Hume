from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone

from things.models import Things, ThingsReadings, States, Districts
from .serializers import ThingsReadingSerializer
from authorization.models import Account
from things.models import Things, ThingsReadings

class LoginView(APIView):
    """
    Authentication View
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Anyone can login using thire mobile number, if its registered in HUME
        """
        mobile_number = request.data.get("mobile_number", None)
        if not mobile_number:
            return Response({"error": "mobile_number is required"}, status=400)
        account_obj = Account.objects.filter(role=Account.UserRole.DATA_COLLECTOR,mobile_number=mobile_number).last()
        # if account is found generate jwt token, else return user not found
        if account_obj:
            refresh = RefreshToken.for_user(account_obj)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })
        else:
            return Response({"error": "This user not registered in HUME"}, status=404)
        

class ThingsReadingsView(generics.ListCreateAPIView):
    queryset = ThingsReadings.objects.all()
    serializer_class = ThingsReadingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        print(self.request.user)
        thing_obj = Things.objects.filter(collector=self.request.user).last()
        if not thing_obj:
            raise ValidationError("No such thing assigned for this user, please contact HUME")
        
        return super().get_queryset().filter(thing=thing_obj)
    
    def perform_create(self, serializer):
        serializer.save(thing=Things.objects.filter(collector=self.request.user).last())