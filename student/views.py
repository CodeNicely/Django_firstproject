from django.contrib.auth import authenticate, login, logout
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
        print (mobile)
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
    try:
        get_user_data = User.objects.get(username=mobile, password=password)
    except Exception as e:
        print (e)
    print ('get_user_data')
    if User.objects.filter(username=mobile, password=password).exists():
        login(request, get_user_data)
        return HttpResponseRedirect('/home/')
    # print (get_user_data)
    # user = authenticate(username=str(mobile), password=str(password))
    # print(user)
    # if user is not None:
    #     login(request, user)
    #     return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/login/')  # @csrf_exempt


def log_out(request):
    print ('inside logout')
    logout(request)
    return HttpResponseRedirect('/login/')


@csrf_exempt
def home(request):
    if request.method == 'GET':
        print ('inside home')
        if request.user.is_authenticated:
            return render(request, "home.html")
        else:
            return HttpResponseRedirect('/login/')


@csrf_exempt
def forgetPass(request):
    if request.method == 'GET':
        print ('inside forget Pass')
        return render(request, "forgetPass.html")
