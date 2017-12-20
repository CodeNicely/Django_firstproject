import random
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from student.models import user_data, user_otp


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    if request.method == 'POST':
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
        return render(request, "login.html")

    if request.method == 'POST':
        mobile = request.POST.get('user_mobile')
        password = request.POST.get('user_password')
    try:
        get_user_data = User.objects.get(username=mobile, password=password)
        request.session['mobile'] = 'mobile'
        session_mobile = request.session[mobile]
    except Exception as e:
        print (e)
    if User.objects.filter(username=mobile, password=password).exists():
        login(request, get_user_data)
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/login/')  # @csrf_exempt


def log_out(request):
    print ('inside logout')
    logout(request)
    return HttpResponseRedirect('/login/')


@csrf_exempt
def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "home.html")
        else:
            return HttpResponseRedirect('/login/')


@csrf_exempt
def forgetPass(request):
    if request.method == 'GET':
        return render(request, "forgetPass.html")

    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        request.session['get_mobile'] = mobile
        if User.objects.filter(username=mobile).exists():
            otp = random.randint(10000, 99999)  # returns a random integer
            mobile = request.POST.get('mobile')
            print (otp)
            user_otp.objects.create(
                mobile=mobile,
                otp=otp,
            )
            result = {'response': True}
            return JsonResponse(result)
        else:
            result = {'response': False}
            return JsonResponse(result)


@csrf_exempt
def changePassword(request):
    if request.method == 'GET':
        return render(request, "changePassword.html")

    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        get_otp = request.POST.get('get_otp')
        mobile = request.session['get_mobile']
        print ('session check')
        try:
            user_mobile_instance = user_otp.objects.filter(mobile=mobile).last()
            print (get_otp)
        except Exception as e:
            print(e)

        if user_mobile_instance.otp == int(get_otp):
            get_user_object = User.objects.get(username=mobile, )
            get_user_object.password = password1
            get_user_object.save()
            return HttpResponseRedirect('/login/')
        else:
            print ('Wrong OTP')
            return HttpResponseRedirect('/changePassword/')
