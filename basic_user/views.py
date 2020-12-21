from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, House, Logger, Point
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Max, Min, Q
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import House_Serializer, Emp_Serializer, Logger_Serializer, Point_Serializer,Emp_SerializerForPatch
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import filters,generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.
def display(request):
    house = House.objects.annotate(pnt=Sum("employee__point__value")).order_by('-pnt')
    # house = House.objects.all().order_by('-point')
    for h in house:
        h.points()
    # h = House.objects.all()
    query = request.GET.get("q")
    if query:
        house =house.filter(name__icontains=query)
    context = {
        'house' : house
    }
    # print(house)
    return render (request, 'basic_user/show.html',context)

def details(request, house_id):
    house= get_object_or_404(House, id=house_id)
    employees = Employee.objects.filter(house=house)
    for employee in employees:
        employee.own_ponits()
    employees = Employee.objects.filter(house=house).annotate(p=Sum("point__value")).order_by('-p')
    # house = House.objects.all().order_by('-point')
    # employees = employees.order_by('-points')
    query = request.GET.get("q")
    query_min = request.GET.get("q_min")
    query_max = request.GET.get("q_max")
    if query:
        employees =employees.filter(name__icontains=query)
    # if query_min and query_max:
    #     # employees = Point.objects.filter(value__range=(query_min, query_max))
    #     employees = employees.filter(point__value__range=(query_min, query_max))
    # if query_max:
    #     employees = employees.annotate(points = Sum("point__value")).filter(points__gte=query_max)
    # if query_min:
    #     employees = employees.annotate(points = Sum("point__value")).filter(points__lte=query_min)

    if query_max:
        employees = employees.filter(points__lte= query_max)
    if query_min:
        employees = employees.filter(points__gte=query_min)
    context= {
        'emp' : employees
    }
    return render(request, 'basic_user/details.html',context)

def taking_logs(request):
    # emps= get_object_or_404(Employee)
    # logs= get_object_or_404(Logger)
    # super().taking_logs(Employee, Logger)
    log = Logger.objects.all().order_by('-date_and_time')
    house = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point')
    context={
        'log' : log, 
        'house' : house
    }
    return render(request, 'basic_user/logs.html', context)

def single_log(request, employee_id):
    emps = get_object_or_404(Employee, id=employee_id)
    logs = Logger.objects.filter(emp=emps.id).order_by('-date_and_time')
    house = House.objects.annotate(pnt=Sum("employee__point__value")).order_by('-point')
    context = {
        'logs' : logs,
        'house' : house
    }   
    return render(request, 'basic_user/single_log.html', context)


#api section
# 
# 
# 

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_display(request):
    if request.method == 'GET':
        # house = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point')
        # house = House.objects.all()
        # for h in house:
        #     h.point()
        house = House.objects.all().order_by('-point')
        ser = House_Serializer(house, many= True)
        return Response(ser.data)
    
    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        ser = House_Serializer(data=request.data)
        
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status = status.HTTP_201_CREATED)
        return Response(ser.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_details(request, house_id):
    if request.method == 'GET':
        house= get_object_or_404(House, id=house_id)
        # employees = Employee.objects.filter(house=house).annotate(points=Sum("point__value")).order_by('-points')
        employees = Employee.objects.filter(house=house).order_by('-points')
        ser = Emp_Serializer(employees, many = True)
        # filter_backends = [filters.SearchFilter]
        # search_fields = ['name']
        return Response(ser.data)
class Emp_list_view(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = Emp_Serializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = {
        'points': ['lte','gte']
    }
    search_fields = ['name']

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     ser = Emp_Serializer(data=data)
        
    #     if ser.is_valid():
    #         ser.save()
    #         return JsonResponse(ser.data,status = 201)
    #     return JsonResponse(ser.errors, status = 400)
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_all_emp(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        ser = Emp_Serializer(employees, many = True)    
        return JsonResponse(ser.data, safe=False)
    
    elif request.method =='POST':
        data = JSONParser().parse(request)
        ser = Emp_Serializer(data=data)

        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status =201)
        return JsonResponse(ser.errors, status = 400)
    
    # elif request.method == 'PUT':
    #     ser = Emp_Serializer(employees,data = request.data)
    #     data = {}
    #     if ser.is_valid():
    #         ser.save()
    #         date["success"]= "update successful"
    #         return JsonResponse(ser.data, status =201)
    #     return JsonResponse(ser.errors,status=400)


@api_view(['PUT','PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_all_emp_update(request,employee_id):
    try:
        employees = Employee.objects.get(id = employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # employees = Employee.objects.all()
        ser = Emp_Serializer(employees,data = request.data)
        data = {}
        if ser.is_valid():
            ser.save()
            data["success"]= "update successful"
            return JsonResponse(ser.data, status =201)
        return JsonResponse(ser.errors,status=400)

@api_view(['PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_all_emp_partial_update(request, house_id,employee_id):
    try:
        employees = Employee.objects.get(id = employee_id,house = house_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        ser = Emp_SerializerForPatch(employees,data=request.data, partial=True)
        data = {}
        if ser.is_valid():
            ser.save()
            data["success"]= "patch successful"
            return JsonResponse(ser.data, status =201)
        return JsonResponse(ser.errors,status=400)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_points(request):
    if request.method == 'GET':
        points = Point.objects.all()
        ser = Point_Serializer(points, many=  True)
        return JsonResponse(ser.data, safe =False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        ser = Point_Serializer(data=data)

        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status = 201)
        return JsonResponse(ser.errors, status = 400)
    

def api_taking_logs(request):
    if request.method == 'GET':
        log = Logger.objects.all().order_by('-date_and_time')
        ser = Logger_Serializer(log, many = True)
        return JsonResponse(ser.data,safe = False)

def api_single_log(request, employee_id):
    if request.method == 'GET':
        emps = get_object_or_404(Employee, id=employee_id)
        logs = Logger.objects.filter(emp=emps.id).order_by('-date_and_time')
        ser = Logger_Serializer(logs, many = True)
        return JsonResponse(ser.data, safe = False)