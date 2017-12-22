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
        print (name)
        print (mobile)
        print (password)
        if User.objects.filter(username=mobile, password=password).exists():
            print ("registers if part")
            print ("user Already Exist")
            return render(request, "register.html", {'result': False})
        else:
            otp = random.randint(10000, 99999)
            print (otp)
            request.session['name'] = name
            request.session['mobile'] = mobile
            request.session['password'] = password
            request.session['otp'] = otp
            json = {'result': True}
            return JsonResponse(json)


@csrf_exempt
def verify_register(request):
    if request.method == 'GET':
        return render(request, "verify_register.html")

    if request.method == 'POST':
        register_otp = request.POST.get('register_otp')
        print ('register_otp')
        print (register_otp)
        name = request.session['name']
        mobile = request.session['mobile']
        password = request.session['password']
        otp = request.session['otp']
        print (name)
        print (mobile)
        print (password)
        print (otp)
        if otp == int(register_otp):
            user_data.objects.create(
                username=name,
                mobile=mobile,
                password=password
            )
            User.objects.create(
                username=str(mobile),
                password=str(password),
            )
            print ('verification successful')
            return HttpResponseRedirect('/login/')
        else:
            print ('inside verify_register else')
        return render(request, "verify_register.html", {'err': True})


@csrf_exempt
def login_check(request):
    if request.method == 'GET':
        return render(request, "login.html")

    if request.method == 'POST':
        mobile = request.POST.get('user_mobile')
        password = request.POST.get('user_password')
        print (mobile)
        print (password)
        try:
            if User.objects.filter(username=mobile, password=password).exists():
                get_user_data = User.objects.get(username=mobile, password=password)
                login(request, get_user_data)
                print ('inside if')
                return HttpResponseRedirect('/home/')
            else:
                print ('inside else part')
                return render(request, "login.html", {'err': True})
        except Exception as e:
            print (e)
            return HttpResponseRedirect('/login/')  # @csrf_exempt


def log_out(request):
    print ('inside logout')
    logout(request)
    return HttpResponseRedirect('/login/')


@csrf_exempt
def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_mobile = request.user
            get_user_name = user_data.objects.get(mobile=str(user_mobile))
            user_name = get_user_name.username
            return render(request, "home.html", {'user_name': user_name})
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
