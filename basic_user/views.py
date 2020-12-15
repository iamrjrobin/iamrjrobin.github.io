from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, House, Logger, Point
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Max, Min, Q
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import House_Serializer, Emp_Serializer, Logger_Serializer, Point_Serializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def display(request):
    # house = House.objects.annotate(pnt=Sum("employee__point__value")).order_by('-pnt')
    house = House.objects.all().order_by('-point')
    for h in house:
        h.points()
    h = House.objects.all()
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
    # employees = Employee.objects.filter(house=house).annotate(p=Sum("point__value")).order_by('-p')
    employees = Employee.objects.filter(house=house)
    for employee in employees:
        employee.own_ponits()
    house = House.objects.all().order_by('-point')
    employees = employees.order_by('-points')
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
@csrf_exempt
def api_display(request):
    if request.method == 'GET':
        # house = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point')
        # house = House.objects.all()
        # for h in house:
        #     h.point()
        house = House.objects.all().order_by('-point')
        ser = House_Serializer(house, many= True)
        return JsonResponse(ser.data, safe = False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        ser = House_Serializer(data=data)
        
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status = 201)
        return JsonResponse(ser.errors, status = 400)

def api_details(request, house_id):
    if request.method == 'GET':
        house= get_object_or_404(House, id=house_id)
        # employees = Employee.objects.filter(house=house).annotate(points=Sum("point__value")).order_by('-points')
        employees = Employee.objects.filter(house=house).order_by('-points')
        ser = Emp_Serializer(employees, many = True)
        return JsonResponse(ser.data, safe=False)
    
    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     ser = Emp_Serializer(data=data)
        
    #     if ser.is_valid():
    #         ser.save()
    #         return JsonResponse(ser.data,status = 201)
    #     return JsonResponse(ser.errors, status = 400)
@csrf_exempt
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

@csrf_exempt
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