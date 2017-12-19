from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, request, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from student.models import user_data


@csrf_exempt
def register(request):
    if request.method == 'GET':
        print ('inside if')
        return render(request, "register.html")

    if request.method == 'POST':
        print ('inside post method')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user_data.objects.create(
            username=name,
            mobile=mobile,
            password=password
        )
        User.objects.create(
            username=str(mobile),
            password=str(password),
        )
        json = {'result': True}
        return JsonResponse(json)


@csrf_exempt
def login_check(request):
    if request.method == 'GET':
        print ('inside login')
        return render(request, "login.html")

    if request.method == 'POST':
        print ('inside post method')
        mobile = request.POST.get('user_mobile')
        password = request.POST.get('user_password')
        print (mobile)
        print (password)
        user = authenticate(username=str(mobile), password=str(password))
        # user = user_data.objects.get(mobile=int(mobile))
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/login/')


@csrf_exempt
def home(request):
    if request.method == 'GET':
        print ('inside home')
        return render(request, "home.html")
