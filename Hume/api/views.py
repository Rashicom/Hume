from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Avg
from django.db.models.functions import TruncDate

from things.models import Things, ThingsReadings, Cluster
from .serializers import ThingsReadingSerializer, ClusterSerializer, DailyAverageSerializer
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


class ClusterView(generics.ListAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

class WeatherHistoryView(APIView):
    def get(self, request, pk):
        # return last 7 days average weather data of cluster(pk)
        today = date.today()
        seven_days_ago = today - timedelta(days=7)
        cluster_obj = Cluster.objects.filter(pk=pk).last()
        if not cluster_obj:
            return Response({"error":"cluster not found"}, status=404)

        # get all reading
        # print(ThingsReadings.objects.filter(thing__cluster=cluster_obj, created_at__date__gte=seven_days_ago))
        readings_history = (
            ThingsReadings.objects
            .filter(
                thing__cluster=cluster_obj,
                created_at__date__gte=seven_days_ago,
            )
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(
                avg_rain=Avg("rain_reading"),
                avg_temp_min=Avg("temp_reading_min"),
                avg_temp_max=Avg("temp_reading_max"),
                avg_soil_temp=Avg("soil_temp_reading"),
                avg_soil_humidity=Avg("soil_humidity_reading"),                
            )
            .order_by("-day")
        )
        serializer = DailyAverageSerializer(readings_history, many=True)
        return Response({"data":serializer.data})
