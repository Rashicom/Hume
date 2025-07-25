from django.shortcuts import render, redirect
from django.views import View
from things.models import States, Districts, Cluster
from .forms import StateForm, DistrictForm, RegistrationForm, ThingsRegistrationForm, ThingsReadingForm
import json
from django.contrib.gis.geos import Polygon, GEOSGeometry, MultiPolygon
from django.db import transaction
from django.core.serializers import serialize
from authorization.models import Account
from things.models import Things, ThingsReadings
from django.contrib.gis.geos import Point
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Exists, OuterRef

class AdminDash(View, LoginRequiredMixin):
    """
    Admin Index View
    """
    login_url = 'admin_login'
    def get(self, request):
        return render(request, 'admin_index.html')

class AccountsManagement(View):
    """
    Accounts Management View
    """
    def get(self, request):
        users = Account.objects.exclude(role=Account.UserRole.ADMIN).exclude(is_superuser=True)
        return render(request, 'admin_accounts.html', {"users":users})
    
    def post(self, request):
        # set password same as mobile number
        # password hashed from Account.save()
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            # TODO: redirect witha message
            print("not valied")
            print(form.errors)
            return redirect("admin-accounts")
        user_obj = form.save()
        user_obj.set_password(user_obj.mobile_number)
        user_obj.save()
        return redirect("admin-accounts")

class ThingsManagement(View):
    """
    Things Management View
    """
    def get(self, request):
        users = Account.objects.annotate(
            has_thing=Exists(Things.objects.filter(collector=OuterRef('pk')))
        ).filter(has_thing=False).exclude(role=Account.UserRole.ADMIN).exclude(is_superuser=True).only("name", "uuid")
        things = Things.objects.all()
        states = States.objects.all().only("uuid", "state_name")
        districts = Districts.objects.all().only("uuid","district_name")
        clusters = Cluster.objects.all().only("uuid", "cluster_name")
        return render(
            request,
            'admin_things.html',
            {
                "users":users,
                "things":things,
                "states":states,
                "districts":districts,
                "clusters":clusters
            }
        )
    
    def post(self, request):
        try:
            lat_str, lon_str = request.POST.get("location_cordinate").split(",")
            # converting to [long,lat] wich postgres hadling way
            point = Point((float(lon_str.strip()), float(lat_str.strip())), srid=4326)
            print(point)
        except Exception as e:
            print(e)
            return redirect("admin-things")
        form = ThingsRegistrationForm(
            {
                'collector':request.POST.get("collector"),
                'thing_type':request.POST.get("thing_type"),
                'state':request.POST.get("state"),
                'district':request.POST.get("district"),
                'location_cordinate':point,
                'cluster':request.POST.get("cluster") if request.POST.get("cluster") else None
            }
        )
        if Things.objects.filter(collector__uuid=request.POST.get("collector")).exists():
            return redirect("admin-things")
        if not form.is_valid():
            # return eorror
            print(form.errors)
            return redirect("admin-things")

        form.save()
        return redirect("admin-things")


class DataManagement(View):
    """
    Data Management View
    """
    def get(self, request):
        return render(request, 'admin_data.html')
    
    def post(self, request):
        data = json.loads(request.body)
        error_data = list()
        for idx,row in enumerate(data):
            user = Account.objects.filter(mobile_number=row.get("mobile_number")).last()
            if not user:
                error_data.append({**row, "error":"user not found", "row_idx":idx})
                continue
            thing = user.my_things.last()
            if not thing:
                error_data.append({**row, "error":"thing not found for the user", "row_idx":idx})
                continue

            # update data
            reading_obj,created=ThingsReadings.objects.update_or_create(
                thing=thing,
                created_at__date=datetime.now().date(),
                defaults={
                    "reading_from":(datetime.now() - timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0),
                    "reading_till":datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
                    "rain_reading":row.get("rain_reading"),
                    "temp_reading_min":row.get("temp_reading_min"),
                    "temp_reading_max":row.get("temp_reading_max")
                }
            )
        return JsonResponse({"status":"success", "error_records":error_data})

class ReadingsManagement(View):

    def get(self, request):
        readings = ThingsReadings.objects.all()
        return render(request, 'admin_readings.html', {"readings":readings})


class AdminMapListingView(View):
    """
    Admin Map Listing View
    """
    def get(self, request):
        states = States.objects.all()
        district_list = Districts.objects.all()
        districts = list()
        for dist in district_list:
            districts.append(
                {
                    "uuid":dist.uuid,
                    "district_name":dist.district_name,
                    "state":dist.state,
                    "polygon":[[cord[1], cord[0]] for cord in dist.boundary.coords[0]]
                }
            )
        # geojson_data = serialize('geojson', districts, geometry_field='boundary', fields=('district_name', 'state'))
        
        return render(request, 'adminmap.html', {
            "states": states,
            "districts": districts,
            "local_authorities": "deprecated",
            "wards": "deprecated",
            "locations": "deprecated",
            # 'districts_geojson':geojson_data
        })


class CreateState(View):
    def post(self, request):
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin-maps")
        else:
            print(form.errors)
            return render("admin-maps")

class DeleteState(View):
    def get(self, request, uuid):
        state = States.objects.get(uuid=uuid)
        state.delete()
        return redirect("admin-maps")


class CreateDistrict(View):
    def post(self, request):
        data = request.POST
        geojson = request.FILES.get("boundary-file", None)
        if not geojson:
            print("boundary file not found")
            return redirect("admin-maps")
        if not geojson.name.endswith(".geojson"):
            print("not a valid boundary file")
            return redirect("admin-maps")
        
        state_obj = States.objects.filter(uuid=data.get("state")).last()
        if not state_obj:
            print("state not found for this state name")
            return redirect("admin-maps")
        
        
        try:
            content = geojson.read().decode("utf-8")
            geojson_data = json.loads(content)
            geojson_features = geojson_data.get("features", None)
            if not geojson_features:
                print("not a valid geojson file cannot find features")
                return redirect("admin-maps")
            if not isinstance(geojson_features, list):
                print("Not a valied geojson, geojson features must be a list")
                return redirect("admin-maps")
            
            # validation
            for dist in geojson_features:
                properties = dist.get("properties", None)
                if not properties:
                    print("not a valid geojson, properties not found")
                    return redirect("admin-maps")
                if not str(properties.get(data.get("geojson_district_field_name"))):
                    print("not a valid geojson, properties does not contain the specified district field name")
                    return redirect("admin-maps")
                geomatry = dist.get("geometry", None)
                if not geomatry:
                    print("not a valid geojson, geojson file does not contain geometry field")
                    return redirect("admin-maps")
                if geomatry.get("type", None) == "Polygon":
                    print("not a valid geojson, geomatry type is not a Polygon")
                    return redirect("admin-maps")
                if not isinstance(geomatry.get("coordinates"), list):
                    print("not a valid geojson, geomatry coordinates must be a list")
                    return redirect("admin-maps")
            
            districts = list()
            # create district
            for dist in geojson_features:
                district_name = dist.get("properties").get(data.get("geojson_district_field_name"))
                geomatry = dist.get("geometry")

                geom = GEOSGeometry(str(geomatry))[0]
                districts.append(Districts(district_name=district_name, state=state_obj, boundary=geom))
            
            with transaction.atomic():
                Districts.objects.bulk_create(districts)

        except Exception as e:
            print(e)
            return redirect("admin-maps")
        print("data",data)
        print("files", type(geojson.name))
        return redirect("admin-maps")
    

class DeleteDistrict(View):
    def get(self, request, uuid):
        dist = Districts.objects.get(uuid=uuid)
        dist.delete()
        return redirect("admin-maps")